from adaptive_balancer import (
    Nodo,
    BalanceadorRoundRobin,
    BalanceadorAdaptativo,
)


ESCENARIOS = {
    "Moderado": [
        (10, 2), (15, 2), (20, 3), (10, 2), (25, 3),
        (15, 2), (20, 3), (10, 2), (25, 2), (15, 3),
        (20, 2), (10, 2), (25, 3), (15, 2), (20, 3),
    ],

    "Alto": [
        (25, 4), (40, 5), (30, 4), (45, 5), (35, 4),
        (50, 5), (30, 3), (45, 4), (40, 5), (35, 4),
        (50, 5), (30, 4), (45, 5), (40, 4), (35, 5),
    ],

    "Pico": [
        (45, 6), (55, 6), (50, 5), (60, 6), (45, 5),
        (55, 6), (50, 5), (60, 6), (45, 5), (55, 6),
        (50, 5), (60, 6), (45, 5), (55, 6), (50, 5),
    ],
}


def crear_nodos():
    return [
        Nodo("Nodo-1", capacidad=100),
        Nodo("Nodo-2", capacidad=100),
        Nodo("Nodo-3", capacidad=100),
    ]


def simular(tareas, clase_balanceador):
    nodos = crear_nodos()
    balanceador = clase_balanceador(nodos)

    tareas_activas = []
    historial_cargas = []
    asignadas = 0
    rechazadas = 0

    for ciclo, (carga, duracion) in enumerate(tareas, start=1):
        finalizadas = [
            tarea for tarea in tareas_activas
            if tarea["fin"] <= ciclo
        ]

        for tarea in finalizadas:
            tarea["nodo"].liberar(tarea["carga"])
            tareas_activas.remove(tarea)

        nodo = balanceador.seleccionar_nodo(carga)

        if nodo is None:
            rechazadas += 1
        else:
            nodo.asignar(carga)
            asignadas += 1

            tareas_activas.append(
                {
                    "nodo": nodo,
                    "carga": carga,
                    "fin": ciclo + duracion,
                }
            )

        # Registramos todos los ciclos, incluso si una tarea fue rechazada.
        historial_cargas.append(
            [n.porcentaje_carga for n in nodos]
        )

    return {
        "asignadas": asignadas,
        "rechazadas": rechazadas,
        "historial": historial_cargas,
    }



def calcular_metricas(resultado):
    historial = resultado["historial"]

    desequilibrios = [
        max(cargas) - min(cargas)
        for cargas in historial
    ]

    cargas_maximas = [
        max(cargas)
        for cargas in historial
    ]

    total = resultado["asignadas"] + resultado["rechazadas"]

    return {
        "asignadas": resultado["asignadas"],
        "rechazadas": resultado["rechazadas"],
        "tasa_rechazo": (
            resultado["rechazadas"] / total * 100
            if total > 0 else 0
        ),
        "desequilibrio_promedio": (
            sum(desequilibrios) / len(desequilibrios)
        ),
        "desequilibrio_maximo": max(desequilibrios),
        "carga_maxima": max(cargas_maximas),
    }



def ejecutar_comparacion():
    estrategias = {
        "Round Robin": BalanceadorRoundRobin,
        "Adaptativo": BalanceadorAdaptativo,
    }

    for nombre_escenario, tareas in ESCENARIOS.items():
        print(f"\n{'=' * 60}")
        print(f"ESCENARIO: {nombre_escenario}")
        print(f"{'=' * 60}")

        for nombre_estrategia, clase_balanceador in estrategias.items():
            resultado = simular(tareas, clase_balanceador)
            metricas = calcular_metricas(resultado)

            print(f"\n{nombre_estrategia}")
            print(f"  Tareas asignadas:       {metricas['asignadas']}")
            print(f"  Tareas rechazadas:      {metricas['rechazadas']}")
            print(f"  Tasa de rechazo:        {metricas['tasa_rechazo']:.2f}%")
            print(
                f"  Desequilibrio promedio: "
                f"{metricas['desequilibrio_promedio']:.2f} puntos"
            )
            print(
                f"  Desequilibrio máximo:   "
                f"{metricas['desequilibrio_maximo']:.2f} puntos"
            )
            print(
                f"  Carga máxima observada: "
                f"{metricas['carga_maxima']:.2f}%"
            )


if __name__ == "__main__":
    ejecutar_comparacion()