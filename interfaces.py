import datetime

def interfaceCredenciais():
    id = input("ID: ")
    senha = input("Senha: ")
    return {"id": id, "senha": senha}


def datasComecoFinal():
    dataComeco = input("Data de comeco (yyyy-mm-dd)")
    dataFinal = input("Data final (yyyy-mm-dd, dia nao incluido)")
    return [dataComeco, dataFinal]

def interfaceMenu():
    texto = "\n0. Sair\n1. Atualizar credenciais\n2. "
    print(texto)