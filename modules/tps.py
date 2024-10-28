import os

class ClienteBase:
    def __init__(self, numero, nombre, apellido, dni, direccion, total_tarjetas_de_credito, total_chequeras, saldo_en_cuenta, saldo_en_dolares, transacciones):
        self.numero = numero
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.direccion = direccion
        self.total_tarjetas_de_credito = total_tarjetas_de_credito
        self.total_chequeras = total_chequeras
        self.saldo_en_cuenta = saldo_en_cuenta
        self.saldo_en_dolares = saldo_en_dolares
        self.transacciones = transacciones

    def mostrar_informacion(self):
        """Método para mostrar información básica del cliente"""
        return f"Cliente {self.nombre} {self.apellido} - Tipo: {self.__class__.__name__}"

class ClienteClassic(ClienteBase):
    def limite_retiro(self):
        return 10000
    
    def max_tarjetas_credito(self):
        return 0
    
    def max_chequeras(self):
        return 0

class ClienteGold(ClienteBase):
    def limite_retiro(self):
        return 20000
    
    def max_tarjetas_credito(self):
        return 1
    
    def max_chequeras(self):
        return 1

class ClienteBlack(ClienteBase):
    def limite_retiro(self):
        return 100000
    
    def max_tarjetas_credito(self):
        return 5
    
    def max_chequeras(self):
        return 2

class Transaccion:
    def __init__(self, estado, tipo, cuentaNumero, monto, fecha, numero, saldoEnCuenta, totalTarjetasDeCreditoActualmente, totalChequerasActualmente, razon_rechazo=""):
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

    def aplicar_chequeos(self, cliente):
        if self.tipo == "RETIRO_EFECTIVO_CAJERO_AUTOMATICO":
            return self.chequeo_retiro(cliente)
        elif self.tipo == "ALTA_TARJETA_CREDITO":
            return self.chequeo_alta_tarjeta(cliente)
        elif self.tipo == "ALTA_CHEQUERA":
            return self.chequeo_alta_chequera(cliente)
        elif self.tipo == "COMPRAR_DOLAR":
            return self.chequeo_comprar_dolar(cliente)
        elif self.tipo == "TRANSFERENCIA_ENVIADA":
            return self.chequeo_transferencia_enviada(cliente)
        elif self.tipo == "TRANSFERENCIA_RECIBIDA":
            return self.chequeo_transferencia_recibida(cliente)
        return "DESCONOCIDO", "Tipo de transacción no reconocido."

    def chequeo_retiro(self, cliente):
        if self.monto > cliente.limite_retiro():
            return "RECHAZADA", f"Monto máximo para {cliente.__class__.__name__} superado."
        return "ACEPTADA", ""

    def chequeo_alta_tarjeta(self, cliente):
        if cliente.total_tarjetas_de_credito >= cliente.max_tarjetas_credito():
            return "RECHAZADA", f"Máximo de tarjetas de crédito alcanzado para {cliente.__class__.__name__}."
        return "ACEPTADA", ""
    
    def chequeo_alta_chequera(self, cliente):
        if cliente.total_chequeras >= cliente.max_chequeras():
            return "RECHAZADA", f"Máximo de chequeras alcanzado para {cliente.__class__.__name__}."
        return "ACEPTADA", ""
    
    def chequeo_comprar_dolar(self, cliente):
        if cliente.saldo_en_cuenta < self.monto:
            return "RECHAZADA", "Saldo en cuenta insuficiente para comprar dólares."
        return "ACEPTADA", ""

    def chequeo_transferencia_enviada(self, cliente):
        comision = 0.01 if isinstance(cliente, ClienteClassic) else 0.005
        if cliente.saldo_en_cuenta < (self.monto + (self.monto * comision)):
            return "RECHAZADA", "Saldo insuficiente para la transferencia."
        return "ACEPTADA", ""

    def chequeo_transferencia_recibida(self, cliente):
        return "ACEPTADA", ""

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
                    <p><strong>Tipo de Cliente:</strong> {cliente.__class__.__name__}</p>
                    <p><strong>Saldo en Cuenta:</strong> ${cliente.saldo_en_cuenta:.2f}</p>
                    <p><strong>Saldo en Dólares:</strong> ${cliente.saldo_en_dolares:.2f}</p>
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
