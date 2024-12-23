from flask_smorest import Blueprint, abort
from flask import request, jsonify
from marshmallow import ValidationError
from db import db
from model.Gasto import Gasto
from model.Departamento import Departamento  # Importa el modelo Departamento
from schema.GastoFechaSchema import GastoFechaSchema

# Definir el Blueprint
GastoBluePrint = Blueprint(
    'gasto', 'gasto', url_prefix='/gastos', description='Operaciones para la tabla Gasto'
)

# Obtener todos los gastos
@GastoBluePrint.route('/', methods=['GET'])
def get_gastos():
    """Obtener todos los gastos."""
    gastos = Gasto.query.all()
    return jsonify([gasto.json() for gasto in gastos])

# Crear un nuevo gasto
@GastoBluePrint.route('/', methods=['POST'])
def create_gasto():
    """Crear un nuevo gasto."""
    data = request.get_json()
    # Validar los campos requeridos
    required_fields = ['fecha', 'descripcion', 'monto', 'id_empleado', 'id_departamento']
    for field in required_fields:
        if field not in data:
            abort(400, message=f"El campo '{field}' es requerido.")

    # Crear el objeto Gasto
    nuevo_gasto = Gasto(
        fecha=data['fecha'],
        descripcion=data['descripcion'],
        monto=data['monto'],
        id_empleado=data['id_empleado'],
        id_departamento=data['id_departamento']
    )
    db.session.add(nuevo_gasto)
    db.session.commit()
    return jsonify(nuevo_gasto.json()), 201

# Actualizar un gasto existente
@GastoBluePrint.route('/<int:id_gasto>', methods=['PUT'])
def update_gasto(id_gasto):
    """Actualizar un gasto existente."""
    gasto = Gasto.query.get_or_404(id_gasto)
    data = request.get_json()

    # Actualizar los campos con datos recibidos o mantener los valores existentes
    gasto.fecha = data.get('fecha', gasto.fecha)
    gasto.descripcion = data.get('descripcion', gasto.descripcion)
    gasto.monto = data.get('monto', gasto.monto)
    gasto.id_empleado = data.get('id_empleado', gasto.id_empleado)
    gasto.id_departamento = data.get('id_departamento', gasto.id_departamento)

    db.session.commit()
    return jsonify(gasto.json())

# Eliminar un gasto
@GastoBluePrint.route('/<int:id_gasto>', methods=['DELETE'])
def delete_gasto(id_gasto):
    """Eliminar un gasto."""
    gasto = Gasto.query.get_or_404(id_gasto)
    db.session.delete(gasto)
    db.session.commit()
    return jsonify({'message': f'Gasto con ID {id_gasto} eliminado exitosamente'}), 200

# Filtrar gastos por rango de fechas y sumar por departamento
@GastoBluePrint.route('/filtrar', methods=['POST'])
@GastoBluePrint.arguments(GastoFechaSchema, location="json")
def filtrar_gastos(params):
    """Filtrar gastos por rango de fechas y sumar por departamento."""
    try:
        # Extraer fechas validadas
        fecha_inicio = params['fechaInicio']
        fecha_fin = params['fechaFin']

        resultados = db.session.query(
            db.func.sum(Gasto.monto).label('total'),
            Departamento.nombre.label('departamento')
        ).join(Departamento, Gasto.id_departamento == Departamento.id_departamento) \
         .filter(Gasto.fecha >= fecha_inicio, Gasto.fecha <= fecha_fin) \
         .group_by(Departamento.nombre).all()

        data = [{'departamento': r.departamento, 'total': float(r.total)} for r in resultados]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
