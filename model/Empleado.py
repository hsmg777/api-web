from db import db

class Empleado(db.Model):
    __tablename__ = 'Empleado'  # Nombre de la tabla en la base de datos

    id_empleado = db.Column(db.Integer, primary_key=True)  # Clave primaria
    nombre = db.Column(db.String(50), nullable=False)  # Columna para el nombre
    apellido = db.Column(db.String(50), nullable=False)  # Columna para el apellido

    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

    def json(self):
        """Método para retornar la representación del modelo en formato JSON."""
        return {
            'id_empleado': self.id_empleado,
            'nombre': self.nombre,
            'apellido': self.apellido
        }
