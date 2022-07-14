
import datetime
import time,json
import urllib.request
check_datetime= datetime.datetime.now()
datalist=[]
filename="marketclose"

def savefile(file_name,data):
    with open(file_name,"w")as outfile:
        outfile.write(data)



def transfertofile():
    if(len(datalist)==0):
        print("no data")
        list={filename:"no data"}
    else:
        list={filename:datalist}

    jsonfomat = json.dumps(list, indent=4)
    print(filename+'.json')
    savefile(filename+'.json', jsonfomat)

def save_result(param):
    pass


def viewdata():
    global filename
    global check_datetime
    global datalist
    try:
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
        utctimezone=datetime.datetime.utcnow()
        currentmyanmartime=utctimezone+datetime.timedelta(hours=6, minutes=30)
        currentmyanmartimestring = currentmyanmartime.strftime("%d/%m/%y %H:%M:%S")

        if(check_datetime==None):
            check_datetime=myanmarstocktime
            print(currentmyanmartimestring, myanmarstocktime.strftime("%d/%m/%y %H:%M:%S"), forshow_set, forshow_totalvalue, result, marketstatus)
            temp={"stocktime_mm":myanmarstocktime.strftime("%d/%m/%y %H:%M:%S"),"mm_currenttime":currentmyanmartimestring,"set":forshow_set,"forshow_totalvalue":forshow_totalvalue,"result":result,"marketstatus":marketstatus}
            datalist.append(temp)
        elif(myanmarstocktime!=check_datetime):
            print(currentmyanmartimestring, myanmarstocktime.strftime("%d/%m/%y %H:%M:%S"), forshow_set, forshow_totalvalue, result, marketstatus)
            temp={"stocktime_mm":myanmarstocktime.strftime("%d/%m/%y %H:%M:%S"),"mm_currenttime":currentmyanmartimestring,"set":forshow_set,"forshow_totalvalue":forshow_totalvalue,"result":result,"marketstatus":marketstatus}
            datalist.append(temp)

        if(datetime.time(9,28,00)<myanmarstocktime.time()<=datetime.time(9,31,0)):
            save_result("9am")
            filename="9am"
            return True
        elif (datetime.time(9,31,0)<myanmarstocktime.time() <= datetime.time(12, 2, 0)):
            save_result("12pm")
            filename = "12pm"
            return True
        elif (datetime.time(12, 2, 0)<myanmarstocktime.time() <= datetime.time(14, 1, 0)):
            filename = "2pm"
            save_result("2pm")
        elif (datetime.time(14, 1, 0)<myanmarstocktime.time() <= datetime.time(16, 31, 0)):
            filename = "4pm"
            save_result("4pm")
        else:
            filename = "marketclose"
            save_result("marketclose")

        if (marketstatus == 'Closed'or marketstatus == ''):
            return True
    except Exception as e:
        print(e)


if __name__ == '__main__':
    filename = "marketclose"
    currenttime = datetime.datetime.now()
    check_datetime = None
    stoptime=currenttime+datetime.timedelta(hours=0, minutes=3)
    datalist=[]
    while currenttime<stoptime:

        timestop=viewdata()
        if(timestop==True):
           break
        currenttime = datetime.datetime.now()
        time.sleep(0.5)
    transfertofile()
    print("finished Task")
