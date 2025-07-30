import inicializacao
import traceback
from manipulacaoArquivos import cria_log
from interfaceGrafica import Application
from tkinter import Tk

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
    
    try:
        gerenciador(pathConfigs, pathResultados, pathEstacoes, tituloJanela, qtdDownloadAsync, versao, pathLogs)
    except Exception as erro:
        print("Houve um erro na execução do programa. Verifique o log de atividades para melhores informações")
        cria_log(erro, traceback.format_exc(), pathLogs)
        input()
