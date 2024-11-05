import streamlit as st
from utils import initialize_gsheet_client
import pandas as pd
from datetime import datetime
import gspread

# Inicializar el cliente
client = initialize_gsheet_client()

try:
    # Intentar abrir la hoja de cálculo
    sheet = client.open('TasksSheet').sheet1
except gspread.exceptions.SpreadsheetNotFound as e:
    st.error(f'No se puede encontrar la hoja de cálculo llamada "TasksSheet". Asegúrate de que el nombre sea correcto y que el acceso esté configurado correctamente. Error: {e}')
    st.stop()

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
st.write("Todas las tareas:")
st.dataframe(df.head(), width=1000)  # Ajustamos el ancho a 1000 píxeles

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
