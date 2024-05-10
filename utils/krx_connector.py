##
import requests
import numpy as np
import pandas as pd
from io import StringIO
from datetime import datetime

class KRX:

    def __init__(self):
        self._endDd = datetime.today().strftime('%Y%m%d')
        self._url_generate = "http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd"
        self._url_download = "http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd"
        self._headers_common = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'http://data.krx.co.kr/',
        }

    def get_prc(self, code, s_date=None, e_date=None):
        if e_date is None:
            e_date = self._endDd

        code_str = str(int(code[0]) * 1) + str(int(code[1]) * 2) + str(int(code[2]) * 1) + \
                   str(int(code[3]) * 2) + str(int(code[4]) * 1) + str(int(code[5]) * 2)
        code_sum = np.sum([int(code_str[j]) for j in range(0, len(code_str))])
        if code_sum % 10 != 0:
            validation_code = (10 - code_sum % 10)
        else:
            validation_code = 0
        isin_ = 'KR7' + code + '00' + str(validation_code)

        data_1 = {
            'isuCd': isin_,
            'strtDd': s_date,
            'endDd': e_date,
            'url': 'dbms/MDC/STAT/standard/MDCSTAT01701',
        }

        otp_req = requests.post(self._url_generate, data=data_1, headers=self._headers_common)

        data_2 = {
            'code': otp_req.content
        }

        dwn_req = requests.post(self._url_download, data=data_2, headers=self._headers_common)
        bytes = dwn_req.content
        bytes_decoded = bytes.decode('euc-kr')

        return pd.read_csv(StringIO(bytes_decoded), sep=",")
