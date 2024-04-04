from suporte import database, app
from suporte.models import Cliente, Atendimento

with app.app_context():
    database.create_all()
