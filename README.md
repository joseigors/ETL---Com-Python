# ETL - Processamento de Dados e Inserção no PostgreSQL

Este projeto realiza o processo de ETL (Extração, Transformação e Carga) de dados de um arquivo Excel para um banco de dados PostgreSQL. O script lê os dados de um arquivo `.xlsx`, realiza transformações necessárias e insere as informações na tabela de um banco de dados PostgreSQL.

# Fonte dos dados
https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica---cnpj
https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/2023-05/

# Observações:
Foi excluida do projeto os dados por serem maiores do que o suportado pelo github

# Justificativas

Eu optei pelo uso do Python em vez do Apache devido à sua flexibilidade, facilidade de integração com bibliotecas como pandas e psycopg2 para manipulação de dados e conexão com bancos de dados. Além disso, o Python oferece uma linguagem simples de manter e adaptar, sendo ideal para processos de ETL mais diretos e ágeis. A conversão do arquivo Excel foi escolhida porque é um formato amplamente utilizado, e o Python, com a biblioteca openpyxl, permite uma leitura e manipulação eficientes de arquivos Excel, sem a necessidade de configurações complexas. Isso torna o processo mais ágil e com baixo custo operacional, facilitando a automação de todo o fluxo.

## Requisitos

- Python 3.x
- Bibliotecas Python:
  - pandas
  - psycopg2
  - openpyxl
  - re
  - datetime
  - os

- Banco de Dados PostgreSQL configurado e em execução
- A tabela `empresas` já criada no banco de dados PostgreSQL com as colunas:

    ```sql
    CREATE TABLE empresas (
        cnpj_basico VARCHAR(14),
        razao_social VARCHAR(255),
        natureza_juridica VARCHAR(255),
        qualificacao_responsavel VARCHAR(255),
        capital_social NUMERIC,
        porte VARCHAR(50),
        localizacao VARCHAR(50)
    );
    ```

## Passos para Rodar

### 1. Instalar as dependências

Primeiro, instale as dependências necessárias usando o `pip`:

``bash
pip install pandas psycopg2 openpyx

### 2. Configurar o Banco de Dados PostgreSQL
Certifique-se de que o PostgreSQL esteja instalado e configurado. Crie o banco de dados ETL e a tabela empresas, se ainda não existirem:
    CREATE DATABASE ETL;
Crie a tabela empresas com a estrutura mencionada acima.

### 3. Preparar o Arquivo Excel
O script espera que o arquivo Excel (chamado Empresa.xlsx) esteja na pasta Data/ dentro do diretório do projeto. O arquivo não precisa ter cabeçalho, pois o script irá definir as colunas manualmente.

### 4. Rodar o Script
Execute o script Python para iniciar o processo ETL:
    python seu_script_etl.py

### 5. Relatório de Execução
O script gera um relatório de execução que é salvo no diretório Resumo_execução/ com o nome relatorio_etl.txt. O relatório inclui informações como:

Data e hora de início e término

Tempo total de execução

Total de registros processados

Total de registros inseridos com sucesso

Total de erros de inserção

### 6. Visualizar a Saída no Console
O script também exibe informações no console sobre o status da execução:

✅ ETL CONCLUÍDO COM SUCESSO
📄 Relatório salvo em: Resumo_execução/relatorio_etl.txt
Registros processados: 1000 | Sucesso: 999 | Erros: 1

## Funcionamento do Script
### Leitura do Arquivo Excel
O script lê o arquivo Empresa.xlsx e define as colunas manualmente. O arquivo não precisa ter cabeçalho. A leitura é feita com o pandas, utilizando a função read_excel.

### Transformações Realizadas
O capital social é tratado para substituir a vírgula por ponto e convertido para o tipo numérico.

O nome da razão social é extraído, removendo o CPF (caso presente) da razão social completa.

Caso haja valores nulos (NaN) nas colunas capital_social ou localizacao, esses valores são convertidos para None, que é o formato esperado pelo banco de dados PostgreSQL.

### Inserção de Dados no PostgreSQL
Os dados transformados são inseridos linha a linha na tabela empresas no PostgreSQL. Se ocorrer algum erro durante a inserção, esse erro é capturado e contabilizado.

### Relatório
Após a execução, o script gera um relatório no diretório Resumo_execução/ com o status completo da execução do ETL, incluindo o número de registros processados, inseridos com sucesso e erros de inserção.

### Exemplo de Uso
Entrada:
Suponha que o arquivo Data/Empresa.xlsx tenha os seguintes dados:

cnpj_basico	  |razao_social_completa|natureza_juridica	|qualificacao_responsavel	|capital_social	|porte	|localizacao
12345678000195|	Empresa X LTDA	    |206-6	            |Responsável A	            |500.000,00	    |Médio	|São Paulo
98765432000176|	Empresa Y SA	    |207-1	            |Responsável B	            |1.000.000,00	|Grande	|Rio de Janeiro

Saída
Após a execução do script, a tabela empresas no banco de dados PostgreSQL será populada com as informações transformadas.

### Relatório Gerado
O relatório gerado poderá ser algo como:

📄 RELATÓRIO DE EXECUÇÃO DO ETL
Data/Hora de início: 2025-05-08 10:00:00
Data/Hora de término: 2025-05-08 10:10:00
Tempo total de execução: 0:10:00
Total de registros processados: 2
Total de registros inseridos com sucesso: 2
Total de erros de inserção: 0

### Possíveis Melhorias
Adicionar validações mais complexas, como checagens de formato para CNPJ, e-mails, etc.

Implementar log de erros mais detalhado.

Adicionar notificações em caso de falha.

Realizar a execução do ETL de forma paralela para grandes volumes de dados.
