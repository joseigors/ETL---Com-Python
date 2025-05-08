import pandas as pd
import openpyxl
# Caminho do arquivo CSV
arquivo_csv = 'Data/Empresa.EMPRECSV'

# Caminho do arquivo Excel de saída
arquivo_excel = 'Data/Empresa.xlsx'

# Leitura do CSV
df = pd.read_csv(arquivo_csv, sep=';', encoding='latin1')

# Limitar os dados ao máximo de linhas do Excel (1048576)
df_limitado = df.head(1048575)

# Salvar os dados no formato Excel
df_limitado.to_excel(arquivo_excel, index=False, engine='openpyxl')

print(f'Arquivo Excel salvo com {len(df_limitado)} registros.')
