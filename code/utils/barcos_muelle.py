# Clases de los barcos


class Barco:
    def __init__(self):
        self.tipoBarco = 0
        self.tiempo_llegada_al_puerto = 0
        self.tiempo_listo_para_salir_del_muelle = 0
        self.tiempo_salida_del_puerto = 0

    def set_tiempo_llegada_al_puerto(self, tiempo):
        self.tiempo_llegada_al_puerto = tiempo

    def set_tiempo_listo_para_salir_del_muelle(self, tiempo):
        self.tiempo_listo_para_salir_del_muelle = tiempo

    def set_tiempo_salida_del_puerto(self, tiempo):
        self.tiempo_salida_del_puerto = tiempo

    def set_tipo_barco(self, tipoBarco):
        self.tipoBarco = tipoBarco

    def get_tiempo_llegada_al_puerto(self):
        return self.tiempo_llegada_al_puerto

    def get_tiempo_listo_para_salir_del_muelle(self):
        return self.tiempo_listo_para_salir_del_muelle

    def get_tiempo_salida_del_puerto(self):
        return self.tiempo_salida_del_puerto

    def get_tipo_barco(self):
        return self.tipoBarco


class Remolcador:
    def __init__(self):
        self.lugar = "puerto"

    def set_lugar(self, lugar):
        self.lugar = lugar

    def get_lugar(self):
        return self.lugar


class Muelle:
    def __init__(self):
        self.barco = None

    def set_barco(self, barco):
        self.barco = barco

    def get_barco(self):
        return self.barco


def crear_muelles(m):
    muelles = []
    for _ in range(0, m):
        muelle = Muelle()
        muelles.append(muelle)

    return muelles


def muelle_libre(muelles):  # da algun muelle si esta libre

    for i in range(len(muelles)):
        m = muelles[i]
        if m.get_barco() == None:
            return i
    return -1
