import json
from datetime import datetime
import os
from error_handler import error_handler

def get_chaves_dicts_str(tipo: str) -> str:
    """Retorna uma string com as chaves dos dicionários de cada tipo de estação separadas por ponto e vírgula"""
    chaves_por_tipo = {
        'Adotada': 'Hora_Medicao;Chuva_Adotada;Cota_Adotada;Vazao_Adotada;',
        'Detalhada': 'Hora_Medicao;Chuva_Acumulada;Chuva_Adotada;Cota_Adotada;Cota_Sensor;Vazao_Adotada;',
        'Sedimentos': (
            "Area_Molhada;Concentracao_PPM;Concentracao_da_Amostra_Extra;Condutividade_Eletrica;"
            "Cota_cm;Cota_de_Mediacao;Data_Hora_Dado;Data_Hora_Medicao_Liquida;Data_Ultima_Alteracao;Largura;"
            "Nivel_Consistencia;Numero_Medicao;Numero_Medicao_Liquida;Observacoes;Temperatura_da_Agua;Vazao_m3_s;"
            "Vel_Media;codigoestacao"
        ),
        'Cota': (
            "Cota_01;Cota_01_Status;Cota_02;Cota_02_Status;Cota_03;Cota_03_Status;Cota_04;Cota_04_Status;"
            "Cota_05;Cota_05_Status;Cota_06;Cota_06_Status;Cota_07;Cota_07_Status;Cota_08;Cota_08_Status;"
            "Cota_09;Cota_09_Status;Cota_10;Cota_10_Status;Cota_11;Cota_11_Status;Cota_12;Cota_12_Status;"
            "Cota_13;Cota_13_Status;Cota_14;Cota_14_Status;Cota_15;Cota_15_Status;Cota_16;Cota_16_Status;"
            "Cota_17;Cota_17_Status;Cota_18;Cota_18_Status;Cota_19;Cota_19_Status;Cota_20;Cota_20_Status;"
            "Cota_21;Cota_21_Status;Cota_22;Cota_22_Status;Cota_23;Cota_23_Status;Cota_24;Cota_24_Status;"
            "Cota_25;Cota_25_Status;Cota_26;Cota_26_Status;Cota_27;Cota_27_Status;Cota_28;Cota_28_Status;"
            "Cota_29;Cota_29_Status;Cota_30;Cota_30_Status;Cota_31;Cota_31_Status;Data_Hora_Dado;"
            "Data_Ultima_Alteracao;Dia_Maxima;Dia_Minima;Maxima;Maxima_Status;Media;Media_Anual;"
            "Media_Anual_Status;Media_Status;Mediadiaria;Minima;Minima_Status;Tipo_Medicao_Cotas;"
            "codigoestacao;nivelconsistencia"
        ),
        'Chuva': (
            "Chuva_01;Chuva_01_Status;Chuva_02;Chuva_02_Status;Chuva_03;Chuva_03_Status;Chuva_04;Chuva_04_Status;"
            "Chuva_05;Chuva_05_Status;Chuva_06;Chuva_06_Status;Chuva_07;Chuva_07_Status;Chuva_08;Chuva_08_Status;"
            "Chuva_09;Chuva_09_Status;Chuva_10;Chuva_10_Status;Chuva_11;Chuva_11_Status;Chuva_12;Chuva_12_Status;"
            "Chuva_13;Chuva_13_Status;Chuva_14;Chuva_14_Status;Chuva_15;Chuva_15_Status;Chuva_16;Chuva_16_Status;"
            "Chuva_17;Chuva_17_Status;Chuva_18;Chuva_18_Status;Chuva_19;Chuva_19_Status;Chuva_20;Chuva_20_Status;"
            "Chuva_21;Chuva_21_Status;Chuva_22;Chuva_22_Status;Chuva_23;Chuva_23_Status;Chuva_24;Chuva_24_Status;"
            "Chuva_25;Chuva_25_Status;Chuva_26;Chuva_26_Status;Chuva_27;Chuva_27_Status;Chuva_28;Chuva_28_Status;"
            "Chuva_29;Chuva_29_Status;Chuva_30;Chuva_30_Status;Chuva_31;Chuva_31_Status;Data_Hora_Dado;"
            "Data_Ultima_Alteracao;Dia_Maxima;Maxima;Maxima_Status;Nivel_Consistencia;Numero_Dias_de_Chuva;"
            "Numero_Dias_de_Chuva_Status;Tipo_Medicao_Chuvas;Total;Total_Anual;Total_Anual_Status;Total_Status;"
            "codigoestacao"
        )
    }
    return chaves_por_tipo.get(tipo, '')

def get_chaves_dicts(tipo: str) -> list:
    """Retorna uma lista das chaves dos dicionários de cada tipo de estação."""
    chaves = {
        'Adotada': ['Hora_Medicao', 'Chuva_Adotada', 'Cota_Adotada', 'Vazao_Adotada'],
        'Detalhada': ['Hora_Medicao', 'Chuva_Acumulada', 'Chuva_Adotada', 'Cota_Adotada', 'Cota_Sensor', 'Vazao_Adotada'],
        'Sedimentos': [
            "Area_Molhada", "Concentracao_PPM", "Concentracao_da_Amostra_Extra", "Condutividade_Eletrica",
            "Cota_cm", "Cota_de_Mediacao", "Data_Hora_Dado", "Data_Hora_Medicao_Liquida", "Data_Ultima_Alteracao",
            "Largura", "Nivel_Consistencia", "Numero_Medicao", "Numero_Medicao_Liquida", "Observacoes",
            "Temperatura_da_Agua", "Vazao_m3_s", "Vel_Media", "codigoestacao"
        ],
        'Cota': [
            "Cota_01", "Cota_01_Status", "Cota_02", "Cota_02_Status",
            "Cota_03", "Cota_03_Status", "Cota_04", "Cota_04_Status",
            "Cota_05", "Cota_05_Status", "Cota_06", "Cota_06_Status",
            "Cota_07", "Cota_07_Status", "Cota_08", "Cota_08_Status",
            "Cota_09", "Cota_09_Status", "Cota_10", "Cota_10_Status",
            "Cota_11", "Cota_11_Status", "Cota_12", "Cota_12_Status",
            "Cota_13", "Cota_13_Status", "Cota_14", "Cota_14_Status",
            "Cota_15", "Cota_15_Status", "Cota_16", "Cota_16_Status",
            "Cota_17", "Cota_17_Status", "Cota_18", "Cota_18_Status",
            "Cota_19", "Cota_19_Status", "Cota_20", "Cota_20_Status",
            "Cota_21", "Cota_21_Status", "Cota_22", "Cota_22_Status",
            "Cota_23", "Cota_23_Status", "Cota_24", "Cota_24_Status",
            "Cota_25", "Cota_25_Status", "Cota_26", "Cota_26_Status",
            "Cota_27", "Cota_27_Status", "Cota_28", "Cota_28_Status",
            "Cota_29", "Cota_29_Status", "Cota_30", "Cota_30_Status",
            "Cota_31", "Cota_31_Status",
            "Data_Hora_Dado", "Data_Ultima_Alteracao",
            "Dia_Maxima", "Dia_Minima", "Maxima", "Maxima_Status",
            "Media", "Media_Anual", "Media_Anual_Status",
            "Media_Status", "Mediadiaria", "Minima", "Minima_Status",
            "Tipo_Medicao_Cotas", "codigoestacao", "nivelconsistencia"
        ],
        'Chuva': [
            "Chuva_01", "Chuva_01_Status", "Chuva_02", "Chuva_02_Status",
            "Chuva_03", "Chuva_03_Status", "Chuva_04", "Chuva_04_Status",
            "Chuva_05", "Chuva_05_Status", "Chuva_06", "Chuva_06_Status",
            "Chuva_07", "Chuva_07_Status", "Chuva_08", "Chuva_08_Status",
            "Chuva_09", "Chuva_09_Status", "Chuva_10", "Chuva_10_Status",
            "Chuva_11", "Chuva_11_Status", "Chuva_12", "Chuva_12_Status",
            "Chuva_13", "Chuva_13_Status", "Chuva_14", "Chuva_14_Status",
            "Chuva_15", "Chuva_15_Status", "Chuva_16", "Chuva_16_Status",
            "Chuva_17", "Chuva_17_Status", "Chuva_18", "Chuva_18_Status",
            "Chuva_19", "Chuva_19_Status", "Chuva_20", "Chuva_20_Status",
            "Chuva_21", "Chuva_21_Status", "Chuva_22", "Chuva_22_Status",
            "Chuva_23", "Chuva_23_Status", "Chuva_24", "Chuva_24_Status",
            "Chuva_25", "Chuva_25_Status", "Chuva_26", "Chuva_26_Status",
            "Chuva_27", "Chuva_27_Status", "Chuva_28", "Chuva_28_Status",
            "Chuva_29", "Chuva_29_Status", "Chuva_30", "Chuva_30_Status",
            "Chuva_31", "Chuva_31_Status", "Data_Hora_Dado", "Data_Ultima_Alteracao",
            "Dia_Maxima", "Maxima", "Maxima_Status", "Nivel_Consistencia",
            "Numero_Dias_de_Chuva", "Numero_Dias_de_Chuva_Status",
            "Tipo_Medicao_Chuvas", "Total", "Total_Anual", "Total_Anual_Status",
            "Total_Status", "codigoestacao"
        ]
    }
    return chaves.get(tipo, [])

def cria_arquivo_resultado(path_arquivo: str, tipo: str):
    """Cria um arquivo com o cabeçalho de um tipo de estação"""
    with open(path_arquivo, 'w') as f:
        chaves = get_chaves_dicts_str(tipo) + '\n'
        f.write(chaves)

def atualizar_arquivo_resultado(path_arquivo: str, lista_dados: list, tipo: str):
    """Realiza o append de dados em um arquivo de estação."""
    with open(path_arquivo, 'a') as f:
        lista_chaves = get_chaves_dicts(tipo)
        formato = ('{};' * len(lista_chaves)) + '\n'

        for item in lista_dados:
            valores = [str(item.get(chave, '')) for chave in lista_chaves]
            linha = formato.format(*valores)
            f.write(linha)

def escrever_estacoes(path_estacoes: str, operacao: int, estacoes: list) -> None:
    """Escreve os códigos das estações no arquivo estacoes.txt"""
    modo = 'w' if operacao == 1 else 'a'
    with open(path_estacoes, modo) as f:
        for estacao in estacoes:
            f.write(f'{estacao}\n')

def atualiza_credenciais_ana(path_configs: str, dados: dict) -> None:
    """Atualiza o arquivo de configuração com as credenciais em 'dados'"""
    def atualizar():
        with open(path_configs, "r+") as f:
            data_json = json.load(f)
            data_json["Credenciais"] = {"Ana": {"Identificador": dados['id'], "Senha": dados['senha']}}

            f.seek(0)
            f.write(json.dumps(data_json))
            f.truncate()
    
    error_handler.safe_execute(
        atualizar,
        context="atualização de credenciais ANA",
        show_message=False
    )

def le_credenciais_ana(path_configs: str) -> list:
    """Lê o arquivo de configuração e retorna as credenciais da ANA"""
    def ler():
        with open(path_configs, 'r') as f:
            dados = json.load(f)
        cred = dados['Credenciais']['Ana']
        return [cred["Identificador"], cred["Senha"]]
    
    return error_handler.safe_execute(
        ler,
        context="leitura de credenciais ANA",
        show_message=False
    )

def cria_log(exception, trace, path_dir: str):
    """Cria um log de erro contendo a exceção e o traceback"""
    os.makedirs(path_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    log_path = os.path.join(path_dir, f'log-{timestamp}.txt')
    with open(log_path, 'w') as file:
        file.write(str(exception))
        file.write('\nTRACEBACK\n')
        file.write(trace)
