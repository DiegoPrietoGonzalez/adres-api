from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError
from flask_basicauth import BasicAuth
import json
from wtforms import Form, StringField, validators


app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root:12345@localhost:3305/adquisiciones'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)


# Configuración de la autenticación básica
app.config['BASIC_AUTH_USERNAME'] = 'root'
app.config['BASIC_AUTH_PASSWORD'] = '1234'
basic_auth = BasicAuth(app)

# Definición del modelo de adquisiciones
class Adquisicion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(100))
    cargo = db.Column(db.String(50))
    departamento = db.Column(db.String(50))
    correo = db.Column(db.String(100))
    numero_telefono = db.Column(db.String(15))
    presupuesto = db.Column(db.Float)
    unidad_tipo = db.Column(db.String(50)) 
    cantidad = db.Column(db.Integer)
    valor_unitario = db.Column(db.Float)
    valor_total = db.Column(db.Float)
    fecha_adquisicion = db.Column(db.Date)
    proveedor = db.Column(db.String(100))
    documentacion = db.Column(db.String(200))
    activo = db.Column(db.Boolean, default=True)
    
    def calcular_valor_total(self):
        return self.cantidad * self.valor_unitario

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()
    
# Esquema de WTForms para la validación de entrada
class AdquisicionForm(Form):
    nombre_completo = StringField('Nombre Completo', [validators.DataRequired()])
    cargo = StringField('cargo', [validators.DataRequired()])
    departamento = StringField('departamento', [validators.DataRequired()])
    correo = StringField('correo', [validators.DataRequired()])
    numero_telefono = StringField('numero_telefono', [validators.DataRequired()])
    presupuesto = StringField('presupuesto', [validators.DataRequired()])
    unidad_tipo = StringField('unidad_tipo', [validators.DataRequired()])
    cantidad = StringField('cantidad', [validators.DataRequired()])
    valor_unitario = StringField('valor_unitario', [validators.DataRequired()])
    valor_total = StringField('corrvalor_totaleo', [validators.DataRequired()])
    fecha_adquisicion = StringField('fecha_adquisicion', [validators.DataRequired()])
    proveedor = StringField('proveedor', [validators.DataRequired()])
    documentacion = StringField('documentacion', [validators.DataRequired()])

# Endpoint para crear un nuevo requerimiento de adquisición
@app.route('/adquisiciones', methods=['POST'])
@basic_auth.required
def crear_adquisicion():
    datos_nueva_adquisicion = request.json

    form = AdquisicionForm(data=datos_nueva_adquisicion)
    if form.validate():
        nueva_adquisicion = Adquisicion(**datos_nueva_adquisicion)
        db.session.add(nueva_adquisicion)
        db.session.commit()
        return jsonify({"mensaje": "Requerimiento de adquisición creado correctamente"})
    else:
         # Agregar errores de validación a la respuesta JSON
        return jsonify({"error": "Datos no válidos", "detalles": form.errors}), 400

# Endpoint para obtener todos los requerimientos de adquisiciones
@app.route('/adquisiciones', methods=['GET'])
@basic_auth.required
def obtener_adquisiciones():
    adquisiciones = Adquisicion.query.filter_by(activo=True).all()
    resultado = json.dumps([adq.serialize() for adq in adquisiciones], indent=2, default=str)
    return resultado

# Método de serialización para convertir un objeto SQLAlchemy en un diccionario serializable
def serialize(self):
    return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# Adjuntar el método de serialización al modelo
Adquisicion.serialize = serialize

# Endpoint para desactivar un requerimiento de adquisición
@app.route('/adquisiciones/<int:id>', methods=['DELETE'])
@basic_auth.required
def desactivar_adquisicion(id):
    adquisicion = Adquisicion.query.get(id)
    if adquisicion:
        adquisicion.activo = False
        db.session.delete(adquisicion)
        db.session.commit()
        return jsonify({"mensaje": "Requerimiento de adquisición desactivado correctamente"})
    else:
        return jsonify({"error": "Requerimiento de adquisición no encontrado"}), 404

# Endpoint para modificar un requerimiento de adquisición
@app.route('/adquisiciones/<int:id>', methods=['PUT'])
@basic_auth.required
def modificar_adquisicion(id):
    adquisicion = Adquisicion.query.get(id)
    if adquisicion:
        datos_modificados = request.json
        for key, value in datos_modificados.items():
            setattr(adquisicion, key, value)
        db.session.commit()
        return jsonify({"mensaje": "Requerimiento de adquisición modificado correctamente"})
    else:
        return jsonify({"error": "Requerimiento de adquisición no encontrado"}), 404

    
if __name__ == '__main__':
    app.run(debug=True, port=4000) # debug app