# Pruebas de rendimiento de CloudTask

## 1. Objetivo

Evaluar el comportamiento de CloudTask ante diferentes niveles de concurrencia y analizar la distribución de solicitudes mediante múltiples procesos worker de Gunicorn.

Las pruebas fueron realizadas con Locust 2.34.0 sobre el entorno local, utilizando el endpoint `/health`, el cual permite verificar la disponibilidad del servicio sin modificar información almacenada en la base de datos.

## 2. Entorno de pruebas

- Aplicación: CloudTask
- Framework: Flask
- Servidor WSGI: Gunicorn 23.0.0
- Herramienta de carga: Locust 2.34.0
- Python: 3.9.6
- Endpoint evaluado: `/health`
- Protocolo local: HTTP
- Dirección: `127.0.0.1:8000`
- Tipo de worker: Gunicorn sync
- Equipo de prueba: entorno local de desarrollo

## 3. Prueba con 2 workers y 10 usuarios

Configuración:

- Workers Gunicorn: 2
- Usuarios virtuales: 10
- Tasa de incorporación: 2 usuarios/s
- Duración: 30 segundos

Resultados:

| Métrica | Resultado |
|---|---:|
| Solicitudes | 151 |
| Fallos | 0 (0,00 %) |
| Tiempo promedio | 5 ms |
| Mediana (P50) | 5 ms |
| P95 | 9 ms |
| P99 | 29 ms |
| Tiempo máximo | 39 ms |
| Solicitudes/s | 5,08 |

## 4. Prueba con 2 workers y 50 usuarios

Configuración:

- Workers Gunicorn: 2
- Usuarios virtuales: 50
- Tasa de incorporación: 10 usuarios/s
- Duración: 30 segundos

Resultados:

| Métrica | Resultado |
|---|---:|
| Solicitudes | 715 |
| Fallos | 0 (0,00 %) |
| Tiempo promedio | 6 ms |
| Mediana (P50) | 6 ms |
| P95 | 12 ms |
| P99 | 14 ms |
| Tiempo máximo | 26 ms |
| Solicitudes/s | 24,02 |

## 5. Prueba con 2 workers y 100 usuarios

Configuración:

- Workers Gunicorn: 2
- Usuarios virtuales: 100
- Tasa de incorporación: 20 usuarios/s
- Duración: 30 segundos

Resultados:

| Métrica | Resultado |
|---|---:|
| Solicitudes | 1.431 |
| Fallos | 0 (0,00 %) |
| Tiempo promedio | 5 ms |
| Mediana (P50) | 5 ms |
| P95 | 14 ms |
| P99 | 20 ms |
| Tiempo máximo | 70 ms |
| Solicitudes/s | 47,94 |

## 6. Comparación: 1 worker frente a 2 workers

Se repitió la prueba de 100 usuarios virtuales utilizando un único worker de Gunicorn para comparar el comportamiento bajo las mismas condiciones de carga.

| Métrica | 1 worker | 2 workers |
|---|---:|---:|
| Solicitudes | 1.447 | 1.431 |
| Fallos | 0 % | 0 % |
| Tiempo promedio | 6 ms | 5 ms |
| Mediana (P50) | 5 ms | 5 ms |
| P95 | 22 ms | 14 ms |
| P99 | 28 ms | 20 ms |
| Tiempo máximo | 178 ms | 70 ms |
| Solicitudes/s | 48,48 | 47,94 |

## 7. Análisis

CloudTask mantuvo una tasa de fallos del 0 % en todas las cargas evaluadas, desde 10 hasta 100 usuarios virtuales.

Al incrementar la concurrencia de 10 a 100 usuarios, el throughput observado aumentó de 5,08 a 47,94 solicitudes por segundo sin producir errores.

En la comparación de 100 usuarios, el throughput de uno y dos workers fue similar. Por lo tanto, los resultados no demuestran un incremento significativo de throughput por utilizar dos workers.

Sin embargo, la configuración con dos workers presentó mejores tiempos en la cola de latencia. El P95 disminuyó de 22 ms a 14 ms, el P99 de 28 ms a 20 ms y el tiempo máximo observado de 178 ms a 70 ms.

Estos resultados indican que, bajo las condiciones específicas de esta prueba y para el endpoint ligero `/health`, disponer de dos procesos worker permitió reducir los picos de latencia, aunque no produjo un incremento relevante del throughput.

## 8. Alcance y limitaciones

Las pruebas fueron ejecutadas localmente y no representan una prueba de escalamiento horizontal de infraestructura cloud.

Los workers de Gunicorn son procesos de ejecución dentro de una misma instancia y no equivalen a múltiples instancias cloud ni a un mecanismo de autoscaling.

La versión gratuita utilizada para el despliegue de CloudTask en Render opera actualmente con un único worker según los registros de despliegue disponibles. Por esta razón, los resultados con dos workers se presentan como evidencia experimental local de distribución de solicitudes entre procesos y no como evidencia de autoscaling en producción.

Los resultados también están condicionados por el hardware local, el endpoint seleccionado, la duración de las pruebas y el patrón de espera configurado en Locust. Para una evaluación de capacidad de producción sería necesario realizar pruebas adicionales con cargas sostenidas, diferentes operaciones de la aplicación y una infraestructura equivalente a la utilizada en producción.

## 9. Conclusión

Las pruebas realizadas muestran que CloudTask respondió correctamente a las cargas evaluadas, sin errores HTTP durante los escenarios ejecutados. La aplicación mantuvo tiempos de respuesta bajos en el entorno local y mostró una reducción de la latencia de cola al utilizar dos workers de Gunicorn.

Estas pruebas proporcionan evidencia reproducible del comportamiento de la aplicación ante incrementos controlados de concurrencia, sin atribuir al entorno de producción capacidades de escalamiento que no han sido implementadas o verificadas.