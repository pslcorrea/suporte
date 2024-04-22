import plotly.offline
from flask import render_template, url_for, redirect, flash, request
from sqlalchemy import or_, not_
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64
import plotly
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
from plotly.offline import plot


from suporte import app, database
from suporte.forms import FormCliente, FormAtendimento, FormPesquisa
from suporte.models import Cliente, Atendimento

@app.route('/')
def home():
    atendimentos = Atendimento.query.all()
    return render_template('home.html', atendimentos=atendimentos)

@app.route('/atendimentos', methods=['GET', 'POST'])
def atendimentos():
    form = FormAtendimento()
    form.cliente.choices = [(cliente.id, cliente.nome) for cliente in Cliente.query.order_by(Cliente.nome)]
    if form.validate_on_submit():
        atendimento = Atendimento(id_cliente = form.cliente.data, titulo=form.titulo.data, descricao=form.descricao.data)
        database.session.add(atendimento)
        database.session.commit()
        flash('Atendimento cadastrado com sucesso!','success')
        return redirect(url_for('home'))
    return render_template('atendimentos.html', form=form)

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    clientes = Cliente.query.all()
    form = FormCliente()
    if form.validate_on_submit():
        cliente = Cliente(nome = form.nome.data)
        database.session.add(cliente)
        database.session.commit()
        flash('Cliente cadastrado com sucesso!','success')
        return redirect(url_for('home'))
    return render_template('clientes.html',form=form, clientes=clientes)

@app.route('/exibirAtendimento/<atendimento_id>', methods=['GET','POST'])
def exibirAtendimento(atendimento_id):
    atendimento = Atendimento.query.get(atendimento_id)
    form = FormAtendimento()
    form.cliente.choices = [(cliente.id, cliente.nome) for cliente in Cliente.query.order_by(Cliente.nome)]
    if request.method == 'GET':
        form.cliente.data = atendimento.id_cliente
        form.titulo.data = atendimento.titulo
        form.descricao.data = atendimento.descricao
        form.solucao.data = atendimento.solucao
    elif form.validate_on_submit():
        atendimento.id_cliente = form.cliente.data
        atendimento.titulo = form.titulo.data
        atendimento.descricao = form.descricao.data
        atendimento.solucao = form.solucao.data
        database.session.commit()
        flash('Atendimento atualizado com sucesso!','success')
        return redirect(url_for('home'))
    return render_template('exibirAtendimento.html', atendimento=atendimento, form=form)

@app.route('/solucao', methods=['GET','POST'])
def solucao():
    atendimentos = Atendimento.query.filter(or_(Atendimento.solucao.isnot(None), not_(Atendimento.solucao == ''), Atendimento.solucao != ''))
    return render_template('solucao.html', atendimentos=atendimentos)

@app.route('/suporte', methods=['GET', 'POST'])
def suporte():

    clientes = Cliente.query.join(Atendimento, Cliente.id == Atendimento.id_cliente).filter(Atendimento.titulo != '').order_by(Cliente.nome).all()
    total_atendimentos = Atendimento.query.count()
    total_mes = Atendimento.query.group_by(database.func.strftime('%m-%Y', Atendimento.data_criacao)). \
        with_entities(database.func.strftime('%m-%Y', Atendimento.data_criacao).label('mes'),
                      database.func.count(Atendimento.id).label('total')).all()
    meses = [meses[0] for meses in total_mes]
    total_mensal = [total[1] for total in total_mes]
    print(f'Atendimentos mensal total:{meses} - {total_mensal}')

    return render_template('suporte.html',clientes=clientes, total_atendimentos=total_atendimentos, total_mes=total_mes)

@app.route('/grafico')
def grafico():
    # Consulta para obter o total de atendimentos por mês
    resultados = Atendimento.query.group_by(database.func.strftime('%m-%Y', Atendimento.data_criacao)). \
        with_entities(database.func.strftime('%m-%Y', Atendimento.data_criacao).label('mes'),
                      database.func.count(Atendimento.id).label('total')).all()
    meses = [result[0] for result in resultados]
    total_atendimentos = [result[1] for result in resultados]

    # Criação do gráfico de barras
    plt.figure(figsize=(8, 4))
    cores = plt.get_cmap('Set3').colors
    plt.bar(meses, total_atendimentos, color=cores)
    plt.xlabel('Mês')
    plt.ylabel('Total de Atendimentos')
    plt.title('Total de Atendimentos por Mês')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Conversão do gráfico em imagem base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    grafico_base64 = base64.b64encode(img.getvalue()).decode()
    img.close()
    return render_template('grafico.html', grafico_base64=grafico_base64)



@app.route('/grafico2')
def grafico2():
    # Consulta para obter o total de atendimentos por mês
    resultados = Atendimento.query.group_by(database.func.strftime('%m-%Y', Atendimento.data_criacao)). \
        with_entities(database.func.strftime('%m-%Y', Atendimento.data_criacao).label('mes'),
                      database.func.count(Atendimento.id).label('total')).all()
    meses = [result[0] for result in resultados]
    total_atendimentos = [result[1] for result in resultados]

    # Criação do gráfico de barras
    data = go.Bar(x=meses, y=total_atendimentos)
    grafico = go.Figure(data=data)
    grafico.update_layout(title='Total de Atendimentos por Mês', xaxis_title='Mêses', yaxis_title='Total de Atendimentos')
    grafico_div = plotly.offline.plot(grafico, auto_open=False, output_type='div')

    return render_template('grafico2.html', grafico_div=grafico_div)


@app.route('/grafico3')
def grafico3():
    # Consulta para obter o total de atendimentos por mês
    resultados = Atendimento.query.group_by(database.func.strftime('%m-%Y', Atendimento.data_criacao)). \
        with_entities(database.func.strftime('%m-%Y', Atendimento.data_criacao).label('mes'),
                      database.func.count(Atendimento.id).label('total')).all()

    df = pd.DataFrame.from_records(resultados,
      columns=['meses','atendimentos']
    )

    fig = px.bar(df,x='meses',y='atendimentos', labels={'meses':'Meses',\
        'atendimentos':'Atendimentos'}, height=500,\
        color_discrete_sequence=px.colors.qualitative.T10, \
        template='plotly_white',text_auto=True, \
        title='Qtde. de Atendimentos Mensais')
    fig.update_traces(textfont_size=20, textangle=0)

    plot_div = plot(fig, output_type='div')

    return render_template('grafico3.html',plot_div=plot_div)

@app.route('/pesquisa', methods=['GET', 'POST'])
def pesquisa():
    form = FormPesquisa()
    dados_pesquisa = form.termo.data
    atendimentos = Atendimento.query.\
        filter(Atendimento.descricao.like(f'%{dados_pesquisa}%')).all()
    return render_template('pesquisa.html',form=form, atendimentos=atendimentos )


