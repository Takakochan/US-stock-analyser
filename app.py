import pandas as pd
from matplotlib.pylab import *
import streamlit as st
from ftplib import FTP_TLS
import ftplib
from io import BytesIO
import io
import numpy as np
import re
import requests
from openai import OpenAI
from datetime import date
from datetime import datetime
from datetime import timedelta

api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)
headers = {"User-Agent": "takakokunugi@gmail.com"}

# Get all companies data once
company_tickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers).json()


# Helper class to robustly parse floats
class FloatProcessor:

    def __init__(self, s):
        self.s = s

    def process(self):
        s = re.sub(r'[^\x00-\x7F]+', '-', str(self.s))
        return float(s)


def get_company_facts(headers, cik):
    facts = requests.get(
        f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json",
        headers=headers).json()
    epss = pd.json_normalize(
        facts['facts']['us-gaap']['EarningsPerShareDiluted']['units']
        ['USD/shares'])
    revenues = pd.json_normalize(facts['facts']['us-gaap'][
        'RevenueFromContractWithCustomerExcludingAssessedTax']['units']['USD'])
    # Clean up dataframe
    epss = epss.dropna(subset=['frame'])
    revenues = revenues.dropna(subset=['frame'])[[
        "end", "val"
    ]].rename(columns={"val": "rev"})
    epss = epss.merge(revenues, on='end')
    return epss, revenues


def add_differ_days(epss):
    # Compute difference in days between 'end' and 'start'
    differ = (pd.to_datetime(epss.end) - pd.to_datetime(epss.start)).dt.days
    epss['differ'] = differ
    return epss[~epss['differ'].between(100, 300)]


def process_eps_revenue(epss):
    # Drop duplicate quarter-ends
    epss = epss.drop_duplicates(subset='end', keep="last")
    # Rolling sums to estimate trailing data
    epss["eps_3_cal_sum"] = epss["val"].rolling(3).sum().shift()
    epss["rev_3_cal_sum"] = epss["rev"].rolling(3).sum().shift()
    # Calculate adjusted EPS and revenue, depending on period gap
    final_epss, final_rev = [], []
    for cal, cal_rev, given, giv_rev, differ in zip(
            epss.eps_3_cal_sum.fillna(0), epss.rev_3_cal_sum.fillna(0),
            epss.val, epss.rev, epss.differ):
        if differ > 300:
            final_epss.append(given - cal)
            final_rev.append(giv_rev - cal_rev)
        else:
            final_epss.append(given)
            final_rev.append(giv_rev)
    epss['EPS'] = final_epss
    epss['Revenue'] = final_rev
    epss = epss.rename(columns={'end': 'closed_dates'})
    return epss


def plot_eps_revenue(epss, title):
    fig, ax1 = plt.subplots(figsize=(8, 4))
    epss.tail(10).plot(x="closed_dates",
                       y="EPS",
                       marker='o',
                       color='#FE53BB',
                       ax=ax1)
    ax2 = ax1.twinx()
    epss.tail(10).plot(x="closed_dates",
                       y="Revenue",
                       secondary_y=True,
                       marker='o',
                       color='#0040ff',
                       ax=ax2)
    plt.title(title)
    plt.xticks(rotation=45)
    st.pyplot(fig)


def extract_eps_list(epss):
    # Returns a list of last N EPS values, ready to use and processed
    lir = list(reversed(list(epss['EPS'])))
    floats = [FloatProcessor(x).process() for x in lir[:5]]
    return floats  # [thisyear, q1prev, q2prev, q3prev, previous]


def fetch_and_plot_ticker(choosensymbol,
                          company_tickers,
                          headers,
                          show_plot=True):
    # Get ticker info
    item = next((item for item in company_tickers.values()
                 if item['ticker'] == choosensymbol), None)
    if not item:
        st.error(f"Ticker {choosensymbol} not found.")
        return None
    try:
        cik = str(item['cik_str']).zfill(10)
        epss, _ = get_company_facts(headers, cik)
        epss = add_differ_days(epss)
        epss = process_eps_revenue(epss)
        if show_plot:
            plot_eps_revenue(
                epss,
                f'Ticker: {choosensymbol} - EPS and Revenue Quarterly Trend')
        return epss
    except Exception as e:
        st.warning(f"Could not fetch data for {choosensymbol}: {e}")
    return None


# --- STREAMLIT START ----

st.set_page_config(layout="wide")
st.set_option('client.showErrorDetails', False)

# User input for stock ticker
choosensymbol = st.text_input('Put Ticker Symbol. e.g.)AAPL').upper()
if not choosensymbol:
    st.stop()

url = f'https://finance.yahoo.com/quote/{choosensymbol}/financials?p={choosensymbol}'
st.markdown(f"[Yahoo Finance Page for {choosensymbol}]({url})")

col1, col2, col3 = st.columns(3)

with col1:
    epss = fetch_and_plot_ticker(choosensymbol, company_tickers, headers)

with col2:
    st.write("OpenAI research")
    try:
        # Compose OpenAI prompt
        prompt = (
            f"What is the name of the company for this symbol {choosensymbol}? "
            "Make a list of the names of the competitors to that company on the US stock market, with their symbols and five main services or products for each, in descending order of sales."
        )
        response = client.responses.create(
            model="gpt-3.5-turbo",
            instructions="You are a specialist of US stock market",
            input=prompt,
        )
        st.write(response.output_text)
    except Exception as e:
        st.write(f"Error from OpenAI: {e}")

with col3:
    st.write("Competitor's growth")
    try:
        res2_prompt = f"Extract only US stock ticker symbols from this text (e.g., AAPL, META, MSFT): {response.output_text}"
        response2 = client.responses.create(
            model="gpt-3.5-turbo",
            input=res2_prompt,
        )
        # Basic parsing, should ideally use regex to extract only valid tickers
        tickers = [
            t.replace("'", '').strip().upper()
            for t in re.split(r'[,\s]+', response2.output_text)
            if t.isalnum() and len(t) <= 5  # crude filter
        ]
        for r in tickers:
            if r == "FB": r = "META"  # handle Facebook->Meta change
            st.write(f"Ticker: {r}")
            fetch_and_plot_ticker(r, company_tickers, headers, show_plot=True)
    except Exception as e:
        st.write(f"OpenAI or fetch competitor data error: {e}")




  
