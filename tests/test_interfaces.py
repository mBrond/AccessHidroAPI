import sys 
import os
import pytest

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from interfaces import _confereEstacaoValida, _confereDataValida


@pytest.mark.parametrize("codigoEstacao,esperado", [('asads',False), (11111, False), (23123920, True),
                                             (2200.3, False), (False, False), (True, False)])
def test_confereEstacaoValida(codigoEstacao, esperado):
    resultado = _confereEstacaoValida(codigoEstacao)
    assert resultado == esperado

@pytest.mark.parametrize("data,resultadoData", [('2024-01-01', True), (222, False), ('çcc', False),
                                           (True, False), (False, False), ('01-01-2024', False),
                                           ('2024-31-12', False), ('2024-02-31', False), ('1850-10-03', True)])
def test_confereDataValida(data, resultadoData):
    resultado = _confereDataValida(data)
    assert resultado == resultadoData
