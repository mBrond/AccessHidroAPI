import inicializacao
import traceback
from hidroaccess.access import Access
from interfaces import *
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

def solicitar_atualizacao_credenciais_ana(pathConfigs):
    novosDadosDict = interfaceCredenciais() #dados na memória    
    atualiza_credenciais_ana(pathConfigs, novosDadosDict)


def solicitar_estacoes(stringComeco: str, stringFinal: str, pathEstacoes: str, pathConfigs:str, tipo):
    credenciais = le_credenciais_ana(pathConfigs)
    sessao = Access(credenciais[0], credenciais[1])
    estacoes = _listaEstacoes(pathEstacoes)

    for estacao in estacoes:
        novoArquivo = 'resultados\\{}-Adotada={}-{}.txt'.format(estacao, stringComeco, stringFinal)
        cria_adotada(novoArquivo)

        token = sessao.safe_request_token()
        
        if tipo == 'Adotada' or tipo == 'Detalhada':
            listaDicionario = sessao.request_telemetrica(int(estacao), stringComeco, stringFinal, token, tipo)
        else:
            listaDicionario = sessao._main_request_convencionais(int(estacao), stringComeco, stringFinal, token, tipo)

        for dadosDiarios in listaDicionario:
            atualiza_adotada(novoArquivo, dadosDiarios)

def solicitar_leitura_credenciais_ana(pathConfigs):
    credenciaisAna = le_credenciais_ana(pathConfigs)
    print(f'\nId: {credenciaisAna[0]}\nSenha: {credenciaisAna[1]}')

def main():
    pathConfigs = 'configs.json'
    pathResultados = 'resultados'
    qtdDowloadAsync = 20
    inicializacao.inicializacao_basico(pathConfigs, pathResultados)

    interfaceVersao()

    pathEstacoes = 'estacoes.txt'
    
    entradaUser = 9
    while(entradaUser!=0):
        interfaceMenu()
        entradaUser = int(input())
        if(entradaUser==1):
            solicitar_atualizacao_credenciais_ana(pathConfigs)

        elif(entradaUser==2):
            operacao = interfaceOperacaoEstacao()
            escreverEstacoes(pathEstacoes, operacao, estacoes=interfaceSolicitarEstacoes())

        elif(entradaUser==3):
            stringComeco, stringFinal = datasComecoFinal()
            solicitar_estacoes(stringComeco, stringFinal, pathEstacoes, pathConfigs, 'Detalhada')

        elif(entradaUser==4):
            stringComeco, stringFinal = datasComecoFinal()
            solicitar_estacoes(stringComeco, stringFinal, pathEstacoes, pathConfigs, 'Adotada')

        elif(entradaUser==5):
            stringComeco, stringFinal = datasComecoFinal()
            solicitar_estacoes(stringComeco, stringFinal, pathEstacoes, pathConfigs, 'Sedimento')
        
        elif(entradaUser==6):
            stringComeco, stringFinal = datasComecoFinal()
            solicitar_estacoes(stringComeco, stringFinal, pathEstacoes, pathConfigs, 'Cota')

        elif(entradaUser==7):
            stringComeco, stringFinal = datasComecoFinal()
            solicitar_estacoes(stringComeco, stringFinal, pathEstacoes, pathConfigs, 'Chuva')

        elif(entradaUser==8):
            solicitar_leitura_credenciais_ana(pathConfigs)

        elif(entradaUser==9):
            qtdDowloadAsync = interfaceqtdDowloadAsync(qtdDowloadAsync)

        else:
            pass

if __name__ == "__main__":
    try:
        main()
    
    except Exception as e:
        print("Houve um erro na execução do programa. Verifique o log de atividades para melhores informações")
        cria_log(e, traceback.format_exc())
        input()