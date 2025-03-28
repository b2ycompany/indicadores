from flask import Flask, render_template, send_file
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

# Função para gerar os gráficos e realizar as análises
def generate_data():
    # Leitura e processamento dos dados
    df = pd.read_csv('data/Pasta13 - Planilha1.csv', thousands='.', decimal=',')
    df['QTD_FATURADA'] = df['QTD FATURADA'].str.replace('\xa0', ' ')  # Remove non-breaking spaces
    df['QTD_FATURADA'] = df['QTD FATURADA'].str.replace(' ', '')
    df['QTD_FATURADA'] = df['QTD FATURADA'].str.replace(',', '.')
    df['QTD_FATURADA'] = pd.to_numeric(df['QTD_FATURADA'], errors='coerce')

    # Classificação ABC
    df_sorted = df.sort_values('QTD_FATURADA', ascending=False)
    total_sales = df['QTD_FATURADA'].sum()
    df_sorted['CUMULATIVE_PERCENTAGE'] = df_sorted['QTD_FATURADA'].cumsum() / total_sales * 100
    df_sorted['ABC_CLASSIFICATION'] = pd.cut(df_sorted['CUMULATIVE_PERCENTAGE'], bins=[0, 80, 95, 100], labels=['A', 'B', 'C'])

    # Preparar o gráfico
    top_10_products = df_sorted.head(10)
    plt.figure(figsize=(15, 6))
    plt.bar(top_10_products['DESCR'], top_10_products['QTD_FATURADA'])
    plt.title('Top 10 Products by Sales Volume', fontsize=15)
    plt.xlabel('Product Description', fontsize=12)
    plt.ylabel('Sales Volume', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('top_10_products.png')
    plt.close()

    # Salvar os dados
    top_10_products[['DESCR', 'SKU', 'QTD_FATURADA']].to_csv('top_10_products.csv', index=False)

    return df_sorted, top_10_products

# Página inicial com os resultados e gráficos
@app.route('/')
def index():
    # Gerar os dados
    df_sorted, top_10_products = generate_data()
    
    # Renderizar a página HTML com os resultados
    return render_template('index.html', 
                           abc_summary=df_sorted.groupby('ABC_CLASSIFICATION').agg({
                               'QTD_FATURADA': ['count', 'sum', 'mean'],
                               'CUMULATIVE_PERCENTAGE': 'max'
                           }).reset_index().to_html(classes='table table-striped'), 
                           top_10_products=top_10_products.to_html(classes='table table-striped'))

# Rota para fazer download do CSV
@app.route('/download_csv')
def download_csv():
    return send_file('top_10_products.csv', as_attachment=True)

# Rota para fazer download do gráfico
@app.route('/download_png')
def download_png():
    return send_file('top_10_products.png', as_attachment=True)

# Rota para exportar a página como PDF (exemplo básico)
@app.route('/download_pdf')
def download_pdf():
    # Aqui você pode usar uma biblioteca como o WeasyPrint para gerar PDFs da página HTML
    # Para simplicidade, vamos apenas enviar o gráfico como exemplo
    return send_file('top_10_products.png', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
