import sys 
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from inicializacao import *

def test_cria_configs_criacao(tmp_path):
    dir = tmp_path / "sub"
    dir.mkdir()
    pathConfigs = dir / 'configs.json'
    cria_configs(pathConfigs)
    assert os.path.isfile(pathConfigs)
    
    arq = open(pathConfigs)
    conteudoArq = arq.read()
    arq.close()
    
    conteudoEsperado = '{"Credenciais":{"Ana":{"Identificador":"", "Senha":""}}}'
    assert conteudoArq == conteudoEsperado 

def test_cria_arq_estacoes(tmp_path):
    dir = tmp_path / "sub2"
    dir.mkdir()
    pathEstacoes = dir / 'estacoes.txt'
    cria_arq_estacoes(pathEstacoes)
    assert os.path.isfile(pathEstacoes)
    
    arq = open(pathEstacoes, 'r')
    conteudoArq = arq.read()

    assert conteudoArq == ''

def test_cria_dir_resultados(tmp_path):
    dir = tmp_path / "sub"
    dir.mkdir()
    resultados = dir / 'resultados'
    cria_dir_resultados(resultados)
    assert os.path.isdir(resultados)
    assert len(list(dir.iterdir())) == 1