from db import db

class Departamento(db.Model):
    __tablename__ = 'Departamento'  # Nombre de la tabla en la base de datos

    id_departamento = db.Column(db.Integer, primary_key=True)  # Clave primaria
    nombre = db.Column(db.String(50), nullable=False)  # Columna para el nombre del departamento

    def __init__(self, nombre):
        self.nombre = nombre

    def json(self):
        """Método para retornar la representación del modelo en formato JSON."""
        return {
            'id_departamento': self.id_departamento,
            'nombre': self.nombre
        }
