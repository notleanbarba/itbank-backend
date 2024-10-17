from modules.tps import Cliente, Transaccion, GeneradorHTML
import json


def procesar_transacciones(json_filepath, cliente_numero=None):
    with open(json_filepath) as file:
        data = json.load(file)

    clientes_procesados = []

    for cliente_data in data:
        cliente_data["numero"] = int(cliente_data["numero"])  
        
        if cliente_numero is not None and cliente_data["numero"] != cliente_numero:
            continue

        cliente = Cliente(
            numero=cliente_data["numero"],
            nombre=cliente_data["nombre"],
            apellido=cliente_data["apellido"],
            dni=cliente_data["DNI"],
            direccion=cliente_data["direccion"],
            tipo=cliente_data["tipo"],
            total_tarjetas_de_credito=cliente_data["totalTarjetasDeCreditoActualmente"],
            total_chequeras=cliente_data["totalChequerasActualmente"],
            saldo_en_cuenta=cliente_data.get("saldoEnCuenta", 10000), 
            saldo_en_dolares=cliente_data.get("saldoEnDolares", 0),  
            transacciones=[] 
        )

        for transaccion_data in cliente_data["transacciones"]:
            transaccion = Transaccion(
                estado=None, 
                tipo=transaccion_data["tipo"],
                cuentaNumero=transaccion_data["cuentaNumero"],
                monto=transaccion_data.get("monto", 0),
                fecha=transaccion_data["fecha"],
                numero=transaccion_data["numero"],
                saldoEnCuenta=transaccion_data["saldoEnCuenta"],
                totalTarjetasDeCreditoActualmente=cliente_data["totalTarjetasDeCreditoActualmente"],
                totalChequerasActualmente=cliente_data["totalChequerasActualmente"]
            )

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

            cliente.transacciones.append(transaccion)

        clientes_procesados.append(cliente)

    for cliente in clientes_procesados:
        GeneradorHTML.generar(cliente)


if __name__ == "__main__":
    import sys
    json_filepath = sys.argv[1]
    cliente_numero = int(sys.argv[2]) if len(sys.argv) > 2 else None
    procesar_transacciones(json_filepath, cliente_numero)
