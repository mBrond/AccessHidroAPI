import asyncio
import aiohttp
from manipulacaoArquivos import *
# from main import decodeRequestAdotada
from datetime import datetime, timedelta
from acess import *

url = 'https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/HidroinfoanaSerieTelemetricaAdotada/v1'  # list of URLs to download

async def download_url(session, url, headers, params, pathArquivo):
    async with session.get(url, headers=headers, params=params) as response:
        return await response.content.read()

async def mainAsync(codEstacao, diaComeco, diaFinal):
    
    diaFinal = datetime.strptime(diaFinal, "%Y-%m-%d")
    diaComeco = datetime.strptime(diaComeco, "%Y-%m-%d")

    acess = Acess()
    acess.lerCredenciais()
    token = acess.forceRequestToken()

    headers = {'Authorization': 'Bearer '+token}

    qtdDias = 366
    params = criaParams(codEstacao, diaComeco, diaFinal, qtdDias)
    
    novoArquivo = 'teste{}.txt'.format(codEstacao)
    cria_adotada(novoArquivo)

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for param in params:
            tasks.append(download_url(session, url, headers, param, novoArquivo))
        respostasLista = await asyncio.gather(*tasks)

    for resposta in respostasLista:
        dados = decodeRequestAdotada(resposta)     
        atualiza_adotada(novoArquivo, dados)       

def criaParams(codEstacao: int, diaComeco, diaFinal, qtdMax):
    paramsL = list()

    while diaComeco < diaFinal and len(paramsL) <= qtdMax:
        params = {
            'Código da Estação': codEstacao,
            'Tipo Filtro Data': "DATA_LEITURA",
            'Data de Busca (yyyy-MM-dd)': datetime.strftime(diaComeco, "%Y-%m-%d"),
            'Range Intervalo de busca': 'HORA_24'
        }
        paramsL.append(params)
        diaComeco = diaComeco + timedelta(days=1)

    return paramsL


if __name__ == "__main__":
    asyncio.run(mainAsync(76310000, '2024-06-01', '2024-07-01'))