import threading
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from threading import Thread
cred = credentials.Certificate('lottery_firebase.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
lottery_2d_collection = db.collection('lottery_2d')
data = {
    u'name': u'Los Angeles',
    u'state': u'dafafafa',
    u'country': u'USA'
}
lottery_2d_collection.document(u'2d').set(data)
print("success")
# Create an Event for notifying main thread.
callback_done = threading.Event()
# Get access to Firestore

print('Connection initialized')

emp_ref = db.collection('lottery_2d')
emp_ref.document("12:01:00").set(None)
emp_ref.document("16:30:00").set(None)

docs = emp_ref.stream()

for doc in docs:
    print('{} => {} '.format(doc.id, doc.to_dict()))

def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(u'Received document snapshot: {}'.format(doc.id))
        print('{} => {} '.format(doc.id, doc.to_dict()))

doc_ref = db.collection('lottery_2d')
doc_watch = doc_ref.on_snapshot(on_snapshot)

# Keep the app running
#while True:
 #  time.sleep(0.5)
