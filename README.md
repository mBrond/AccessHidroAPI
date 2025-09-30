# AccessHidroAPI (AHAPI)
![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17234552.svg)](https://doi.org/10.5281/zenodo.17234552)

## Sobre

O **Access Hidro API (AHAPI)** é um software em **Python 3** para requisição de dados da **API Hidro Webservice** da Agência Nacional de Águas (ANA).
Ele permite registrar credenciais, gerenciar estações e realizar o download de dados hidrometeorológicos de forma prática.

---

## Instalação

### Via Código Fonte

O programa foi desenvolvido em **Python 3**. Para executar:

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/AHAPI.git
cd AHAPI

# (Opcional) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute
python main.py
```

### Via Executável

Também há disponível uma versão compilada para **Windows 11**.
Observações:

* Pode não funcionar corretamente em outros sistemas operacionais.
* Não possui assinatura digital, então seu antivírus pode sinalizar como potencial ameaça.

---

## Obtendo Credenciais

As credenciais são concedidas pela **ANA** via e-mail.
Siga as instruções disponíveis no Hidroweb: [Solicitar credenciais no Hidroweb](https://www.snirh.gov.br/hidroweb/acesso-api) para adquiri-lás.

---

## Como Utilizar

### 1. Registrando credenciais

Antes de solicitar dados:

* Selecione **Atualizar Credenciais**.
* Insira os dados fornecidos pela ANA nos campos de Login e Senha.
* Selecione **Confirmar**

---

### 2. Adicionando Estações

#### Pelo AHAPI

1. Clique em **Atualizar estações**.
2. Selecione **Adicionar estações**.
3. Insira os códigos das estações (um por linha).
4. Clique em **Atualizar**.

Opções adicionais:

* **Sobreescrever estações** → apaga registros anteriores e substitui pelas novas.
* **Adicionar estações** → mantém registros anteriores e adiciona novas.
* **Visualizar estações** → abre a lista atual de estações. É possível remover selecionadas.

#### Manualmente

Edite ou substitua o arquivo `estacoes.txt` manualmente.

* O arquivo deve conter apenas códigos de estações
* Cada código deve estar em **uma linha separada**.

---

### 3. Selecionando Tipo das Estações

Os tipos de dados disponíveis:

* Telemétricas Adotadas
* Telemétricas Detalhadas
* Convencionais de Chuva
* Convencionais de Cota
* Convencionais de Sedimentos

---

### 4. Solicitando Dados

1. Clique em **Baixar Estações**.
2. Selecione o período de datas.
3. Clique em **Baixar estações**.

O tempo de download depende da **disponibilidade da API da ANA** e da **velocidade de internet**.
Uma barra de progresso indica o andamento da operação.

---

### 5. Acessando Dados

Os arquivos baixados ficam organizados em `resultados/`, separados por tipo de estação:

```
resultados/
 ├── Adotadas/
 ├── Detalhadas/
 ├── Chuvas/
 ├── Cotas/
 └── Sedimentos/
```

Cada arquivo segue o padrão:

```
códigoEstação-tipoEstação-dataInicial-dataFinal.txt
```

---

##  Erros de Execução

* Erros de uso são exibidos em **popups** para o usuário.
* Logs detalhados ficam registrados em `logs/`.

## Contato

Para mais informações sobre o projeto, sugestões ou reportar erros:
- Miguel Brondani - Desenvolvedor: brondani.miguel@gmail.com
- Daniel Allasia - Professor Orientador: dallasia@gmail.com
- Ecotecnologias - Grupo de Pesquisa: eco@ecotecnologias.org
- https://github.com/mBrond/AccessHidroAPI