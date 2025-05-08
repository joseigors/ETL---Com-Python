import pandas as pd
import re
import psycopg2
from datetime import datetime
import os

# Início da contagem de tempo
inicio = datetime.now()

# Configurações do PostgreSQL
db_config = {
    'dbname': 'ETL',
    'user': 'postgres',
    'password': 'sua_senha', 
    'host': 'localhost',
    'port': '5432'
}

# Caminho do arquivo .xlsx
arquivo_excel = 'Data/Empresa.xlsx'

# Nome das colunas (o .xlsx não tem cabeçalho)
colunas = [
    'cnpj_basico',
    'razao_social_completa',
    'natureza_juridica',
    'qualificacao_responsavel',
    'capital_social',
    'porte',
    'localizacao'  # ignorada depois
]

# Leitura do .xlsx com tudo como texto
df = pd.read_excel(
    arquivo_excel,
    names=colunas,
    header=None,
    dtype=str,
    engine='openpyxl'
)

# Tratamento do capital social
# Substitui vírgula por ponto e converte para numérico
df['capital_social'] = df['capital_social'].str.replace(',', '.', regex=False)
df['capital_social'] = pd.to_numeric(df['capital_social'], errors='coerce')

# Remove CPF do nome (últimos 11 dígitos, se existirem)
def extrair_razao_social(texto):
    match = re.match(r'^(.+?)\s(\d{11})$', texto.strip())
    return match.group(1) if match else texto.strip()

df['razao_social'] = df['razao_social_completa'].apply(extrair_razao_social)

# Filtrar colunas necessárias
df_final = df[['cnpj_basico', 'razao_social', 'natureza_juridica', 'qualificacao_responsavel', 'capital_social', 'porte', 'localizacao']].copy()

# Conexão com PostgreSQL
conexao = psycopg2.connect(**db_config)
cursor = conexao.cursor()

# Contadores
inseridos = 0
erros = 0

# Inserção linha a linha
for _, row in df_final.iterrows():
    try:
        cnpj_basico = row['cnpj_basico']
        razao_social = row['razao_social']
        natureza_juridica = row['natureza_juridica']
        qualificacao_responsavel = row['qualificacao_responsavel']
        capital_social = row['capital_social']
        porte = row['porte']
        localizacao = row['localizacao']

        # Converte NaN para None (caso ainda exista)
        if pd.isna(capital_social):
            capital_social = None

        if pd.isna(localizacao):
            localizacao = None

        cursor.execute("""
            INSERT INTO empresas (cnpj_basico, razao_social, natureza_juridica, qualificacao_responsavel, capital_social, porte, localizacao)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            cnpj_basico,
            razao_social,
            natureza_juridica,
            qualificacao_responsavel,
            capital_social,
            porte,
            localizacao
        ))
        inseridos += 1
    except Exception as e:
        erros += 1
        print(f"Erro ao inserir: {e}")

# Finaliza e salva
conexao.commit()
cursor.close()
conexao.close()

# Fim da contagem
fim = datetime.now()
duracao = fim - inicio

# Geração de relatório
os.makedirs('Resumo_execução', exist_ok=True)
with open('Resumo_execução/relatorio_etl.txt', 'w', encoding='utf-8') as rel:
    rel.write("📄 RELATÓRIO DE EXECUÇÃO DO ETL\n")
    rel.write(f"Data/Hora de início: {inicio.strftime('%Y-%m-%d %H:%M:%S')}\n")
    rel.write(f"Data/Hora de término: {fim.strftime('%Y-%m-%d %H:%M:%S')}\n")
    rel.write(f"Tempo total de execução: {duracao}\n")
    rel.write(f"Total de registros processados: {len(df_final)}\n")
    rel.write(f"Total de registros inseridos com sucesso: {inseridos}\n")
    rel.write(f"Total de erros de inserção: {erros}\n")

# Saída no console
print("✅ ETL CONCLUÍDO COM SUCESSO")
print(f"📄 Relatório salvo em: Resumo_execução/relatorio_etl.txt")
print(f"Registros processados: {len(df_final)} | Sucesso: {inseridos} | Erros: {erros}")
