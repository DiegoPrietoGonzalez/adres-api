import unittest
from flask import Flask
from app.categoria import db, Adquisicion

class AdquisicionTest(unittest.TestCase):

    def setUp(self):
        # Configurar la aplicación Flask para las pruebas
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost:3305/adquisiciones'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)

        with self.app.app_context():
            # Crear las tablas en una base de datos temporal en memoria
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            # Eliminar las tablas después de las pruebas
            db.drop_all()

    def test_calcular_valor_total(self):
        # Crear una instancia de Adquisicion para realizar la prueba
        nueva_adquisicion = Adquisicion(
            nombre_completo='diego',
            cargo='Gerente',
            cantidad=5,
            valor_unitario=100.0
        )

        # Asegurarse de que el cálculo del valor total sea correcto
        self.assertEqual(nueva_adquisicion.calcular_valor_total(), 500.0)

if __name__ == '__main__':
    unittest.main()
