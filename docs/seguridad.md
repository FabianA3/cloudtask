# Seguridad de CloudTask

## 1. Objetivo

CloudTask aplica controles de seguridad en las capas de aplicación, autenticación, autorización, sesión, transporte y persistencia con el propósito de proteger la confidencialidad, integridad y disponibilidad de la información.

Este documento describe únicamente controles implementados o verificados en el proyecto. La correspondencia formal con las guías de seguridad exigidas por la actividad académica se documentará utilizando las referencias oficiales correspondientes.

## 2. Gestión de contraseñas

Las contraseñas de los usuarios no se almacenan en texto plano.

CloudTask utiliza Werkzeug para generar hashes mediante:

`PBKDF2-SHA256` con `600.000` iteraciones.

La autenticación compara la contraseña proporcionada con el hash almacenado.

Durante las pruebas se verificó que:

- La contraseña almacenada no coincide con el texto original.
- Una contraseña válida puede verificarse correctamente contra el hash.
- Una contraseña incorrecta no permite iniciar sesión.

## 3. Autenticación

CloudTask utiliza Flask-Login para administrar las sesiones autenticadas.

Las rutas que requieren autenticación utilizan `login_required`.

Entre ellas se encuentra el panel de tareas y las operaciones relacionadas con los recursos privados del usuario.

Se verificó mediante pruebas automatizadas que un usuario no autenticado que intenta acceder a `/dashboard` es redirigido al inicio de sesión.

## 4. Autorización y aislamiento entre usuarios

La autenticación por sí sola no concede acceso a todas las tareas.

Para editar o eliminar una tarea, CloudTask consulta simultáneamente:

- El identificador de la tarea.
- El identificador del usuario autenticado.

Si el recurso no pertenece al usuario, la aplicación devuelve HTTP 404.

Este comportamiento fue verificado mediante pruebas automatizadas y mediante una prueba funcional con dos cuentas diferentes.

Por lo tanto, la aplicación implementa control de acceso a nivel de objeto para evitar que un usuario modifique tareas pertenecientes a otro usuario mediante manipulación de identificadores en la URL.

## 5. Protección CSRF

CloudTask utiliza Flask-WTF y `CSRFProtect`.

Las solicitudes que modifican información requieren un token CSRF válido.

La protección se aplica, entre otras operaciones, a:

- Registro.
- Inicio de sesión.
- Creación de tareas.
- Edición de tareas.
- Eliminación de tareas.
- Cierre de sesión.

Una solicitud POST sin un token CSRF válido fue probada y rechazada con HTTP 400.

También existe una prueba automatizada específica que verifica este comportamiento.

## 6. Cierre de sesión seguro

El endpoint `/logout` acepta únicamente solicitudes POST.

Esto evita utilizar una solicitud GET para realizar una operación que cambia el estado de la sesión.

El formulario de cierre de sesión incluye protección CSRF.

Se verificó que:

- GET `/logout` devuelve HTTP 405.
- POST sin token CSRF devuelve HTTP 400.
- POST válido mediante el formulario cierra correctamente la sesión.

## 7. Cookies de sesión

La aplicación configura las cookies de sesión con:

- `HttpOnly`
- `SameSite=Lax`
- `Secure` en producción

`HttpOnly` limita el acceso a la cookie desde JavaScript ejecutado en el navegador.

`SameSite=Lax` proporciona protección adicional frente a determinados escenarios de solicitudes entre sitios.

`Secure` hace que la cookie de sesión de producción sea transmitida mediante conexiones HTTPS.

La presencia de estos atributos fue verificada en respuestas HTTP del entorno desplegado.

## 8. Gestión de secretos

CloudTask no almacena la clave secreta de producción directamente en el código fuente.

Los valores sensibles y dependientes del entorno se administran mediante variables de entorno, incluyendo:

- `SECRET_KEY`
- `DATABASE_URL`
- `APP_ENV`

La configuración de producción se administra desde la plataforma de despliegue.

Durante el desarrollo del proyecto, la clave secreta de producción fue rotada como medida preventiva después de una exposición durante una verificación visual de configuración.

Los valores secretos no deben incluirse en documentación, capturas públicas ni repositorios.

## 9. Seguridad de la base de datos

La aplicación utiliza SQLAlchemy como ORM.

Las operaciones habituales se realizan mediante consultas construidas por el ORM en lugar de concatenar directamente entradas de usuario dentro de sentencias SQL.

La cadena de conexión de PostgreSQL se obtiene mediante `DATABASE_URL`.

Las credenciales de conexión no se almacenan directamente en el repositorio.

Además, las tareas están asociadas mediante `usuario_id` al propietario correspondiente.

## 10. HTTPS y seguridad de transporte

El servicio desplegado se encuentra disponible mediante HTTPS.

En producción CloudTask agrega:

`Strict-Transport-Security: max-age=31536000; includeSubDomains`

Este encabezado indica al navegador que debe utilizar HTTPS para futuras conexiones durante el período definido.

La presencia de HSTS fue verificada mediante solicitudes HTTP al entorno desplegado.

## 11. Content Security Policy

CloudTask implementa la siguiente política CSP:

`default-src 'self'; style-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'`

La política restringe por defecto la carga de recursos a recursos del mismo origen y establece restricciones adicionales para formularios, inclusión en marcos y URL base.

La presencia del encabezado fue verificada tanto mediante pruebas automatizadas como mediante consultas HTTP al servicio desplegado.

## 12. Protección contra MIME sniffing

Se utiliza:

`X-Content-Type-Options: nosniff`

Este encabezado indica al navegador que no debe intentar reinterpretar el tipo MIME declarado por el servidor.

## 13. Protección contra framing

Se utiliza:

`X-Frame-Options: DENY`

Adicionalmente, la CSP incluye:

`frame-ancestors 'none'`

Estas medidas impiden que CloudTask sea incorporado dentro de frames de otros sitios bajo navegadores compatibles con estas políticas.

## 14. Referrer Policy

CloudTask utiliza:

`Referrer-Policy: strict-origin-when-cross-origin`

Esta política limita la información enviada mediante el encabezado Referer cuando se navega hacia otros orígenes.

## 15. Permissions Policy

La aplicación utiliza:

`Permissions-Policy: camera=(), microphone=(), geolocation=()`

CloudTask no requiere acceso a cámara, micrófono ni geolocalización, por lo que estas capacidades se deshabilitan mediante política HTTP.

## 16. Manejo controlado de errores

CloudTask implementa páginas personalizadas para:

- HTTP 400.
- HTTP 404.
- HTTP 500.

Esto evita depender únicamente de páginas de error predeterminadas y permite mantener una respuesta controlada ante condiciones excepcionales.

Ante un error HTTP 500, la aplicación ejecuta:

`db.session.rollback()`

antes de devolver la respuesta, evitando dejar una transacción fallida activa en la sesión de base de datos.

## 17. Modo de depuración

El modo debug no se activa de manera predeterminada.

Su activación depende explícitamente de la configuración de desarrollo.

Esto evita exponer en producción el depurador interactivo y detalles internos innecesarios de la aplicación.

## 18. Health check

CloudTask dispone del endpoint:

`/health`

Su función es comprobar la disponibilidad básica del servicio.

El endpoint no modifica información de usuarios y ha sido utilizado para verificaciones posteriores al despliegue y pruebas controladas de carga.

## 19. Pruebas automatizadas de seguridad

La suite automatizada incluye verificaciones relacionadas con:

- Almacenamiento seguro de contraseñas.
- Credenciales incorrectas.
- Protección de rutas autenticadas.
- Aislamiento de tareas entre usuarios.
- Rechazo de edición de recursos ajenos.
- Rechazo de eliminación de recursos ajenos.
- Protección CSRF.
- Encabezados HTTP de seguridad.
- HSTS en producción.

La suite actual contiene 14 pruebas automatizadas y fue ejecutada satisfactoriamente sin fallos.

## 20. Seguridad en el proceso de despliegue

El código se administra mediante Git y GitHub.

Los cambios se incorporan mediante commits identificables y Render realiza despliegues automáticos desde la rama configurada.

Después de cambios relevantes se realizan verificaciones del endpoint `/health` y de los encabezados HTTP de seguridad.

Este proceso proporciona trazabilidad entre cambios del código y versiones desplegadas.

## 21. Limitaciones y mejoras futuras

La implementación constituye un prototipo académico funcional y puede reforzarse para un escenario de producción de mayor escala.

Entre las mejoras posibles se encuentran:

- Rate limiting.
- Registro centralizado de eventos de seguridad.
- Alertas automáticas.
- Gestión avanzada y rotación periódica de secretos.
- WAF dedicado.
- Copias de seguridad y estrategia formal de recuperación.
- Gestión de migraciones de base de datos.
- Análisis automático de dependencias vulnerables.
- Escaneo SAST y DAST integrado al proceso de desarrollo.
- Políticas avanzadas de observabilidad y auditoría.

Estas capacidades se consideran mejoras propuestas y no controles actualmente demostrados en la implementación.

## 22. Referencias académicas

Ministerio de Tecnologías de la Información y las Comunicaciones – MinTIC. (2021). *Guía técnica de computación en la nube (v.1.1).* Bogotá D.C.: MinTIC.

La implementación de CloudTask adopta principios de seguridad tratados en la guía académica, especialmente la responsabilidad compartida, el control de acceso, el principio de mínimo privilegio, la protección de credenciales y secretos, el uso de comunicaciones seguras y la verificación de controles de seguridad.