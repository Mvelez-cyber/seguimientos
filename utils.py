import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import gspread

def get_gsheet_credentials():
    """Obtiene y formatea las credenciales de Google Sheets desde los secrets de Streamlit"""
    try:
        # Obtener la clave privada y asegurarse de que tenga el formato correcto
        private_key = st.secrets["gcp_service_account"]["private_key"]
        # Reemplazar \\n con saltos de línea reales si es necesario
        private_key = private_key.replace('\\n', '\n')
        
        credentials = {
            "type": st.secrets["gcp_service_account"]["type"],
            "project_id": st.secrets["gcp_service_account"]["project_id"],
            "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
            "private_key": private_key,
            "client_email": st.secrets["gcp_service_account"]["client_email"],
            "client_id": st.secrets["gcp_service_account"]["client_id"],
            "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
            "token_uri": st.secrets["gcp_service_account"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"]
        }
        return credentials
    except Exception as e:
        st.error(f"Error al obtener las credenciales: {str(e)}")
        st.stop()

def initialize_gsheet_client():
    """Inicializa y retorna el cliente de Google Sheets"""
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    
    try:
        credentials = get_gsheet_credentials()
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error al inicializar el cliente: {str(e)}")
        st.stop() 