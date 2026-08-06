import pandas as pd
from polotrial_client import PoloTrialClient


def carregar_dados_protocolo(client: PoloTrialClient, protocolos: list[str]) -> pd.DataFrame:
    """
    Carrega os dados dos protocolos fornecidos usando o cliente Polotrial.

    Args:
        client (PoloTrialClient): Instância do cliente Polotrial.
        protocolos (list[str]): Lista de protocolos a serem carregados.

    Returns:
        pd.DataFrame: DataFrame contendo os dados dos protocolos.
    """
    protocolos_data = client.get_protocolos(protocolos)
    
    # Converte a lista de dicionários em um DataFrame
    df_protocolos = pd.DataFrame(protocolos_data)
    
    return df_protocolos

def carregar_dados_participantes(client: PoloTrialClient, participantes: list[str]) -> pd.DataFrame:
    """
    Carrega os dados dos participantes fornecidos usando o cliente Polotrial.

    Args:
        client (PoloTrialClient): Instância do cliente Polotrial.
        participantes (list[str]): Lista de participantes a serem carregados.

    Returns:
        pd.DataFrame: DataFrame contendo os dados dos participantes.
    """
    participantes_data = client.get_participantes(participantes)
    
    # Converte a lista de dicionários em um DataFrame
    df_participantes = pd.DataFrame(participantes_data)
    
    return df_participantes


def carregar_dados_participante_visita(client: PoloTrialClient, participante_visita: list[str]) -> pd.DataFrame:
    """
    Carrega os dados das visitas dos participantes fornecidos usando o cliente Polotrial.

    Args:
        client (PoloTrialClient): Instância do cliente Polotrial.
        participante_visita (list[str]): Lista de visitas dos participantes a serem carregadas.

    Returns:
        pd.DataFrame: DataFrame contendo os dados das visitas dos participantes.
    """
    participante_visita_data = client.get_participante_visita(participante_visita)
    
    # Converte a lista de dicionários em um DataFrame
    df_participante_visita = pd.DataFrame(participante_visita_data)
    
    return df_participante_visita

# if __name__ == "__main__":
#     from dotenv import load_dotenv
#     import os
#     load_dotenv(override=True)
#     BASE_URL = os.getenv("POLOTRIAL_API_URL")
#     USERNAME = os.getenv("POLOTRIAL_API_USERNAME")
#     PASSWORD = os.getenv("POLOTRIAL_API_PASSWORD")
    
#     # Exemplo de uso
#     client = PoloTrialClient(base_url=BASE_URL, username=USERNAME, password=PASSWORD)
#     protocolos = ["protocolo1", "protocolo2"]
#     df = carregar_dados_protocolo(client, protocolos)
#     print(df.head())