import json

def cria_detalhada(pathArquivo):
    f = open(pathArquivo, 'w')
    f.write('Data_Hora;Chuva_Acumulada;Chuva_Adotada;Cota_Adotada;Cota_Sensor;Vazao_Adotada;\n')
    f.close()

def cria_adotada(pathArquivo): ##Testar
    f = open(pathArquivo, 'w')
    f.write('Data_Hora;Chuva_Adotada;Cota_Adotada;Vazao_Adotada;\n')
    f.close()

def atualiza_adotada(pathArquivo, listaDados):
    f = open(pathArquivo, 'a')
    for item in listaDados:
        linha = '{};{};{};{};\n'.format(item['Hora_Medicao'], item['Chuva_Adotada'], item['Cota_Adotada'], item['Vazao_Adotada'])
        f.write(linha)

    f.close()

def atualiza_detalhada(pathArquivo, listaDados):
    f = open(pathArquivo, 'a')
    for item in listaDados:
        linha = '{};{};{};{};{};{};\n'.format(item['Hora_medicao'], item["Chuva_Acumulada"], item["Chuva_Adotada"], item["Cota_Adotada"], item["Cota_Sensor"], item["Vazao_Adotada"])
        f.write(linha)
    f.close()


def escreverEstacoes(pathEstacoes: str, operacao: int, estacoes:list)->None:
    """Escreve o código das estações no arquivo estacoes.txt

    Args:
        pathEstacoes (str): Path para o arquivo estacoes.txt
        operacao (int): 1-> Sobreescreve arquivo. 0-> Adiciona ao final do arquivo. 
        estacoes (list): Lista com os códigos de estações
    """
    if(operacao == 1):
        f = open(pathEstacoes, 'w')
    else:
        f = open(pathEstacoes, 'a')

    for estacao in estacoes:
        f.write(f'{estacao}\n')

    f.close()

def atualiza_credenciais_ana(pathConfigs: str, dados: dict)->None:
    """Atualiza o arquivo de configuração com as credenciais em 'dados'

    Args:
        pathConfigs (str): Path para o arquivo de configurações
        dados (dict): Dicionário com as chaves 'id' e 'senha'
    """
    
    arq = open(pathConfigs, 'r+')
     
    dataArqStr = arq.read()
    dataJson = json.loads(dataArqStr)
    
    dataJson.update({"Credenciais":{"Ana":{"Identificador":dados['id'], "Senha":dados['senha']}}})

    #arq.read() faz o ponteiro ir para o final do arquivo, e sendo necessário voltar pro começo para sobre-escrever as modificações
    arq.seek(0)

    arq.write(json.dumps(dataJson))

    arq.close()

def le_credenciais_ana(pathConfigs)->list:
    """Lê o arquivo de configuração e retorna as credenciais da ANA salvas nele.

    Args:
        pathConfigs str: Path para o arquivo de configuracao

    Returns:
        list: Primeiro item -> identificador, Segundo item -> Senha
    """
    arq = open(pathConfigs, 'r')
    dataArqStr = arq.read()
    arq.close()

    dicionario =json.loads(dataArqStr)['Credenciais']['Ana']

    return [ dicionario["Identificador"], dicionario["Senha"]] 