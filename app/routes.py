
from app import app
from flask import render_template, request, jsonify
import requests

class ConversorMoeda:

    def cotacao(self):
        try:
            link = "https://open.er-api.com/v6/latest"
            req = requests.get(link)
            req.raise_for_status()  # Lança exceção se houver erro HTTP
            dados = req.json()
            return dados["rates"]
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter taxas de câmbio: {e}")
            return {}

    def converter(self, quantidade, moedaOrigem, moedaDestino):
        taxa = self.cotacao()

        if moedaOrigem.upper() not in taxa or moedaDestino.upper() not in taxa:
            return "Moeda não localizada - Moeda Incorreta"
        
        taxaOrigem = taxa[moedaOrigem.upper()]
        taxaDestino = taxa[moedaDestino.upper()]
        
        valorConvertido = quantidade * (taxaDestino / taxaOrigem)
        
        return valorConvertido

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/converter', methods=['POST'])
def converter():
    try:
        quantidade = float(request.form.get('valor'))
        moedaOrigem = request.form.get('origem')
        moedaDestino = request.form.get('destino')

        conversorMoeda = ConversorMoeda()
        resultado = conversorMoeda.converter(quantidade, moedaOrigem, moedaDestino)
        
        if isinstance(resultado, str):  # Se o resultado é uma mensagem de erro
            return jsonify({'Resultado': resultado})

        resultado2 = f'{resultado:.2f}'  # Formatando para duas casas decimais
        
        return jsonify({'Resultado da conversao escolhida': resultado2})

    except ValueError as e:
        return jsonify({'erro': f"Erro na conversão: {e}"})


