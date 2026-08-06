"""
Camada de Integração de Dados: Responsável exclusivamente por conversar com sistemas externos (HTTP, Autenticação, APIs, etc). Não deve conter regras de negócio, apenas integração com sistemas externos.
"""

from __future__ import annotations
import logging
from typing import Any, Dict, Optional
from urllib.parse import urljoin
import requests
import os
logger = logging.getLogger(__name__)

class PoloTrialClient:
    
    
    def __init__(self, base_url: str, username: str, password: str, timeout: int = 30):
        """
        Initializes the PoloTrialClient with the provided base URL, username, password, and timeout.
        """
        self.base_url = base_url.rstrip("/") + "/"
        self.username = username
        self.password = password
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json"
        })
        self._authed = False
    
    def _login(self) -> None:
        """ Logs in to the PoloTrial service using the provided username and password.
        
        Args:
            None
        Raises:
            RuntimeError: If the login fails or the 'userId' cookie is not found in the response.
        Returns:
            None
        """
        session_url = urljoin(self.base_url, "sessions")
        payload = {
            "nome" : self.username,
            "password" : self.password
        }
        
        login_headers = {
            "Content-Type": "application/json"
        }
        
        polotrial_requests = self.session.post(session_url, json=payload, headers=login_headers, timeout=self.timeout)
        if polotrial_requests.status_code not in (200, 201):
            raise RuntimeError(f"Failed to login to PoloTrial. Status code: {polotrial_requests.status_code}, Response: {polotrial_requests.text}")
        
        if not self.session.cookies.get("userId"):
            raise RuntimeError("Login failed: 'userId' cookie not found in the response.")
        
        self._authed = True
        logger.info("Successfully logged in to PoloTrial.")
        
        #Extraindo o userid e armazenando em uma variável de ambiente
        user_id = self.session.cookies.get("userId")
        endpoint_header = user_id
        
        logger.info("User ID extracted and stored in environment variable 'POLOTRIAL_USER_ID' = %s.", endpoint_header)

    def _requests(self, method: str, path:str, *, params=None, json=None) -> requests.Response:
        """Sends an HTTP request to the PoloTrial service.

        Args:
            method (str): _description_
            path (str): _description_
            params (_type_, optional): _description_. Defaults to None.
            json (_type_, optional): _description_. Defaults to None.

        Returns:
            requests.Response: _description_
        """
        if not self._authed:
            self._login()
        
        url = urljoin(self.base_url, path.lstrip("/"))
        polotrial_response = self.session.request(
            method,
            url,
            params = params,
            json = json,
            timeout = self.timeout
        )
        
        # If sessions expired, re-authenticate and retry once
        if polotrial_response.status_code in (401, 403):
            logger.warning("Polotrial: auth failed(%s). Retrying login once...", polotrial_response.status_code)
            self._authed = False
            self._login()
            polotrial_response = self.session.request(
                method,
                url,
                params = params, 
                json = json,
                timeout = self.timeout
            )
        return polotrial_response
    
    def get_protocolos(self, protocolos: list[str]) -> list[Dict[str, Any]]:
        
        protocolos_data = []
        
        
        
        for protocolo in protocolos:
            try:
                response = self._requests(
                    method="GET",
                    path="/protocolo",
                    params={
                        "nested": "true"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        protocolos_data.extend(data)
                        logger.info(f"Successfully fetched data for protocolo {protocolo}.")
                else:
                    logger.warning(f"Unexpected response format for protocolo {protocolo}: {response.text}")
                        
            except Exception as e:
                logger.error(f"Error fetching protocolo {protocolo}: {e}")
        return protocolos_data
    
    def get_participantes(self, participantes: list[str]) -> list[Dict[str, Any]]:
        
        participantes_data = []
        
        
        
        for participante in participantes:
            try:
                response = self._requests(
                    method="GET",
                    path="/participantes",
                    params={
                        "nested": "true"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        participantes_data.extend(data)
                        logger.info(f"Successfully fetched data for participante {participante}.")
                else:
                    logger.warning(f"Unexpected response format for participante {participante}: {response.text}")
                        
            except Exception as e:
                logger.error(f"Error fetching participante {participante}: {e}")
        return participantes_data
    
    def get_participante_visita(self, participante_visita: list[str]) -> list[Dict[str, Any]]:
        
        participante_visita_data = []
        
        
        
        for visita in participante_visita:
            try:
                response = self._requests(
                    method="GET",
                    path='/participante_visita',
                    params={
                        "nested": "true"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        participante_visita_data.extend(data)
                        logger.info(f"Successfully fetched data for participante visita {visita}.")
                else:
                    logger.warning(f"Unexpected response format for participante visita {visita}: {response.text}")
            except Exception as e:
                logger.error(f"Error fetching participante visita {visita}: {e}")
        return participante_visita_data
    
    def get_participante_visita_procedimento_executor(self, participante_visita_procedimento_executor: list[str]) -> list[Dict[str, Any]]:
        
        participante_visita_procedimento_executor_data = []
        try:
            response = self._requests(
                method = "GET",
                path = "/participante_visita_procedimento_executor",
                params = {
                    "nested": "true"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    participante_visita_procedimento_executor_data.extend(data)
                    logger.info(f"Successfully fetched data for participante visita procedimento executor.")
            else:
                logger.warning(f"Unexpected response format for participante visita procedimento executor: {response.text}")
        except Exception as e:
            logger.error(f"Error fetching participante visita procedimento executor: {e}")
        return participante_visita_procedimento_executor_data
#--------------------------------------------------------------------------------------------------------
#TESTING
#--------------------------------------------------------------------------------------------------------
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
#     from dotenv import load_dotenv
#     load_dotenv(override=True)
#     BASE_URL = os.getenv("POLOTRIAL_API_URL")
#     USERNAME = os.getenv("POLOTRIAL_API_USERNAME")
#     PASSWORD = os.getenv("POLOTRIAL_API_PASSWORD")
    
#     print("---Iniciando Teste do Client---")
    
#     try:
#         client = PoloTrialClient(
#             base_url=BASE_URL,
#             username=USERNAME,
#             password=PASSWORD
#         )
        
#         client._login()
        
        
#         # 3. Testar o disparador de requisições
#         # Substitua 'endpoint_de_teste' por um caminho válido que requeira autenticação
#         # resposta = client._requests("GET", "/protocolo", params={"nested": "true"})
#         # print(f"Status da Requisição: {resposta.status_code}")
#         # print(f"Corpo da Resposta: {resposta.text}")
        
#     except Exception as e:
#         logger.error("Erro ao testar o PoloTrialClient: %s", e)
    