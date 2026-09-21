# Arquitectura de CloudTask

## 1. Descripción general

CloudTask es una aplicación web de gestión de tareas desarrollada con Flask y desplegada en infraestructura cloud mediante Render.

La solución utiliza una arquitectura web de tres capas, separando la interfaz de usuario, la lógica de aplicación y la persistencia de datos.

El código fuente se administra mediante Git y GitHub, mientras que Render realiza el despliegue automático de la aplicación a partir de los cambios incorporados a la rama principal del repositorio.

## 2. Arquitectura implementada

Flujo general de la solución:

Usuario / Navegador
        |
        | HTTPS
        v
Cloudflare / infraestructura de entrada de Render
        |
        v
Render Web Service
        |
        v
Gunicorn
        |
        v
Aplicación Flask - CloudTask
        |
        | SQLAlchemy
        v
PostgreSQL administrado en Render

El flujo de despliegue es:

Desarrollo local
        |
        | Git
        v
GitHub
        |
        | Auto-Deploy
        v
Render Web Service

## 3. Capa de presentación

La capa de presentación está compuesta por plantillas HTML renderizadas mediante Jinja2.

Desde el navegador el usuario puede:

- Registrarse.
- Iniciar sesión.
- Cerrar sesión.
- Consultar sus tareas.
- Crear tareas.
- Editar tareas.
- Eliminar tareas.

Las operaciones protegidas requieren autenticación.

## 4. Capa de aplicación

La lógica de negocio está implementada con Flask.

Gunicorn funciona como servidor WSGI encargado de ejecutar la aplicación en el entorno de producción.

Entre las responsabilidades de esta capa se encuentran:

- Gestión de usuarios.
- Autenticación.
- Autorización.
- Validación de formularios.
- Gestión CRUD de tareas.
- Protección CSRF.
- Manejo de errores HTTP.
- Aplicación de encabezados de seguridad.
- Comunicación con la capa de persistencia.

La aplicación incluye además el endpoint `/health`, utilizado para comprobar la disponibilidad del servicio y para realizar pruebas controladas de rendimiento.

## 5. Capa de datos

CloudTask utiliza SQLAlchemy como capa ORM.

En desarrollo se puede utilizar SQLite, mientras que el entorno desplegado utiliza PostgreSQL administrado por Render.

La cadena de conexión se obtiene mediante la variable de entorno `DATABASE_URL`, evitando almacenar credenciales de la base de datos directamente en el código fuente.

La comunicación entre la aplicación desplegada y PostgreSQL utiliza la configuración de conexión proporcionada por la plataforma cloud.

## 6. Gestión de configuración y secretos

Los parámetros sensibles y dependientes del entorno se gestionan mediante variables de entorno.

Entre ellos se encuentran:

- `SECRET_KEY`
- `DATABASE_URL`
- `APP_ENV`

La clave secreta no se almacena en el repositorio.

La aplicación diferencia el comportamiento de desarrollo y producción mediante `APP_ENV`.

## 7. Seguridad

La arquitectura implementa controles de seguridad en diferentes capas.

### Autenticación y autorización

Flask-Login administra las sesiones de usuario.

Las operaciones de gestión de tareas están protegidas mediante autenticación y cada consulta de edición o eliminación valida también el identificador del usuario propietario de la tarea.

Esto impide que un usuario autenticado modifique recursos pertenecientes a otro usuario mediante manipulación directa de las URL.

### Contraseñas

Las contraseñas no se almacenan en texto plano.

CloudTask utiliza derivación de claves mediante PBKDF2-SHA256 con 600.000 iteraciones para generar los hashes almacenados.

### CSRF

Flask-WTF proporciona protección CSRF para las solicitudes que modifican información.

También se utiliza CSRF en operaciones como eliminación de tareas y cierre de sesión mediante POST.

### Cookies de sesión

La configuración incluye:

- `HttpOnly`
- `SameSite=Lax`
- `Secure` en producción

### Encabezados HTTP

En producción se aplican:

- Content-Security-Policy
- Permissions-Policy
- Referrer-Policy
- Strict-Transport-Security
- X-Content-Type-Options
- X-Frame-Options

### Manejo de errores

CloudTask dispone de páginas controladas para errores:

- HTTP 400
- HTTP 404
- HTTP 500

Ante un error interno, la sesión de SQLAlchemy ejecuta `rollback()` antes de devolver la respuesta de error.

## 8. Disponibilidad y monitoreo básico

El endpoint:

`/health`

permite comprobar que el servicio se encuentra operativo.

Una respuesta correcta devuelve HTTP 200 e información básica del servicio.

Este endpoint también permite realizar pruebas de disponibilidad sin modificar información de los usuarios.

## 9. Integración y despliegue

El código fuente se encuentra versionado con Git.

El flujo utilizado es:

1. Desarrollo y pruebas locales.
2. Commit en Git.
3. Push a la rama `main` de GitHub.
4. Render detecta el nuevo commit.
5. Auto-Deploy inicia automáticamente el proceso de construcción.
6. Se instalan las dependencias de producción.
7. Gunicorn inicia CloudTask.
8. Render publica la nueva versión del servicio.

Después de los despliegues se verifica `/health` para comprobar el funcionamiento de la aplicación.

## 10. Concurrencia

En las pruebas locales se ejecutó Gunicorn con uno y dos procesos worker.

Con dos workers se verificó que diferentes procesos pueden atender solicitudes de la aplicación.

Las pruebas realizadas con Locust permitieron evaluar cargas de 10, 50 y 100 usuarios virtuales.

Estos workers representan concurrencia a nivel de procesos dentro de una instancia y no deben confundirse con escalamiento horizontal entre múltiples instancias cloud.

Los resultados detallados se encuentran en:

`docs/pruebas_rendimiento.md`

## 11. Limitaciones del entorno actual

El despliegue utilizado para el proyecto corresponde al nivel gratuito disponible en Render.

La instancia web utilizada dispone de recursos limitados y los registros de despliegue han mostrado una configuración de un worker de Gunicorn en producción.

Por lo tanto, la implementación actual no se presenta como una infraestructura con autoscaling horizontal.

La base de datos PostgreSQL gratuita también está destinada al desarrollo, demostración y pruebas y tiene las restricciones de vigencia y capacidad establecidas por el proveedor.

Estas limitaciones no afectan la demostración funcional del proyecto, pero deben considerarse antes de utilizar la arquitectura para cargas reales de producción.

## 12. Arquitectura escalable propuesta

Para una evolución orientada a producción, CloudTask puede adoptar la siguiente arquitectura:

Usuarios
        |
        | HTTPS
        v
CDN / WAF / Reverse Proxy
        |
        v
Load Balancer
        |
        +-------------------+
        |                   |
        v                   v
Instancia CloudTask A   Instancia CloudTask B
Gunicorn + Flask        Gunicorn + Flask
        |                   |
        +---------+---------+
                  |
                  v
          PostgreSQL administrado

Esta arquitectura permitiría distribuir solicitudes entre varias instancias de la aplicación.

En una infraestructura que soporte escalamiento automático, las métricas de utilización y demanda podrían utilizarse para aumentar o reducir dinámicamente el número de instancias.

La aplicación ya mantiene la persistencia fuera del proceso web mediante PostgreSQL, lo cual facilita una futura evolución hacia múltiples instancias. Sin embargo, la implementación de autoscaling horizontal corresponde a una evolución propuesta y no a una característica demostrada en el nivel gratuito actualmente utilizado.

## 13. Separación entre arquitectura implementada y propuesta

Es importante diferenciar los dos escenarios:

**Implementado y verificado:**

- Aplicación Flask.
- Gunicorn.
- PostgreSQL administrado.
- HTTPS.
- Variables de entorno.
- Controles de autenticación y autorización.
- CSRF.
- Encabezados de seguridad.
- Health check.
- GitHub.
- Auto-Deploy.
- Pruebas automatizadas.
- Pruebas locales de concurrencia y carga.

**Arquitectura propuesta para mayor escala:**

- Varias instancias de CloudTask.
- Balanceador de carga entre instancias.
- Escalamiento horizontal automático.
- Métricas centralizadas.
- Monitoreo y alertas avanzadas.
- WAF dedicado.

Esta separación permite documentar de forma precisa las capacidades verificadas del prototipo y las mejoras necesarias para una arquitectura de producción de mayor escala.