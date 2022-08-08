
import datetime
import sys
import time,json
import urllib.request
import pymongo
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
check_datetime= datetime.datetime.now()
catch_data=None
time_for_catch=None
operator=""
time_str =""
cred = credentials.Certificate('lottery_firebase.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
lottery_2d_collection = db.collection('lottery_2d')
def transfertofile():
    if(catch_data!=None):
        client = pymongo.MongoClient("mongodb+srv://flame:flame123@lottery.g8kow.mongodb.net/?retryWrites=true&w=majority")
        mydb = client.lottery
        collection2D = mydb.lottery_2D
        collection2D.insert_one(catch_data)
        if(catch_data['result']!='Market closed'):
            lottery_2d_collection.document(time_str).set(catch_data)


def checkand_add_data(myanmarstocktime,data):
    global catch_data
    if(operator=="lessthanequal"):
        if ( myanmarstocktime.time()<= time_for_catch.time()):
            catch_data=data
            return False
        else:
            return True


def initial_2d_day():
    print("reach")
    if(time_str=="09:30:00"):
        lottery_2d_collection.document("12:01:00").set(None)
        lottery_2d_collection.document("16:30:00").set(None)


def collecteddata():
    global catch_data
    global check_datetime
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

        marketstatus = data['market_status']
        utctimezone = datetime.datetime.utcnow()
        currentmyanmartime = utctimezone + datetime.timedelta(hours=6, minutes=30)
        currentmyanmartimestring = currentmyanmartime.strftime("%d/%m/%Y %H:%M:%S")

        if (check_datetime == None):

            if (marketstatus == 'Closed' or marketstatus == '' or marketstatus == None):
                catch_data = {"_id": currentmyanmartime.strftime("%d/%m/%Y %H:%M:%S"),
                              "readed_date": currentmyanmartime.strftime("%d/%m/%Y"),
                              "stocktime_mm": currentmyanmartimestring, "result": "Market closed",
                              "Result_for": time_str}
                return True
            else:
                initial_2d_day()

        stockdatetime = data['datetime']
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

        if(check_datetime==None or myanmarstocktime!=check_datetime):
            print(check_datetime)
            print(myanmarstocktime.strftime("%d/%m/%Y %H:%M:%S"))
            print(currentmyanmartimestring, myanmarstocktime.strftime("%d/%m/%Y %H:%M:%S"), forshow_set, forshow_totalvalue, result, marketstatus)
            data={"_id":currentmyanmartime.strftime("%d/%m/%Y %H:%M:%S"),"readed_date":currentmyanmartime.strftime("%d/%m/%Y"),"stocktime_mm":myanmarstocktime.strftime("%d/%m/%Y %H:%M:%S"),"mm_currenttime":currentmyanmartimestring,"set":forshow_set,"forshow_totalvalue":forshow_totalvalue,"result":result,"marketstatus":marketstatus,"Result_for":time_str}
            check_datetime=myanmarstocktime
            return checkand_add_data(myanmarstocktime,data)
    except Exception as e:
        print(e)
    return False

if __name__ == '__main__':
    try:

        operator=sys.argv[1]
        time_str=sys.argv[2]
        time_for_catch=datetime.datetime.strptime(time_str,"%H:%M:%S")

        currenttime = datetime.datetime.now()
        check_datetime = None
        stoptime=currenttime+datetime.timedelta(hours=0, minutes=4)
        while currenttime<stoptime:

            timestop=collecteddata()
            if(timestop==True):
               break
            currenttime = datetime.datetime.now()
            time.sleep(0.5)
        transfertofile()
        print("Thread Run Success")
    except Exception as e:
        print(e)
        print("operator and ""%H:%M:%S should be assign argument")


