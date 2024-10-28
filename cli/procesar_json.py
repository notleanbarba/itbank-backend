from modules.tps import ClienteClassic, ClienteGold, ClienteBlack, Transaccion, GeneradorHTML
import json
import sys


def procesar_transacciones(json_filepath, cliente_numero=None):
    with open(json_filepath) as file:
        data = json.load(file)

    clientes_procesados = []

    for cliente_data in data:
        cliente_data["numero"] = int(cliente_data["numero"])  
        
        if cliente_numero is not None and cliente_data["numero"] != cliente_numero:
            continue

        tipo_cliente = cliente_data["tipo"].upper()
        if tipo_cliente == "CLASSIC":
            cliente = ClienteClassic(
                cliente_data["numero"],
                cliente_data["nombre"],
                cliente_data["apellido"],
                cliente_data["DNI"],
                cliente_data["direccion"],
                cliente_data["totalTarjetasDeCreditoActualmente"],
                cliente_data["totalChequerasActualmente"],
                cliente_data.get("saldoEnCuenta", 10000), 
                cliente_data.get("saldoEnDolares", 0),  
                []
            )
        elif tipo_cliente == "GOLD":
            cliente = ClienteGold(
                cliente_data["numero"],
                cliente_data["nombre"],
                cliente_data["apellido"],
                cliente_data["DNI"],
                cliente_data["direccion"],
                cliente_data["totalTarjetasDeCreditoActualmente"],
                cliente_data["totalChequerasActualmente"],
                cliente_data.get("saldoEnCuenta", 10000), 
                cliente_data.get("saldoEnDolares", 0),  
                []
            )
        elif tipo_cliente == "BLACK":
            cliente = ClienteBlack(
                cliente_data["numero"],
                cliente_data["nombre"],
                cliente_data["apellido"],
                cliente_data["DNI"],
                cliente_data["direccion"],
                cliente_data["totalTarjetasDeCreditoActualmente"],
                cliente_data["totalChequerasActualmente"],
                cliente_data.get("saldoEnCuenta", 10000), 
                cliente_data.get("saldoEnDolares", 0),  
                []
            )
        else:
            print(f"Tipo de cliente desconocido: {tipo_cliente}")
            continue

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

            cliente.transacciones.append(transaccion)

        clientes_procesados.append(cliente)

    for cliente in clientes_procesados:
        GeneradorHTML.generar(cliente)


if __name__ == "__main__":
    json_filepath = sys.argv[1]
    cliente_numero = int(sys.argv[2]) if len(sys.argv) > 2 else None
    procesar_transacciones(json_filepath, cliente_numero)
