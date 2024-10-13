import unittest
from modules.tps import Cliente, Transaccion, Reporte

class TestCliente(unittest.TestCase):
    def test_cliente_str(self):
        cliente = Cliente("Juan Perez", "12345678", "Calle Falsa 123", "001")
        self.assertEqual(str(cliente), "Juan Perez (DNI: 12345678)")

class TestTransaccion(unittest.TestCase):
    def setUp(self):
        self.cliente = Cliente("Jhon Doe", "12345634", "Calle Falsa 243", "002")
    
    def test_transaccion_aceptada(self):
        transaccion = Transaccion("123", self.cliente, "TRANSFERENCIA_ENVIADA", "aceptado", 500.0, "2024-10-10", "")
        self.assertTrue(transaccion.es_aceptada())
        self.assertFalse(transaccion.es_rechazada())
    
    def test_transaccion_rechazada(self):
        transaccion = Transaccion("124", self.cliente, "RETIRO_EFECTIVO_CAJERO_AUTOMATICO", "rechazado", 1500.0, "2024-10-11", "Fondos insuficientes")
        self.assertTrue(transaccion.es_rechazada())
        self.assertFalse(transaccion.es_aceptada())

class TestReporte(unittest.TestCase):
    def setUp(self):
        cliente1 = Cliente("Juan Perez", "12345678", "Calle Falsa 123", "001")
        cliente2 = Cliente("Jhon Doe", "12345634", "Calle Falsa 243", "002")
        self.transacciones = [
            Transaccion("123", cliente1, "TRANSFERENCIA_ENVIADA", "aceptado", 750.0, "2024-10-10", ""),
            Transaccion("124", cliente2, "RETIRO_EFECTIVO_CAJERO_AUTOMATICO", "rechazado", 1500.0, "2024-10-11", "Fondos insuficientes")
        ]
    
    def test_generar_resumen(self):
        reporte = Reporte(self.transacciones)
        resumen = reporte.generar_resumen()
        self.assertEqual(len(resumen["aceptadas"]), 1)
        self.assertEqual(len(resumen["rechazadas"]), 1)

if __name__ == "__main__":
    unittest.main()
