import json
import requests
import aiohttp
import asyncio
from datetime import datetime, timedelta

class Acess:
    def __init__(self) -> None:
        self.id = str()
        self.senha = str()
        self.urlApi = 'https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas'
        self.pathResultados = '\\medicoes'
        self.pathConfigs = 'configs.json'

    def lerCredenciais(self) -> None:
        try:
            f = open(self.pathConfigs, "r")
            credenciais = json.loads(f.read())['Credenciais']['Ana']
            self.id = credenciais['Identificador']
            self.senha = credenciais['Senha']
        except Exception as e:
            print(e)
            print('Falha na leitura das credenciais da ANA.')

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
        qtdMaxParams = kwargs.get('qtdMaxParams')
        if not qtdMaxParams:
            qtdMaxParams = 2 #0 - 2


        paramsL = list()

        while diaComeco < diaFinal and len(paramsL) <= qtdMaxParams:
            params = {
                'Código da Estação': codEstacao,
                'Tipo Filtro Data': filtroData,
                'Data de Busca (yyyy-MM-dd)': datetime.strftime(diaComeco, "%Y-%m-%d"),
                'Range Intervalo de busca': intervaloBusca
            }
            paramsL.append(params)
            diaComeco = diaComeco + timedelta(days=1)

        return paramsL

    def requestTelemetricaDetalhada(self, estacaoCodigo: int, data: str, token: str, intervaloBusca="HORA_24", filtroData = "DATA_LEITURA"):
        """
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
        Realiza o login com o ID e senha cadastrados pela Agência Nacional de Águas.
        :param id: Identificador cadastrado.
        :param password: Senha cadastrada.
        :return: Objeto 'response'.
        """
        url = self.urlApi + '/OAUth/v1'
        headers = {'Identificador': self.id, 'Senha': self.senha}
        return requests.get(url=url, headers=headers)

    def forceRequestToken(self):

        token = self.requestToken()
        print(token)
        tentativas = 1  #melhorar lógica com TRY-EXCEPT (?)
        while(token.status_code!=200 and tentativas <5):
            token = self.requestToken()  
            tentativas = tentativas+1
            print(token)

        if(token.status_code==200):
            token = json.loads(token.content)
            itens = token['items']
            return itens['tokenautenticacao']
        else:
            print("Não foi possível requisitar o token. Finalizando aplicação")
            exit()

    async def requestTelemetricaAdotadaAsync(self, estacaoCodigo: int, stringComeco: str, stringFinal: str, headers: dict, qtdDias=2):

        diaFinal = datetime.strptime(stringFinal, "%Y-%m-%d")
        diaComeco = datetime.strptime(stringComeco, "%Y-%m-%d")

        #Total de dias que terão os dados baixados (se não exceder data atual. Ex: hoje ser dia 12/09 e tentar baixar até 31/12 pode dar erro)
        diasDownload = (diaFinal - diaComeco).days

        url = self.urlApi + "/HidroinfoanaSerieTelemetricaAdotada/v1"

        iteracao = 1
        respostaLista = list()
        while(iteracao * qtdDias <= diasDownload):
            params = self._criaParams(estacaoCodigo, diaComeco, diaFinal=diaFinal)

            async with aiohttp.ClientSession(headers=headers) as session:
                tasks = []
                for param in params:
                    tasks.append(_download_url(session, url, headers, param))
                respostaLista.append(await asyncio.gather(*tasks))

            diaComeco = diaComeco + timedelta(days=1)
            iteracao = iteracao + 1 
        return respostaLista

async def _download_url(session, url, headers, params):
    async with session.get(url, headers=headers, params=params) as response:
        return await response.content.read()

def decodeRequestDetalhada(request):
    content = json.loads(request)
    itens = content['items']
    listaOrdenada = list()
    for item in itens:
        dicionarioDiario = dict()
        dicionarioDiario["Hora_medicao"] = item['Data_Hora_Medicao']
        dicionarioDiario["Chuva_Acumulada"] = item["Chuva_Acumulada"]
        dicionarioDiario["Chuva_Adotada"] = item["Chuva_Adotada"]
        dicionarioDiario["Cota_Adotada"] = item["Cota_Adotada"]
        dicionarioDiario["Cota_Sensor"] = item["Cota_Sensor"]
        dicionarioDiario["Vazao_Adotada"] = item["Vazao_Adotada"]
        listaOrdenada.append(dicionarioDiario)
    return listaOrdenada

def decodeRequestAdotada(request):
    content = json.loads(request)
    itens = content['items']
    listaOrdenada = list()
    if itens != None:
        for item in itens:
            dicionarioDiario = dict()
            dicionarioDiario["Hora_Medicao"] = item["Data_Hora_Medicao"]
            dicionarioDiario["Chuva_Adotada"] = item["Chuva_Adotada"]
            dicionarioDiario["Cota_Adotada"] = item["Cota_Adotada"]
            dicionarioDiario["Vazao_Adotada"] = item["Vazao_Adotada"]
            listaOrdenada.append(dicionarioDiario)
    else:
        print(content)
        print('\n')
        print(request)
    return listaOrdenada

if __name__ =='__main__':
    acess = Acess()

    x = datetime(2024, 1, 1)
    print(x)
    p = acess.criaParams(2, x, diaFinal=datetime(2024, 1, 10))

    acess.lerCredenciais()


    print(p)
    print(len(p))