from flask import Flask, render_template, send_file
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

data_file = 'data/Pasta13 - Planilha1.csv'
output_dir = 'static/'  # Pasta para salvar gráficos

# Criar a pasta static se não existir
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def process_data():
    # Ler os dados
    df = pd.read_csv(data_file, thousands='.', decimal=',')
    df['QTD_FATURADA'] = df['QTD FATURADA'].str.replace(' ', '').astype(float)
    
    # Ordenar e calcular totais
    df_sorted = df.sort_values('QTD_FATURADA', ascending=False)
    total_sales = df['QTD_FATURADA'].sum()
    df_sorted['CUMULATIVE_PERCENTAGE'] = df_sorted['QTD_FATURADA'].cumsum() / total_sales * 100
    df_sorted['ABC_CLASSIFICATION'] = pd.cut(
        df_sorted['CUMULATIVE_PERCENTAGE'], 
        bins=[0, 80, 95, 100], 
        labels=['A', 'B', 'C']
    )
    
    # Top 10 produtos
    top_10_products = df_sorted.head(10)
    
    # Resumo ABC
    abc_summary = df_sorted.groupby('ABC_CLASSIFICATION').agg({
        'QTD_FATURADA': ['count', 'sum', 'mean'],
        'CUMULATIVE_PERCENTAGE': 'max'
    }).reset_index()
    abc_summary.columns = ['Category', 'Product Count', 'Total Sales', 'Average Sales', 'Cumulative Percentage']
    
    # Salvar gráficos
    plt.figure(figsize=(12, 6))
    plt.bar(top_10_products['DESCR'], top_10_products['QTD_FATURADA'])
    plt.title('Top 10 Produtos por Volume de Vendas')
    plt.xticks(rotation=45, ha='right')
    plt.savefig(f'{output_dir}top_10_products.png')
    plt.close()
    
    plt.figure(figsize=(8, 6))
    abc_sales = df_sorted.groupby('ABC_CLASSIFICATION')['QTD_FATURADA'].sum()
    plt.pie(abc_sales, labels=abc_sales.index, autopct='%1.1f%%', colors=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    plt.title('Distribuição de Vendas por Classificação ABC')
    plt.savefig(f'{output_dir}abc_distribution.png')
    plt.close()
    
    # Salvar CSVs
    top_10_products[['DESCR', 'SKU', 'QTD_FATURADA']].to_csv(f'{output_dir}top_10_products.csv', index=False)
    abc_summary.to_csv(f'{output_dir}abc_analysis_summary.csv', index=False)
    
    return top_10_products, abc_summary

@app.route('/')
def index():
    top_10_products, abc_summary = process_data()
    return render_template('index.html', top_10=top_10_products.to_dict(orient='records'), abc_summary=abc_summary.to_dict(orient='records'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(f'static/{filename}', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
