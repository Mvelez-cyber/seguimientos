import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_gsheet_credentials():
    """Obtiene las credenciales de Google Sheets desde los secrets de Streamlit"""
    required_fields = [
        "type", "project_id", "private_key_id", "private_key",
        "client_email", "client_id", "auth_uri", "token_uri",
        "auth_provider_x509_cert_url", "client_x509_cert_url",
        "universe_domain"
    ]
    
    credentials = {}
    for field in required_fields:
        try:
            credentials[field] = st.secrets["gcp_service_account"][field]
        except KeyError:
            st.error(f"Falta la credencial requerida: {field}")
            st.stop()
            
    return credentials

def initialize_gsheet_client():
    """Inicializa y retorna el cliente de Google Sheets"""
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    
    try:
        credentials = get_gsheet_credentials()
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"Error al inicializar el cliente de Google Sheets: {str(e)}")
        st.stop() 