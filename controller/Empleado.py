from flask_smorest import Blueprint
from flask import request, jsonify
from db import db
from model.Empleado import Empleado 

EmpleadoBluePrint = Blueprint(
    'empleado', 'empleado', url_prefix='/empleados', description='Operaciones para la tabla Empleado'
)

@EmpleadoBluePrint.route('/', methods=['GET'])
def get_empleados():
    """Obtener todos los empleados."""
    empleados = Empleado.query.all()
    return jsonify([empleado.json() for empleado in empleados])

@EmpleadoBluePrint.route('/', methods=['POST'])
def create_empleado():
    """Crear un nuevo empleado."""
    data = request.get_json()
    nuevo_empleado = Empleado(nombre=data['nombre'], apellido=data['apellido'])
    db.session.add(nuevo_empleado)
    db.session.commit()
    return jsonify(nuevo_empleado.json()), 201

@EmpleadoBluePrint.route('/<int:id_empleado>', methods=['PUT'])
def update_empleado(id_empleado):
    """Actualizar un empleado existente."""
    empleado = Empleado.query.get_or_404(id_empleado)
    data = request.get_json()
    empleado.nombre = data.get('nombre', empleado.nombre)
    empleado.apellido = data.get('apellido', empleado.apellido)
    db.session.commit()
    return jsonify(empleado.json())

@EmpleadoBluePrint.route('/<int:id_empleado>', methods=['DELETE'])
def delete_empleado(id_empleado):
    """Eliminar un empleado."""
    empleado = Empleado.query.get_or_404(id_empleado)
    db.session.delete(empleado)
    db.session.commit()
    return jsonify({'message': f'Empleado con ID {id_empleado} eliminado exitosamente'}), 200
