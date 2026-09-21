from adaptive_balancer import (
    Nodo,
    BalanceadorRoundRobin,
    BalanceadorAdaptativo,
)


def test_nodo_inicia_sin_carga():
    nodo = Nodo("Nodo-Test", capacidad=100)

    assert nodo.carga_actual == 0
    assert nodo.tareas_asignadas == 0
    assert nodo.porcentaje_carga == 0


def test_nodo_asigna_carga_correctamente():
    nodo = Nodo("Nodo-Test", capacidad=100)

    resultado = nodo.asignar(40)

    assert resultado is True
    assert nodo.carga_actual == 40
    assert nodo.tareas_asignadas == 1
    assert nodo.porcentaje_carga == 40


def test_nodo_no_supera_su_capacidad():
    nodo = Nodo("Nodo-Test", capacidad=100)

    nodo.asignar(80)
    resultado = nodo.asignar(30)

    assert resultado is False
    assert nodo.carga_actual == 80
    assert nodo.tareas_asignadas == 1


def test_nodo_libera_carga_sin_valores_negativos():
    nodo = Nodo("Nodo-Test", capacidad=100)

    nodo.asignar(30)
    nodo.liberar(50)

    assert nodo.carga_actual == 0
    assert nodo.porcentaje_carga == 0



def test_round_robin_distribuye_secuencialmente():
    nodos = [
        Nodo("Nodo-1", capacidad=100),
        Nodo("Nodo-2", capacidad=100),
        Nodo("Nodo-3", capacidad=100),
    ]

    balanceador = BalanceadorRoundRobin(nodos)

    assert balanceador.seleccionar_nodo(10).nombre == "Nodo-1"
    assert balanceador.seleccionar_nodo(10).nombre == "Nodo-2"
    assert balanceador.seleccionar_nodo(10).nombre == "Nodo-3"


def test_round_robin_omite_nodo_sin_capacidad():
    nodos = [
        Nodo("Nodo-1", capacidad=100, carga_actual=100),
        Nodo("Nodo-2", capacidad=100),
        Nodo("Nodo-3", capacidad=100),
    ]

    balanceador = BalanceadorRoundRobin(nodos)

    nodo_seleccionado = balanceador.seleccionar_nodo(20)

    assert nodo_seleccionado.nombre == "Nodo-2"


def test_round_robin_retorna_none_si_no_hay_capacidad():
    nodos = [
        Nodo("Nodo-1", capacidad=100, carga_actual=90),
        Nodo("Nodo-2", capacidad=100, carga_actual=95),
        Nodo("Nodo-3", capacidad=100, carga_actual=100),
    ]

    balanceador = BalanceadorRoundRobin(nodos)

    nodo_seleccionado = balanceador.seleccionar_nodo(20)

    assert nodo_seleccionado is None



def test_adaptativo_selecciona_nodo_menos_cargado():
    nodos = [
        Nodo("Nodo-1", capacidad=100, carga_actual=60),
        Nodo("Nodo-2", capacidad=100, carga_actual=20),
        Nodo("Nodo-3", capacidad=100, carga_actual=40),
    ]

    balanceador = BalanceadorAdaptativo(nodos)

    nodo_seleccionado = balanceador.seleccionar_nodo(20)

    assert nodo_seleccionado.nombre == "Nodo-2"


def test_adaptativo_ignora_nodo_sin_capacidad_suficiente():
    nodos = [
        Nodo("Nodo-1", capacidad=100, carga_actual=20),
        Nodo("Nodo-2", capacidad=100, carga_actual=90),
        Nodo("Nodo-3", capacidad=100, carga_actual=50),
    ]

    balanceador = BalanceadorAdaptativo(nodos)

    nodo_seleccionado = balanceador.seleccionar_nodo(20)

    assert nodo_seleccionado.nombre == "Nodo-1"


def test_adaptativo_retorna_none_si_todos_estan_saturados():
    nodos = [
        Nodo("Nodo-1", capacidad=100, carga_actual=90),
        Nodo("Nodo-2", capacidad=100, carga_actual=95),
        Nodo("Nodo-3", capacidad=100, carga_actual=100),
    ]

    balanceador = BalanceadorAdaptativo(nodos)

    nodo_seleccionado = balanceador.seleccionar_nodo(20)

    assert nodo_seleccionado is None