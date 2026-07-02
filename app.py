import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import re
import requests
from openai import OpenAI

api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)
headers = {"User-Agent": "takakokunugi@gmail.com"}


@st.cache_data(ttl="1d")
def get_company_tickers(headers):
    return requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers).json()


company_tickers = get_company_tickers(headers)


# Helper class to robustly parse floats
class FloatProcessor:

    def __init__(self, s):
        self.s = s

    def process(self):
        s = re.sub(r'[^\x00-\x7F]+', '-', str(self.s))
        return float(s)


# Some filers use different us-gaap tags for the same concept.
EPS_TAGS = ["EarningsPerShareDiluted", "EarningsPerShareBasic"]
REVENUE_TAGS = [
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "RevenueFromContractWithCustomerIncludingAssessedTax",
    "Revenues",
]


def _first_available_tag(us_gaap_facts, tags):
    for tag in tags:
        if tag in us_gaap_facts:
            return tag
    raise KeyError(f"None of the expected tags found: {tags}")


@st.cache_data(ttl="1h")
def get_company_facts(headers, cik):
    facts = requests.get(
        f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json",
        headers=headers).json()
    us_gaap = facts['facts']['us-gaap']
    eps_tag = _first_available_tag(us_gaap, EPS_TAGS)
    revenue_tag = _first_available_tag(us_gaap, REVENUE_TAGS)
    epss = pd.json_normalize(us_gaap[eps_tag]['units']['USD/shares'])
    revenues = pd.json_normalize(us_gaap[revenue_tag]['units']['USD'])
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
    fig, ax1 = plt.subplots(figsize=(8, 5), facecolor='white')

    # Plot EPS
    data = epss.tail(10)
    ax1.plot(data["closed_dates"], data["EPS"],
             marker='o', markersize=8, linewidth=2.5,
             color='#FE53BB', label='EPS')
    ax1.set_xlabel('Quarter End Date', fontsize=11, fontweight='bold')
    ax1.set_ylabel('EPS ($)', fontsize=11, fontweight='bold', color='#FE53BB')
    ax1.tick_params(axis='y', labelcolor='#FE53BB')
    ax1.grid(True, alpha=0.3, linestyle='--')

    # Plot Revenue on secondary axis
    ax2 = ax1.twinx()
    ax2.plot(data["closed_dates"], data["Revenue"],
             marker='s', markersize=8, linewidth=2.5,
             color='#0040ff', label='Revenue')
    ax2.set_ylabel('Revenue ($)', fontsize=11, fontweight='bold', color='#0040ff')
    ax2.tick_params(axis='y', labelcolor='#0040ff')

    # Formatting
    plt.title(title, fontsize=13, fontweight='bold', pad=15)
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()

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

st.set_page_config(
    page_title="US Stock Analyser",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.set_option('client.showErrorDetails', False)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #FE53BB 0%, #0040ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stTextInput > div > div > input {
        font-size: 1.1rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">US Stock Analyser</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Quarterly financials from SEC EDGAR, with competitor summaries from OpenAI</p>', unsafe_allow_html=True)

# User input for stock ticker
choosensymbol = st.text_input(
    'Enter a stock symbol to analyze:',
    placeholder='e.g., AAPL, MSFT, GOOGL',
    help='Enter any US publicly traded company ticker symbol'
).upper()

if not choosensymbol:
    st.info("Enter a stock symbol above to get started.")
    st.markdown("---")
    st.markdown("""
    ### What this app does
    - Plots EPS and revenue trends over the last 10 quarters, from SEC filings
    - Summarizes a company's main competitors using OpenAI
    - Charts the same trends for up to 5 of those competitors
    - Links out to Yahoo Finance for further research

    ### Example tickers
    - **AAPL** - Apple Inc.
    - **MSFT** - Microsoft Corporation
    - **GOOGL** - Alphabet Inc.
    - **TSLA** - Tesla Inc.
    """)
    st.stop()

url = f'https://finance.yahoo.com/quote/{choosensymbol}/financials?p={choosensymbol}'
st.markdown(f"### {choosensymbol}")
st.markdown(f"[View on Yahoo Finance]({url}) | [SEC Filings](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&ticker={choosensymbol})")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Financial Performance")
    with st.spinner(f'Fetching data for {choosensymbol}...'):
        epss = fetch_and_plot_ticker(choosensymbol, company_tickers, headers)
    if epss is not None and len(epss) > 0:
        latest_eps = epss['EPS'].iloc[-1]
        latest_rev = epss['Revenue'].iloc[-1]
        st.metric(
            label="Latest EPS",
            value=f"${latest_eps:.2f}",
            help="Earnings Per Share (latest quarter)"
        )
        st.metric(
            label="Latest Revenue",
            value=f"${latest_rev/1e9:.2f}B" if latest_rev > 1e9 else f"${latest_rev/1e6:.2f}M",
            help="Quarterly Revenue"
        )

competitor_text = None

with col2:
    st.markdown("### Competitor Analysis")
    with st.spinner('Asking OpenAI for competitors...'):
        try:
            # Compose OpenAI prompt
            prompt = (
                f"What is the name of the company for this symbol {choosensymbol}? "
                "Make a list of the names of the competitors to that company on the US stock market, with their symbols and five main services or products for each, in descending order of sales."
            )
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a specialist of US stock market"},
                    {"role": "user", "content": prompt},
                ],
            )
            competitor_text = response.choices[0].message.content
            st.markdown("#### Competitive Landscape")
            st.write(competitor_text)
        except Exception as e:
            st.error(f"Unable to fetch AI analysis: {e}")
            st.info("Please check your OpenAI API key configuration.")

with col3:
    st.markdown("### Competitor Growth Trends")
    with st.spinner('Loading competitor data...'):
        if competitor_text is None:
            st.info("No competitor data available at this time.")
        else:
            try:
                res2_prompt = f"Extract only US stock ticker symbols from this text (e.g., AAPL, META, MSFT): {competitor_text}"
                response2 = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": res2_prompt}],
                )
                # Tickers are the all-caps 1-5 letter tokens in the reply
                seen = set()
                tickers = []
                for t in re.findall(r'\b[A-Z]{1,5}\b', response2.choices[0].message.content):
                    if t not in seen:
                        seen.add(t)
                        tickers.append(t)

                competitor_count = 0
                for r in tickers:
                    if competitor_count >= 5:  # Limit to 5 competitors
                        break
                    if r == "FB": r = "META"  # handle Facebook->Meta change
                    if r != choosensymbol:  # Don't show the same company
                        st.markdown(f"#### {r}")
                        fetch_and_plot_ticker(r, company_tickers, headers, show_plot=True)
                        competitor_count += 1

                if competitor_count == 0:
                    st.info("No competitor data available at this time.")
            except Exception as e:
                st.error(f"Unable to fetch competitor data: {e}")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Data from <a href='https://www.sec.gov/edgar' target='_blank'>SEC EDGAR</a>,
        competitor summaries from <a href='https://openai.com' target='_blank'>OpenAI</a></p>
        <p><a href='https://www.linkedin.com/in/takako-kunugi-b901361b4/' target='_blank'>Takako Kunugi</a></p>
    </div>
""", unsafe_allow_html=True)




  
