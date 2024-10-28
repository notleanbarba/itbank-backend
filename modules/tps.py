import json

class Cliente:
    def __init__(self, nombre, dni, direccion, numero_cliente):
        self.nombre = nombre
        self.dni = dni
        self.direccion = direccion
        self.numero_cliente = numero_cliente
    
    def __str__(self):
        return f"{self.nombre} (DNI: {self.dni})"

class Transaccion:
    def __init__(self,numero,cliente,tipo_operacion,estado,monto,fecha,razon_rechazo):
        self.numero = numero
        self.cliente = cliente
        self.tipo_operacion = tipo_operacion
        self.estado = estado
        self.monto = monto 
        self.fecha = fecha 
        self.razon_rechazo = razon_rechazo
    
    def es_aceptada(self):
        return self.estado == "aceptado"
    
    def es_rechazada(self):
        return self.estado == "rechazado"
    
class Reporte:
    def __init__(self,transacciones):
        self.transacciones = transacciones
    
    def generar_resumen(self):
        aceptadas = [t for t in self.transacciones if t.es_aceptada()]
        rechazadas = [t for t in self.transacciones if t.es_rechazada()]
        return {"aceptadas": aceptadas, "rechazadas": rechazadas}
    
    def get_transacciones_por_cliente(self,dni):
        return [t for t in self.transacciones if t.cliente.dni == dni]

class GeneradorHTML:
    def __init__(self, reporte):
        self.reporte = reporte
    
    def generar_html(self,archivo_salida):
        resumen = self.reporte.generar_resumen()
        
        html_content = "<html><head><Title>Reporte de Transacciones</title></head><body>"
        html_content += "<h1>Reporte de transacciones del TPS</h1>"
        
        html_content += "<h2>Transacciones aceptadas</h2>"
        for t in resumen["aceptadas"]:
            html_content += f"<p>{t.fecha}: {t.tipo_operacion} - Monto: {t.monto}</p>"
            
        html_content += "<h2> Transacciones Rechazadas</h2>"
        for t in resumen["rechazadas"]:
            html_content += f"<p>{t.fecha}: {t.tipo_operacion} - Monto: {t.monto} - Razón: {t.razon_rechazo}</p>"
        
        html_content += "</body></html>"
        
        with open(archivo_salida, "w", encoding="utf-8") as file:
            file.write(html_content)