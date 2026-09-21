from adaptive_balancer import (
    Nodo,
    BalanceadorRoundRobin,
    BalanceadorAdaptativo,
)


# Carga variable y reproducible para el experimento.
CARGAS = [
    10, 35, 15, 40, 20,
    30, 10, 45, 15, 25,
    35, 20, 10, 40, 30,
]


def crear_nodos():
    return [
        Nodo("Nodo-1", capacidad=100),
        Nodo("Nodo-2", capacidad=100),
        Nodo("Nodo-3", capacidad=100),
    ]


def ejecutar_experimento(nombre, clase_balanceador):
    nodos = crear_nodos()
    balanceador = clase_balanceador(nodos)

    asignadas = 0
    rechazadas = 0

    print(f"\n=== {nombre} ===")

    for numero, carga in enumerate(CARGAS, start=1):
        nodo = balanceador.seleccionar_nodo(carga)

        if nodo is None:
            rechazadas += 1
            print(f"Tarea {numero:02d} | carga={carga:>2} | RECHAZADA")
            continue

        nodo.asignar(carga)
        asignadas += 1

        print(
            f"Tarea {numero:02d} | carga={carga:>2} | "
            f"{nodo.nombre} | carga nodo={nodo.carga_actual:.0f}%"
        )

    return nodos, asignadas, rechazadas



def mostrar_resumen(nodos, asignadas, rechazadas):
    cargas = [nodo.porcentaje_carga for nodo in nodos]

    print("\n--- Resumen ---")

    for nodo in nodos:
        print(
            f"{nodo.nombre}: "
            f"{nodo.tareas_asignadas} tareas | "
            f"{nodo.porcentaje_carga:.1f}% de carga"
        )

    print(f"Tareas asignadas: {asignadas}")
    print(f"Tareas rechazadas: {rechazadas}")
    print(f"Carga máxima: {max(cargas):.1f}%")
    print(f"Carga mínima: {min(cargas):.1f}%")
    print(f"Diferencia de carga: {max(cargas) - min(cargas):.1f} puntos")



if __name__ == "__main__":
    nodos_rr, asignadas_rr, rechazadas_rr = ejecutar_experimento(
        "ROUND ROBIN",
        BalanceadorRoundRobin,
    )
    mostrar_resumen(nodos_rr, asignadas_rr, rechazadas_rr)

    nodos_ad, asignadas_ad, rechazadas_ad = ejecutar_experimento(
        "BALANCEO ADAPTATIVO",
        BalanceadorAdaptativo,
    )
    mostrar_resumen(nodos_ad, asignadas_ad, rechazadas_ad)