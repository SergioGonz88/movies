import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account

import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="movies")
dbNames = db.collection("movies")
st.header("Nuevo registro")
company = st.text_input("Company")
director = st.text_input("Director")
genre = st.selectbox(
    'Select genre',
    ('Male','Female','Other'))
name = st.text_input("Name")

submit = st.button("Crear nuevo registro")

#Once the name has submitted, upload it to the database
if company and director and genre and name and submit:
  doc_ref = db.collection("movies").document(name)
  doc_ref.set({
     "company": company,
     "director": director,
     "genre": genre,
     "name": name
  })
  st.sidebar.write("Registro inserado correctamente")
# ...
def loadByName(name):
  names_ref = dbNames.where(u'name', u'==', name)
  currentName = None
  for myname in names_ref.stream():
    currentName = myname
  return currentName

st.sidebar.subheader("Buscar nombre")
nameSearch = st.sidebar.text_input("nombre")
btnFiltrar = st.sidebar.button("Buscar")

if btnFiltrar:
  doc = loadByName(nameSearch)
  if doc is None:
    st.sidebar.write("Nombre no existe")
  else:
    st.sidebar.write(doc.to_dict())
# ...
st.sidebar.markdown("""---""")
btnEliminar = st.sidebar.button("Eliminar")

if btnEliminar:
  deletename = loadByName(nameSearch)
  if deletename is None:
    st.sidebar.write(f"{nameSearch} no existe")
  else:
    dbNames.document(deletename.id).delete()
    st.sidebar.write(f"{nameSearch} eliminado")
#...

st.sidebar.markdown("""---""")
newname = st.sidebar.text_input("Actualizar nombre")
btnActualizar = st.sidebar.button("Actualizar")

if btnActualizar:
  updatename = loadByName(nameSearch)
  if updatename is None:
    st.write(f"{nameSearch} no existe")
  else:
    myupdatename = dbNames.document(updatename.id)
    myupdatename.update(
        {
            "name": newname
        }
    )
# ...
names_ref = list(db.collection(u'names').stream())
names_dict = list(map(lambda x: x.to_dict(), names_ref))
names_dataframe = pd.DataFrame(names_dict)
st.dataframe(names_dataframe)
