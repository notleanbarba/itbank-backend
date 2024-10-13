import sys 
import json
from modules.tps import Cliente, Transaccion, Reporte, GeneradorHTML

def procesar_transacciones(filepath):
    try:
        with open(filepath,'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print("Error: File dont have a valid JSON format.")
        return

    transacciones = []
    for trans in data.get("transacciones",[]):
        cliente_data = trans["cliente"]
        cliente = Cliente(
            cliente_data["nombre"],
            cliente_data["dni"],
            cliente_data["direccion"],
            cliente_data.get("numero_cliente", "N/A")
        )
        
        transaccion = Transaccion(
            trans["numero"],
            cliente,
            trans["tipo_operacion"],
            trans["estado"],
            trans["monto"],
            trans["fecha"],
            trans["razon_rechazo"]
        )
        
        transacciones.append(transaccion)
    
    return transacciones

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python procesar_tps.py <archivo_json>")
        sys.exit(1)
    
    json_filepath = sys.argv[1]
    
    transacciones = procesar_transacciones(json_filepath)
    if not transacciones:
        print("Transaction cannot be processed.")
        sys.exit(1)
    
    reporte = Reporte(transacciones)
    
    generador_html = GeneradorHTML(reporte)
    generador_html.generar_html("reporte_transacciones.html")
    
    print(f"{len(transacciones)} transaction have been processed. Report created successfully.")