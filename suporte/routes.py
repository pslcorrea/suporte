from flask import render_template, url_for
from suporte import app


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/atendimentos', methods=['GET', 'POST'])
def atendimentos():
    return render_template('atendimentos.html')

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    return render_template('clientes.html')
