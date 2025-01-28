from acess import Acess
from datetime import datetime
import pytest
import asyncio
import json

def login_valido():
    f = open('tests//credenciais.txt', 'r')
    login = f.read(11)
    f.seek(13)
    senha = f.read(8)
    f.close()
    return Acess(str(login), str(senha))

@pytest.fixture
def login_valido_fixture():
    return login_valido()

@pytest.fixture
def estacao_valida():
    return 76310000

def login_invalido():
    return Acess('1', '123')

@pytest.mark.parametrize("acesso, validade", [
    (login_valido(), True),
    (login_invalido(), False)
])

def test_forceRequestToken(acesso, validade):
    if validade:
        assert acesso.forceRequestToken() != '-1'#valor do token
    else:
        assert acesso.forceRequestToken() == '-1'#valor erro

def test_requestTelemetricaDetalhadaAsync_realiza_requisicao_valida(login_valido_fixture):
    acesso = login_valido_fixture

    headers = {'Authorization': 'Bearer {}'.format(acesso.forceRequestToken())}

    ListaListaRespostas = asyncio.run(acesso.requestTelemetricaDetalhadaAsync(76310000, '2024-01-01', '2024-01-03', headers))
    for resposta in ListaListaRespostas:
        for dia in resposta:
            contentDia = json.loads(dia) #dict
            print(contentDia)
            if contentDia['status'] != 'OK':
                assert contentDia['code'] == 200
    assert True

#ultimo dia nao incluso
@pytest.mark.parametrize('diaComeco, diaFinal, maxRequest, qtdDiasEsperado', [
    ('2024-01-01', '2024-01-03', 20, 2),
    ('2024-02-01', '2024-02-27', 20, 26)])

def test_QtdDownloads(diaComeco, diaFinal, maxRequest, qtdDiasEsperado):
    acesso = login_valido()
    headers = {'Authorization': 'Bearer {}'.format(acesso.forceRequestToken())}
    ListaListaRespostas = asyncio.run(acesso.requestTelemetricaDetalhadaAsync(76310000, diaComeco, diaFinal, headers, qtdDownloadsAsync=maxRequest))
    somaDiasBaixados = 0
    for lista in ListaListaRespostas:
        somaDiasBaixados = somaDiasBaixados + len(lista)
    assert qtdDiasEsperado == somaDiasBaixados

@pytest.mark.parametrize('diaInicio, diaFim, resultado', [
    ('2024-01-01', '2024-03-01', 30),
    ('2024-01-01', '2024-01-04', 2),
    ('2024-01-01', '2024-01-02', 1),
    ('2024-01-01', '2024-01-29', 21),
    ('2024-01-01', '2024-01-18', 14),
    ('2024-01-01', '2024-01-08', 7),
    ('2024-01-01', '2024-01-07', 5)
])
def test__defQtdDiasParam(diaInicio, diaFim, resultado):
    acesso = login_valido()

    resposta = acesso._defQtdDiasParam(datetime.strptime(diaInicio, "%Y-%m-%d"), datetime.strptime(diaFim, "%Y-%m-%d"))
    assert resultado == resposta