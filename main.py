import inicializacao
import traceback
from manipulacaoArquivos import cria_log
from interfaceGrafica import Application
from tkinter import Tk
from error_handler import error_handler

def gerenciador(pathConfigs, pathResultados, pathEstacoes, tituloJanela, qtdDownloadAsync, versao, pathLogs):
    inicializacao.inicializacao_basico(pathConfigs, pathResultados, pathEstacoes)

    janelaRoot = Tk()
    janelaRoot.geometry("600x450")
    app = Application(janelaRoot, versao, pathConfigs, pathResultados, pathEstacoes,
    tituloJanela, qtdDownloadAsync, pathLogs)
    janelaRoot.mainloop()

if __name__ == "__main__":
    pathLogs = 'logs'
    pathConfigs = 'configs.json'
    pathResultados = 'resultados'
    pathEstacoes = 'estacoes.txt'
    tituloJanela = 'AHAPI'
    qtdDownloadAsync = 20
    versao = "1.1.0"
    
    error_handler.safe_execute(
        gerenciador,
        pathConfigs, pathResultados, pathEstacoes, tituloJanela, qtdDownloadAsync, versao, pathLogs,
        context="inicialização da aplicação",
        show_message=True
    )
