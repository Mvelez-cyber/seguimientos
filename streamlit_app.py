import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

# Configuración de autenticación de Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
service_account_info = dict(st.secrets["gcp_service_account"])
service_account_info['private_key'] = service_account_info['private_key'].replace('\\n', '\n')
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)
sheet = client.open('TasksSheet').sheet1

# Cargar datos desde Google Sheets
def load_data():
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    return df

# Función para guardar datos en Google Sheets
def save_data(df):
    sheet.clear()
    sheet.update([df.columns.tolist()] + df.values.tolist())

st.title('Gestión de Tareas - Proyecto')

# Cargar datos
df = load_data()

# Diagnóstico
st.write("Todas las tareas:")
st.dataframe(df.head(), width=1000)

# Verifica si la columna 'Fecha' está presente
if 'Fecha' not in df.columns:
    st.error("La columna 'Fecha' no está presente en el DataFrame. Verifica el nombre de la columna en Google Sheets.")
    st.stop()

# Seleccionar rango de fechas para visualización
col1, col2 = st.columns(2)
with col1:
    fecha_inicio = st.date_input('Fecha inicial', datetime.today())
with col2:
    fecha_fin = st.date_input('Fecha final', datetime.today())

# Mostrar las tareas del rango seleccionado
st.write(f'Tareas desde {fecha_inicio} hasta {fecha_fin}')
mask = (df['Fecha'] >= str(fecha_inicio)) & (df['Fecha'] <= str(fecha_fin))
tareas_periodo = df[mask]
st.table(tareas_periodo)

# Formulario para añadir una tarea
with st.form(key='task_form'):
    fecha_tarea = st.date_input('Fecha de la tarea', datetime.today())
    tarea = st.text_input('Descripción de la tarea')
    estado = st.selectbox('Estado', ['Pendiente', 'En Progreso', 'Completa'])
    submit_button = st.form_submit_button(label='Añadir tarea')

    if submit_button and tarea:
        new_task = pd.DataFrame({'Fecha': [str(fecha_tarea)], 'Tarea': [tarea], 'Estado': [estado]})
        df = pd.concat([df, new_task], ignore_index=True)
        save_data(df)
        st.success('Tarea añadida correctamente')

# Opción para eliminar una tarea
tarea_eliminar = st.selectbox('Eliminar tarea', df['Tarea'].unique())
if st.button('Eliminar tarea'):
    df = df[df['Tarea'] != tarea_eliminar]
    save_data(df)
    st.success('Tarea eliminada correctamente')
