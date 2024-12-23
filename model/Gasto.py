from db import db

class Gasto(db.Model):
    __tablename__ = 'Gasto'  # Nombre de la tabla en la base de datos

    id_gasto = db.Column(db.Integer, primary_key=True)  # Clave primaria
    fecha = db.Column(db.Date, nullable=False)  # Fecha del gasto
    descripcion = db.Column(db.String(100), nullable=False)  # Descripción del gasto
    monto = db.Column(db.Numeric(10, 2), nullable=False)  # Monto del gasto
    id_empleado = db.Column(db.Integer, db.ForeignKey('Empleado.id_empleado'), nullable=False)  # FK a Empleado
    id_departamento = db.Column(db.Integer, db.ForeignKey('Departamento.id_departamento'), nullable=False)  # FK a Departamento

    def __init__(self, fecha, descripcion, monto, id_empleado, id_departamento):
        self.fecha = fecha
        self.descripcion = descripcion
        self.monto = monto
        self.id_empleado = id_empleado
        self.id_departamento = id_departamento

    def json(self):
        """Método para retornar la representación del modelo en formato JSON."""
        return {
            'id_gasto': self.id_gasto,
            'fecha': self.fecha,
            'descripcion': self.descripcion,
            'monto': str(self.monto),
            'id_empleado': self.id_empleado,
            'id_departamento': self.id_departamento
        }
