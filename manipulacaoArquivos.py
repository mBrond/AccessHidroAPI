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

