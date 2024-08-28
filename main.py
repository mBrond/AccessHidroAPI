
def criaConfigs():
    path = 'configs.json'
    existeArq =os.path.isfile(path)
    if(not existeArq):
        conteudoJson = '{"Credenciais":{"Ana":""}}'

        arq = open(path, 'w')
        arq.write(conteudoJson)

        arq.close()

def main():
    criaConfigs()
    entradaUser = 9
    if(entradaUser==1):
        pass #criaCredenciais
    elif():
        pass
if __name__ == "__main__":
    main()