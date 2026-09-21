# Matriz de trazabilidad de seguridad de CloudTask

## 1. Objetivo

Relacionar los lineamientos de seguridad estudiados en la Unidad 3 de Computación en la Nube con los riesgos identificados, los controles implementados en CloudTask y las evidencias utilizadas para verificar su funcionamiento.

## 2. Matriz de controles

| Lineamiento | Riesgo asociado | Control implementado en CloudTask | Evidencia |
|---|---|---|---|
| Responsabilidad compartida | Configuración insegura de los servicios cloud | Configuración de seguridad realizada tanto en la aplicación como mediante variables de entorno del servicio desplegado | Configuración de Render y pruebas HTTP |
| Control de acceso | Acceso no autorizado a funciones privadas | Rutas protegidas mediante Flask-Login y `login_required` | `test_dashboard_requiere_autenticacion` |
| Mínimo privilegio | Un usuario puede acceder a recursos de otro usuario | Las consultas de edición y eliminación validan simultáneamente `tarea_id` y `current_user.id` | `test_usuario_no_puede_editar_tarea_ajena` y `test_usuario_no_puede_eliminar_tarea_ajena` |
| Protección de credenciales | Exposición de contraseñas de usuarios | Contraseñas almacenadas mediante PBKDF2-SHA256 con 600.000 iteraciones | `test_registro_usuario` y verificación del hash |
| Gestión de secretos | Exposición de credenciales o claves en el código fuente | `SECRET_KEY` y `DATABASE_URL` administradas mediante variables de entorno | Configuración del servicio y repositorio sin secretos de producción |
| Rotación de secretos | Uso prolongado de una credencial potencialmente expuesta | Rotación preventiva de `SECRET_KEY` de producción | Evidencia del cambio y despliegue posterior |
| Comunicaciones seguras | Intercepción de información durante el tránsito | Acceso al servicio mediante HTTPS y HSTS en producción | `test_hsts_en_produccion` y verificación mediante `curl` |
| Protección de sesión | Robo o uso indebido de cookies de sesión | Cookies con `HttpOnly`, `SameSite=Lax` y `Secure` en producción | Encabezado `Set-Cookie` verificado en producción |
| Protección CSRF | Ejecución de operaciones POST no autorizadas desde otro origen | Flask-WTF y `CSRFProtect` | `test_csrf_rechaza_post_sin_token` |
| Operaciones sensibles | Cambio de estado mediante solicitudes GET | `/logout` acepta únicamente POST y requiere CSRF | GET `/logout` → HTTP 405; POST sin token → HTTP 400 |
| Seguridad del navegador | Carga de recursos o ejecución desde orígenes no autorizados | Content-Security-Policy | `test_encabezados_seguridad` y respuesta HTTP de producción |
| Protección contra framing | Clickjacking | `X-Frame-Options: DENY` y `frame-ancestors 'none'` | Prueba automatizada y encabezados HTTP |
| MIME sniffing | Interpretación incorrecta de contenido por el navegador | `X-Content-Type-Options: nosniff` | `test_encabezados_seguridad` |
| Minimización de capacidades del navegador | Uso innecesario de cámara, micrófono o geolocalización | `Permissions-Policy: camera=(), microphone=(), geolocation=()` | Verificación automatizada y en producción |
| Manejo de errores | Exposición o comportamiento no controlado ante errores | Manejadores personalizados HTTP 400, 404 y 500 | Pruebas funcionales realizadas |
| Integridad transaccional | Sesión de base de datos inconsistente después de un error interno | `db.session.rollback()` ante HTTP 500 | Implementación del manejador 500 |
| Disponibilidad | Falta de mecanismo básico para comprobar el estado del servicio | Endpoint `/health` | `test_health` y HTTP 200 en producción |
| Auditoría y trazabilidad | Dificultad para relacionar cambios con versiones desplegadas | Historial Git, commits y Auto-Deploy desde GitHub | Historial del repositorio y Events de Render |
| Verificación de controles | Controles implementados pero no comprobados | Suite automatizada con 14 pruebas | `14 passed` mediante pytest |
| Evaluación bajo carga | Degradación o fallos ante concurrencia | Pruebas con Locust de 10, 50 y 100 usuarios virtuales | 0 % de fallos en los escenarios ejecutados |

## 3. Controles recomendados aún no implementados

La guía académica también aborda controles que no deben presentarse como implementados actualmente en CloudTask.

Entre las mejoras pendientes se encuentran:

- Autenticación multifactor para cuentas privilegiadas.
- Registro centralizado y monitoreo continuo de eventos.
- Alertas de seguridad.
- Rotación automatizada de secretos.
- Copias de seguridad y estrategia formal de recuperación.
- Definición formal de RPO y RTO.
- Auditorías periódicas de configuración.
- Herramientas de análisis de postura de seguridad cloud.
- WAF dedicado.
- Estrategia formal de respuesta a incidentes.

Estos elementos se consideran parte de la evolución propuesta del proyecto y no de las capacidades actualmente verificadas.

## 4. Referencia académica

Ministerio de Tecnologías de la Información y las Comunicaciones – MinTIC. (2021). *Guía técnica de computación en la nube (v.1.1).* Bogotá D.C.: MinTIC.

La matriz también utiliza como base conceptual los contenidos de seguridad, identidad, auditoría y protección de datos incluidos en la Guía de estudio de la Unidad 3 de Computación en la Nube de la Tecnológica del Oriente.