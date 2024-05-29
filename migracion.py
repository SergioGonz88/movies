import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

path = "./"

cred = credentials.Certificate(path +"practica-firebase-sergio.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
doc_ref = db.collection(u'movies')
#Import data
df = pd.read_csv(path+'movies.csv')
tmp = df.to_dict(orient='records')
list(map(lambda x: doc_ref.add(x), tmp))