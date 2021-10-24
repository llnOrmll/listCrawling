#
#
import requests
from bs4 import BeautifulSoup
import pandas as pd
from utils.krx_connector import KRX
import time
from datetime import datetime, timedelta

class eventList:

    def __init__(self, lastsearch):
        self.sosok = [0, 1]
        self.volume = None
        self.mktcap = None
        self.lastsearch = lastsearch

    def list_by_volume(self):
        for div in self.sosok:
            url = "https://finance.naver.com/sise/sise_quant.naver?sosok={}".format(div)
            res = requests.get(url)
            soup = BeautifulSoup(res.text, "html.parser")
            item = soup.select("a.tltle")
            item_all = [(div, name.get_text(), name['href'][-6:]) for name in item[:50]]
            if self.volume is None:
                self.volume = pd.DataFrame(item_all)
            else:
                self.volume = pd.concat([self.volume, pd.DataFrame(item_all)], axis=0)

        self.volume = self.volume.reset_index(drop=True)
        self.volume.columns = ['market', 'name', 'iscd']
        self.volume = self.volume.drop(self.volume[self.volume['name'].isin(self.lastsearch)].index.tolist(),
                                       axis=0).reset_index(drop=True)
        self.volume["category"] = "volume"

        trading_v = []
        for iscd in self.volume['iscd']:
            temp = KRX().get_prc(iscd, s_date=(datetime.today()-timedelta(days=7)).strftime("%Y%m%d"))
            trading_v.append(temp['거래대금'].mean())
            time.sleep(3)
        self.volume["trading_v"] = trading_v

        return self.volume

    def list_by_mktcap(self):
        for div in self.sosok:
            url = "https://finance.naver.com/sise/sise_market_sum.naver?sosok={}".format(div)
            res = requests.get(url)
            soup = BeautifulSoup(res.text, "html.parser")
            item = soup.select("a.tltle")
            item_all = [(div, name.get_text(), name['href'][-6:]) for name in item]
            if self.mktcap is None:
                self.mktcap = pd.DataFrame(item_all)
            else:
                self.mktcap = pd.concat([self.mktcap, pd.DataFrame(item_all)], axis=0)

        self.mktcap = self.mktcap.reset_index(drop=True)
        self.mktcap.columns = ['market', 'name', 'iscd']
        self.mktcap = self.mktcap.drop(self.mktcap[self.mktcap['name'].isin(self.lastsearch)].index.tolist(),
                                       axis=0).reset_index(drop=True)
        self.mktcap['category'] = "mktcap"

        trading_v = []
        for iscd in self.mktcap['iscd']:
            temp = KRX().get_prc(iscd, s_date=(datetime.today()-timedelta(days=7)).strftime("%Y%m%d"))
            trading_v.append(temp['거래대금'].mean())
            time.sleep(3)
        self.mktcap["trading_v"] = trading_v

        return self.mktcap

    def generate_list(self):
        v = self.list_by_volume()
        m = self.list_by_mktcap()
        combinedlist = pd.concat([v, m], axis=0)
        combinedlist = combinedlist.reset_index(drop=True)
        cols = ['name', 'iscd', 'market', 'category', 'trading_v']
        return combinedlist[cols]

    def summary(self, dataframe=None):
        if dataframe is None:
            df = self.generate_list()
        else:
            df = dataframe

        df = df.drop(df[df['name'].str.contains('인버스|레버리지')].index.tolist(), axis=0)
        df_v = df[df['category'] == 'volume'].copy()
        ksp_v = df_v[df_v['market']==0].sort_values(by='trading_v', ascending=False)[:9]['name'].values
        ksq_v = df_v[df_v['market']==1].sort_values(by='trading_v', ascending=False)[:9]['name'].values
        df_m = df[df['category'] == 'mktcap'].copy()
        ksp_m = df_m[df_m['market']==0].drop(df_m[df_m['name'].isin(ksp_v)].index.tolist(), axis=0).sort_values(by='trading_v', ascending=False)[:9]['name'].values
        ksq_m = df_m[df_m['market']==1].drop(df_m[df_m['name'].isin(ksq_v)].index.tolist(), axis=0).sort_values(by='trading_v', ascending=False)[:9]['name'].values

        return pd.DataFrame([self.lastsearch, ksp_v, ksq_v, ksp_m, ksq_m], index=["네이버검색", "거래량(코스피)", "거래량(코스닥)", "시총(코스피)", "시총(코스닥)"]).T
