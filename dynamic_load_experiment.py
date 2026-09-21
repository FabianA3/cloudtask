from adaptive_balancer import (
    Nodo,
    BalanceadorRoundRobin,
    BalanceadorAdaptativo,
)


# Cada elemento representa: (carga, duración en ciclos).
# La secuencia es idéntica para ambas estrategias.
TAREAS = [
    (10, 2),
    (35, 5),
    (15, 2),
    (40, 4),
    (20, 3),
    (30, 5),
    (10, 2),
    (45, 4),
    (15, 3),
    (25, 2),
    (35, 4),
    (20, 3),
    (10, 2),
    (40, 5),
    (30, 3),
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
    tareas_activas = []
    historial_cargas = []

    print(f"\n=== {nombre} ===")

    for ciclo, (carga, duracion) in enumerate(TAREAS, start=1):

        # Liberar las tareas que terminaron antes de procesar
        # la nueva llegada de este ciclo.
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
            print(
                f"Ciclo {ciclo:02d} | carga={carga:>2} | "
                f"duración={duracion} | RECHAZADA"
            )
            continue

        nodo.asignar(carga)
        asignadas += 1

        tareas_activas.append(
            {
                "nodo": nodo,
                "carga": carga,
                "fin": ciclo + duracion,
            }
        )

        historial_cargas.append(
            [nodo_actual.porcentaje_carga for nodo_actual in nodos]
        )

        estado = " | ".join(
            f"{n.nombre}={n.porcentaje_carga:.0f}%"
            for n in nodos
        )

        print(
            f"Ciclo {ciclo:02d} | carga={carga:>2} | "
            f"duración={duracion} | {nodo.nombre} | {estado}"
        )

    return nodos, asignadas, rechazadas, historial_cargas



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


def calcular_metricas_temporales(historial):
    desequilibrios = [
        max(cargas) - min(cargas)
        for cargas in historial
    ]

    picos = [
        max(cargas)
        for cargas in historial
    ]

    return {
        "desequilibrio_promedio": sum(desequilibrios) / len(desequilibrios),
        "desequilibrio_maximo": max(desequilibrios),
        "carga_maxima_observada": max(picos),
    }


if __name__ == "__main__":
    nodos_rr, asignadas_rr, rechazadas_rr, historial_rr = ejecutar_experimento(
    "ROUND ROBIN",
    BalanceadorRoundRobin,
)
    mostrar_resumen(nodos_rr, asignadas_rr, rechazadas_rr)

    metricas_rr = calcular_metricas_temporales(historial_rr)

    print("\n--- Métricas temporales Round Robin ---")
    print(
        f"Desequilibrio promedio: "
        f"{metricas_rr['desequilibrio_promedio']:.2f} puntos"
    )
    print(
        f"Desequilibrio máximo: "
        f"{metricas_rr['desequilibrio_maximo']:.2f} puntos"
    )
    print(
        f"Carga máxima observada: "
        f"{metricas_rr['carga_maxima_observada']:.2f}%"
    )

    nodos_ad, asignadas_ad, rechazadas_ad, historial_ad = ejecutar_experimento(
    "BALANCEO ADAPTATIVO",
    BalanceadorAdaptativo,
)
    mostrar_resumen(nodos_ad, asignadas_ad, rechazadas_ad)


    metricas_ad = calcular_metricas_temporales(historial_ad)

    print("\n--- Métricas temporales Balanceo Adaptativo ---")
    print(
        f"Desequilibrio promedio: "
        f"{metricas_ad['desequilibrio_promedio']:.2f} puntos"
    )
    print(
        f"Desequilibrio máximo: "
        f"{metricas_ad['desequilibrio_maximo']:.2f} puntos"
    )
    print(
        f"Carga máxima observada: "
        f"{metricas_ad['carga_maxima_observada']:.2f}%"
    )