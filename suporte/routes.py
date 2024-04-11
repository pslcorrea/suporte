from flask import render_template, url_for, redirect, flash, request
from sqlalchemy import or_, not_
from suporte import app, database
from suporte.forms import FormCliente, FormAtendimento
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
    form = FormCliente()
    if form.validate_on_submit():
        cliente = Cliente(nome = form.nome.data)
        database.session.add(cliente)
        database.session.commit()
        flash('Cliente cadastrado com sucesso!','success')
        return redirect(url_for('home'))
    return render_template('clientes.html',form=form)

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
