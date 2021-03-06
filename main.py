import json
import datetime
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from dateutil.parser import parse


def createHeader():
    ua = UserAgent()
    user_agent = ua.random
    headers = {
        'Referer': 'https://itunes.apple.com',
        'User-Agent': user_agent,
        'Connection': 'close',
        "Host": "cn.investing.com",
        "X-Requested-With": "XMLHttpRequest",
    }
    return headers


def is_date(string, fuzzy=False):

    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def process_day(date):
    date = date.replace('/', '').replace('-', '')
    year = int(date[0:4])
    mon = int(date[5:6])
    days = int(date[6:8])

    return datetime.datetime(year, mon, days).strftime("%Y/%m/%d")

if __name__ == '__main__':


    start_day = input('請輸入查詢起始時間(20210101).')
    end_day = input('請輸入結束時間(20210531).')

    # 檢查日期格式
    if not is_date(start_day) or not is_date(end_day) :
        exit('日期輸入錯誤')

    # 將日期轉換為固定格式
    start_day = process_day(start_day)
    end_day = process_day(end_day)

    # start_day = '2021/09/10'
    # end_day = '2021/09/25'

    # reauest所需的data格式
    payload = {
        'curr_id': '6408',
        'smlID': '1159963',
        'header': 'AAPL历史数据',
        'st_date': start_day,
        'end_date': end_day,
        'interval_sec': 'Daily',
        'sort_col': 'date',
        'sort_ord': 'DESC',
        'action': 'historical_data'
    }


    url = 'https://cn.investing.com/instruments/HistoricalDataAjax'
    res = requests.post(url, stream=True, data=payload, headers=createHeader(), timeout=20)
    soup = BeautifulSoup(res.text, 'lxml')
    vest_list = [item.get_text().strip().split('\n') for item in soup.find_all('tr')]   # 數據處理

    # 將數據轉換為dict
    result_dict = {}
    for i in range(len(vest_list[0])):
        info = []
        for j in range(1, len(vest_list)-1):
            info.append(vest_list[j][i])
        result_dict.setdefault(vest_list[0][i],info)

    # dict to json
    result = json.dumps(result_dict, indent = 4,ensure_ascii=False)
    print(result)