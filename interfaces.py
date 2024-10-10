import datetime

def _confereEstacaoValida(estacao: str)->bool:
    """Confere se o código de 'estacao' é válido: número com oito dígitos.

    Args:
        estacao (str): Código de estação telemétrica

    Returns:
        bool: Verdadeiro se 'estacao' é um código válido.
    """
    if(len(estacao)!=8):
        return False
    try:
        val = int(estacao)
    except:
        return False
    else:
        return True
    
def _confereDataValida(data: str)->bool:
    """Confere se 'data' é uma data existente. 

    Args:
        data (str): String referente a uma data no formato yyyy-mm-dd

    Returns:
        bool: Verdadeiro se a data existe
    """
    try:
        data = datetime.strptime(data, "%Y-%m-%d")
    except:
        return False
    return True

def _confereComparaDatas(data1, data2):
    return data1<=data2

def interfaceDataInvalida():
    print('\nInsira uma data válida.')

def interfaceCredenciais():
    id = input("ID: ")
    senha = input("Senha: ")
    return {"id": id, "senha": senha}

def unicaData():
    strData = input("Qual a data?")
    if _confereDataValida(strData):
        return strData
    else:
        print('\nData inválida. ')
        return False

def datasComecoFinal(): #FAZER CHECAGEM DE DATAS CORRETAS
    strComeco = input("Data de comeco (yyyy-mm-dd)")
    
    strFinal = input("Data final (yyyy-mm-dd, dia nao incluido)")

    return [strComeco, strFinal]

def interfaceMenu():
    texto = "\n0. Sair\n1. Atualizar credenciais\n2. Atualizar estacoes\n3. Data única (Detalhada)\n"
    texto = texto+"4. Data única (Adotada)\n5. Período (Detalhada)\n6. Período (Adotada)\n7. Mostrar credenciais salvas."
    print(texto)

def interfaceSolicitarEstacoes():
    estacoes = list()
    print('\nDigite a estacao e aperte enter para confirmar. Digite 0 para voltar.')
    entrada = input()
    while(entrada != '0'):
        if _confereEstacaoValida(estacao=entrada):
            estacoes.append(entrada)
        else:
            print('\nCodigo de estação inválido. Apenas são aceitos números de oito dígitos.')
        entrada = input()

    return estacoes

def interfaceOperacaoEstacao():
    """
    Interface para definir qual o tipo de operação será realizada no arquivo estacoes.txt
    """
    texto = '\n1. Sobreescrever\n2. Adicionar\n'
    entrada = input(texto)
    while(entrada != '2' and entrada != '1'):
            entrada = input(texto)
            print(entrada)
    return int(entrada)

def interfaceVersao():
    print('-----\n Versão 1.0.1 - Miguel Brondani')