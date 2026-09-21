# Balanceo dinámico de carga en CloudTask

## 1. Objetivo

Este documento describe la estrategia utilizada en CloudTask para estudiar el balanceo dinámico de carga y su relación con los conceptos presentados por Rajammal y Chinnadurai (2025).

El objetivo es evaluar cómo una estrategia adaptativa puede distribuir solicitudes entre diferentes recursos de cómputo teniendo en cuenta su estado de carga, evitando presentar como implementadas capacidades de escalamiento que no están disponibles en la infraestructura gratuita utilizada para el despliegue del proyecto.

## 2. Referente académico

Rajammal, K., & Chinnadurai, M. (2025). *Dynamic load balancing in cloud computing using predictive graph networks and adaptive neural scheduling*. Scientific Reports, 15(1), Artículo 22181. https://doi.org/10.1038/s41598-025-97494-2

El trabajo aborda el balanceo dinámico de carga mediante mecanismos predictivos y adaptativos orientados a mejorar la asignación de recursos en entornos cloud.

CloudTask no pretende reproducir completamente el modelo propuesto por los autores. En cambio, se desarrollará un prototipo experimental simplificado inspirado en el principio de tomar decisiones de distribución utilizando información dinámica sobre el estado de los recursos.

## 3. Situación actual de CloudTask

La aplicación utiliza Gunicorn como servidor WSGI.

En el entorno local se realizaron pruebas con uno y dos workers de Gunicorn. Con dos workers se comprobó que las solicitudes podían ser atendidas por diferentes procesos mediante el identificador de proceso expuesto temporalmente por el endpoint `/health`.

Las pruebas con Locust permitieron evaluar escenarios de 10, 50 y 100 usuarios virtuales.

Sin embargo, el número de workers de Gunicorn es una configuración estática y, por sí mismo, no constituye un algoritmo de balanceo dinámico basado en el estado de los recursos.

En producción, el plan gratuito utilizado en Render asigna actualmente un solo worker de Gunicorn y no proporciona escalamiento horizontal automático para este proyecto.

Por esta razón, se diferencian tres conceptos:

1. **Concurrencia:** capacidad de atender múltiples solicitudes.
2. **Distribución entre procesos:** reparto de solicitudes entre workers de Gunicorn.
3. **Balanceo dinámico:** selección de recursos utilizando información cambiante sobre su carga o estado.

## 4. Estrategia experimental propuesta

Se desarrollará un prototipo de balanceador adaptativo para representar el comportamiento de varios nodos de procesamiento.

Cada nodo mantendrá información dinámica de carga y el algoritmo seleccionará el recurso disponible con menor carga estimada para recibir la siguiente tarea.

El experimento permitirá comparar al menos dos estrategias:

- Distribución Round Robin.
- Distribución adaptativa basada en carga.

Las pruebas utilizarán cargas variables para observar cómo cambia la distribución de tareas y analizar métricas como:

- Número de tareas asignadas a cada nodo.
- Carga acumulada.
- Tiempo estimado de procesamiento.
- Diferencia de carga entre los nodos.
- Comportamiento ante incrementos de demanda.

## 5. Alcance y limitaciones

El prototipo será una implementación académica y experimental del concepto de balanceo adaptativo.

No se afirmará que CloudTask implementa el modelo completo de Rajammal y Chinnadurai ni que el despliegue gratuito de Render dispone de autoescalado horizontal.

La arquitectura de producción actual y la arquitectura escalable propuesta se mantendrán claramente diferenciadas en la documentación.