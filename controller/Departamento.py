from flask_smorest import Blueprint
from flask import request, jsonify
from db import db
from model.Departamento import Departamento  # Importa el modelo Departamento

DepartamentoBluePrint = Blueprint(
    'departamento', 'departamento', url_prefix='/departamentos', description='Operaciones para la tabla Departamento'
)

@DepartamentoBluePrint.route('/', methods=['GET'])
def get_departamentos():
    """Obtener todos los departamentos."""
    departamentos = Departamento.query.all()
    return jsonify([departamento.json() for departamento in departamentos])

@DepartamentoBluePrint.route('/', methods=['POST'])
def create_departamento():
    """Crear un nuevo departamento."""
    data = request.get_json()
    nuevo_departamento = Departamento(nombre=data['nombre'])
    db.session.add(nuevo_departamento)
    db.session.commit()
    return jsonify(nuevo_departamento.json()), 201

@DepartamentoBluePrint.route('/<int:id_departamento>', methods=['PUT'])
def update_departamento(id_departamento):
    """Actualizar un departamento existente."""
    departamento = Departamento.query.get_or_404(id_departamento)
    data = request.get_json()
    departamento.nombre = data.get('nombre', departamento.nombre)
    db.session.commit()
    return jsonify(departamento.json())

@DepartamentoBluePrint.route('/<int:id_departamento>', methods=['DELETE'])
def delete_departamento(id_departamento):
    """Eliminar un departamento."""
    departamento = Departamento.query.get_or_404(id_departamento)
    db.session.delete(departamento)
    db.session.commit()
    return jsonify({'message': f'Departamento con ID {id_departamento} eliminado exitosamente'}), 200
