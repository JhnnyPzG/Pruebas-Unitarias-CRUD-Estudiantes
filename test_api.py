import unittest
from api import app

class EstudiantesTestCase(unittest.TestCase):
    # Configuración para crear un ambiente controlado de pruebas
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    # Prueba para verificar que se pueden obtener todos los estudiantes
    def test_obtener_estudiantes(self):
        response = self.app.get('/estudiantes')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)

    # Prueba para verificar que se obtiene un estudiante por id 3 y que este debe de dar el Nombre correspondiente
    def test_obtener_estudiante_id(self):
        response = self.app.get('/estudiantes/3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['Nombre'], "David Hernandez")
    
    # Prueba para verificar que se puede crear un nuevo estudiante
    def test_crear_estudiante(self):
        nuevo_estudiante = {
            'nombre': 'David Hernandez',
            'edad': 22,
            'celular': '312-1234',
            'nota': 2
        }
        response = self.app.post('/estudiantes', json=nuevo_estudiante)
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.json['id'], int)
    
    # Prueba para verificar que funcione la funcion de actualizar estudiante
    def test_actualizar_estudiante(self):
        nuevos_datos = {
            'nombre': 'David Hernandez',
            'edad': 22,
            'celular': '312-1234',
            'nota': 5
        }
        response = self.app.put('/estudiantes/3', json=nuevos_datos)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json['mensaje'], str)
        self.assertEqual(response.json["mensaje"], "Estudiante actualizado con éxito")

    # Prueba para verificar que funciona la funcion de eliminar estudiante
    def test_eliminar_estudiante(self):
        response = self.app.delete('/estudiantes/4')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json['mensaje'], str)
        self.assertEqual(response.json["mensaje"], "Estudiante eliminado con éxito")



