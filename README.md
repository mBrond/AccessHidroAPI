# AcessHidroAPI

## Sobre 
Software para requisitar dados da API Hidro Webservice, nomeado Acess Hidro API (AHAPI).

## Como Utilizar
O software realiza requisições para a API de Consulta Hidro Webservice (https://www.ana.gov.br/hidrowebservice/swagger-ui/index.html#/WSEstacoesTelemetricasController). Para tal, é necessário solicitar a criação de um login e senha próprios através do e-mail telemetria@ana.gov.br.

### Utilização do AcessHidroAPI
O programa foi desenvolvido em Python, sendo necessário ter um interpretador desta linguagem instalado no computador do usuário para sua utilização. A inicialização do programa é feita ao rodar o arquivo *main.py*. 
A interação do usuário se dá por meio de um menu no prompt de comando. As opções são mostradas na tela e são acessíveis através do input do número relacionado a elas.

### Registrando credenciais

Antes de solicitar quaisquer dados, é preciso inserir as credenciais do usuário da API Webservice. Selecione a opção *Atualizar Credenciais* e insira os dados.

### Registrando estações

Os códigos das estações cujos dados serão baixados ficam salvos no arquivo *estacoes.txt*. É possível atualizá-lo manualmente, porém tal ação também pode ser realizada pelo AHAPI. Atente-se que, ao modificar manualmente o arquivo, cada código de estação deve estar em uma linha.
Na opção *Atualizar Estações*, é possível escolher entre *Sobrescrever* e *Adicionar*. *Sobrescrever* apagará todos os códigos já salvos, substituindo-os pelos que serão informados. *Adicionar* complementa o arquivo com os novos códigos inseridos.

### Solicitando dados

As opções de índices 4 e 5 solicitam dados de um único dia. Já os índices 5 e 6 solicitam dados de períodos, independentemente da duração. Serão solicitados dados de **todas** as estações com códigos salvos, conforme o tópico anterior. O mesmo intervalo de tempo será aplicado para todas as estações. 

Os dados são salvos na pasta '//resultados//', em arquivos *.txt* nomeados de acordo com o código da estação e seu período de tempo.

O download e a velocidade de download de qualquer dado estão sujeitos à disponibilidade de acesso à API de consulta do Hidro Webservice e à conexão de internet do usuário.

## Falhas Conhecidas
Há certos comportamentos do usuário que podem causar mau funcionamento no programa. Todos serão tratados em versões posteriores do software. Abaixo há uma lista das falhas conhecidas:

- Input de datas inválidas:
    - 'Data de começo' ser posterior à 'Data final'
    - Data não possuir a formatação correta (yyyy-mm-dd)
- Código de estação inválido
- Dispositivo não conectado à internet
