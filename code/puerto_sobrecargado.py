import random as rnd
import heapq
from pathlib import Path

from utils.generaciones import generar_barco, generar_arribo_barcos, generar_llevar_barco_a_muelle
from utils.generaciones import generar_llevar_barco_a_puerto, generar_tiempo_carga, generar_traslado_remolcador_solo

from utils.barcos_muelle import *


# VARIABLES GLOBALES

m = 3  # esta es la cantidad de muelles (en el ejercicio nos dicen que son 3)
# lista SS = muelles + barcos_en_espera
barcos_en_espera = []
muelles = crear_muelles(m)
remolcador = Remolcador()
eventos = []

tiempo = 0  # tiempo en que se desarrolla la simulacion
barcos_atendidos = []


# EVENTOS

def arribo_barco(T):
    global tiempo
    global eventos

    T_t_ap = generar_arribo_barcos()
    t_ap = tiempo + T_t_ap

    if t_ap < T:  # agrego al heap un nuevo arribo
        barco = Barco()
        barco.set_tipo_barco(generar_barco())
        barco.set_tiempo_llegada_al_puerto(t_ap)
        heapq.heappush(
            eventos, (t_ap, ("ArriboBarco", barco, None)))

    barcoM = Barco()
    barcoM.set_tipo_barco(generar_barco())
    pos_muelle_libre = muelle_libre(muelles)

    if pos_muelle_libre == -1:
        barcos_en_espera.append(barcoM)

    else:
        heapq.heappush(
            eventos, (tiempo, ("LlevarAlMuelle", barcoM, pos_muelle_libre)))


def llevar_barco_al_muelle(barco, muelle_pos):
    global remolcador
    global tiempo
    global eventos

    if remolcador.get_lugar() == "muelle":
        t_rs = generar_traslado_remolcador_solo()
        tiempo = tiempo + t_rs

    # llevar barco al muelle

    t_bm = generar_llevar_barco_a_muelle()
    tiempo += t_bm

    t_cb = generar_tiempo_carga(barco.get_tipo_barco())
    t_lsm = tiempo + t_cb
    barco.set_tiempo_listo_para_salir_del_muelle(t_lsm)
    muelles[muelle_pos].set_barco(barco)
    heapq.heappush(
        eventos, (t_lsm, ("SalirDelMuelle", barco, muelle_pos)))
    remolcador.set_lugar("muelle")


def sacar_barco_del_muelle(barco, muelle_pos):
    global remolcador
    global tiempo

    if remolcador.get_lugar() == "puerto":
        t_rs = generar_traslado_remolcador_solo()
        tiempo += t_rs

    # sacar barco del muelle
    t_bp = generar_llevar_barco_a_puerto()
    tiempo += t_bp
    t_sp = tiempo

    barco.set_tiempo_salida_del_puerto(t_sp)

    # guardo cada barco con su tiempo de entrada y salida
    barcos_atendidos.append(barco)

    muelles[muelle_pos].set_barco(None)
    remolcador.set_lugar("puerto")

    if len(barcos_en_espera) > 0:
        barco = barcos_en_espera.pop()
        # llevar barco al muelle
        llevar_barco_al_muelle(barco, muelle_pos)


# SIMULACION

def simulacion(T):
    # Inicializacion

    global tiempo
    global eventos

    # generar el primer arribo

    T_0 = generar_arribo_barcos()
    t_ap = T_0
    tiempo = t_ap

    barco = Barco()
    barco.set_tipo_barco(generar_barco())
    barco.set_tiempo_llegada_al_puerto(t_ap)
    heapq.heappush(eventos, (tiempo, ("ArriboBarco", barco, None)))

    while len(eventos) > 0:
        evento = heapq.heappop(eventos)
        # esto es xq puede haber un barco q llego con un tiempo de arribo (que se usa para saber el orden en el heap) y ya haber avanzado el tiempo y ponemos el maximo para el inicio
        tiempo = max(evento[0], tiempo)

        if evento[1][0] == "ArriboBarco":
            arribo_barco(T)

        elif evento[1][0] == "LlevarAlMuelle":
            barco = evento[1][1]
            muelle_pos = evento[1][2]
            llevar_barco_al_muelle(barco, muelle_pos)

        elif evento[1][0] == "SalirDelMuelle":
            barco = evento[1][1]
            muelle_pos = evento[1][2]
            sacar_barco_del_muelle(barco, muelle_pos)

        else:
            print("Este evento no es aceptado")


def main_simulacion(corrida):
    suma = 0
    for barco in barcos_atendidos:
        suma += (barco.get_tiempo_salida_del_puerto() -
                 barco.get_tiempo_llegada_al_puerto())

    with open(Path.cwd() / 'salida.txt', mode="a") as file:
        file.write("Corrida " + f'{corrida}'+'\n')
        file.write("barcos atendidos: " + f'{len(barcos_atendidos)}'+'\n')
        file.write("promedio de demora de un barco " +
                   f'{suma/len(barcos_atendidos)}'+'\n')
        file.write(
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ "+'\n')
        file.close()

    print("Corrida ", corrida)
    print("barcos atendidos: ", len(barcos_atendidos))
    print("promedio de demora de un barco", suma/len(barcos_atendidos))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" + "\n")
    return suma/len(barcos_atendidos)


# MAIN

def puerto_sobrecargado(horas, corridas):
    global barcos_en_espera
    global m
    global muelles
    global remolcador
    global eventos
    global tiempo
    global barcos_atendidos

    with open(Path.cwd() / 'salida.txt', mode="a") as file:
        file.write(
            "################################################################################################" + "\n")
        file.close()
    ac = 0
    for corrida in range(1, corridas+1):

        m = 3
        barcos_en_espera = []
        muelles = crear_muelles(m)
        remolcador = Remolcador()
        eventos = []

        tiempo = 0
        barcos_atendidos = []

        simulacion(horas)
        ac += main_simulacion(corrida)

    with open(Path.cwd() / 'salida.txt', mode="a") as file:
        file.write("Promedio del promedio de demora de un barco en " + f'{horas} horas y ' +
                   f'{corridas} corridas: ' + f'{ac/corridas}'+"\n")
        file.write("\n")
        file.write("\n")
        file.close()

    print("Promedio del promedio de demora de un barco en " + f'{horas} horas y ' +
          f'{corridas}' + " corridas: ", ac/corridas)


puerto_sobrecargado(24, 50)
