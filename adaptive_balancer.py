from dataclasses import dataclass


@dataclass
class Nodo:
    nombre: str
    capacidad: float = 100.0
    carga_actual: float = 0.0
    tareas_asignadas: int = 0

    @property
    def porcentaje_carga(self):
        return (self.carga_actual / self.capacidad) * 100

    def puede_recibir(self, carga):
        return self.carga_actual + carga <= self.capacidad

    def asignar(self, carga):
        if not self.puede_recibir(carga):
            return False

        self.carga_actual += carga
        self.tareas_asignadas += 1
        return True

    def liberar(self, carga):
        self.carga_actual = max(0.0, self.carga_actual - carga)


class BalanceadorRoundRobin:
    def __init__(self, nodos):
        self.nodos = nodos
        self.indice = 0

    def seleccionar_nodo(self, carga):
        total = len(self.nodos)

        for _ in range(total):
            nodo = self.nodos[self.indice]
            self.indice = (self.indice + 1) % total

            if nodo.puede_recibir(carga):
                return nodo

        return None


class BalanceadorAdaptativo:
    def __init__(self, nodos):
        self.nodos = nodos

    def seleccionar_nodo(self, carga):
        candidatos = [
            nodo for nodo in self.nodos
            if nodo.puede_recibir(carga)
        ]

        if not candidatos:
            return None

        return min(
            candidatos,
            key=lambda nodo: (
                nodo.porcentaje_carga,
                nodo.tareas_asignadas
            )
        )