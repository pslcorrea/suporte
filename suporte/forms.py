from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired

class FormCliente(FlaskForm):
    nome = StringField('Nome do Cliente', validators=[DataRequired()])
    botaoSubmit = SubmitField('Cadastrar Cliente')

class FormAtendimento(FlaskForm):
    cliente = SelectField('Selecione o Cliente', validators=[DataRequired()])
    titulo = StringField('Titulo do Chamado', validators=[DataRequired()])
    descricao = TextAreaField('Descrição do Chamado', validators=[DataRequired()])
    solucao = TextAreaField('Solução do Chamado')
    botaoSubmit = SubmitField('Cadastrar Chamado')

class FormPesquisa(FlaskForm):
    termo = StringField('Digite sua Consulta', validators=[DataRequired()])
    botaoSubmit = SubmitField('Realizar Pesquisa')
