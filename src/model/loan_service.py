"""
Servicio para manejar la lógica de préstamos con trazabilidad completa de deudas.
"""

import sys
sys.path.append("src")

class LoanService:
    """
    Servicio para calcular y gestionar préstamos con trazabilidad de deudas.
    Implementa amortización de préstamos con seguimiento de saldo restante.
    """

    @staticmethod
    def calcular_cuota_mensual(monto, tasa_interes_anual, numero_cuotas):
        """
        Calcula la cuota mensual de un préstamo usando amortización.

        Args:
            monto (float): Monto principal del préstamo
            tasa_interes_anual (float): Tasa de interés anual en porcentaje
            numero_cuotas (int): Número total de cuotas

        Returns:
            float: Cuota mensual a pagar
        """
        if numero_cuotas <= 0:
            return monto

        if numero_cuotas == 1:
            # Para una sola cuota, devolver el monto total con interés
            return monto * (1 + tasa_interes_anual / 100)

        # Fórmula de amortización: P * [r(1+r)^n] / [(1+r)^n - 1]
        # Donde:
        # P = monto principal
        # r = tasa de interés mensual
        # n = número de cuotas

        tasa_mensual = (tasa_interes_anual / 100) / 12

        cuota_mensual = monto * (tasa_mensual * (1 + tasa_mensual) ** numero_cuotas) / \
                       ((1 + tasa_mensual) ** numero_cuotas - 1)

        return cuota_mensual

    @staticmethod
    def calcular_interes_mensual(saldo_restante, tasa_interes_anual):
        """
        Calcula el interés correspondiente al mes actual.

        Args:
            saldo_restante (float): Saldo restante del préstamo
            tasa_interes_anual (float): Tasa de interés anual en porcentaje

        Returns:
            float: Interés del mes actual
        """
        tasa_mensual = (tasa_interes_anual / 100) / 12
        return saldo_restante * tasa_mensual

    @staticmethod
    def calcular_capital_mensual(cuota_mensual, interes_mensual):
        """
        Calcula el capital amortizado en el mes actual.

        Args:
            cuota_mensual (float): Cuota mensual del préstamo
            interes_mensual (float): Interés del mes actual

        Returns:
            float: Capital amortizado en el mes
        """
        return cuota_mensual - interes_mensual

    @staticmethod
    def calcular_nuevo_saldo(saldo_actual, capital_amortizado):
        """
        Calcula el nuevo saldo después de un pago.

        Args:
            saldo_actual (float): Saldo actual antes del pago
            capital_amortizado (float): Capital amortizado en este pago

        Returns:
            float: Nuevo saldo restante
        """
        nuevo_saldo = saldo_actual - capital_amortizado
        # Evitar saldos negativos por redondeo
        return max(0, nuevo_saldo)

    @staticmethod
    def determinar_estado_prestamo(saldo_restante, cuota_mensual):
        """
        Determina el estado del préstamo basado en el saldo restante.

        Args:
            saldo_restante (float): Saldo restante del préstamo
            cuota_mensual (float): Cuota mensual del préstamo

        Returns:
            str: Estado del préstamo ('ACTIVO', 'COMPLETADO', 'VENCIDO')
        """
        if saldo_restante <= 0:
            return 'COMPLETADO'
        elif saldo_restante < cuota_mensual:
            # Si el saldo restante es menor que una cuota, está en la última cuota
            return 'ACTIVO'
        else:
            return 'ACTIVO'

    @staticmethod
    def calcular_pago_mensual_actual(saldo_restante, cuota_mensual, tasa_interes_anual):
        """
        Calcula el pago mensual actual considerando el saldo restante.
        Para la última cuota, ajusta el pago para no exceder el saldo.

        Args:
            saldo_restante (float): Saldo restante del préstamo
            cuota_mensual (float): Cuota mensual regular del préstamo
            tasa_interes_anual (float): Tasa de interés anual en porcentaje

        Returns:
            dict: Diccionario con 'pago_mensual', 'interes', 'capital', 'nuevo_saldo'
        """
        if saldo_restante <= 0:
            return {
                'pago_mensual': 0,
                'interes': 0,
                'capital': 0,
                'nuevo_saldo': 0
            }

        # Calcular interés del mes actual
        interes_mensual = LoanService.calcular_interes_mensual(saldo_restante, tasa_interes_anual)

        # Determinar el pago mensual (regular o ajustado para la última cuota)
        if saldo_restante + interes_mensual <= cuota_mensual:
            # Última cuota: pagar solo lo que queda
            pago_mensual = saldo_restante + interes_mensual
        else:
            # Cuota regular
            pago_mensual = cuota_mensual

        # Calcular capital amortizado
        capital_amortizado = pago_mensual - interes_mensual

        # Calcular nuevo saldo
        nuevo_saldo = LoanService.calcular_nuevo_saldo(saldo_restante, capital_amortizado)

        return {
            'pago_mensual': pago_mensual,
            'interes': interes_mensual,
            'capital': capital_amortizado,
            'nuevo_saldo': nuevo_saldo
        }

    @staticmethod
    def generar_tabla_amortizacion(monto, tasa_interes_anual, numero_cuotas):
        """
        Genera una tabla completa de amortización del préstamo.

        Args:
            monto (float): Monto principal del préstamo
            tasa_interes_anual (float): Tasa de interés anual en porcentaje
            numero_cuotas (int): Número total de cuotas

        Returns:
            list: Lista de diccionarios con la tabla de amortización
        """
        if numero_cuotas <= 0:
            return []

        cuota_mensual = LoanService.calcular_cuota_mensual(monto, tasa_interes_anual, numero_cuotas)
        saldo_restante = monto
        tabla = []

        for cuota_num in range(1, numero_cuotas + 1):
            detalle_pago = LoanService.calcular_pago_mensual_actual(
                saldo_restante, cuota_mensual, tasa_interes_anual
            )

            tabla.append({
                'numero_cuota': cuota_num,
                'saldo_anterior': saldo_restante,
                'pago_mensual': detalle_pago['pago_mensual'],
                'interes': detalle_pago['interes'],
                'capital': detalle_pago['capital'],
                'saldo_restante': detalle_pago['nuevo_saldo']
            })

            saldo_restante = detalle_pago['nuevo_saldo']

            # Si el saldo llega a cero, terminar
            if saldo_restante <= 0:
                break

        return tabla
