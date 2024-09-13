import asyncio
import aiohttp
from manipulacaoArquivos import *
from main import decodeRequestAdotada

from acess import Acess

url = 'https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/HidroinfoanaSerieTelemetricaAdotada/v1'  # list of URLs to download

async def download_url(session, url, headers, params, pathArquivo):
    async with session.get(url, headers=headers, params=params) as response:
        # print(await response.content.read())
        dados = decodeRequestAdotada( await response.content.read())
        atualiza_adotada(pathArquivo, dados)

async def main():
    
    acess = Acess()
    acess.lerCredenciais()
    token = acess.forceRequestToken()

    headers = {'Authorization': 'Bearer '+token}

    params1 = {
            'Código da Estação': 76310000,
            'Tipo Filtro Data': "DATA_LEITURA",
            'Data de Busca (yyyy-MM-dd)': '2024-01-01',
            'Range Intervalo de busca': 'HORA_24'
        }
    
    params2 = {
            'Código da Estação': 76310000,
            'Tipo Filtro Data': "DATA_LEITURA",
            'Data de Busca (yyyy-MM-dd)': '2024-01-02',
            'Range Intervalo de busca': 'HORA_24'
        }
    
    novoArquivo = 'teste{}.txt'.format(params2['Código da Estação'])
    cria_adotada(novoArquivo)


    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [
            download_url(session, url, headers, params1, novoArquivo),
            download_url(session, url, headers, params2, novoArquivo),]
        await asyncio.gather(*tasks)




asyncio.run(main())