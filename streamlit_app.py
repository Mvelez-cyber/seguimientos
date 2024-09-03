import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

# Configuración de autenticación de Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open('TasksSheet').sheet1  # Abre la hoja de cálculo

# Función para cargar datos desde Google Sheets
def load_data():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Función para guardar datos en Google Sheets
def save_data(df):
    sheet.clear()  # Limpia la hoja
    sheet.update([df.columns.tolist()] + df.values.tolist())  # Actualiza la hoja

st.title('Gestión de Tareas - Proyecto')

# Cargar datos
df = load_data()

# Seleccionar una fecha
fecha = st.date_input('Selecciona una fecha', datetime.today())

# Mostrar las tareas del día seleccionado
st.write(f'Tareas para {fecha}')
tareas_dia = df[df['Fecha'] == str(fecha)]
st.table(tareas_dia)

# Formulario para añadir una tarea
with st.form(key='task_form'):
    tarea = st.text_input('Descripción de la tarea')
    estado = st.selectbox('Estado', ['Pendiente', 'En Progreso', 'Completa'])
    submit_button = st.form_submit_button(label='Añadir tarea')

    if submit_button and tarea:
        new_task = pd.DataFrame({'Fecha': [str(fecha)], 'Tarea': [tarea], 'Estado': [estado]})
        df = pd.concat([df, new_task], ignore_index=True)
        save_data(df)
        st.success('Tarea añadida correctamente')

# Opción para eliminar una tarea
tarea_eliminar = st.selectbox('Eliminar tarea', df['Tarea'].unique())
if st.button('Eliminar tarea'):
    df = df[df['Tarea'] != tarea_eliminar]
    save_data(df)
    st.success('Tarea eliminada correctamente')
