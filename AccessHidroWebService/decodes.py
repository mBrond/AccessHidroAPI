import json
def decodeRequestDetalhada(request):
    content = json.loads(request.decode('latin-1'))
    itens = content['items']
    listaOrdenada = list()
    if itens != None:
        for item in itens:
            dicionarioDiario = dict()
            dicionarioDiario["Hora_medicao"] = item['Data_Hora_Medicao']
            dicionarioDiario["Chuva_Acumulada"] = item["Chuva_Acumulada"]
            dicionarioDiario["Chuva_Adotada"] = item["Chuva_Adotada"]
            dicionarioDiario["Cota_Adotada"] = item["Cota_Adotada"]
            dicionarioDiario["Cota_Sensor"] = item["Cota_Sensor"]
            dicionarioDiario["Vazao_Adotada"] = item["Vazao_Adotada"]
            listaOrdenada.append(dicionarioDiario)
    else:
        dicionarioDiario = dict()
        dicionarioDiario["Hora_medicao"] = None
        dicionarioDiario["Chuva_Acumulada"] = None
        dicionarioDiario["Chuva_Adotada"] = None
        dicionarioDiario["Cota_Adotada"] = None
        dicionarioDiario["Cota_Sensor"] = None
        dicionarioDiario["Vazao_Adotada"] = None
        listaOrdenada.append(dicionarioDiario)
    return listaOrdenada

def decodeRequestAdotada(request: bytes) -> list:
    """_summary_

    Args:
        request (bytes): Resposta da requisição a API

    Returns:
        list: Lista de dicionarios com a data e medições correspondentes
    """
    content = json.loads(request.decode('latin-1'))
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
        dicionarioDiario = dict()
        dicionarioDiario["Hora_Medicao"] = None
        dicionarioDiario["Chuva_Adotada"] = None
        dicionarioDiario["Cota_Adotada"] = None
        dicionarioDiario["Vazao_Adotada"] = None
        listaOrdenada.append(dicionarioDiario)
    return listaOrdenada