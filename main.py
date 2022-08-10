import calendar
import json
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uvicorn
from fastapi import FastAPI
import os
import datetime
from threading import Thread
import pymongo
cred = credentials.Certificate('lottery_firebase.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
lottery_2d_collection = db.collection('lottery_2d')

app = FastAPI()
compareservertime=datetime.datetime.now()

def thread_fun():

    #os.system("venv\Scripts\python lottery_result.py")
    os.system("python lottery_result.py")


def thread_12pm_fun(wanted_time):

    os.system("python lottery_result_new.py lessthanequal "+wanted_time)

def thread_4pm_fun(wanted_time):
    os.system("python lottery_result_new.py lessthanequal " + wanted_time)

def thread_9pm_fun(wanted_time):
    os.system("python lottery_result_new.py lessthanequal " + wanted_time)

@app.get("/insert")
async def insert():
    thread=Thread(target=thread_fun)
    thread.start()
    return {"load": "Success"}

@app.get("/insert_12pm")
async def insert_12pm():

    utctimezone = datetime.datetime.utcnow()
    currentmyanmartime = utctimezone + datetime.timedelta(hours=6, minutes=30)
    changedtime=currentmyanmartime.replace(hour=12,minute=1,second=0)
    wanted_time=changedtime.strftime("%H:%M:%S")
    subtime=changedtime-currentmyanmartime

    if(subtime.total_seconds()<=180 and subtime.total_seconds()>=5):
        thread = Thread(target=thread_12pm_fun,args=(wanted_time,))
        thread.start()
        return {"message": "Thread Run Success"}
    else:
        return {"Error": "This function only work between 180s to 5s before 12:01"}


@app.get("/insert_9am")
async def insert_9am():
    utctimezone = datetime.datetime.utcnow()
    currentmyanmartime = utctimezone + datetime.timedelta(hours=6, minutes=30)
    changedtime=currentmyanmartime.replace(hour=9,minute=30,second=0)
    wanted_time=changedtime.strftime("%H:%M:%S")
    subtime=changedtime-currentmyanmartime
    if(subtime.total_seconds()<=180 and subtime.total_seconds()>=5):
        thread = Thread(target=thread_9pm_fun,args=(wanted_time,))
        thread.start()
        return {"message": "Thread Run Success"}
    else:
        return {"Error": "This function only work between 180s to 5s before 9:30"}

@app.get("/insert_4pm")
async def insert_4pm():
    utctimezone = datetime.datetime.utcnow()
    currentmyanmartime = utctimezone + datetime.timedelta(hours=6, minutes=30)
    changedtime=currentmyanmartime.replace(hour=16,minute=30,second=0)
    wanted_time=changedtime.strftime("%H:%M:%S")
    subtime=changedtime-currentmyanmartime
    if(subtime.total_seconds()<=180 and subtime.total_seconds()>=5):
        thread = Thread(target=thread_4pm_fun,args=(wanted_time,))
        thread.start()
        return {"message": "Thread Run Success"}
    else:
        return {"Error": "This function only work between 180s to 5s before 16:30"}


@app.get("/")
async def root():
    client = pymongo.MongoClient(
        "mongodb+srv://flame:flame123@lottery.g8kow.mongodb.net/?retryWrites=true&w=majority")
    return client.list_database_names()

def excesstime(define_time):
    if(define_time=='9am'):
        if(compareservertime.time()> datetime.time(9,30,0)):
            return True
    elif(define_time=='12pm'):
        if (compareservertime.time() > datetime.time(12, 1,0)):
            return True
    elif(define_time=='2pm'):
        if(compareservertime.time() > datetime.time(14, 0,0)):
            return True
    elif(define_time=='4pm'):
        if(compareservertime.time() > datetime.time(16, 30,0)):
            return True
    else:
        return False
    return False
@app.get("/result/{name}")
async def say_hello(name: str):
    if(name=='marketclose'or name=='9am'or name=='12pm'or name=='2pm'or name=='4pm'):
        f=open(name+'.json', "r")
        data=json.loads(f.read())
        return data
    else:
        return {"url":["/result/marketclose","/result/9am","/result/12pm","/result/2pm","/result/4pm"]}


@app.get("/monthly/{time}")
async def monthly(time:str):
    try:
        requestedtime=datetime.datetime.strptime(time,"%m-%Y")
        days_in_month = calendar.monthrange(requestedtime.year, requestedtime.month)[1]
        nexttime= requestedtime + datetime.timedelta(days=days_in_month)
        client = pymongo.MongoClient('mongodb+srv://flame:flame123@lottery.g8kow.mongodb.net/test')
        result = client['lottery']['lottery_2D'].aggregate([
            {
                '$project': {
                    'calendar_date': {
                        '$dateFromString': {
                            'format': '%d/%m/%Y',
                            'dateString': '$readed_date'
                        }
                    },
                    'set': 1,
                    'result': 1,
                    'forshow_totalvalue': 1,
                    'marketstatus': 1,
                    'Result_for': 1
                }
            },
            {
                '$match': {
                    'calendar_date': {
                        '$gte': datetime.datetime(requestedtime.year,requestedtime.month,1,00,00,00),
                        '$lt': datetime.datetime(nexttime.year,nexttime.month,1,00,00,00)
                    },
                    '$or': [
                        {
                            'Result_for': '16:30:00'
                        }, {
                            'Result_for': '12:01:00'
                        }
                    ]
                    },
            },
            {
                    '$sort': {
                    'calendar_date': -1
                    }
            }

        ])
        bc=[];
        for r in result:
            if(r["result"]!="Market closed"):
                i={
                    r["calendar_date"].strftime("%d/%m/%Y")+" "+r["Result_for"]:{
                        "r": "(" + r["result"] + ")",
                         "s":r["set"],
                        "v":r["forshow_totalvalue"],

                    }
                }
                bc.append(i);
            else:
                i = {
                    r["calendar_date"].strftime("%d/%m/%Y")+" "+ r["Result_for"]:{
                        "r":"-"
                    }
                }
                bc.append(i);


        return bc;
    except Exception as e:
       print(e)
       return {"error":e.__str__()}

@app.get("/monthly_result/{time}")
async def monthly_result(time: str):
        try:
            requestedtime = datetime.datetime.strptime(time, "%m-%Y")
            days_in_month = calendar.monthrange(requestedtime.year, requestedtime.month)[1]

            nexttime = requestedtime + datetime.timedelta(days=days_in_month)
            client = pymongo.MongoClient('mongodb+srv://flame:flame123@lottery.g8kow.mongodb.net/test')
            result = client['lottery']['lottery_2D'].aggregate([
                {
                    '$project': {
                        'calendar_date': {
                            '$dateFromString': {
                                'format': '%d/%m/%Y',
                                'dateString': '$readed_date'
                            }
                        },
                        'set': 1,
                        'result': 1,
                        'forshow_totalvalue': 1,
                        'marketstatus': 1,
                        'Result_for': 1
                    }
                },
                {
                    '$match': {
                        'calendar_date': {
                            '$gte': datetime.datetime(requestedtime.year, requestedtime.month, 1, 00, 00, 00),
                            '$lt': datetime.datetime(nexttime.year, nexttime.month, 1, 00, 00, 00)
                        },
                        '$or': [
                            {
                                'Result_for': '16:30:00'
                            }, {
                                'Result_for': '12:01:00'
                            }
                        ]
                    },
                },
                {
                    '$sort': {
                        'calendar_date': -1
                    }
                }

            ])
            bc = [];
            for r in result:
                if (r["result"] != "Market closed"):
                    i = {
                        r["calendar_date"].strftime("%d/%m/%Y") + " " + r["Result_for"]:  "<<"+r["result"]+">>"
                    }
                    bc.append(i)
                else:
                    i = {
                        r["calendar_date"].strftime("%d/%m/%Y")+" "+ r["Result_for"]:  "-"
                    }
                    bc.append(i)

            return bc;
        except Exception as e:
            print(e)
            return {"error": e.__str__()}


@app.get("/selectedresult/{name}")
async def say_hello(name: str):
    global compareservertime
    if ( name == '9am' or name == '12pm' or name == '2pm' or name == '4pm'):

        tempsetdata = {"temp": "temp"}
        finaldata={"temp": "temp"}
        olddata={"temp": "temp"}

        client = pymongo.MongoClient(
            "mongodb+srv://flame:flame123@lottery.g8kow.mongodb.net/?retryWrites=true&w=majority")
        mydb = client.lottery
        collection2D = mydb.l_2d

        for resultlist in collection2D.find({"_id":name+".json"}):
            for setlist in resultlist['results']:
                compareservertime=datetime.datetime.strptime(setlist['stocktime_mm'], "%d/%m/%y %H:%M:%S")
                mmcurrenttime = datetime.datetime.strptime(setlist['mm_currenttime'], "%d/%m/%y %H:%M:%S")
                print(compareservertime,"---",mmcurrenttime)

                if (excesstime(name)):
                    finaldata=olddata
                    record={"Result_For":name,"stocktime_mm":finaldata['stocktime_mm'],"SET":finaldata["set"],"Total_Value":finaldata["forshow_totalvalue"],"Result":finaldata["result"]}
                    mydb.lottery2D.insert_one(record)
                    print("finaldata---", finaldata)
                    break
                if(name == '4pm'):
                    finaldata=setlist
                    print("finaldata", "else---", finaldata)
                olddata=setlist
            if(name == '4pm'):
                record = {"Result_For": name, "stocktime_mm": finaldata['stocktime_mm'], "SET": finaldata["set"],
                          "Total_Value": finaldata["forshow_totalvalue"], "Result": finaldata["result"]}
                mydb.lottery2D.insert_one(record)
            return {name+"_result":finaldata,"datalist":resultlist['results']}
        return {"result": "no Record"}
    else:
        return {"url": [ "/selectedresult/9am", "/selectedresult/12pm", "/selectedresult/2pm", "/selectedresult/4pm"]}

@app.get("/display")
async def display():
    pm12_doc = lottery_2d_collection.document('12:01:00')
    pm12_data=pm12_doc.get().to_dict()
    data1={}
    if (pm12_data):
        data1={"result":pm12_data["result"],"Date":pm12_data["readed_date"],"SET":pm12_data["set"],"Total_value":pm12_data["forshow_totalvalue"]}
    pm4_doc = lottery_2d_collection.document('16:30:00')
    pm4_data=pm4_doc.get().to_dict()
    data2 = {}
    if(pm4_data):
        data2={"result":pm4_data["result"],"Date":pm4_data["readed_date"],"SET":pm4_data["set"],"Total_value":pm4_data["forshow_totalvalue"]}
    return {"12:01pm":data1,"4:30pm":data2}

@app.get("/displaydetail")
async def display():
    pm12_doc = lottery_2d_collection.document('12:01:00')
    pm12_data=pm12_doc.get().to_dict()
    pm4_doc = lottery_2d_collection.document('16:30:00')
    pm4_data=pm4_doc.get().to_dict()
    return {"12:01pm":pm12_data,"4:30pm":pm4_data}