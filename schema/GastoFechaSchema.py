from marshmallow import Schema, fields, ValidationError

def validate_date(value):
    """Valida que el formato de la fecha sea YYYY-MM-DD"""
    from datetime import datetime
    try:
        datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        raise ValidationError('El formato de la fecha debe ser YYYY-MM-DD.')

class GastoFechaSchema(Schema):
    fechaInicio = fields.String(
        required=True, 
        validate=validate_date,
        description="Fecha de inicio del filtro en formato YYYY-MM-DD",
    )
    fechaFin = fields.String(
        required=True, 
        validate=validate_date,
        description="Fecha de fin del filtro en formato YYYY-MM-DD",
    )
