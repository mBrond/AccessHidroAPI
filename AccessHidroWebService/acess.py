import json
import requests
import aiohttp
import asyncio
from datetime import datetime, timedelta

import time

class Acess:
    def __init__(self, id=str(), senha=str()) -> None:
        self._id = id
        self._senha = senha
        self.urlApi = 'https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas'
        self.pathResultados = '\\medicoes'
        self.pathConfigs = 'configs.json'

    def atualizarCredenciais(self, id=str(), senha=str()) -> None:
        """Atualiza as credencias salvas no objeto

        Args:
            id (str, optional): _description_. Defaults to str().
            senha (str, optional): _description_. Defaults to str().
        """
        self._senha = senha
        self._id=id

    def _defineIntervaloBuscaLongo(self, qtdDiasDownload: int)->str:
        """Define o melhor parâmetro para o campo "Range Intervalo de Busca" para longos períodos

        Args:
            qtdDiasDownload (int): Quantidade total de dias desejados

        Returns:
            str: Parâmetro para requisição
        """

        if qtdDiasDownload >= 30:
            return "DIAS_30"
        elif qtdDiasDownload >= 21:
            return "DIAS_21"
        elif qtdDiasDownload >= 14:
            return "DIAS_14"
        elif qtdDiasDownload >= 7:
            return "DIAS_7"
        elif qtdDiasDownload >= 2:
            return "DIAS_2"
        else:
            return "HORA_24"

    def _criaParams(self, codEstacao: int, diaComeco: datetime, intervaloBusca="HORA_24", filtroData = "DATA_LEITURA", **kwargs) -> list:
        """
        :param codEstacao: Codigo da estacao
        :param diaComeco:
        :param intervaloBusca: [OPCIONAL] 
        :param filtroData: [OPCIONAL]
        :param diaFinal: [OPCIONAL] Utilizado apenas quando é necessário parâmetros para mais de um dia. Data final, posterior à diaComeco.
        :param qtdMaxParams: [OPCIONAL] Utilizado em conjunto com com diaFinal. Máximo de parametrôs para aquele período  
        """

        diaFinal= kwargs.get('diaFinal')
        if not diaFinal:
            diaFinal = diaComeco + timedelta(days=1)

        paramsL = list()

        while diaComeco < diaFinal:
            params = {
                'Código da Estação': codEstacao,
                'Tipo Filtro Data': filtroData,
                'Data de Busca (yyyy-MM-dd)': datetime.strftime(diaComeco, "%Y-%m-%d"),
                'Range Intervalo de busca': intervaloBusca
            }
            paramsL.append(params)
            diaComeco = diaComeco + timedelta(days=1)

        return paramsL

    def paramUnico(self, codEstacao, filtroData, qtdDiasParam, dia):

        intervaloBusca = self._defineIntervaloBuscaLongo(qtdDiasParam)
        param = {
            'Código da Estação': codEstacao,
            'Tipo Filtro Data': filtroData,
            'Data de Busca (yyyy-MM-dd)': datetime.strftime(dia, "%Y-%m-%d"),
            'Range Intervalo de busca': intervaloBusca
        }
        return param


    def _defineQtdDownloadsAsync(self, maxRequests, qtdDownloads)->int:
        if qtdDownloads < maxRequests:
            return qtdDownloads
        else:
            return maxRequests

    def _defQtdDiasParam(self, dataComeco: datetime, dataFinal: datetime)->int:
        diferenca = (dataFinal - dataComeco).days

        if diferenca >=30:
            return 30
        elif diferenca >= 21:
            return 21
        elif diferenca >= 14:
            return 14
        elif diferenca >= 7:
            return 7
        elif diferenca >=5:
            return 5
        elif diferenca >= 2:
            return 2
        else:
            return 1

    def requestTelemetricaDetalhada(self, estacaoCodigo: int, data: str, token: str, intervaloBusca="HORA_24", filtroData = "DATA_LEITURA"):
        """
        !!!Utilizar requestTelemetricaDetalhadaAsync!!!
        :param estacaoCodigo: Código de 8 dígitos
        :param data: Data dos dados requisitados. Formato yyyy-MM-dd.
        :param token: AcessToken adquirido
        :param filtroData:
        :param intervaloBusca: Intervalo das medições.
        :return: Objeto 'response'.
        """

        url = self.urlApi+ "/HidroinfoanaSerieTelemetricaDetalhada/v1"

        headers = {
            'Authorization': 'Bearer '+token
        }

        params = self._criaParams(estacaoCodigo)[0]

        return requests.get(url=url, headers = headers, params = params)

    def requestTelemetricaAdotada(self, estacaoCodigo: int, data: str, token: str, intervaloBusca="HORA_24", filtroData = "DATA_LEITURA"):
        """
        !!!Utilizar versão requestTelemetricaAdotadaAsync!!!
        :param estacaoCodigo: Código de 8 dígitos
        :param data: Data dos dados requisitados. Formato yyyy-MM-dd.
        :param token: AcessToken adquirido
        :param filtroData:
        :param intervaloBusca: Intervalo das medições.
        :return: Objeto 'response'.
        """ 

        url = self.urlApi + "/HidroinfoanaSerieTelemetricaAdotada/v1"

        headers = {
            'Authorization': 'Bearer '+token
        }

        params = {
            'Código da Estação': estacaoCodigo,
            'Tipo Filtro Data': filtroData,
            'Data de Busca (yyyy-MM-dd)': data,
            'Range Intervalo de busca': intervaloBusca
        }

        return requests.get(url=url, headers = headers, params = params)
    
    def requestToken(self):
        """
        Requisita o token de autenticação da API com o ID e Senha
        :param id: Identificador cadastrado.
        :param password: Senha cadastrada.
        :return: Objeto 'response'.
        """
        url = self.urlApi + '/OAUth/v1'
        headers = {'Identificador': self._id, 'Senha': self._senha}
        return requests.get(url=url, headers=headers)

    def forceRequestToken(self)->str:
        """Realiza requisições até conseguir um token válido. Credenciais utilizadas 

        Returns:
            str: '-1' caso as credenciais não sejam válidas, se não str de token válido.
        """
        tokenRequest = self.requestToken()
        tentativas = 1  #melhorar lógica com TRY-EXCEPT (?)
        if (tokenRequest.status_code == 401): #Não autorizado, sem motivos tentar novamente.
            return '-1'

        while(tokenRequest.status_code!=200 and tentativas <5):
            tokenRequest = self.requestToken()  
            tentativas = tentativas+1

        if(tokenRequest.status_code==200):
            token = json.loads(tokenRequest.content)
            itens = token['items']
            return itens['tokenautenticacao']

    async def requestTelemetricaAdotadaAsync(self, estacaoCodigo: int, stringComeco: str, stringFinal: str, headers: dict, qtdDownloadsAsync=20):

        diaFinal = datetime.strptime(stringFinal, "%Y-%m-%d")
        diaComeco = datetime.strptime(stringComeco, "%Y-%m-%d")

        diasRestantesParaDownload = (diaFinal - diaComeco).days

        url = self.urlApi + "/HidroinfoanaSerieTelemetricaAdotada/v1"

        respostaLista = list()
        qtdDiasParam = qtdDownloadsAsync+1 #garante que é maior

        while diasRestantesParaDownload != 0 :
            blocoAsync = list()

            while (len(blocoAsync) <= qtdDownloadsAsync) and (diaComeco!=diaFinal):
                qtdDiasParam = self._defQtdDiasParam(diaComeco, diaFinal)
                diaComeco += timedelta(days=qtdDiasParam)
                blocoAsync.append(self.paramUnico(estacaoCodigo, "DATA_LEITURA", qtdDiasParam, diaComeco - timedelta(days=1)))

            async with aiohttp.ClientSession(headers=headers) as session:
                tasks = list()
                for param in blocoAsync:
                    tasks.append(_download_url(session, url, param))
                resposta = await asyncio.gather(*tasks)
                respostaLista.append(resposta)

            diasRestantesParaDownload = (diaFinal - diaComeco).days
            
        return respostaLista
    
    async def requestTelemetricaDetalhadaAsync(self, estacaoCodigo: int, stringComeco: str, stringFinal: str, headers: dict, qtdDownloadsAsync=20) -> list:

        diaFinal = datetime.strptime(stringFinal, "%Y-%m-%d")
        diaComeco = datetime.strptime(stringComeco, "%Y-%m-%d")

        diasRestantesParaDownload = (diaFinal - diaComeco).days

        url = self.urlApi + "/HidroinfoanaSerieTelemetricaDetalhada/v1"

        respostaLista = list()
        qtdDiasParam = qtdDownloadsAsync+1 #garante que é maior

        while diasRestantesParaDownload != 0 :
            blocoAsync = list()

            while (len(blocoAsync) <= qtdDownloadsAsync) and (diaComeco!=diaFinal):
                qtdDiasParam = self._defQtdDiasParam(diaComeco, diaFinal)
                diaComeco += timedelta(days=qtdDiasParam)
                blocoAsync.append(self.paramUnico(estacaoCodigo, "DATA_LEITURA", qtdDiasParam, diaComeco - timedelta(days=1)))

            async with aiohttp.ClientSession(headers=headers) as session:
                tasks = list()
                for param in blocoAsync:
                    tasks.append(_download_url(session, url, param))
                resposta = await asyncio.gather(*tasks)
                respostaLista.append(resposta)

            diasRestantesParaDownload = (diaFinal - diaComeco).days
            
        return respostaLista

async def _download_url(session, url, params): 
    async with session.get(url, params=params) as response:
        return await response.content.read()

if __name__ =='__main__':
    pass