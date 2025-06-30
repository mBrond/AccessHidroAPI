from hidroaccess.access import Access
from manipulacaoArquivos import *

def _listaEstacoes(pathEstacoes) -> list:
    f = open(pathEstacoes, 'r')
    estacoes = f.read().split('\n')
    try:
        estacoes.remove('')
    except:
        pass
    f.close()
    return estacoes

def solicitar_estacoes(stringComeco: str, stringFinal: str, pathEstacoes: str, pathConfigs:str, tipo: str, qtdDownloadAsync: int):
    credenciais = le_credenciais_ana(pathConfigs)
    sessao = Access(credenciais[0], credenciais[1])
    estacoes = _listaEstacoes(pathEstacoes)

    for estacao in estacoes:
        novoArquivo = 'resultados\\{}-{}-{}-{}.txt'.format(estacao, tipo, stringComeco, stringFinal)
        cria_arquivo_resultado(novoArquivo, tipo)

        token = sessao.safe_request_token()
        
        if tipo == 'Adotada' or tipo == 'Detalhada':
            listaDicionario = sessao.request_telemetrica(int(estacao), stringComeco, stringFinal, token, tipo, qtdDownloadAsync)    
        elif tipo == 'Cota':
            listaDicionario = sessao.request_cota(int(estacao), stringComeco, stringFinal, token, qtdDownloadAsync)
        elif tipo == 'Sedimentos':
            listaDicionario = sessao.request_sedimentos(int(estacao), stringComeco, stringFinal, token, qtdDownloadAsync)
        elif tipo == 'Chuva':
            listaDicionario = sessao.request_chuva(int(estacao), stringComeco, stringFinal, token, qtdDownloadAsync)

        atualizar_arquivo_resultado(novoArquivo, listaDicionario, tipo)