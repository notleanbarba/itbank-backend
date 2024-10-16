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
    def __init__(self, estado, tipo, cuentaNumero, monto, fecha, numero, saldoEnCuenta, totalTarjetasDeCreditoActualmente, totalChequerasActualmente):
        self.estado = estado
        self.tipo = tipo
        self.cuentaNumero = cuentaNumero
        self.monto = monto
        self.fecha = fecha
        self.numero = numero
        self.saldoEnCuenta = saldoEnCuenta
        self.total_tarjetas_de_credito = totalTarjetasDeCreditoActualmente
        self.total_chequeras = totalChequerasActualmente

    def chequeo_retiro(self, cliente):
        # Chequeo de monto máximo para retiros
        if cliente.tipo == "CLASSIC":
            if self.monto > 10000:
                return "RECHAZADA", "Monto máximo para Classic superado."
        elif cliente.tipo == "GOLD":
            if self.monto > 20000:
                return "RECHAZADA", "Monto máximo para Gold superado."
        elif cliente.tipo == "BLACK":
            if self.monto > 100000:
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
        if cliente.saldo_en_dolares <= 0:
            return "RECHAZADA", "Saldo en dólares insuficiente."
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
        if self.estado == "RECHAZADA":
            if self.tipo == "ALTA_CHEQUERA":
                estado, razon = self.chequeo_alta_chequera(cliente)
                return razon
            if self.tipo == "ALTA_TARJETA_CREDITO":
                estado, razon = self.chequeo_alta_tarjeta(cliente)
                return razon
            if self.tipo == "RETIRO_EFECTIVO_CAJERO_AUTOMATICO":
                estado, razon = self.chequeo_retiro(cliente)
                return razon
            if self.tipo == "COMPRAR_DOLAR":
                estado, razon = self.chequeo_comprar_dolar(cliente)
                return razon
            if self.tipo == "TRANSFERENCIA_ENVIADA":
                estado, razon = self.chequeo_transferencia_enviada(cliente)
                return razon
        return ""

class GeneradorHTML:
    @staticmethod
    def generar(cliente):
        html = f"<h1>Reporte de Transacciones</h1> <span>Nombre: {cliente.nombre} {cliente.apellido} | Numero: {cliente.numero} | DNI: {cliente.dni} | Direccion:{cliente.direccion} | Tipo: {cliente.tipo}</span>"
        for transaccion in cliente.transacciones:
            html += f"<p>Transacción: {transaccion.tipo} - Fecha: {transaccion.fecha} - Estado: {transaccion.estado}</p>"
            if transaccion.estado == "RECHAZADA":
                razon_rechazo = transaccion.obtener_razon_rechazo(cliente)
                html += f"<p>Razón de rechazo: {razon_rechazo}</p>"
        with open('Reportes/reporte_transacciones.html', 'w', encoding='utf-8') as file:
            file.write(html)
