from flask_smorest import Blueprint, abort
from flask import request, jsonify
from db import db
from model.Gasto import Gasto
from model.Departamento import Departamento  # Importa el modelo Departamento
from schema.GastoFechaSchema import GastoFechaSchema
from Factory.ResponseFactory import ResponseFactory  # Importa la ResponseFactory

# Definir el Blueprint
GastoBluePrint = Blueprint(
    'gasto', 'gasto', url_prefix='/gastos', description='Operaciones para la tabla Gasto'
)

# Obtener todos los gastos
@GastoBluePrint.route('/', methods=['GET'])
def get_gastos():
    """Obtener todos los gastos."""
    try:
        gastos = Gasto.query.all()
        return jsonify(ResponseFactory.success([gasto.json() for gasto in gastos]))
    except Exception as e:
        return jsonify(ResponseFactory.error(f"Ocurrió un error: {str(e)}"))

# Crear un nuevo gasto
@GastoBluePrint.route('/', methods=['POST'])
def create_gasto():
    """Crear un nuevo gasto."""
    try:
        data = request.get_json()
        # Validar los campos requeridos
        required_fields = ['fecha', 'descripcion', 'monto', 'id_empleado', 'id_departamento']
        for field in required_fields:
            if field not in data:
                return jsonify(ResponseFactory.error(f"El campo '{field}' es requerido.", code=400)), 400

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
        return jsonify(ResponseFactory.success(nuevo_gasto.json(), "Gasto creado exitosamente")), 201
    except Exception as e:
        return jsonify(ResponseFactory.error(f"Ocurrió un error: {str(e)}")), 500

# Actualizar un gasto existente
@GastoBluePrint.route('/<int:id_gasto>', methods=['PUT'])
def update_gasto(id_gasto):
    """Actualizar un gasto existente."""
    try:
        gasto = Gasto.query.get_or_404(id_gasto)
        data = request.get_json()

        # Actualizar los campos con datos recibidos o mantener los valores existentes
        gasto.fecha = data.get('fecha', gasto.fecha)
        gasto.descripcion = data.get('descripcion', gasto.descripcion)
        gasto.monto = data.get('monto', gasto.monto)
        gasto.id_empleado = data.get('id_empleado', gasto.id_empleado)
        gasto.id_departamento = data.get('id_departamento', gasto.id_departamento)

        db.session.commit()
        return jsonify(ResponseFactory.success(gasto.json(), "Gasto actualizado exitosamente"))
    except Exception as e:
        return jsonify(ResponseFactory.error(f"Ocurrió un error: {str(e)}")), 500

# Eliminar un gasto
@GastoBluePrint.route('/<int:id_gasto>', methods=['DELETE'])
def delete_gasto(id_gasto):
    """Eliminar un gasto."""
    try:
        gasto = Gasto.query.get_or_404(id_gasto)
        db.session.delete(gasto)
        db.session.commit()
        return jsonify(ResponseFactory.success(None, f"Gasto con ID {id_gasto} eliminado exitosamente")), 200
    except Exception as e:
        return jsonify(ResponseFactory.error(f"Ocurrió un error: {str(e)}")), 500

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
        return jsonify(ResponseFactory.success(data, "Resultados obtenidos exitosamente"))
    except Exception as e:
        return jsonify(ResponseFactory.error(f"Ocurrió un error: {str(e)}")), 500
