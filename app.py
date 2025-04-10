import pandas as pd
from matplotlib.pylab import *
import streamlit as st
from ftplib import FTP_TLS
import ftplib
from io import BytesIO
import io

import requests
from datetime import date
from datetime import datetime
from datetime import timedelta


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



symbols = []
try:
    #ftp = FTP_TLS('minty-web.com')
    #print('going to the sever....')
    #print('loged in....')
    #ftp.login(st.secrets["ftpname"], st.secrets["key"])
    #ftp.prot_p()
    #ftp.set_pasv('true')
    #ftp.cwd(st.secrets["path"])
    #
    #flo = BytesIO()
    #ftp.retrlines('RETR ' + 'excelentones.txt', symbols.append)
    #symbols = symbols[0]
    #symbols = symbols.split(', ')
    #flo = BytesIO()
    #ftp.retrbinary('RETR ' + 'EPS.csv', flo.write)
    #flo.seek(0)
    #df2 = pd.read_csv(flo, index_col=None, header=0)
    #df2 = df2.set_index('Symbol')
    #df2 = df2.drop(columns='Industry')
    #df2 = df2.drop(columns='Sector')
    #df2 = df2.drop(columns='EST1')
    #df2 = df2.drop(columns='EST2')
    #df2 = df2.drop(columns='EST3')
    #df2 = df2.drop(columns='EST4')
    ##df2 = df2.drop(columns='Surprise(%)')
    #df2 = df2.drop(columns='date check')
    #df2 = df2.dropna(how='all', axis=1)
    #
    #flo = BytesIO()
    #ftp.retrbinary('RETR ' + 'revenue.csv', flo.write)
    #flo.seek(0)
    #df1 = pd.read_csv(flo, index_col=None, header=0)
    #df1 = df1.set_index('Symbol')
    #df1 = df1.drop(columns='Industry')
    #df1 = df1.drop(columns='Sector')
    #df1 = df1.drop(columns='EST1')
    #df1 = df1.drop(columns='EST2')
    #df1 = df1.drop(columns='EST3')
    #df1 = df1.drop(columns='EST4')
    #df1 = df1.dropna(how='all', axis=1)
    
    
    def calculate_eps_growth(current_eps, previous_eps):
        eps_growth = ((current_eps - previous_eps) / abs(previous_eps)) * 100
        return eps_growth
    
    
    st.set_page_config(layout="wide")
    
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False
    #choosensymbol = st.sidebar.selectbox('Select', symbols)
    #on = st.toggle('Select a symbol which has revenue announcement today')
    on2 = st.toggle('Search from symbol')
    #if on:
        #st.write('昨日良いEPS成長率が出た銘柄から選ぶ')
        #choosensymbol = st.radio("Select", (symbols), horizontal=True)
    if on2:
        choosensymbol = st.text_input('Put Ticker Symbol. e.g.)AAPL').upper()
    
    
    url = 'https://finance.yahoo.com/quote/' + choosensymbol + '/financials?p=' + choosensymbol
    st.write("Yahoo Finance [Page](%s)" % url)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        #EPS推移のグラフ
        #tickersymbol2 = df2.loc[choosensymbol]
        #surprise = tickersymbol2.loc["Surprise(%)"]
        #tickersymbol2 = tickersymbol2.drop('Surprise(%)')
        #print(tickersymbol2)
        eps_list = []
        paireddate_list = []
        #df2 = df2.drop(columns='Surprise(%)')
        #date_list2 = df2.columns[-10:].to_list()
        ##print(date_list2)
        #del date_list2[0]
    #
        #for d in date_list2:
        #    print(d)
        #    paireddate_list.append((d))
        #    if tickersymbol2[d] == float:
        #        eps_list.append(tickersymbol2[d])
        #    else:
        #        t = str(tickersymbol2[d])
        #        t = t.replace('−','-')
        #        eps_list.append(float(t))
        ##eps_list2 = []
        ##for p in eps_list:
        ##    p2 = str(p)
        ##    eps_list2.append(p2)





        item = next((item for item in companyTickers.json().values() if item['ticker'] == choosensymbol), None)
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
        if int(filed)  < 40:
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

        fig = plt.figure(figsize=(10, 5))
        #grid(color='#2A3459')
        ax = epss.tail(10).plot(x="closed_dates", y=["EPS"], marker='o', color='#FE53BB')
        epss.tail(10).plot(x="closed_dates", y=["Revenue"], secondary_y=True, ax =ax,  marker='o', color='#0040ff')
        plt.title('Ticker: ' + choosensymbol + '    ESP and Revenue Quately Trend')
        plt.xticks(size=8, rotation=-75)
        #plt.savefig(r"C://Users//TK//Desktop//pimage//" + choosensymbol + ".png")  # save the figure to file
        st.pyplot(fig)








#        #fig = plt.figure()
#        #eps = plot(paireddate_list, eps_list)
#        #plt.title('Ticker: ' + choosensymbol + '    EPS Quately Trend')
#        #st.pyplot(fig)
#        ###########################################################
#        date_list = df1.columns.to_list()
#        del date_list[0]
#        #choosensymbol = st.text_input('Put ticker symbol', 'AAPL')
#        tickersymbol = df1.loc[choosensymbol]
#        rev_list = []
#        qrev_list = []
#        rpaireddate_list = []
#        qrpaireddate_list = []
#        for d in date_list:
#            if len(d) > 5:
#                qrpaireddate_list.append((d))
#                tt = str(tickersymbol[d])
#                t = tt.replace(',', '')
#                qrev_list.append(float(t))
#            else:
#                rpaireddate_list.append((d))
#                tt = str(tickersymbol[d])
#                t = tt.replace(',', '')
#                rev_list.append(float(t))
#        #print(rev_list)
#        #print(rpaireddate_list)
#    with col2:
#        fig2 = plt.figure()
#        rev = plot(qrpaireddate_list, qrev_list)
#        plt.title('Ticker: ' + choosensymbol + '    Revenue Quately Trend')
#        st.pyplot(fig2)
#    with col3:
#        fig1 = plt.figure()
#        rev = plot(rpaireddate_list, rev_list)
#        plt.title('Ticker: ' + choosensymbol + '    Revenue Yearly Trend')
#        st.pyplot(fig1)
#    
#    #今四半期前年度成長率　数値比、　前四半期前年度成長率　数値比
#    #date_list2  #EPS日付リスト
#    #tickersymbol2  #EPS数値リスト
#    
#    tickersymbol2 = tickersymbol2.dropna(how='all')
#    #今期
#    this = tickersymbol2[-1]
#    if this == float:
#        this = this
#    else:
#        this = this.replace('−','-')
#    peps_q2 = float(this)  #今期EPS
#    
#    t = tickersymbol2[-5]
#    if t == float:
#        t = t
#    else:
#        t = t.replace('−','-')
#    peps_q1 = float(t)  #一年前ののEPS
#    
#    #前期
#    l = tickersymbol2[-2]
#    eps_q2 = float(l)  #前期の四半期EPS
#    la = tickersymbol2[-6]
#    if la == float:
#        la = la
#    else:
#        la = la.replace('−','-')
#    eps_q1 = float(la)  #前期の一年前の四半期EPS
#    
#    with col1:  #(当期EPS－前期EPS）÷前期EPS×100
#        st.text('Year-on-year change')
#        # Example EPS values
#        # Calculate EPS growth QoQ
#        eps_growth_qoq = calculate_eps_growth(
#            peps_q2, peps_q1)  #calculate_eps_growth(current_eps, previous_eps)
#        st.subheader(f"EPS growth rate (YoY) for last quarter was: {eps_growth_qoq:.2f}%")
#    
#        eps_growth_qoq = calculate_eps_growth(eps_q2, eps_q1)
#        st.subheader(f"EPS growth rate (YoY) 2 quater before was: {eps_growth_qoq:.2f}%"
#                     )  #calculate_eps_growth(current_eps, previous_eps)
#        
#    
#    st.subheader('EPS surprises this quarter are' + str(surprise) + '%')
except:
    pass


