import pandas as pd
import matplotlib.pyplot as plt
import os

# Criar pasta de saída se não existir
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# Ler a planilha
df = pd.read_csv('data/Pasta13 - Planilha1.csv', thousands='.', decimal=',')
df['QTD_FATURADA'] = df['QTD FATURADA'].str.replace('\xa0', ' ')  # Remove espaços especiais
df['QTD_FATURADA'] = df['QTD FATURADA'].str.replace(' ', '').str.replace(',', '.').astype(float)

# Classificação ABC
df_sorted = df.sort_values('QTD_FATURADA', ascending=False)
total_sales = df['QTD_FATURADA'].sum()
df_sorted['CUMULATIVE_PERCENTAGE'] = df_sorted['QTD_FATURADA'].cumsum() / total_sales * 100
df_sorted['ABC_CLASSIFICATION'] = pd.cut(df_sorted['CUMULATIVE_PERCENTAGE'], bins=[0, 80, 95, 100], labels=['A', 'B', 'C'])

# Gráfico Top 10 Produtos
top_10_products = df_sorted.head(10)
plt.figure(figsize=(15, 6))
plt.bar(top_10_products['DESCR'], top_10_products['QTD_FATURADA'])
plt.title('Top 10 Produtos por Volume de Vendas')
plt.xlabel('Produto')
plt.ylabel('Quantidade Faturada')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f'{output_folder}/top_10_products.png')
plt.close()

# Salvar CSVs
top_10_products[['DESCR', 'SKU', 'QTD_FATURADA']].to_csv(f'{output_folder}/top_10_products.csv', index=False)
df_sorted.to_csv(f'{output_folder}/abc_analysis_summary.csv', index=False)

print("✅ Arquivos gerados com sucesso na pasta 'output'.")
