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

headers = {"User-Agent" : "takakokunugi@gmil.com"}
#get all companies data
companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json",
                             headers = headers)
class floatProcessor:
    def __init__(self, s):
        self.s = s
    def process(self):
        self.s = str(self.s)
        self.s = re.sub(r'[^\x00-\x7F]+', '-', self.s)
        self.s = float(self.s)
        return self.s

def get_company_facts(headers, cik):
    facts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers= headers)
    epss = pd.json_normalize(facts.json()['facts']['us-gaap']['EarningsPerShareDiluted']['units']['USD/shares'])
    revenues = pd.json_normalize(facts.json()['facts']['us-gaap']['RevenueFromContractWithCustomerExcludingAssessedTax']['units']['USD'])
    epss = epss.dropna(subset=['frame'])
    revenues = revenues.dropna(subset=['frame'])
    revenues = revenues[['end','val']]
    revenues = revenues.rename(columns={'val': 'rev'})
    epss = epss.merge(revenues, on = 'end')
    return epss, revenues



def get_days_differ(epss):
    differ = []
    for row in epss.itertuples():
        differDays = pd.to_datetime(row.end) - pd.to_datetime(row.start)
        differDays = pd.to_timedelta(differDays).days
        differ.append(differDays)
        
    epss['differ'] = differ
    epss = epss[~epss['differ'].between(100,300)]
    return epss

    
def calculate_eps_growth(current_eps, previous_eps):
    eps_growth = ((current_eps - previous_eps) / abs(previous_eps)) * 100
    return eps_growth

st.set_option('client.showErrorDetails', False)
st.set_page_config(layout="wide")

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
#choosensymbol = st.sidebar.selectbox('Select', symbols)
#on = st.toggle('Select a symbol which has revenue announcement today')
#on2 = st.toggle('Search from symbol')
#if on:
    #st.write('昨日良いEPS成長率が出た銘柄から選ぶ')
    #choosensymbol = st.radio("Select", (symbols), horizontal=True)
#if on2:
choosensymbol = st.text_input('Put Ticker Symbol. e.g.)AAPL').upper()


url = 'https://finance.yahoo.com/quote/' + choosensymbol + '/financials?p=' + choosensymbol
st.write("Yahoo Finance [Page](%s)" % url)

col1, col2, col3 = st.columns(3)
with col1:
    item = next((item for item in companyTickers.json().values() if item['ticker'] == choosensymbol), None)

    try:
        directCik = item['cik_str']
        comname = item['title']
        cik = str(directCik).zfill(10)
        filingMetadata = requests.get(
            f'https://data.sec.gov/submissions/CIK{cik}.json',
            headers=headers
            )
        companyFacts = requests.get(f'https://data.sec.gov/submissions/CIK{cik}.json', headers=headers)
        
        epss, revenues = get_company_facts(headers, cik)
        
        today = pd.Timestamp.today()
        filed = today - pd.to_datetime(epss.iloc[-1,7]).normalize()
        filed = filed / timedelta(days=1)
    
        get_days_differ(epss)
        epss = epss.drop_duplicates(subset='end',keep = "last")
        epss["eps_3_cal_sum"] = epss["val"].rolling(3).sum().shift()
        epss["rev_3_cal_sum"] = epss["rev"].rolling(3).sum().shift()
        
        #print(epss.tail(20))
        
        eps_3_cal_sum = epss.eps_3_cal_sum.tolist()
        rev_3_cal_sum = epss.rev_3_cal_sum.tolist()
        given_eps = epss.val.tolist()
        given_rev = epss.rev.tolist()
        differ_days = epss.differ.tolist()
        final_epss =[]
        final_rev=[]
        for cal, cal_rev, given, giv_rev, differ in zip(eps_3_cal_sum, rev_3_cal_sum, given_eps, given_rev, differ_days):
            if differ > 300:
                f = given - cal
                r = giv_rev - cal_rev
                final_epss.append(f)
                final_rev.append(r)
            else:
                f=given
                r = giv_rev
                final_epss.append(f)
                final_rev.append(r)
        
        epss['EPS'] = final_epss 
        epss['Revenue'] = final_rev
        epss = epss.rename({'end':'closed_dates'}, axis='columns')
        
        lir=epss['EPS']
        lir = list(lir)
        lir=reversed(lir)  
        lir = list(lir)
        previous = lir[4]
        thisyear = lir[0]
        q1previouseps = lir[1]
        q2previouseps = lir[2]
        q3previouseps = lir[3]
        processor = floatProcessor(previous)
        previous= processor.process()
        processor = floatProcessor(q3previouseps)
        q3previouseps= processor.process()
        processor = floatProcessor(q2previouseps)
        q2previouseps= processor.process()
        processor = floatProcessor(q1previouseps)
        q1previouseps= processor.process()
        processor = floatProcessor(thisyear)
        thisyear= processor.process()
    
        fig = plt.figure()
        ax = epss.tail(10).plot(x="closed_dates", y=["EPS"], marker='o', color='#FE53BB')
        epss.tail(10).plot(x="closed_dates", y=["Revenue"], secondary_y=True, ax =ax,  marker='o', color='#0040ff')
        plt.title('Ticker: ' + choosensymbol + '    ESP and Revenue Quately Trend')
        plt.xticks(size=8, rotation=-75)
        
        st.pyplot(plt)
    except:
      pass


with col2:
  st.write("OpenAI research")

  response = client.responses.create(
      model="gpt-3.5-turbo",
      instructions="You are a specialist of US stock market",
      input="What is the name of the company for this symbol" + choosensymbol + "? Make a list of the names of the competitors to that company on the US stock market, with their symbols and five main services or products for each, in descending order of sales.",)
  st.write(response.output_text)




with col3:
  st.write("competitor's growth")
  responce2 = client.responses.create(model="gpt-3.5-turbo", input = "return only a list in python script, extracting only stock symbols from the text, (eg.['AAPL', 'META', 'MSFT']) "+ response.output_text)
  st.write(responce2.output_text)
  res = responce2.output_text
  for r in res:
    item = next((item for item in companyTickers.json().values() if item['ticker'] == r), None)
    try:
        directCik = item['cik_str']
        comname = item['title']
        cik = str(directCik).zfill(10)
        filingMetadata = requests.get(
            f'https://data.sec.gov/submissions/CIK{cik}.json',
            headers=headers
            )
        companyFacts = requests.get(f'https://data.sec.gov/submissions/CIK{cik}.json', headers=headers)
        
        epss, revenues = get_company_facts(headers, cik)
        
        today = pd.Timestamp.today()
        filed = today - pd.to_datetime(epss.iloc[-1,7]).normalize()
        filed = filed / timedelta(days=1)
    
        get_days_differ(epss)
        epss = epss.drop_duplicates(subset='end',keep = "last")
        epss["eps_3_cal_sum"] = epss["val"].rolling(3).sum().shift()
        epss["rev_3_cal_sum"] = epss["rev"].rolling(3).sum().shift()
        
        #print(epss.tail(20))
        
        eps_3_cal_sum = epss.eps_3_cal_sum.tolist()
        rev_3_cal_sum = epss.rev_3_cal_sum.tolist()
        given_eps = epss.val.tolist()
        given_rev = epss.rev.tolist()
        differ_days = epss.differ.tolist()
        final_epss =[]
        final_rev=[]
        for cal, cal_rev, given, giv_rev, differ in zip(eps_3_cal_sum, rev_3_cal_sum, given_eps, given_rev, differ_days):
            if differ > 300:
                f = given - cal
                r = giv_rev - cal_rev
                final_epss.append(f)
                final_rev.append(r)
            else:
                f=given
                r = giv_rev
                final_epss.append(f)
                final_rev.append(r)
        
        epss['EPS'] = final_epss 
        epss['Revenue'] = final_rev
        epss = epss.rename({'end':'closed_dates'}, axis='columns')
        
        lir=epss['EPS']
        lir = list(lir)
        lir=reversed(lir)  
        lir = list(lir)
        previous = lir[4]
        thisyear = lir[0]
        q1previouseps = lir[1]
        q2previouseps = lir[2]
        q3previouseps = lir[3]
        processor = floatProcessor(previous)
        previous= processor.process()
        processor = floatProcessor(q3previouseps)
        q3previouseps= processor.process()
        processor = floatProcessor(q2previouseps)
        q2previouseps= processor.process()
        processor = floatProcessor(q1previouseps)
        q1previouseps= processor.process()
        processor = floatProcessor(thisyear)
        thisyear= processor.process()
    
        fig = plt.figure()
        ax = epss.tail(10).plot(x="closed_dates", y=["EPS"], marker='o', color='#FE53BB')
        epss.tail(10).plot(x="closed_dates", y=["Revenue"], secondary_y=True, ax =ax,  marker='o', color='#0040ff')
        plt.title('Ticker: ' + choosensymbol + '    ESP and Revenue Quately Trend')
        plt.xticks(size=8, rotation=-75)
        
        st.pyplot(plt)
    except:
      pass




  
