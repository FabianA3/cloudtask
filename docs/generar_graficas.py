from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


SALIDA = Path(__file__).parent / "evidencias"
SALIDA.mkdir(parents=True, exist_ok=True)


def grafica_concurrencia():
    metricas = ["Promedio", "P95", "P99", "Máxima"]
    un_worker = [6, 22, 28, 178]
    dos_workers = [5, 14, 20, 70]

    x = np.arange(len(metricas))
    ancho = 0.36

    fig, ax = plt.subplots(figsize=(10, 6))

    barras_1 = ax.bar(
        x - ancho / 2,
        un_worker,
        ancho,
        label="1 worker"
    )

    barras_2 = ax.bar(
        x + ancho / 2,
        dos_workers,
        ancho,
        label="2 workers"
    )

    ax.set_title(
        "Comparación de latencias con 100 usuarios concurrentes",
        fontsize=14,
        fontweight="bold"
    )
    ax.set_xlabel("Métrica de latencia")
    ax.set_ylabel("Latencia (ms)")
    ax.set_xticks(x)
    ax.set_xticklabels(metricas)
    ax.legend()
    ax.grid(axis="y", alpha=0.25)

    ax.bar_label(barras_1, padding=3, fmt="%d ms")
    ax.bar_label(barras_2, padding=3, fmt="%d ms")

    fig.text(
        0.5,
        0.01,
        "Prueba local con Gunicorn y Locust. 100 usuarios concurrentes.",
        ha="center",
        fontsize=9
    )

    fig.tight_layout(rect=[0, 0.04, 1, 1])

    archivo = SALIDA / "figura_12_concurrencia_workers.png"

    fig.savefig(
        archivo,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print(f"Generada: {archivo}")



def grafica_desequilibrio_promedio():
    escenarios = ["Moderado", "Alto", "Pico"]
    round_robin = [17.67, 41.00, 33.33]
    adaptativo = [17.67, 31.00, 43.33]

    x = np.arange(len(escenarios))
    ancho = 0.36

    fig, ax = plt.subplots(figsize=(10, 6))

    barras_rr = ax.bar(
        x - ancho / 2,
        round_robin,
        ancho,
        label="Round Robin"
    )

    barras_adapt = ax.bar(
        x + ancho / 2,
        adaptativo,
        ancho,
        label="Adaptativo"
    )

    ax.set_title(
        "Desequilibrio promedio por escenario",
        fontsize=14,
        fontweight="bold"
    )
    ax.set_xlabel("Escenario de carga")
    ax.set_ylabel("Desequilibrio promedio (puntos)")
    ax.set_xticks(x)
    ax.set_xticklabels(escenarios)
    ax.legend()
    ax.grid(axis="y", alpha=0.25)

    ax.bar_label(
        barras_rr,
        padding=3,
        fmt="%.2f"
    )
    ax.bar_label(
        barras_adapt,
        padding=3,
        fmt="%.2f"
    )

    fig.text(
        0.5,
        0.01,
        "Comparación experimental con tres nodos simulados de capacidad 100.",
        ha="center",
        fontsize=9
    )

    fig.tight_layout(rect=[0, 0.04, 1, 1])

    archivo = SALIDA / "figura_14_desequilibrio_promedio.png"

    fig.savefig(
        archivo,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print(f"Generada: {archivo}")



def grafica_desequilibrio_maximo():
    escenarios = ["Moderado", "Alto", "Pico"]
    round_robin = [25.00, 60.00, 55.00]
    adaptativo = [25.00, 45.00, 95.00]

    x = np.arange(len(escenarios))
    ancho = 0.36

    fig, ax = plt.subplots(figsize=(10, 6))

    barras_rr = ax.bar(
        x - ancho / 2,
        round_robin,
        ancho,
        label="Round Robin"
    )

    barras_adapt = ax.bar(
        x + ancho / 2,
        adaptativo,
        ancho,
        label="Adaptativo"
    )

    ax.set_title(
        "Desequilibrio máximo por escenario",
        fontsize=14,
        fontweight="bold"
    )
    ax.set_xlabel("Escenario de carga")
    ax.set_ylabel("Desequilibrio máximo (puntos)")
    ax.set_xticks(x)
    ax.set_xticklabels(escenarios)
    ax.legend()
    ax.grid(axis="y", alpha=0.25)

    ax.bar_label(
        barras_rr,
        padding=3,
        fmt="%.0f"
    )
    ax.bar_label(
        barras_adapt,
        padding=3,
        fmt="%.0f"
    )

    fig.text(
        0.5,
        0.01,
        "Comparación experimental con tres nodos simulados de capacidad 100.",
        ha="center",
        fontsize=9
    )

    fig.tight_layout(rect=[0, 0.04, 1, 1])

    archivo = SALIDA / "figura_15_desequilibrio_maximo.png"

    fig.savefig(
        archivo,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print(f"Generada: {archivo}")



def grafica_carga_maxima():
    escenarios = ["Moderado", "Alto", "Pico"]
    round_robin = [25.00, 95.00, 100.00]
    adaptativo = [25.00, 90.00, 100.00]

    x = np.arange(len(escenarios))
    ancho = 0.36

    fig, ax = plt.subplots(figsize=(10, 6))

    barras_rr = ax.bar(
        x - ancho / 2,
        round_robin,
        ancho,
        label="Round Robin"
    )

    barras_adapt = ax.bar(
        x + ancho / 2,
        adaptativo,
        ancho,
        label="Adaptativo"
    )

    ax.set_title(
        "Carga máxima observada por escenario",
        fontsize=14,
        fontweight="bold"
    )
    ax.set_xlabel("Escenario de carga")
    ax.set_ylabel("Carga máxima observada (%)")
    ax.set_xticks(x)
    ax.set_xticklabels(escenarios)
    ax.set_ylim(0, 110)
    ax.legend()
    ax.grid(axis="y", alpha=0.25)

    ax.bar_label(
        barras_rr,
        padding=3,
        fmt="%.0f%%"
    )
    ax.bar_label(
        barras_adapt,
        padding=3,
        fmt="%.0f%%"
    )

    fig.text(
        0.5,
        0.01,
        "Porcentaje máximo de utilización registrado durante cada escenario.",
        ha="center",
        fontsize=9
    )

    fig.tight_layout(rect=[0, 0.04, 1, 1])

    archivo = SALIDA / "figura_16_carga_maxima.png"

    fig.savefig(
        archivo,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print(f"Generada: {archivo}")



if __name__ == "__main__":
    grafica_concurrencia()
    grafica_desequilibrio_promedio()
    grafica_desequilibrio_maximo()
    grafica_carga_maxima()



