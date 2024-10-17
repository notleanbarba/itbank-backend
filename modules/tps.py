import os

class Cliente:
    def __init__(self,numero, nombre, apellido, dni,direccion, tipo, total_tarjetas_de_credito, total_chequeras, saldo_en_cuenta, saldo_en_dolares, transacciones):
        self.numero = numero
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.direccion = direccion
        self.tipo = tipo
        self.total_tarjetas_de_credito = total_tarjetas_de_credito
        self.total_chequeras = total_chequeras
        self.saldo_en_cuenta = saldo_en_cuenta
        self.saldo_en_dolares = saldo_en_dolares
        self.transacciones = transacciones

class Transaccion:
    def __init__(self, estado, tipo, cuentaNumero, monto, fecha, numero, saldoEnCuenta, totalTarjetasDeCreditoActualmente, totalChequerasActualmente,razon_rechazo=""):
        self.estado = estado
        self.tipo = tipo
        self.cuentaNumero = cuentaNumero
        self.monto = monto
        self.fecha = fecha
        self.numero = numero
        self.saldoEnCuenta = saldoEnCuenta
        self.total_tarjetas_de_credito = totalTarjetasDeCreditoActualmente
        self.total_chequeras = totalChequerasActualmente
        self.razon_rechazo = razon_rechazo

    def chequeo_retiro(self, cliente):
        if cliente.tipo == "CLASSIC" and self.monto > 10000:
            return "RECHAZADA", "Monto máximo para Classic superado."
        elif cliente.tipo == "GOLD" and self.monto > 20000:
            return "RECHAZADA", "Monto máximo para Gold superado."
        elif cliente.tipo == "BLACK" and self.monto > 100000:
            return "RECHAZADA", "Monto máximo para Black superado."
        return "ACEPTADA", ""

    def chequeo_alta_tarjeta(self, cliente):
        # Chequeo de cantidad máxima de tarjetas de crédito
        if cliente.tipo == "CLASSIC":
            return "RECHAZADA", "Clientes Classic no pueden tener tarjetas de crédito."
        elif cliente.tipo == "GOLD":
            if cliente.total_tarjetas_de_credito >= 1:
                return "RECHAZADA", "Máximo de tarjetas de crédito alcanzado para Gold."
        elif cliente.tipo == "BLACK":
            if cliente.total_tarjetas_de_credito >= 5:
                return "RECHAZADA", "Máximo de tarjetas de crédito alcanzado para Black."
        return "ACEPTADA", ""
    
    def chequeo_alta_chequera(self, cliente):
        # Verify 
        if cliente.tipo == "CLASSIC":
            return "RECHAZADA", "Clientes Classic no pueden tener chequeras."
        elif cliente.tipo == "GOLD":
            if cliente.total_chequeras >= 1:
                return "RECHAZADA", "Máximo de chequeras alcanzado para Gold."
        elif cliente.tipo == "BLACK":
            if cliente.total_chequeras >= 2:
                return "RECHAZADA", "Máximo de chequeras alcanzado para Black."
        return "ACEPTADA", ""
    
    def chequeo_comprar_dolar(self, cliente):
        if cliente.saldo_en_cuenta < self.monto:
            return "RECHAZADA", "Saldo en cuenta insuficiente para comprar dólares."
        return "ACEPTADA", ""

    
    def chequeo_transferencia_enviada(self, cliente):
        comision = 0
        if cliente.tipo == "CLASSIC":
            comision = 0.01  # 1%
        elif cliente.tipo == "GOLD":
            comision = 0.005  # 0.5%
        if cliente.saldo_en_cuenta < (self.monto + (self.monto * comision)):
            return "RECHAZADA", "Saldo insuficiente para la transferencia."
        return "ACEPTADA", ""

    def chequeo_transferencia_recibida(self, cliente):
        return "ACEPTADA", ""

    def obtener_razon_rechazo(self, cliente):
        return self.razon_rechazo

class GeneradorHTML:
    @staticmethod
    def generar(cliente):
            
        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reporte de Transacciones - {cliente.nombre} {cliente.apellido}</title>
            <style>
                body {{
                    font-family: 'Roboto', Arial, sans-serif;
                    background-color: #f8f9fa;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }}
                h1, h2 {{
                    color: #2c3e50;
                    text-align: center;
                    font-weight: 700;
                }}
                .navbar {{
                    background-color: #1a73e8;
                    color: white;
                    text-align: center;
                    padding: 20px;
                    font-size: 20px;
                    font-weight: bold;
                }}
                .container {{
                    width: 85%;
                    margin: 50px auto;
                    background-color: #fff;
                    padding: 40px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                    border-radius: 8px;
                }}
                .client-info {{
                    margin-bottom: 30px;
                    padding: 10px;
                    background-color: #f1f3f4;
                    border-radius: 8px;
                    line-height: 1.8;
                    font-size: 15px;
                }}
                .client-info strong {{
                    color: #1a73e8;
                }}
                .transaction-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 30px 0;
                    font-size: 15px;
                }}
                .transaction-table th {{
                    background-color: #1a73e8;
                    color: white;
                    padding: 15px 10px;
                    text-align: left;
                    font-weight: bold;
                }}
                .transaction-table td {{
                    padding: 15px 10px;
                    border-bottom: 1px solid #ddd;
                }}
                .transaction-table tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                .transaction-table tr:hover {{
                    background-color: #f1f3f4;
                }}
                .summary {{
                    text-align: center;
                    margin-top: 40px;
                    color: #2c3e50;
                    font-size: 16px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    font-size: 14px;
                    color: #777;
                }}
                .footer-logo {{
                    margin-top: 20px;
                    font-weight: bold;
                    color: #1a73e8;
                }}
            </style>
        </head>
        <body>
            <div class="navbar">
                BANCO: ARGENTARIUS by DevFive - Reporte de Transacciones
            </div>

            <div class="container">
                <h1>Reporte de Transacciones</h1>

                <div class="client-info">
                    <p><strong>Nombre:</strong> {cliente.nombre} {cliente.apellido}</p>
                    <p><strong>Número de Cuenta:</strong> {cliente.numero}</p>
                    <p><strong>DNI:</strong> {cliente.dni}</p>
                    <p><strong>Dirección:</strong> {cliente.direccion}</p>
                    <p><strong>Tipo de Cliente:</strong> {cliente.tipo}</p>
                    <p><strong>Saldo en Cuenta:</strong> ${cliente.saldo_en_cuenta:.2f}</p>
                    <p><strong>Saldo en Dólares:</strong> ${cliente.saldo_en_dolares}</p>
                </div>

                <h2>Detalle de Transacciones</h2>
                <table class="transaction-table">
                    <tr>
                        <th>Tipo</th>
                        <th>Fecha</th>
                        <th>Monto</th>
                        <th>Estado</th>
                        <th>Razón de Rechazo</th>
                    </tr>
        """

        for transaccion in cliente.transacciones:
            if transaccion.tipo == "RETIRO_EFECTIVO_CAJERO_AUTOMATICO":
                estado, razon = transaccion.chequeo_retiro(cliente)
            elif transaccion.tipo == "ALTA_TARJETA_CREDITO":
                estado, razon = transaccion.chequeo_alta_tarjeta(cliente)
            elif transaccion.tipo == "ALTA_CHEQUERA":
                estado, razon = transaccion.chequeo_alta_chequera(cliente)
            elif transaccion.tipo == "COMPRAR_DOLAR":
                estado, razon = transaccion.chequeo_comprar_dolar(cliente)
            elif transaccion.tipo == "TRANSFERENCIA_ENVIADA":
                estado, razon = transaccion.chequeo_transferencia_enviada(cliente)
            elif transaccion.tipo == "TRANSFERENCIA_RECIBIDA":
                estado, razon = transaccion.chequeo_transferencia_recibida(cliente)
            else:
                estado, razon = "DESCONOCIDO", "Tipo de transacción no reconocido"

            transaccion.estado = estado
            transaccion.razon_rechazo = razon if estado == "RECHAZADA" else ""

            estado_clase = "approved" if transaccion.estado == "ACEPTADA" else "rejected"
            razon_rechazo = transaccion.razon_rechazo if transaccion.estado == "RECHAZADA" else "N/A"

            html += f"""
            <tr>
                <td>{transaccion.tipo}</td>
                <td>{transaccion.fecha}</td>
                <td>${transaccion.monto:.2f}</td>
                <td class="{estado_clase}">{transaccion.estado}</td>
                <td>{razon_rechazo}</td>
            </tr>
            """

        html += """
                </table>

                <div class="footer">
                    <p>Reporte generado automáticamente por el sistema de transacciones del BANCO: ARGENTARIUS</p>
                    <div class="footer-logo">BANCO: ARGENTARIUS</div>
                </div>
            </div>
        </body>
        </html>
        """
        if not os.path.exists('Reportes'):
            os.makedirs('Reportes')
        with open(f'Reportes/reporte_transacciones_cliente_{cliente.numero}.html', 'w', encoding='utf-8') as file:
            file.write(html)
