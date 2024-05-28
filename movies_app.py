import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account

import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="reto-firebase-sergio")
dbNames = db.collection("movies")
st.title("Sergio Netflix app")

def get_movies():
    collection_ref = db.collection("movies")
    movies = collection_ref.stream()
    return [doc.to_dict() for doc in movies]

# Sidebar
st.sidebar.header('Opciones')
show_movies = st.sidebar.checkbox('Mostrar Todos los Filmes')

# Mostrar todos los filmes si el checkbox está marcado
if show_movies:
    st.subheader('Todos los Filmes')
    names_ref = list(db.collection(u'movies').stream())
    names_dict = list(map(lambda x: x.to_dict(), names_ref))
    names_dataframe = pd.DataFrame(names_dict)
    st.dataframe(names_dataframe)


# ...
def loadByName(name):
  names_ref = dbNames.where(u'name', u'==', name)
  currentName = None
  for myname in names_ref.stream():
    currentName = myname
  return currentName

st.sidebar.subheader("Buscar filmes")
nameSearch = st.sidebar.text_input("Titulo del filme")
btnFiltrar = st.sidebar.button("Buscar filme")

if btnFiltrar:
  doc = loadByName(nameSearch)
  if doc is None:
    st.sidebar.write("Filme no existe")
  else:
    st.sidebar.write(doc.to_dict())

# ...

def loadByDirector(name):
  names_ref = dbNames.where(u'director', u'==', name)
  currentName = None
  for myname in names_ref.stream():
    currentName = myname
  return currentName

st.sidebar.subheader("Seleccionar director")
# Obtener nombres de directores de la colección "movies"
directores_ref = db.collection("movies")
directores_docs = directores_ref.stream()

# Obtener nombres únicos de directores
nombres_directores = set()
for doc in directores_docs:
    nombres_directores.add(doc.to_dict()["director"])

# Convertir nombres de directores en lista para usar en el selectbox
nombres_directores = list(nombres_directores)

# Mostrar nombres de directores en un selectbox
selected_director = st.sidebar.selectbox('Selecciona un director', nombres_directores)

# Filtrar datos según el director seleccionado
query = directores_ref.where("director", "==", selected_director)
resultados = query.stream()

# Mostrar resultados en el dashboard
st.title('Resultados')
for resultado in resultados:
    st.write(resultado.to_dict())

# ...

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
st.sidebar.markdown("""---""")
newfilme = st.sidebar.text_input("Nuevo filme")
#company = st.text_input("Company")
#director = st.text_input("Director")
#genre = st.selectbox(
#    'Select genre',
#    ('Male','Female','Other'))
#name = st.text_input("Name")
#submit = st.button("NUevo filme")

##Once the name has submitted, upload it to the database
#if company and director and genre and name and submit:
#  doc_ref = db.collection("movies").document(name)
#  doc_ref.set({
#     "company": company,
#     "director": director,
#     "genre": genre,
#     "name": name
#  })
#  st.sidebar.write("Registro inserado correctamente")
