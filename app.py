from flask import Flask, render_template, send_file
import os

app = Flask(__name__)

# Página inicial com os resultados
@app.route('/')
def index():
    return render_template('index.html')

# Rota para baixar os arquivos
@app.route('/download_csv')
def download_csv():
    return send_file('output/top_10_products.csv', as_attachment=True)

@app.route('/download_png')
def download_png():
    return send_file('output/top_10_products.png', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
