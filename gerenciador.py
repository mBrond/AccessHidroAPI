from hidroaccess.access import Access
from manipulacaoArquivos import *
from error_handler import error_handler
from typing import Callable, Optional

def _lista_estacoes(pathEstacoes) -> list:
    def ler_estacoes():
        arquivo = open(pathEstacoes, 'r')
        listaEstacoes = arquivo.read().split('\n')
        try:
            listaEstacoes.remove('')
        except:
            pass
        arquivo.close()
        return listaEstacoes
    
    return error_handler.safe_execute(
        ler_estacoes,
        context="leitura de lista de estações",
        show_message=False
    )

def solicitar_estacoes(stringComeco: str, stringFinal: str, pathEstacoes: str, pathConfigs: 
    str, tipo: str, qtdDownloadAsync: int, pathDownload: str, on_progress: Optional[Callable[[int, int, str], None]] = None):
    def processar_estacoes():
        credenciais = le_credenciais_ana(pathConfigs)
        if credenciais is None:
            raise ValueError("Não foi possível ler as credenciais")
        
        sessao = Access(credenciais[0], credenciais[1])
        estacoes = _lista_estacoes(pathEstacoes)
        
        if estacoes is None:
            raise ValueError("Não foi possível ler a lista de estações")

        total_estacoes = len(estacoes)
        if on_progress is not None:
            try:
                on_progress(0, total_estacoes, "")
            except Exception:
                pass

        for indice, estacao in enumerate(estacoes, start=1):
            caminhoArquivo = f'{pathDownload}\\{estacao}-{tipo}-{stringComeco}-{stringFinal}.txt'
            cria_arquivo_resultado(caminhoArquivo, tipo)

            token = sessao.safe_request_token()
            if token == '-1':
                raise PermissionError("Token de autenticação inválido. Confira credenciais") 

            if tipo == 'Adotada' or tipo == 'Detalhada':
                listaDicionario = sessao.request_telemetrica(int(estacao), stringComeco, stringFinal, token, tipo, qtdDownloadAsync)    
            elif tipo == 'Cota':
                listaDicionario = sessao.request_cota(int(estacao), stringComeco, stringFinal, token, qtdDownloadAsync)
            elif tipo == 'Sedimentos':
                listaDicionario = sessao.request_sedimentos(int(estacao), stringComeco, stringFinal, token, qtdDownloadAsync)
            elif tipo == 'Chuva':
                listaDicionario = sessao.request_chuva(int(estacao), stringComeco, stringFinal, token, qtdDownloadAsync)

            atualizar_arquivo_resultado(caminhoArquivo, listaDicionario, tipo)
            if on_progress is not None:
                try:
                    on_progress(indice, total_estacoes, estacao)
                except Exception:
                    pass
    
    error_handler.safe_execute(
        processar_estacoes,
        context="download de estações",
        show_message=True
    )