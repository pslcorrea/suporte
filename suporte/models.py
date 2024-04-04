from suporte import database
from datetime import datetime

class Cliente(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    atendimentos = database.relationship('Atendimento', backref='suporte', lazy=True)

class Atendimento(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    descricao = database.Column(database.Text, nullable=False)
    data_criacao= database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    solucao = database.Column(database.Text)
    id_cliente = database.Column(database.Integer, database.ForeignKey('cliente.id'), nullable=False)
