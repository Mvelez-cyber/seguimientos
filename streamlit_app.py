import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

# Configuración de autenticación de Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

try:
    # Intentar abrir la hoja de cálculo
    sheet = client.open('TasksSheet').sheet1
except gspread.exceptions.SpreadsheetNotFound as e:
    st.error(f'No se puede encontrar la hoja de cálculo llamada "TasksSheet". Asegúrate de que el nombre sea correcto y que el acceso esté configurado correctamente. Error: {e}')
    st.stop()  # Detiene la ejecución del script si ocurre un error

# Cargar datos desde Google Sheets
def load_data():
    # Usa get_all_values para obtener los valores crudos
    data = sheet.get_all_values()
    # Convertir los valores en DataFrame usando la primera fila como encabezados
    df = pd.DataFrame(data[1:], columns=data[0])
    return df

# Función para guardar datos en Google Sheets
def save_data(df):
    sheet.clear()  # Limpia la hoja
    sheet.update([df.columns.tolist()] + df.values.tolist())  # Actualiza la hoja

st.title('Gestión de Tareas - Proyecto')

# Cargar datos
df = load_data()

# Diagnóstico
st.write("Columnas disponibles en el DataFrame:")
st.write(df.columns)
st.write("Primeras filas del DataFrame:")
st.write(df.head())

# Verifica si la columna 'Fecha' está presente
if 'Fecha' not in df.columns:
    st.error("La columna 'Fecha' no está presente en el DataFrame. Verifica el nombre de la columna en Google Sheets.")
    st.stop()

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
