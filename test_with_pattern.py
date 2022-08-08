import datetime
import sys
import time,json
import urllib.request
import pymongo
import re
import firebase_admin
from jsonpath_ng import jsonpath, parse
firebase_db={
    "firebase_db":[{
        "url":"https://api.settrade.com/api/market/SET/info",
        "market_status":'market_status',
        "server_time":'datetime',
        "SET":"index[0].last",
        "value":"index[0].total_value",
        "Setting":
            {
                "servertime_format":"%d/%m/%Y %H:%M:%S",
                "servertime_pattern":"\\d{1,2}/\\d{1,2}/\\d{4} \\d{2}:\\d{2}:\\d{2}",

                "market_status_for_close":"close",

                "SET_digit":"1",
                "SET_represent_digit":"{:.2f}",

                "Set_index":-1,

                "Value_digit":"1000000",
                "Value_represent_digit":"{:.2f}",

                "Value_start_index":-4,
                "Value_end_index":-3

            }
    },{
        "url": "https://www.settrade.com/api/set/index/info/list?type=INDEX",
        "market_status": 'indexIndustrySectors[0].marketStatus',
        "server_time": 'indexIndustrySectors[0].marketDateTime',
        "SET": "indexIndustrySectors[0].last",
        "value": "indexIndustrySectors[0].value",
        "Setting":
            {
                "servertime_format": "%Y-%m-%dT%H:%M:%S",
                "servertime_pattern":"\\d{4}-\\d{1,2}-\\d{1,2}T\\d{2}:\\d{2}:\\d{2}",

                "  bb": "close",

                "SET_digit": "1",
                "SET_represent_digit": "{:.2f}",
                "Set_index": -1,

                "Value_digit": "1000000",
                "Value_represent_digit": "{:.2f}",
                "Value_start_index": -4,
                "Value_end_index": -3

            }
    }]}
def print_2d(data_market_status,data_servertime,data_set,data_value,label_setting):

    print("Market:",data_market_status)

    #Thai Sever time to Myanmar time
    datetime_pattern = re.compile(label_setting['servertime_pattern'])
    thaistocktime = datetime.datetime.strptime(datetime_pattern.search(data_servertime).group(), label_setting["servertime_format"])
    myanmarstocktime = thaistocktime - datetime.timedelta(hours=0, minutes=30)
    print("Myanmar Stocktime",myanmarstocktime)

    #Set value
    divider=int(label_setting["SET_digit"])
    set_divider=data_set/divider
    set_value=label_setting["SET_represent_digit"].format(set_divider)
    print("SET:", set_value)
    d2_1 = str(set_value)[label_setting["Set_index"]:]

    #Total Value
    divider=int(label_setting["Value_digit"])
    totalvalue_divider=data_value/divider
    total_value=label_setting["Value_represent_digit"].format(totalvalue_divider)
    print("TotalValue:", total_value)
    d2_2 = str(total_value)[label_setting["Value_start_index"]:label_setting["Value_end_index"]]

    #2digit
    print("Result:"+d2_1+":"+d2_2)
def urlload(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    info = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    return info

def  print_data(marketinfo,selector):
    jsonpath_expression = parse(selector)
    data = jsonpath_expression.find(marketinfo)
    print(data[0].value)
    return data[0].value
def readdata(marketinfo,label_martket_status,label_servertime,label_set,label_value,label_setting):
    data_market_status=print_data(marketinfo, label_martket_status)
    data_servertime=print_data(marketinfo, label_servertime)
    data_set=print_data(marketinfo, label_set);
    data_value=print_data(marketinfo, label_value);
    print_2d(data_market_status,data_servertime,data_set,data_value,label_setting)
def assign_attribute(urldb):
    label_market_status=urldb["market_status"]
    label_servertime=urldb["server_time"]
    label_set=urldb["SET"]
    label_value=urldb["value"]
    label_setting=urldb["Setting"]
    marekt_info=urlload(urldb["url"])
    readdata(marekt_info,label_market_status,label_servertime,label_set,label_value,label_setting)

if __name__ == '__main__':


    for urldb in firebase_db["firebase_db"]:
        print(urldb["url"])
        assign_attribute(urldb)


