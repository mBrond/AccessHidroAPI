import inicializacao
import traceback
from manipulacaoArquivos import cria_log
from interfaceGrafica import Application
from tkinter import Tk

def gerenciador(pathConfigs, pathResultados, pathEstacoes, tituloJanela, qtdDownloadAsync, versao):
    inicializacao.inicializacao_basico(pathConfigs, pathResultados)

    pathEstacoes = 'estacoes.txt'
    root = Tk()
    root.geometry("600x450")
    app = Application(root, versao, pathConfigs, pathResultados, pathEstacoes, tituloJanela, qtdDownloadAsync)
    root.mainloop()

if __name__ == "__main__":
    pathLogs = 'logs'
    pathConfigs = 'configs.json'
    pathResultados = 'resultados'
    pathEstacoes = 'estacoes.txt'
    tituloJanela = 'AHAPI'
    qtdDownloadAsync = 20
    
    versao = "1.1.0"
    try:
        gerenciador(pathConfigs, pathResultados, pathEstacoes, tituloJanela, qtdDownloadAsync, versao)
    
    except Exception as e:
        print("Houve um erro na execução do programa. Verifique o log de atividades para melhores informações")
        cria_log(e, traceback.format_exc(), pathLogs)
        input()