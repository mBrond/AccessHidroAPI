import datetime

def interfaceCredenciais():
    id = input("ID: ")
    senha = input("Senha: ")
    return {"id": id, "senha": senha}


def datasComecoFinal(): #FAZER CHECAGEM DE DATAS CORRETAS
    dataComeco = input("Data de comeco (yyyy-mm-dd)")
    dataFinal = input("Data final (yyyy-mm-dd, dia nao incluido)")
    return [dataComeco, dataFinal]

def interfaceMenu():
    texto = "\n0. Sair\n1. Atualizar credenciais\n2. Atualizar estacoes\n3. Data única\n"
    print(texto)

def interfaceSolicitarEstacoes():
    estacoes = list()
    print('\nDigite a estacao e aperte enter para confirmar. Digite 0 para voltar.\n')
    entrada = input()
    while(entrada != '0'):
        estacoes.append(entrada)
        entrada = input()

    return estacoes

def interfaceOperacaoEstacao():
    """
    Interface para definir qual o tipo de operação será realizada no arquivo estacoes.txt
    """
    texto = '\n1. Sobreescrever\n2. Adicionar'
    return int(input(texto))