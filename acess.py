import json
import requests

class Acess:
    def __init__(self) -> None:
        self.id = str()
        self.senha = str()
        self.urlApi = 'https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas'
        self.pathResultados = '\\medicoes'
        self.pathConfigs = 'configs.json'

    def lerCredenciais(self):
        try:
            f = open(self.pathConfigs, "r")
            credenciais = json.loads(f.read())['Credenciais']['Ana']
            self.id = credenciais['Identificador']
            self.senha = credenciais['Senha']
        except Exception as e:
            print(e)
            print('Falha na leitura das credenciais da ANA.')

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

        params = {
            'Código da Estação': estacaoCodigo,
            'Tipo Filtro Data': filtroData,
            'Data de Busca (yyyy-MM-dd)': data,
            'Range Intervalo de busca': intervaloBusca
        }

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

        url = self.urlApi+ "/HidroinfoanaSerieTelemetricaAdotada/v1"

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
        params = {'Identificador': self.id, 'Senha': self.senha}
        return requests.get(url=url, headers=params)

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