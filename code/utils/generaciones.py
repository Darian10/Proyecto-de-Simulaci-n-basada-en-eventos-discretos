import random as rnd
import math

# Generacion de variables aleatorias


def exponential(_lambda):
    U = rnd.random()
    return -(1/_lambda)*math.log(U)


def normal(miu, o_2):
    while True:
        Y = exponential(1)
        U = rnd.random()
        if U <= math.exp((-1/2)*(Y-1)**2):
            break

    U = rnd.random()
    Z = Y if U < 0.5 else -Y

    # Z = (X - miu)/o ~ N(0,1) => X = Zo + miu ~ N(miu,o^2)
    return Z*math.sqrt(o_2) + miu


# metodos de generacion usando las variables aleatorias y los datos del problema

def generar_barco():  # genera los barcos de acuerdo a las probabilidades que daban en los datos

    r = rnd.random()
    if r <= 0.25:
        return 0
    if r <= 0.5:
        return 1
    return 2


# genera el tiempo de carga de acuerdo a los tamannos de los barcos (pequenno = 0, mediano = 1, grande = 2)
# t_cb
def generar_tiempo_carga(tipo_barco):

    if tipo_barco == 0:
        return normal(9, 1)

    if tipo_barco == 1:
        return normal(12, 2)

    return normal(18, 3)

# t_ap


def generar_arribo_barcos():
    return exponential(8)

# t_rs


def generar_traslado_remolcador_solo():
    return exponential(0.25)

# t_bm


def generar_llevar_barco_a_muelle():
    return exponential(2)

# t_bp


def generar_llevar_barco_a_puerto():
    return exponential(1)
