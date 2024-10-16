from modules.tps import Cliente, Transaccion, GeneradorHTML

def procesar_transacciones(json_filepath):
    import json
    
    with open(json_filepath) as file:
        data = json.load(file)
    
    # Crear cliente
    cliente = Cliente(
        nombre=data["nombre"],
        apellido=data["apellido"],
        dni=data["DNI"],
        tipo=data["tipo"],
        total_tarjetas_de_credito=data["totalTarjetasDeCreditoActualmente"],
        total_chequeras=data["totalChequerasActualmente"],
        saldo_en_cuenta=10000,  # Asignar saldo inicial en pesos
        saldo_en_dolares=0,  # Inicializar saldo en dólares
        transacciones=[]  # Inicializar lista de transacciones
    )

    # Procesar transacciones
    for transaccion_data in data["transacciones"]:
        transaccion = Transaccion(
            estado=None,  # El estado se determinará a través de los cheques
            tipo=transaccion_data["tipo"],
            cuentaNumero=transaccion_data["cuentaNumero"],
            monto=transaccion_data.get("monto", 0),
            fecha=transaccion_data["fecha"],
            numero=transaccion_data["numero"],
            saldoEnCuenta=transaccion_data["saldoEnCuenta"],
            totalTarjetasDeCreditoActualmente=data["totalTarjetasDeCreditoActualmente"],
            totalChequerasActualmente=data["totalChequerasActualmente"]
        )
        
        # Realizar chequeo de la transacción
        if transaccion.tipo == "RETIRO_EFECTIVO_CAJERO_AUTOMATICO":
            transaccion.estado = transaccion.chequeo_retiro(cliente)
        elif transaccion.tipo == "ALTA_TARJETA_CREDITO":
            transaccion.estado = transaccion.chequeo_alta_tarjeta(cliente)
        elif transaccion.tipo == "ALTA_CHEQUERA":
            transaccion.estado = transaccion.chequeo_alta_chequera(cliente)
        elif transaccion.tipo == "COMPRAR_DOLAR":
            transaccion.estado = transaccion.chequeo_comprar_dolar(cliente)
        elif transaccion.tipo == "TRANSFERENCIA_ENVIADA":
            transaccion.estado = transaccion.chequeo_transferencia_enviada(cliente)
        elif transaccion.tipo == "TRANSFERENCIA_RECIBIDA":
            transaccion.estado = transaccion.chequeo_transferencia_recibida(cliente)

        # Agregar transacción al cliente
        cliente.transacciones.append(transaccion)

    # Generar el HTML con el reporte de transacciones
    GeneradorHTML.generar(cliente)

if __name__ == "__main__":
    import sys
    json_filepath = sys.argv[1]
    procesar_transacciones(json_filepath)
