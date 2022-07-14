
import datetime
import time,json
import urllib.request
check_datetime= datetime.datetime.now()
def viewdata():
    global check_datetime
    url = "https://api.settrade.com/api/market/SET/info"
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Referer': 'https://classic.set.or.th/set/mainpage.do/',
        'Pragma': 'no-cache',
    }
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    stockdatetime = data['datetime']
    marketstatus = data['market_status']

    Raw_set = data['index'][0]['last']
    forshow_set = "{:.2f}".format(Raw_set)
    d2_1 = str(forshow_set)[-1:]

    Raw_total_value = data['index'][0]['total_value']
    changed_digit = Raw_total_value / 1000000
    forshow_totalvalue = "{:.2f}".format(changed_digit)
    d2_2 = str(forshow_totalvalue)[-4:-3]
    result=d2_1+d2_2
    datetimeformat = "%d/%m/%Y %H:%M:%S"
    formatedstockdatetime = datetime.datetime.strptime(stockdatetime, datetimeformat)
    myanmarstocktime = formatedstockdatetime - datetime.timedelta(hours=0, minutes=30)
    currentmyanmartime=datetime.datetime.now()
    currentmyanmartimestring = currentmyanmartime.strftime("%d/%m/%y %H:%M:%S")
    if(check_datetime==None):
        check_datetime=myanmarstocktime
        print(currentmyanmartimestring, myanmarstocktime, forshow_set, forshow_totalvalue, result, marketstatus)

    elif(myanmarstocktime!=check_datetime):
        print(currentmyanmartimestring, myanmarstocktime, forshow_set, forshow_totalvalue, result, marketstatus)
    if (marketstatus == 'Closed'or marketstatus == ''):
        return True

if __name__ == '__main__':
    currenttime = datetime.datetime.now()
    check_datetime = None
    stoptime=currenttime+datetime.timedelta(hours=0, minutes=3)

    while currenttime<stoptime:

        timestop=viewdata()
        #if(timestop==True):
         #   break
        currenttime = datetime.datetime.now()
        time.sleep(0.5)
