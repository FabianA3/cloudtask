# CloudTask
## Sistema web de gestión de tareas en la nube

### Informe técnico final

---

## 1. Introducción
CloudTask es una aplicación web de gestión de tareas desarrollada con el propósito de aplicar de manera práctica conceptos de computación en la nube, seguridad de la información, persistencia de datos, despliegue de aplicaciones, pruebas de rendimiento y estrategias de distribución de carga.

La solución permite a los usuarios registrarse, autenticarse y administrar sus propias tareas mediante operaciones de creación, consulta, actualización y eliminación. Cada tarea puede contener información como título, descripción, prioridad, estado y fecha de creación, manteniendo separación entre los datos pertenecientes a diferentes usuarios.

Para el desarrollo se utilizó Flask como framework web en Python, SQLAlchemy para la gestión de persistencia y PostgreSQL como sistema de base de datos en el entorno de producción. La aplicación fue desplegada mediante Render, permitiendo disponer de un servicio accesible a través de Internet mediante HTTPS. El código fuente y su historial de versiones se administraron mediante Git y GitHub, integrándose además un mecanismo de despliegue automático a partir de los cambios realizados en la rama principal del repositorio.

La implementación incorpora diferentes controles orientados a la protección de la información, entre ellos autenticación de usuarios, almacenamiento seguro de contraseñas mediante funciones de derivación criptográfica, protección CSRF, control de acceso por usuario, configuración segura de cookies, administración de secretos mediante variables de entorno y encabezados HTTP de seguridad.

Adicionalmente, se desarrolló un prototipo experimental para estudiar el comportamiento de diferentes estrategias de distribución de carga. Se comparó una política Round Robin con una estrategia adaptativa basada en el estado de carga de los nodos, utilizando escenarios de carga moderada, alta y pico. Esta experimentación permite analizar tanto las ventajas como las limitaciones de una estrategia dinámica bajo diferentes condiciones.

Finalmente, la solución fue sometida a pruebas funcionales automatizadas, pruebas de seguridad, pruebas de carga, pruebas de concurrencia y experimentos de balanceo. Los resultados obtenidos constituyen las evidencias utilizadas en este informe para analizar el comportamiento, la seguridad, la disponibilidad y las posibilidades de escalabilidad de CloudTask.

## 2. Objetivos

### 2.1 Objetivo general
Diseñar, implementar y evaluar una aplicación web de gestión de tareas desplegada en un entorno de computación en la nube, integrando mecanismos de persistencia de datos, seguridad de la información, control de acceso, pruebas automatizadas y estrategias experimentales de distribución dinámica de carga, con el fin de analizar su funcionamiento, rendimiento, protección de la información y posibilidades de escalabilidad de acuerdo con los lineamientos y conceptos estudiados.

### 2.2 Objetivos específicos
- Desarrollar una aplicación web funcional para la gestión de tareas, incorporando registro y autenticación de usuarios, control de acceso y operaciones de creación, consulta, actualización y eliminación de información.

- Implementar la persistencia de los datos mediante una base de datos PostgreSQL en el entorno de producción, utilizando servicios de computación en la nube para garantizar el acceso remoto a la aplicación.

- Aplicar mecanismos de seguridad orientados a proteger la confidencialidad, integridad y acceso a la información, considerando los lineamientos de seguridad estudiados y las recomendaciones establecidas por MinTIC.

- Evaluar el comportamiento y rendimiento de CloudTask mediante pruebas funcionales automatizadas, pruebas de seguridad, carga y concurrencia, conservando evidencias reproducibles de los resultados obtenidos.

- Implementar y evaluar experimentalmente estrategias de distribución de carga mediante Round Robin y un balanceador adaptativo basado en el estado de carga de los nodos, analizando su comportamiento bajo diferentes niveles de demanda.

- Analizar las posibilidades de escalabilidad de la solución, diferenciando las capacidades actualmente implementadas de las mejoras que podrían incorporarse en una arquitectura cloud de mayor capacidad.

## 3. Descripción de la solución CloudTask

### 3.1 Problemática y necesidad identificada
La gestión de actividades y tareas requiere mecanismos que permitan organizar, consultar y actualizar información de manera centralizada y accesible desde diferentes ubicaciones. Cuando esta información se administra únicamente de forma local o mediante mecanismos no centralizados, pueden presentarse dificultades relacionadas con el acceso remoto, la persistencia de los datos, la separación de información entre usuarios y la disponibilidad del servicio.

A partir de esta necesidad se plantea CloudTask como una solución web que centraliza la administración de tareas y permite que cada usuario gestione su propia información mediante autenticación y control de acceso. El sistema proporciona operaciones para crear, consultar, actualizar y eliminar tareas, manteniendo los datos asociados al usuario correspondiente.

El proyecto también responde a la necesidad académica de analizar una aplicación más allá de su funcionamiento básico. Por esta razón, CloudTask se utiliza como caso práctico para estudiar aspectos relacionados con despliegue en la nube, persistencia mediante una base de datos administrada, seguridad de la información, pruebas automatizadas, comportamiento ante diferentes niveles de carga y estrategias de distribución de solicitudes.

De esta manera, la problemática abordada comprende tanto la necesidad funcional de disponer de un sistema centralizado de gestión de tareas como el reto técnico de implementar y evaluar una solución web desplegada en un entorno de computación en la nube.

### 3.2 Descripción general de la aplicación
CloudTask es una aplicación web multiusuario orientada a la administración de tareas personales. Su funcionamiento se basa en un modelo cliente-servidor en el que los usuarios acceden a la aplicación mediante un navegador web y las solicitudes son procesadas por el backend desarrollado con Flask.

El sistema dispone de un módulo de registro que permite crear cuentas de usuario mediante nombre, correo electrónico y contraseña. Las contraseñas no se almacenan en texto plano, sino mediante un hash generado utilizando PBKDF2 con SHA-256. Posteriormente, los usuarios pueden autenticarse para acceder a las funcionalidades protegidas de la aplicación.

Una vez autenticado, cada usuario dispone de un panel desde el cual puede administrar sus tareas. El sistema permite crear, consultar, editar y eliminar tareas, registrando atributos como título, descripción, prioridad, estado y fecha de creación. Cada tarea se encuentra asociada al usuario que la creó, evitando que otros usuarios puedan modificar o eliminar información que no les pertenece.

La aplicación utiliza SQLAlchemy como capa de acceso y abstracción de datos. Durante el desarrollo local puede utilizar una base de datos SQLite, mientras que en el entorno de producción la persistencia se realiza mediante PostgreSQL, cuya conexión se configura mediante variables de entorno.

CloudTask incorpora además un endpoint de comprobación de estado (`/health`) que permite verificar la disponibilidad básica del servicio. En producción, la aplicación es ejecutada mediante Gunicorn y desplegada como un servicio web en Render, mientras que PostgreSQL se utiliza como servicio independiente para la persistencia de la información.

El proyecto complementa las funcionalidades de la aplicación con mecanismos de seguridad, pruebas automatizadas, pruebas de rendimiento y experimentos de distribución de carga, permitiendo evaluar CloudTask no solamente desde una perspectiva funcional, sino también desde aspectos relacionados con seguridad, disponibilidad, rendimiento y escalabilidad.

### 3.3 Justificación del uso de computación en la nube
La computación en la nube resulta adecuada para CloudTask debido a que permite desplegar la aplicación y sus servicios de persistencia sobre infraestructura accesible a través de Internet, evitando depender exclusivamente de un servidor local y facilitando que los usuarios puedan utilizar el sistema desde diferentes ubicaciones mediante un navegador web.

En términos de accesibilidad, el despliegue de CloudTask como servicio web permite disponer de una URL pública protegida mediante HTTPS. De esta manera, la ejecución de la aplicación, la persistencia de la información y el acceso del usuario se integran dentro de una infraestructura remota administrada.

Desde la perspectiva de costos, el prototipo fue desplegado utilizando los recursos gratuitos disponibles en Render, lo que permitió implementar y evaluar la solución sin incurrir en costos de infraestructura durante el desarrollo académico. Este modelo resulta apropiado para prototipos y pruebas de concepto, aunque presenta limitaciones de capacidad, disponibilidad y permanencia de algunos recursos que deben considerarse antes de utilizarlo en un entorno productivo real.

Respecto a la escalabilidad, la arquitectura utilizada permite separar la capa de aplicación de la capa de persistencia, lo que constituye una base para evolucionar hacia configuraciones con múltiples instancias de aplicación, mecanismos de balanceo de carga y recursos de mayor capacidad. Sin embargo, el despliegue realizado para este proyecto utiliza una única instancia web del plan gratuito, por lo que el escalamiento horizontal y el autoescalado no forman parte de la implementación actual.

Para estudiar estos conceptos sin atribuir capacidades inexistentes a la infraestructura desplegada, se desarrollaron pruebas locales de concurrencia y un prototipo experimental de distribución de carga. Estas pruebas permiten analizar el comportamiento de diferentes estrategias y plantear una arquitectura escalable futura manteniendo una separación clara entre las funcionalidades implementadas y las mejoras propuestas.

## 4. Tecnologías y servicios utilizados

### 4.1 Tecnologías de desarrollo
Para la construcción de CloudTask se seleccionaron tecnologías orientadas al desarrollo web, persistencia de datos, seguridad, pruebas y ejecución de aplicaciones Python.

**Python:** lenguaje de programación utilizado para implementar la lógica principal de la aplicación, los modelos de datos, los mecanismos de autenticación y los prototipos experimentales de balanceo de carga.

**Flask:** framework web utilizado para construir el backend de CloudTask, definir las rutas de la aplicación, procesar las solicitudes HTTP y coordinar la interacción entre las diferentes funcionalidades del sistema.

**Flask-SQLAlchemy y SQLAlchemy:** utilizados como capa de abstracción para la persistencia de información. Permiten definir los modelos `Usuario` y `Tarea` y trabajar con diferentes motores de base de datos según el entorno.

**Flask-Login:** utilizado para administrar las sesiones de usuario, proteger rutas que requieren autenticación y obtener la identidad del usuario autenticado.

**Flask-WTF y WTForms:** utilizados para implementar y validar formularios, incluyendo mecanismos de protección contra ataques Cross-Site Request Forgery (CSRF).

**Werkzeug:** proporciona las funciones utilizadas para generar y verificar de forma segura los hashes de las contraseñas mediante PBKDF2 con SHA-256.

**SQLite:** base de datos utilizada durante el desarrollo y las pruebas locales, permitiendo ejecutar la aplicación sin depender de infraestructura externa.

**PostgreSQL:** sistema gestor de base de datos utilizado en el entorno desplegado en la nube para almacenar persistentemente la información de usuarios y tareas.

**Gunicorn:** servidor WSGI utilizado para ejecutar la aplicación Flask en el entorno de producción. También fue utilizado localmente para realizar pruebas controladas de concurrencia con diferente cantidad de procesos worker.

**Pytest:** framework utilizado para automatizar las pruebas funcionales y de seguridad del proyecto, incluyendo las pruebas correspondientes al prototipo de balanceo de carga.

**Locust:** herramienta utilizada para generar carga concurrente sobre el endpoint de comprobación de estado de CloudTask y obtener métricas como cantidad de solicitudes, tasa de fallos, solicitudes por segundo y latencias.

**Git:** sistema de control de versiones utilizado para registrar de forma incremental los cambios realizados durante el desarrollo.

**HTML y CSS:** tecnologías utilizadas para construir la interfaz web presentada a los usuarios mediante el navegador.

### 4.2 Servicios cloud
La infraestructura de CloudTask fue desplegada utilizando servicios administrados de Render, separando la ejecución de la aplicación web de la persistencia de los datos.

**Render Web Service:** aloja y ejecuta la aplicación Flask. El servicio obtiene el código fuente desde el repositorio de GitHub, instala las dependencias definidas en `requirements.txt` y ejecuta la aplicación mediante Gunicorn. El despliegue proporciona una dirección pública para acceder a CloudTask mediante HTTPS.

Para el proyecto se utilizó el plan gratuito disponible durante el desarrollo. La instancia web asignada dispone de recursos limitados y puede entrar en estado de inactividad cuando no recibe solicitudes durante determinado tiempo. Por esta razón, el servicio resulta adecuado para fines académicos y pruebas de concepto, pero estas características deben considerarse como una limitación frente a un entorno productivo de alta disponibilidad.

**Render PostgreSQL:** se utiliza como servicio de base de datos para el entorno desplegado. PostgreSQL almacena la información correspondiente a los usuarios y sus tareas de manera independiente al ciclo de ejecución de la aplicación web.

La conexión entre CloudTask y PostgreSQL se configura mediante la variable de entorno `DATABASE_URL`. Esto evita incorporar las credenciales de conexión directamente en el código fuente y permite utilizar configuraciones diferentes entre los entornos local y cloud.

**Variables de entorno:** Render también se utiliza para administrar parámetros de configuración sensibles o dependientes del entorno. Entre ellos se encuentran `DATABASE_URL`, `SECRET_KEY` y `APP_ENV`. De esta manera, los secretos y datos de conexión no necesitan almacenarse dentro del repositorio público.

La infraestructura utilizada mantiene separadas las responsabilidades principales: el servicio web procesa las solicitudes de los usuarios, mientras que PostgreSQL proporciona la capa de persistencia. Esta separación facilita el mantenimiento de la solución y constituye una base para plantear posteriormente una arquitectura de mayor capacidad.

El despliegue utilizado no debe interpretarse como una infraestructura de alta disponibilidad o autoescalado. La versión implementada para el proyecto utiliza una única instancia web del plan gratuito; las configuraciones con múltiples instancias, balanceadores administrados y escalamiento horizontal se presentan posteriormente como una evolución arquitectónica propuesta.

### 4.3 Control de versiones y despliegue
El código fuente de CloudTask se administra mediante Git como sistema de control de versiones y GitHub como repositorio remoto. Durante el desarrollo se realizaron commits incrementales para conservar la trazabilidad de los cambios relacionados con funcionalidades, seguridad, pruebas, documentación y experimentación con estrategias de balanceo de carga.

La rama principal (`main`) constituye la versión utilizada como referencia para el despliegue. Una vez validados localmente los cambios, estos se incorporan mediante commits y posteriormente se sincronizan con el repositorio remoto utilizando Git.

El servicio web de Render se encuentra vinculado con el repositorio de GitHub y tiene habilitado el mecanismo de despliegue automático. De esta manera, los cambios enviados a la rama principal pueden iniciar un nuevo proceso de construcción y despliegue de CloudTask.

Durante este proceso, Render obtiene el código fuente, instala las dependencias especificadas en `requirements.txt` y ejecuta la aplicación mediante el comando de inicio configurado con Gunicorn. Las variables sensibles y los parámetros propios del entorno de producción se mantienen separados del código mediante variables de entorno.

Este flujo establece una secuencia de trabajo compuesta por desarrollo local, validación mediante pruebas, control de versiones, publicación en GitHub y despliegue en la infraestructura cloud. Además de facilitar la actualización de la aplicación, el historial de Git proporciona evidencia de la evolución técnica del proyecto y permite identificar las modificaciones realizadas durante cada etapa.

Como medida de control, antes de incorporar cambios relevantes se ejecutaron pruebas automatizadas y se verificó el estado del repositorio. Al finalizar la fase principal de implementación y pruebas, la suite completa alcanzó 24 pruebas automatizadas aprobadas sin fallos.

## 5. Arquitectura de la solución

### 5.1 Arquitectura implementada
La arquitectura implementada en CloudTask sigue un modelo web cliente-servidor con separación entre la capa de presentación, la lógica de aplicación y la persistencia de datos. La solución combina componentes ejecutados en el navegador del usuario con servicios desplegados en la infraestructura cloud de Render.

El flujo general de la arquitectura implementada puede representarse de la siguiente manera:

**Usuario / Navegador web → HTTPS → Render Web Service → Gunicorn → Aplicación Flask → SQLAlchemy → PostgreSQL**

**1. Cliente web:**  
El usuario accede a CloudTask desde un navegador mediante la URL pública de la aplicación. La interfaz desarrollada con HTML y CSS permite interactuar con las funciones de registro, autenticación y administración de tareas.

**2. Comunicación mediante HTTPS:**  
Las solicitudes entre el navegador y el servicio desplegado se realizan mediante HTTPS, proporcionando cifrado para los datos transmitidos entre el cliente y la infraestructura cloud.

**3. Render Web Service:**  
Render aloja la instancia web de CloudTask y proporciona el entorno de ejecución utilizado por la aplicación. El servicio recibe las solicitudes provenientes de Internet y ejecuta el backend de la solución.

**4. Gunicorn:**  
La aplicación Flask se ejecuta mediante Gunicorn como servidor WSGI. En el entorno gratuito utilizado durante el proyecto, la configuración observada en producción asignó un único worker de Gunicorn de acuerdo con los recursos disponibles en la instancia.

**5. Aplicación Flask:**  
Flask contiene la lógica principal del sistema. Esta capa procesa las solicitudes HTTP, administra la autenticación, aplica controles de acceso, valida formularios, ejecuta las operaciones correspondientes a las tareas y genera las respuestas enviadas al navegador.

**6. SQLAlchemy:**  
La capa de persistencia utiliza SQLAlchemy para representar y administrar los modelos de datos de la aplicación. Esta abstracción permite utilizar SQLite durante el desarrollo local y PostgreSQL en el entorno desplegado.

**7. PostgreSQL:**  
La base de datos PostgreSQL desplegada como servicio independiente almacena persistentemente la información correspondiente a usuarios y tareas. La aplicación obtiene los parámetros de conexión mediante la variable de entorno `DATABASE_URL`.

Adicionalmente, CloudTask utiliza variables de entorno para separar la configuración sensible del código fuente. Parámetros como `SECRET_KEY`, `DATABASE_URL` y `APP_ENV` son administrados en el entorno de despliegue y no se incorporan directamente al repositorio.

La arquitectura implementada mantiene, por tanto, una separación lógica entre cliente, aplicación y persistencia. Aunque el prototipo utiliza una única instancia web, esta separación permite plantear posteriormente una evolución hacia una arquitectura con múltiples instancias, balanceo de carga y mecanismos adicionales de alta disponibilidad.

### 5.2 Flujo de funcionamiento
El funcionamiento de CloudTask se basa en un flujo de solicitudes y respuestas entre el usuario, la aplicación web y la base de datos.

Cuando un usuario accede a CloudTask, el navegador establece una conexión HTTPS con el servicio web desplegado en Render. La solicitud es recibida por la infraestructura cloud y posteriormente procesada por Gunicorn, encargado de ejecutar la aplicación Flask.

Flask identifica la ruta solicitada y aplica la lógica correspondiente. En las rutas protegidas, Flask-Login verifica que exista una sesión autenticada antes de permitir el acceso. Cuando la operación utiliza un formulario, Flask-WTF realiza las validaciones definidas y comprueba el token CSRF correspondiente a las solicitudes que modifican información.

Para las operaciones que requieren consultar o modificar datos, la aplicación utiliza SQLAlchemy como capa de acceso a la base de datos. En producción, las consultas son ejecutadas sobre PostgreSQL mediante la conexión configurada a través de `DATABASE_URL`.

El flujo simplificado de una operación autenticada puede representarse de la siguiente manera:

**1.** El usuario realiza una acción desde el navegador.  
**2.** La solicitud se transmite mediante HTTPS.  
**3.** Render recibe la solicitud y la dirige al servicio web.  
**4.** Gunicorn entrega la solicitud a la aplicación Flask.  
**5.** Flask verifica autenticación, autorización y validaciones aplicables.  
**6.** SQLAlchemy realiza la operación requerida sobre PostgreSQL.  
**7.** PostgreSQL devuelve el resultado a la aplicación.  
**8.** Flask genera la respuesta correspondiente.  
**9.** La respuesta regresa mediante HTTPS al navegador del usuario.

En las operaciones relacionadas con tareas se aplica adicionalmente un control de propiedad. La aplicación consulta los registros asociados al usuario autenticado y evita que un usuario pueda editar o eliminar directamente una tarea perteneciente a otra cuenta.

CloudTask también dispone del endpoint `/health`, cuya finalidad es proporcionar una comprobación básica del estado del servicio sin requerir autenticación. Este endpoint fue utilizado durante las pruebas de disponibilidad, concurrencia y generación de carga debido a que permite evaluar la respuesta del servicio mediante una operación ligera y reproducible.

### 5.3 Persistencia de datos
La persistencia de CloudTask fue diseñada para mantener separada la lógica de la aplicación del sistema gestor de base de datos. Para ello se utiliza SQLAlchemy como capa de abstracción, permitiendo configurar diferentes motores de almacenamiento dependiendo del entorno de ejecución.

Durante el desarrollo local, CloudTask utiliza SQLite. Esta configuración facilita la ejecución, depuración y realización de pruebas sin depender permanentemente de un servicio externo.

En el entorno desplegado en la nube, la aplicación utiliza PostgreSQL como sistema gestor de base de datos. La conexión se establece mediante la variable de entorno `DATABASE_URL`, suministrada al servicio web desde la configuración del entorno de Render. De esta manera, los datos de conexión no necesitan incorporarse directamente al código fuente.

El modelo de datos principal está compuesto por las entidades `Usuario` y `Tarea`. La entidad `Usuario` almacena la información necesaria para identificar y autenticar las cuentas, mientras que `Tarea` contiene los datos asociados a las actividades administradas por cada usuario.

Cada tarea mantiene una relación con el usuario propietario mediante `usuario_id`, estableciendo una asociación entre ambas entidades. Esta relación también es utilizada por la lógica de aplicación para restringir las operaciones sobre tareas al usuario autenticado correspondiente.

De forma simplificada, el modelo puede representarse como:

**Usuario (1) ───────── (N) Tarea**

Esto significa que un usuario puede disponer de múltiples tareas, mientras que cada tarea pertenece a un único usuario.

La separación entre la instancia web y PostgreSQL permite que la persistencia no dependa del almacenamiento local del proceso que ejecuta Flask. Este aspecto es especialmente relevante en entornos cloud, donde las instancias de aplicación pueden reiniciarse, reemplazarse o evolucionar hacia configuraciones con múltiples procesos o instancias.

Para un entorno productivo de mayor criticidad sería necesario complementar esta arquitectura con políticas formales de copias de seguridad, restauración, recuperación ante desastres y objetivos RPO/RTO. Estas capacidades se consideran mejoras futuras y no se presentan como funcionalidades implementadas en el prototipo actual.

### 5.4 Arquitectura escalable propuesta
La arquitectura actualmente desplegada de CloudTask utiliza una única instancia web, por lo que no implementa escalamiento horizontal automático. Sin embargo, la separación existente entre aplicación y persistencia permite plantear una evolución hacia una arquitectura distribuida capaz de atender mayores niveles de demanda.

La arquitectura escalable propuesta puede representarse conceptualmente de la siguiente manera:

**Usuarios → HTTPS → Balanceador de carga → Múltiples instancias CloudTask → PostgreSQL administrado**

En esta arquitectura, un balanceador de carga recibiría las solicitudes de los usuarios y las distribuiría entre múltiples instancias de la aplicación. Las instancias ejecutarían la misma versión de CloudTask y utilizarían una capa de persistencia compartida, evitando que la información dependa de una instancia específica.

El número de instancias podría ajustarse según métricas operativas como utilización de CPU, memoria, cantidad de solicitudes, latencia o número de conexiones activas. De esta manera, una plataforma cloud con soporte para escalamiento horizontal podría incrementar o reducir la capacidad disponible de acuerdo con la demanda.

La distribución de solicitudes podría realizarse inicialmente mediante estrategias tradicionales como Round Robin. Para escenarios en los que los nodos presenten niveles de utilización diferentes, podrían evaluarse mecanismos adaptativos que consideren información sobre el estado de los recursos antes de seleccionar el destino de una nueva solicitud.

Como parte del proyecto se desarrolló un prototipo experimental independiente de la infraestructura de producción para estudiar este comportamiento. El experimento compara Round Robin con una estrategia adaptativa que selecciona nodos teniendo en cuenta su porcentaje de carga y capacidad disponible. Los resultados de estas pruebas se presentan posteriormente y no deben interpretarse como un balanceador desplegado actualmente en Render.

Una evolución de mayor capacidad también podría incorporar servicios adicionales como almacenamiento de sesiones compartidas, caché distribuida, monitoreo centralizado, alertas, copias de seguridad automatizadas, mecanismos de recuperación ante desastres y políticas de escalamiento basadas en métricas.

Por tanto, se distinguen dos niveles dentro del proyecto: una **arquitectura implementada**, utilizada para ejecutar y validar CloudTask en la nube, y una **arquitectura escalable propuesta**, diseñada conceptualmente a partir de los resultados obtenidos y de los principios de computación distribuida estudiados.

## 6. Implementación técnica

### 6.1 Gestión de usuarios
CloudTask implementa un sistema de gestión de usuarios que permite registrar cuentas, autenticar credenciales, mantener sesiones y restringir el acceso a funcionalidades protegidas.

Durante el registro, el usuario proporciona su nombre, correo electrónico y contraseña. Los datos son validados mediante formularios implementados con Flask-WTF y WTForms. Entre las validaciones se incluyen la obligatoriedad de los campos, validación del formato del correo electrónico, longitud mínima de la contraseña y comprobación de coincidencia entre la contraseña y su confirmación.

El correo electrónico funciona como identificador único de la cuenta. Antes de completar un registro, la aplicación comprueba que no exista previamente otro usuario con la misma dirección de correo, evitando la creación de cuentas duplicadas.

Las contraseñas no se almacenan en texto plano. Antes de guardarlas en la base de datos se genera un hash utilizando PBKDF2 con SHA-256 y un número elevado de iteraciones. Durante el inicio de sesión, la contraseña proporcionada por el usuario se verifica contra el hash almacenado, evitando la necesidad de recuperar o comparar contraseñas en texto plano.

La administración de sesiones se realiza mediante Flask-Login. Una vez autenticado, el usuario puede acceder a las rutas protegidas de CloudTask y la aplicación puede identificarlo mediante `current_user`. Las rutas que requieren autenticación utilizan el mecanismo `login_required`.

El cierre de sesión se implementó mediante una solicitud HTTP POST protegida por CSRF. Esta decisión evita utilizar una operación GET para modificar el estado de autenticación y proporciona una protección adicional frente a solicitudes no autorizadas.

La gestión de usuarios constituye también la base del control de acceso sobre las tareas, debido a que cada registro se encuentra asociado al identificador del usuario propietario. De esta forma, la autenticación no solamente permite iniciar una sesión, sino que también determina qué información puede consultar y modificar cada cuenta.

### 6.2 Gestión de tareas
CloudTask implementa las operaciones fundamentales de creación, consulta, actualización y eliminación de tareas (CRUD), disponibles para los usuarios autenticados.

Cada tarea almacena un título, descripción, prioridad, estado, fecha de creación y el identificador del usuario propietario. Los niveles de prioridad disponibles son Baja, Media y Alta, mientras que el estado permite clasificar las tareas como Pendiente, En progreso o Completada.

Durante la creación de una tarea, Flask-WTF valida los datos recibidos antes de realizar la operación sobre la base de datos. El título es obligatorio y debe cumplir los límites de longitud establecidos, mientras que la descripción dispone igualmente de una longitud máxima. La prioridad y el estado se seleccionan a partir de valores previamente definidos.

Una vez creada, la tarea queda asociada al usuario autenticado mediante `usuario_id`. Esta relación permite que el panel de cada cuenta muestre únicamente la información correspondiente a su propietario.

Las operaciones de edición y eliminación incorporan controles de autorización. La aplicación comprueba que la tarea solicitada pertenezca al usuario autenticado antes de permitir su modificación. Cuando un usuario intenta acceder directamente a una tarea perteneciente a otra cuenta, la aplicación no autoriza la operación.

Las acciones que modifican información se realizan mediante solicitudes protegidas con tokens CSRF, reduciendo el riesgo de que operaciones sensibles sean ejecutadas desde solicitudes externas no autorizadas.

El comportamiento del módulo fue verificado mediante pruebas automatizadas que comprueban la creación, edición y eliminación de tareas, además de escenarios en los que un usuario intenta modificar o eliminar información perteneciente a otra cuenta.

De esta manera, el CRUD de tareas no solamente proporciona las funcionalidades principales de CloudTask, sino que integra validación, autenticación, autorización y protección de las operaciones que modifican el estado del sistema.

### 6.3 Persistencia y configuración por entorno
CloudTask utiliza una configuración diferenciada según el entorno de ejecución, permitiendo trabajar localmente con recursos simples y utilizar servicios cloud durante el despliegue.

La dirección de conexión a la base de datos se obtiene mediante la variable de entorno `DATABASE_URL`. Cuando esta variable no se encuentra definida, la aplicación utiliza SQLite como alternativa para el entorno local. En producción, `DATABASE_URL` contiene la configuración necesaria para establecer la conexión con PostgreSQL.

La aplicación también obtiene `SECRET_KEY` mediante una variable de entorno. Esta clave es utilizada por Flask para proteger información relacionada con las sesiones y los mecanismos que dependen de la firma criptográfica. De esta forma, el valor utilizado en producción permanece separado del código fuente y del repositorio público.

La variable `APP_ENV` permite identificar el entorno de producción y activar configuraciones específicas. Entre ellas se encuentra el atributo `Secure` de las cookies de sesión y el encabezado HTTP Strict-Transport-Security (HSTS).

Esta estrategia permite mantener una misma base de código mientras determinados parámetros cambian según el entorno:

- **Desarrollo local:** SQLite y configuración orientada a desarrollo y pruebas.
- **Producción:** PostgreSQL, secretos administrados mediante variables de entorno, cookies seguras y controles HTTP adicionales.

La separación entre código y configuración reduce la exposición accidental de credenciales, facilita el despliegue en diferentes entornos y evita depender de valores sensibles incorporados directamente en los archivos versionados.

Durante el desarrollo también se realizó la rotación de la clave secreta configurada en el entorno cloud después de identificar que un valor anterior había quedado expuesto durante el proceso de verificación. Esta acción permitió aplicar de manera práctica el principio de sustitución de credenciales ante una posible exposición.

### 6.4 Despliegue en la nube
El despliegue de CloudTask se realizó en Render utilizando un servicio web conectado al repositorio del proyecto alojado en GitHub. Esta integración permite mantener un flujo de despliegue asociado al control de versiones de la aplicación.

El proceso de construcción del servicio utiliza el archivo `requirements.txt` para instalar las dependencias necesarias mediante el comando:

`pip install -r requirements.txt`

Una vez finalizada la construcción, CloudTask se inicia mediante Gunicorn utilizando el comando:

`gunicorn app:app`

Durante la ejecución en Render, Gunicorn actúa como servidor WSGI entre la infraestructura web y la aplicación Flask. Los registros de despliegue permitieron comprobar el inicio correcto del servidor y la disponibilidad posterior del servicio.

La aplicación desplegada puede ser accedida públicamente mediante HTTPS. Además, el endpoint `/health` permite realizar una comprobación básica del funcionamiento del servicio y fue utilizado como mecanismo de verificación después de diferentes despliegues.

El servicio web mantiene configuradas las variables de entorno requeridas por la aplicación, incluyendo la conexión con PostgreSQL, la clave secreta y la identificación del entorno de producción. Los valores sensibles no se almacenan dentro del repositorio.

El repositorio de GitHub se encuentra vinculado al servicio de Render mediante despliegue automático desde la rama `main`. Por tanto, después de validar y publicar un cambio en dicha rama, Render puede iniciar automáticamente un nuevo proceso de construcción y despliegue.

Durante el proyecto se verificó este flujo mediante diferentes actualizaciones del código fuente, comprobando posteriormente tanto el estado del despliegue como la respuesta del endpoint `/health`.

La infraestructura utilizada corresponde a recursos gratuitos adecuados para demostración y evaluación académica. En consecuencia, características como escalamiento horizontal automático, múltiples instancias de producción y alta disponibilidad no forman parte del despliegue implementado y se consideran elementos de una arquitectura futura.

### 6.5 Manejo de errores y disponibilidad
CloudTask incorpora mecanismos básicos para manejar errores de forma controlada y proporcionar información sobre el estado operativo de la aplicación.

Se implementaron manejadores personalizados para los códigos HTTP 400, 404 y 500. Estos permiten responder de manera controlada ante solicitudes inválidas, recursos inexistentes y errores internos del servidor, evitando depender exclusivamente de las páginas de error predeterminadas del framework.

El error HTTP 400 también forma parte del comportamiento esperado de determinados controles de seguridad. Por ejemplo, cuando una solicitud POST protegida no contiene un token CSRF válido, Flask-WTF rechaza la operación y la aplicación devuelve una respuesta 400.

Para los errores internos HTTP 500 se ejecuta adicionalmente `db.session.rollback()`. Esta operación permite revertir una transacción pendiente de SQLAlchemy cuando se produce un error durante una operación con la base de datos, evitando conservar una sesión transaccional en un estado inconsistente.

CloudTask dispone además del endpoint:

`/health`

Este endpoint devuelve una respuesta HTTP 200 cuando la aplicación puede procesar correctamente la solicitud e incluye información básica del servicio. Durante las pruebas también se incorporó el identificador del proceso worker que atendió la petición, lo que permitió observar la distribución de solicitudes durante los experimentos locales de concurrencia con Gunicorn.

El endpoint `/health` fue utilizado para:

- comprobar la disponibilidad básica de CloudTask después de los despliegues;
- verificar la respuesta HTTP del entorno de producción;
- realizar pruebas de carga reproducibles con Locust;
- observar la distribución de solicitudes entre procesos Gunicorn durante las pruebas locales.

Este mecanismo constituye una comprobación básica de disponibilidad de la aplicación y no debe confundirse con una plataforma completa de observabilidad. Una solución productiva de mayor criticidad debería complementarse con monitoreo continuo, métricas centralizadas, registros agregados, alertas y comprobaciones específicas sobre las dependencias críticas.

Las pruebas realizadas confirmaron que los manejadores de error, el endpoint de salud y los controles relacionados continúan funcionando junto con el resto de las funcionalidades de CloudTask. Al finalizar la fase de implementación, la suite completa alcanzó 24 pruebas automatizadas aprobadas sin fallos.

## 7. Seguridad y protección de la información

### 7.1 Modelo de responsabilidad compartida
La seguridad de CloudTask se aborda considerando el modelo de responsabilidad compartida propio de los servicios de computación en la nube. Bajo este enfoque, la protección de la solución no depende exclusivamente del proveedor cloud ni únicamente del desarrollador, sino que las responsabilidades se distribuyen de acuerdo con los componentes administrados por cada parte.

En la infraestructura utilizada para CloudTask, Render proporciona y administra elementos de la plataforma subyacente necesarios para ejecutar el servicio web y PostgreSQL. Por su parte, el proyecto mantiene la responsabilidad sobre la seguridad de la aplicación, su código, la configuración utilizada, las credenciales, el control de acceso y el tratamiento de los datos gestionados por el sistema.

Dentro de las responsabilidades asumidas a nivel de aplicación se encuentran:

- implementar mecanismos de autenticación y autorización;
- proteger las contraseñas almacenadas;
- evitar la inclusión de secretos y credenciales directamente en el código fuente;
- configurar adecuadamente las sesiones y cookies;
- proteger las operaciones sensibles frente a ataques CSRF;
- validar los datos recibidos mediante formularios;
- incorporar encabezados HTTP de seguridad;
- controlar el acceso de cada usuario a sus propios recursos;
- mantener actualizadas y verificadas las configuraciones utilizadas por la aplicación;
- realizar pruebas para comprobar el funcionamiento de los controles implementados.

El proveedor cloud, por otra parte, administra componentes de infraestructura que no son controlados directamente desde el código de CloudTask, incluyendo aspectos asociados con la plataforma física y los servicios administrados utilizados para alojar la aplicación y la base de datos.

La adopción de este modelo permite evitar la interpretación incorrecta de que el simple hecho de desplegar una aplicación en la nube garantiza automáticamente su seguridad. CloudTask incorpora controles en la capa que corresponde al desarrollo y configuración de la aplicación, mientras que otros mecanismos de infraestructura dependen de las capacidades ofrecidas por el proveedor seleccionado.

Esta distribución de responsabilidades se encuentra alineada con los conceptos de seguridad en computación en la nube estudiados en la guía de la unidad, donde la responsabilidad compartida constituye un elemento relevante para identificar qué controles corresponden al proveedor y cuáles deben ser administrados por el cliente o desarrollador de la solución.

### 7.2 Autenticación y control de acceso
CloudTask aplica mecanismos de autenticación y autorización para restringir el acceso a las funcionalidades y evitar que un usuario pueda operar sobre información perteneciente a otra cuenta.

La autenticación se implementa mediante Flask-Login. Cuando el usuario proporciona sus credenciales, la aplicación localiza la cuenta asociada al correo electrónico y verifica la contraseña utilizando el hash almacenado. Si las credenciales son válidas, se establece una sesión autenticada.

Las rutas que contienen funcionalidades privadas utilizan `login_required`, impidiendo el acceso de usuarios que no hayan iniciado sesión. De esta manera, operaciones como consultar el panel de tareas, crear registros, editar información o eliminar tareas requieren previamente una identidad autenticada.

La autorización se aplica adicionalmente a nivel de recurso. Cada tarea se encuentra asociada al identificador de su propietario mediante `usuario_id`. Antes de permitir operaciones de modificación o eliminación, CloudTask verifica que el recurso solicitado corresponda al usuario autenticado.

Este mecanismo fue validado mediante pruebas automatizadas específicas. Se comprobó que:

- un usuario no autenticado no puede acceder directamente al panel protegido;
- un usuario autenticado puede crear, editar y eliminar sus propias tareas;
- un usuario no puede editar una tarea perteneciente a otra cuenta;
- un usuario no puede eliminar una tarea perteneciente a otra cuenta.

En los intentos de acceso a tareas de otros usuarios, la aplicación responde como recurso no disponible para la cuenta solicitante, evitando autorizar la operación.

Estos controles aplican el principio de mínimo privilegio a nivel de la aplicación: una cuenta recibe acceso únicamente a las funcionalidades autorizadas y a los recursos que le pertenecen. El control de acceso se combina con la autenticación, la gestión de sesiones y las demás medidas de seguridad implementadas para proporcionar protección por capas.

### 7.3 Protección de contraseñas y secretos
CloudTask aplica mecanismos diferenciados para proteger las contraseñas de los usuarios y los secretos utilizados por la aplicación.

Las contraseñas no se almacenan en texto plano. Al crear una cuenta, la aplicación utiliza las funciones de seguridad proporcionadas por Werkzeug para generar un hash mediante PBKDF2 con SHA-256. La configuración implementada utiliza 600.000 iteraciones, incrementando el costo computacional requerido para intentar obtener una contraseña a partir de su hash.

Durante la autenticación, CloudTask no descifra la contraseña almacenada. En su lugar, verifica la contraseña proporcionada por el usuario utilizando el mecanismo de comprobación de hashes correspondiente.

Los secretos de configuración reciben un tratamiento diferente. Valores como `SECRET_KEY` y la información de conexión contenida en `DATABASE_URL` se administran mediante variables de entorno en Render, evitando incorporarlos directamente al repositorio público de GitHub.

Esta separación entre código y secretos reduce el riesgo de exposición accidental mediante el control de versiones y permite sustituir las credenciales sin modificar el código fuente de la aplicación.

Durante el desarrollo se identificó la exposición accidental de una clave utilizada previamente en el entorno cloud. Como medida correctiva, dicha clave fue reemplazada mediante una rotación del secreto en la configuración de Render. El nuevo valor se mantuvo fuera del código fuente y no se incorporó a la documentación ni a las evidencias públicas.

Esta experiencia permitió aplicar de forma práctica un principio fundamental de gestión de secretos: una credencial potencialmente expuesta no debe continuar considerándose segura, por lo que debe ser sustituida y mantenerse posteriormente en un mecanismo de configuración independiente del código.

La protección de contraseñas, la separación de secretos y la rotación de credenciales se complementan con los demás controles de CloudTask para reducir el riesgo asociado con el acceso no autorizado a cuentas y recursos de la aplicación.

### 7.4 Protección CSRF
CloudTask incorpora protección frente a ataques Cross-Site Request Forgery (CSRF) mediante Flask-WTF y el componente `CSRFProtect`.

Este tipo de ataque busca conseguir que el navegador de un usuario autenticado envíe una solicitud no deseada hacia una aplicación aprovechando la sesión existente. Para reducir este riesgo, las operaciones que modifican el estado de CloudTask requieren un token CSRF válido.

Los formularios utilizados para registro, autenticación y administración de tareas integran el token correspondiente. Asimismo, las operaciones sensibles implementadas mediante solicitudes POST, como la eliminación de tareas y el cierre de sesión, se encuentran protegidas por este mecanismo.

La protección se aplica globalmente mediante:

`csrf = CSRFProtect(app)`

Durante las pruebas automatizadas se verificó explícitamente el funcionamiento de este control enviando una solicitud POST sin un token CSRF válido. La aplicación rechazó correctamente la solicitud mediante una respuesta HTTP 400.

También se modificó el mecanismo de cierre de sesión para utilizar exclusivamente el método POST en lugar de GET. Como comprobación adicional, una solicitud GET dirigida a `/logout` fue rechazada con el código HTTP 405 (Method Not Allowed), confirmando que el cierre de sesión no puede activarse mediante una navegación GET convencional.

La combinación de tokens CSRF, solicitudes POST para operaciones que modifican estado y validación de métodos HTTP proporciona una capa adicional de protección frente a solicitudes generadas desde contextos externos no autorizados.

### 7.5 Cookies y sesiones
CloudTask incorpora configuraciones específicas para fortalecer la protección de las cookies utilizadas durante la gestión de sesiones autenticadas.

La configuración `SESSION_COOKIE_HTTPONLY` se encuentra habilitada. Este atributo evita que la cookie de sesión pueda ser accedida directamente mediante código JavaScript ejecutado en el navegador, reduciendo la exposición de la sesión frente a determinados escenarios de ejecución de scripts maliciosos.

También se configura `SESSION_COOKIE_SAMESITE` con el valor `Lax`. Esta política restringe el envío de la cookie en determinados contextos entre sitios y complementa la protección proporcionada por los tokens CSRF.

En el entorno identificado como producción se habilita adicionalmente:

`SESSION_COOKIE_SECURE = True`

El atributo `Secure` indica al navegador que la cookie de sesión debe transmitirse únicamente mediante conexiones HTTPS, evitando su envío a través de conexiones HTTP sin cifrar.

Por tanto, la configuración utilizada combina tres propiedades principales:

- **HttpOnly:** restringe el acceso a la cookie desde JavaScript.
- **SameSite=Lax:** limita determinados envíos de la cookie entre sitios.
- **Secure:** exige HTTPS para la transmisión de la cookie en producción.

Estas medidas se complementan con la autenticación mediante Flask-Login, la protección CSRF y el uso de HTTPS, proporcionando diferentes capas de protección para las sesiones de usuario.

La configuración diferencia además el entorno local del entorno de producción. El atributo `Secure` se activa cuando `APP_ENV` identifica el entorno productivo, permitiendo mantener una configuración compatible con el desarrollo local mientras se aplica una política más restrictiva en el servicio desplegado.

### 7.6 HTTPS y encabezados de seguridad
CloudTask complementa los controles implementados a nivel de aplicación con el uso de HTTPS y diferentes encabezados HTTP orientados a fortalecer la seguridad del navegador.

El servicio desplegado en Render es accesible mediante HTTPS, permitiendo que la comunicación entre el navegador y la aplicación se realice utilizando un canal cifrado. En el entorno de producción se incorpora además el encabezado HTTP Strict-Transport-Security (HSTS):

`Strict-Transport-Security: max-age=31536000; includeSubDomains`

Este encabezado indica al navegador que debe utilizar conexiones HTTPS durante el periodo definido por la política.

CloudTask incorpora adicionalmente los siguientes encabezados:

**Content-Security-Policy (CSP):** establece restricciones sobre los recursos que pueden ser cargados por la aplicación. La política implementada limita por defecto los recursos al mismo origen y establece restricciones adicionales para estilos, formularios, inclusión en marcos y definición de la URL base.

**X-Content-Type-Options: nosniff:** evita que el navegador intente interpretar un recurso utilizando un tipo MIME diferente al declarado.

**X-Frame-Options: DENY:** impide que CloudTask sea cargado dentro de frames, proporcionando protección frente a determinados ataques de clickjacking.

**Referrer-Policy: strict-origin-when-cross-origin:** limita la información enviada mediante el encabezado `Referer` cuando se realizan solicitudes hacia otros orígenes.

**Permissions-Policy:** deshabilita para la aplicación el acceso a capacidades del navegador que CloudTask no necesita, específicamente cámara, micrófono y geolocalización.

La política CSP utilizada en la implementación establece:

`default-src 'self'; style-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'`

Mientras que la política de permisos establece:

`camera=(), microphone=(), geolocation=()`

Estos controles fueron verificados mediante solicitudes HTTP realizadas contra el endpoint `/health` de la aplicación desplegada. La respuesta de producción confirmó la presencia de HSTS, CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy y Permissions-Policy.

La existencia de estos encabezados también forma parte de las pruebas automatizadas del proyecto, permitiendo comprobar que cambios posteriores en el código no eliminen accidentalmente los controles configurados.

### 7.7 Aplicación de lineamientos MinTIC
La implementación de CloudTask tomó como referencia los principios y controles de seguridad en computación en la nube estudiados durante la unidad y la Guía técnica de computación en la nube de MinTIC (2021). Su aplicación se realizó de acuerdo con el alcance académico del prototipo y con las responsabilidades correspondientes a la capa de aplicación.

Entre los principios considerados se encuentra el modelo de responsabilidad compartida. CloudTask diferencia los componentes administrados por el proveedor cloud de aquellos que continúan siendo responsabilidad del desarrollador, como la autenticación, autorización, gestión de secretos, configuración de sesiones y protección de los datos utilizados por la aplicación.

En materia de identidad y acceso se implementaron mecanismos de autenticación y autorización, protección de rutas y separación de los recursos pertenecientes a cada usuario. Estos controles se relacionan con el principio de mínimo privilegio, debido a que una cuenta solamente puede acceder a las funcionalidades autorizadas y a las tareas asociadas con su propia identidad.

La protección de credenciales y secretos se abordó mediante hashing de contraseñas, variables de entorno y rotación de una clave que había sido potencialmente expuesta. De esta forma, las credenciales sensibles se mantienen separadas del código fuente y del repositorio público.

Para la protección de las comunicaciones se utiliza HTTPS y, en producción, HSTS. Asimismo, se incorporaron configuraciones seguras de cookies, protección CSRF y encabezados HTTP orientados a reducir diferentes vectores de ataque desde el navegador.

La validación de los controles se realizó mediante pruebas automatizadas y verificaciones directas sobre la aplicación desplegada. Estas pruebas permiten conservar evidencia reproducible de mecanismos como autenticación, autorización entre usuarios, rechazo de solicitudes sin token CSRF, encabezados de seguridad y comportamiento de HSTS en producción.

No obstante, CloudTask constituye un prototipo académico y no representa una implementación integral de todos los controles que podrían requerirse en una infraestructura productiva. Elementos como autenticación multifactor, gestión centralizada de registros, alertas, copias de seguridad automatizadas, definición formal de RPO y RTO, auditorías periódicas, herramientas CSPM, WAF y un procedimiento completo de respuesta a incidentes fueron identificados como mejoras futuras.

Por lo tanto, el proyecto no afirma una certificación ni un cumplimiento integral de todos los controles posibles. En su lugar, demuestra la aplicación práctica y verificable de un conjunto de medidas de seguridad coherentes con los principios estudiados para entornos de computación en la nube.

## 8. Escalabilidad y balanceo dinámico de carga

### 8.1 Estrategia de concurrencia
CloudTask utiliza Gunicorn como servidor WSGI para ejecutar la aplicación Flask. Gunicorn permite utilizar múltiples procesos worker, haciendo posible que diferentes solicitudes sean atendidas por procesos independientes dentro de una misma instancia de ejecución.

En el entorno de producción desplegado mediante el plan gratuito de Render, los registros del servicio indicaron que Gunicorn configuró un único worker de acuerdo con los recursos de CPU disponibles. Por esta razón, la implementación cloud actual no debe considerarse una configuración con múltiples workers ni un sistema de escalamiento horizontal.

Para estudiar experimentalmente el efecto de la concurrencia se realizaron pruebas locales utilizando Gunicorn con uno y dos workers. El endpoint `/health` fue configurado para devolver el identificador del proceso que atendía cada solicitud, permitiendo comprobar que, al utilizar dos workers, las solicitudes podían ser procesadas por procesos diferentes.

Posteriormente se realizaron pruebas de carga con Locust utilizando 100 usuarios concurrentes sobre el endpoint `/health`. La configuración con dos workers procesó 1.431 solicitudes sin fallos y alcanzó aproximadamente 47,94 solicitudes por segundo. La configuración con un worker procesó 1.447 solicitudes sin fallos y alcanzó aproximadamente 48,48 solicitudes por segundo.

Los resultados muestran que, bajo este escenario específico, incrementar de uno a dos workers no produjo una mejora significativa en el throughput. Sin embargo, sí se observó una reducción de las latencias de cola: el percentil 95 pasó aproximadamente de 22 ms a 14 ms, el percentil 99 de 28 ms a 20 ms y la latencia máxima observada de aproximadamente 178 ms a 70 ms.

Estos resultados no demuestran escalamiento horizontal, debido a que ambos experimentos se realizaron localmente sobre una misma máquina. La evidencia demuestra únicamente distribución de solicitudes entre procesos Gunicorn y una mejora en las latencias extremas bajo las condiciones concretas de la prueba.

La prueba permite diferenciar tres conceptos relevantes para el análisis de CloudTask: concurrencia mediante múltiples procesos dentro de una instancia, distribución de carga entre recursos y escalamiento horizontal mediante múltiples instancias. Solamente el primero fue comprobado directamente con Gunicorn, mientras que la distribución adaptativa se estudió mediante un prototipo experimental y el escalamiento horizontal se plantea como evolución arquitectónica.

### 8.2 Balanceo Round Robin
Round Robin fue utilizado como estrategia de referencia para los experimentos de distribución de carga realizados en CloudTask. Su funcionamiento consiste en recorrer secuencialmente el conjunto de nodos disponibles e intentar asignar cada nueva tarea al siguiente nodo correspondiente.

En el prototipo desarrollado, cada nodo dispone de una capacidad máxima y mantiene información sobre su carga actual. Antes de realizar una asignación, el balanceador verifica si el nodo seleccionado dispone de capacidad suficiente para recibir la nueva carga.

Si el nodo correspondiente al turno no dispone de capacidad, el algoritmo continúa evaluando los demás nodos hasta encontrar uno que pueda recibir la tarea. Cuando ninguno dispone de capacidad suficiente, la solicitud se considera rechazada.

De forma simplificada, el procedimiento utilizado es:

1. seleccionar el siguiente nodo de acuerdo con el orden circular;
2. comprobar si dispone de capacidad para recibir la carga;
3. asignar la tarea cuando existe capacidad;
4. continuar con el siguiente nodo para la próxima solicitud;
5. rechazar la tarea cuando ningún nodo dispone de capacidad suficiente.

Round Robin presenta como ventaja su simplicidad y un costo reducido para seleccionar el destino de las solicitudes. Sin embargo, la decisión no utiliza directamente el porcentaje de carga actual de cada nodo para determinar cuál constituye el destino más conveniente.

Esta característica permitió utilizarlo como línea base para comparar el comportamiento del balanceador adaptativo. Ambos algoritmos fueron sometidos a los mismos escenarios y capacidades, permitiendo analizar diferencias en tareas asignadas, tareas rechazadas, tasa de rechazo, desequilibrio entre nodos y carga máxima observada.

Las pruebas automatizadas verificaron adicionalmente que la implementación de Round Robin distribuye las selecciones secuencialmente, omite nodos que no disponen de capacidad suficiente y devuelve una condición de ausencia de destino cuando todos los nodos se encuentran sin capacidad para recibir la carga solicitada.

### 8.3 Balanceador adaptativo
Como alternativa a Round Robin, se implementó un balanceador adaptativo cuyo criterio de selección utiliza información sobre el estado actual de los nodos antes de asignar una nueva carga.

Cada nodo del prototipo mantiene los siguientes atributos principales:

- capacidad máxima;
- carga actual;
- porcentaje de utilización;
- número de tareas asignadas.

Cuando llega una nueva tarea, el balanceador identifica primero los nodos que disponen de capacidad suficiente para recibirla. Los nodos que superarían su capacidad máxima después de la asignación son descartados como candidatos.

Entre los nodos disponibles, el algoritmo selecciona aquel que presenta el menor porcentaje de carga. Cuando existen nodos con el mismo porcentaje de utilización, el número de tareas asignadas se utiliza como criterio adicional de desempate.

De forma simplificada, la estrategia implementada sigue el siguiente procedimiento:

1. recibir la carga correspondiente a una nueva tarea;
2. identificar los nodos con capacidad suficiente;
3. calcular o consultar el porcentaje de carga de cada candidato;
4. seleccionar el nodo con menor porcentaje de utilización;
5. utilizar la cantidad de tareas asignadas como criterio secundario;
6. rechazar la tarea cuando ningún nodo dispone de capacidad suficiente.

A diferencia de Round Robin, esta estrategia incorpora información dinámica del estado de los recursos al momento de realizar la selección. Sin embargo, el algoritmo implementado constituye una heurística experimental simplificada y no realiza predicción de cargas futuras ni utiliza modelos de aprendizaje automático.

Las pruebas automatizadas verificaron que el balanceador selecciona el nodo menos cargado entre los candidatos disponibles, ignora los nodos que no disponen de capacidad suficiente y devuelve una condición de ausencia de destino cuando todos los recursos se encuentran saturados.

Posteriormente, el algoritmo fue evaluado mediante escenarios con tareas de diferente carga y duración. Debido a que las tareas liberan los recursos después de determinados ciclos, el estado de los nodos cambia durante la simulación y las decisiones posteriores se realizan utilizando la nueva distribución de carga.

Los resultados demostraron que la estrategia adaptativa puede reducir el desequilibrio bajo determinadas condiciones, pero también evidenciaron que seleccionar únicamente el nodo menos cargado no garantiza un comportamiento superior en todos los escenarios. Esta limitación fue especialmente visible durante las pruebas de carga pico y se analiza posteriormente en los resultados del experimento.

### 8.4 Relación con Rajammal y Chinnadurai (2025)
La guía de estudio utilizada como base para la actividad incluye como referencia el trabajo de Rajammal y Chinnadurai (2025), titulado *Dynamic load balancing in cloud computing using predictive graph networks and adaptive neural scheduling*, publicado en Scientific Reports.

Dentro del alcance de CloudTask, esta referencia se utiliza como fundamento académico para estudiar la importancia de adaptar las decisiones de distribución de carga al estado cambiante de los recursos en un entorno de computación en la nube.

El prototipo desarrollado para CloudTask aplica este principio de manera simplificada. En lugar de utilizar exclusivamente una asignación secuencial, el balanceador adaptativo consulta el estado actual de los nodos y selecciona, entre aquellos que disponen de capacidad suficiente, el recurso con menor porcentaje de utilización.

Sin embargo, la implementación realizada no pretende reproducir de forma completa el método presentado por Rajammal y Chinnadurai. CloudTask utiliza una heurística propia y simplificada orientada a fines académicos y experimentales. Por tanto, los resultados obtenidos corresponden exclusivamente al prototipo desarrollado en este proyecto y no deben atribuirse al algoritmo ni a los resultados experimentales de los autores citados.

La comparación con Round Robin permite estudiar empíricamente una diferencia fundamental entre una política estática de distribución y una estrategia que incorpora información dinámica del estado de los recursos. Los escenarios evaluados muestran además que disponer de información de carga no garantiza por sí solo una distribución óptima, debido a que el comportamiento depende de factores como la intensidad de las tareas, su duración, la capacidad disponible y el criterio utilizado para seleccionar los nodos.

Esta relación entre referencia académica, implementación simplificada y evaluación experimental permite aplicar el concepto de balanceo dinámico dentro del alcance del proyecto sin presentar el prototipo como una reproducción de un modelo más complejo.

### 8.5 Limitaciones de la implementación
El prototipo de balanceo desarrollado para CloudTask fue diseñado con fines académicos y experimentales, por lo que presenta diferencias importantes frente a un sistema de balanceo dinámico utilizado en una infraestructura cloud de producción.

En primer lugar, los nodos utilizados durante los experimentos son recursos simulados mediante objetos Python. Cada nodo dispone de una capacidad definida y una variable que representa su carga actual. Por tanto, las métricas utilizadas por el balanceador no corresponden a mediciones reales de CPU, memoria, latencia o tráfico obtenidas desde servidores independientes.

En segundo lugar, el balanceador adaptativo utiliza una heurística basada principalmente en el porcentaje de carga actual. No incorpora predicción de demanda futura, aprendizaje automático ni mecanismos avanzados de planificación. Su objetivo es permitir una comparación controlada entre una distribución secuencial y una distribución sensible al estado de los recursos.

Las tareas utilizadas en las simulaciones poseen valores predeterminados de carga y duración. Estos valores permiten reproducir exactamente los experimentos, pero no representan por sí mismos todos los patrones de tráfico que podrían presentarse en una aplicación real.

Asimismo, el balanceador experimental no se encuentra conectado al tráfico de producción de CloudTask. La instancia desplegada en Render continúa utilizando la configuración correspondiente al servicio gratuito y no distribuye solicitudes entre múltiples instancias mediante el algoritmo desarrollado.

Los resultados multiescenario también demostraron una limitación de la heurística utilizada. En el escenario de carga pico, tanto Round Robin como el balanceador adaptativo asignaron 11 de 15 tareas y rechazaron 4, obteniendo una tasa de rechazo del 26,67 %. Sin embargo, el balanceador adaptativo presentó un desequilibrio promedio de 43,33 puntos frente a 33,33 puntos de Round Robin y alcanzó un desequilibrio máximo de 95 puntos frente a 55 puntos.

Este resultado demuestra que seleccionar el nodo menos cargado en cada instante no garantiza una distribución global óptima cuando las tareas presentan diferentes cargas y duraciones y los recursos se aproximan a la saturación.

Por estas razones, los experimentos deben interpretarse como una prueba de concepto reproducible sobre estrategias de asignación y no como evidencia de un balanceador cloud listo para producción. Una evolución futura podría incorporar métricas reales de infraestructura, predicción de demanda, ponderación de recursos, planificación basada en duración estimada, múltiples instancias reales y mecanismos de autoescalado.

## 9. Plan y metodología de pruebas

### 9.1 Pruebas funcionales automatizadas
Las pruebas automatizadas de CloudTask se implementaron utilizando Pytest con el objetivo de verificar de forma reproducible el comportamiento de las funcionalidades principales y de los controles técnicos incorporados durante el desarrollo.

La suite completa está compuesta por 24 pruebas automatizadas. De estas, 14 corresponden a la aplicación web y sus mecanismos de seguridad, mientras que 10 verifican el comportamiento de los componentes utilizados en los experimentos de balanceo de carga.

Las pruebas correspondientes a CloudTask verifican los siguientes aspectos:

- disponibilidad del endpoint `/health`;
- registro correcto de usuarios y almacenamiento de la contraseña mediante hash;
- rechazo del registro de correos electrónicos duplicados;
- autenticación con credenciales correctas;
- rechazo de contraseñas incorrectas;
- restricción de acceso al panel para usuarios no autenticados;
- creación de tareas;
- edición de tareas;
- eliminación de tareas;
- impedimento de edición de tareas pertenecientes a otro usuario;
- impedimento de eliminación de tareas pertenecientes a otro usuario;
- rechazo de solicitudes POST sin un token CSRF válido;
- presencia de encabezados HTTP de seguridad;
- activación de HSTS en el entorno de producción.

Las 10 pruebas adicionales verifican el comportamiento de los nodos y de los algoritmos Round Robin y adaptativo. Entre los aspectos evaluados se encuentran la asignación y liberación de carga, prevención de sobreasignación de capacidad, distribución secuencial, omisión de nodos saturados, selección del nodo menos cargado y comportamiento cuando ningún recurso dispone de capacidad suficiente.

Para realizar la validación final se ejecutó la suite completa mediante:

`python -m pytest -v`

La ejecución recopiló las 24 pruebas y todas finalizaron satisfactoriamente, sin fallos, en aproximadamente 3,85 segundos.

La ejecución conjunta de la suite se utilizó como prueba de regresión al finalizar la fase principal de implementación, permitiendo comprobar que la incorporación de los experimentos de balanceo no había afectado negativamente las funcionalidades previamente desarrolladas en CloudTask.

### 9.2 Pruebas de seguridad
Las pruebas de seguridad tuvieron como objetivo comprobar que los controles implementados en CloudTask funcionaran de acuerdo con el comportamiento esperado y no permanecieran únicamente como configuraciones declaradas en el código.

La validación se realizó mediante pruebas automatizadas y comprobaciones directas sobre la aplicación desplegada. Los principales controles evaluados fueron los siguientes:

- **Protección de contraseñas:** se verificó que las contraseñas registradas no fueran almacenadas en texto plano y que el usuario pudiera autenticarse mediante la verificación del hash correspondiente.
- **Control de acceso:** se comprobó que las rutas protegidas requirieran autenticación y que un usuario no pudiera editar ni eliminar tareas pertenecientes a otra cuenta.
- **Protección CSRF:** se realizó una solicitud POST sin un token CSRF válido y se verificó que la aplicación rechazara la operación mediante una respuesta HTTP 400.
- **Métodos HTTP:** se verificó que `/logout` aceptara únicamente el método POST para realizar el cierre de sesión. Una solicitud GET fue rechazada mediante HTTP 405.
- **Encabezados de seguridad:** se comprobaron los encabezados CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy y Permissions-Policy.
- **HSTS:** en el entorno identificado como producción se verificó la presencia del encabezado Strict-Transport-Security.
- **HTTPS:** se comprobó el acceso a la aplicación desplegada mediante una conexión HTTPS.
- **Gestión de secretos:** se verificó que los parámetros sensibles de producción fueran administrados mediante variables de entorno y se realizó la rotación de una clave después de detectar una posible exposición durante el proceso de desarrollo.

Las comprobaciones HTTP realizadas directamente sobre el endpoint `/health` de producción permitieron verificar simultáneamente la disponibilidad del servicio y la presencia de los encabezados configurados.

Estas pruebas proporcionan evidencia técnica de los controles implementados, aunque no constituyen una auditoría de seguridad integral ni una prueba de penetración completa. El alcance se concentra en verificar los mecanismos de protección desarrollados específicamente para CloudTask.

### 9.3 Pruebas de carga y rendimiento
Las pruebas de carga se realizaron utilizando Locust con el propósito de observar el comportamiento de CloudTask frente a diferentes cantidades de usuarios concurrentes y recopilar métricas reproducibles de rendimiento.

Para mantener una operación controlada y evitar que factores como autenticación, escritura en base de datos o contenido variable alteraran la comparación, las solicitudes se dirigieron al endpoint `/health`. Este endpoint ejecuta una operación ligera y permite evaluar principalmente la capacidad de respuesta del servicio web.

El archivo `locustfile.py` define usuarios simulados que realizan solicitudes HTTP GET sobre `/health`, utilizando tiempos de espera aleatorios entre 1 y 3 segundos.

Se evaluaron tres niveles principales de carga local utilizando Gunicorn con dos workers:

| Usuarios concurrentes | Solicitudes | Fallos | Solicitudes/s | Latencia promedio | P95 | P99 |
|---:|---:|---:|---:|---:|---:|---:|
| 10 | 151 | 0 | 5,08 | 5 ms | 9 ms | 29 ms |
| 50 | 715 | 0 | 24,02 | 6 ms | 12 ms | 14 ms |
| 100 | 1.431 | 0 | 47,94 | 5 ms | 14 ms | 20 ms |

En los tres escenarios se obtuvo una tasa de fallos del 0 %. El incremento de usuarios produjo un aumento progresivo en la cantidad de solicitudes procesadas por segundo, mientras que las latencias se mantuvieron reducidas bajo las condiciones específicas del experimento.

La prueba con 100 usuarios concurrentes también se repitió utilizando un único worker de Gunicorn para disponer de una referencia comparativa. Esta segunda ejecución procesó 1.447 solicitudes sin fallos, con aproximadamente 48,48 solicitudes por segundo, una latencia promedio de 6 ms, P95 de 22 ms y P99 de 28 ms.

Los resultados corresponden a pruebas locales y a un endpoint ligero, por lo que no deben extrapolarse directamente al comportamiento de todas las operaciones de CloudTask ni a la capacidad de la infraestructura de producción. Su finalidad es proporcionar una referencia experimental reproducible para analizar concurrencia, latencia y estabilidad bajo carga controlada.

### 9.4 Pruebas de concurrencia
Las pruebas de concurrencia tuvieron como objetivo observar el comportamiento de CloudTask al modificar la cantidad de procesos worker utilizados por Gunicorn en un entorno local controlado.

Para comprobar que las solicitudes podían ser atendidas por procesos diferentes, el endpoint `/health` fue configurado para incluir el identificador del proceso (`worker_pid`) responsable de generar cada respuesta. Al ejecutar Gunicorn con dos workers y realizar múltiples solicitudes se observaron identificadores de proceso diferentes, proporcionando evidencia de distribución de solicitudes entre ambos procesos.

Posteriormente se ejecutó el mismo escenario de carga con 100 usuarios concurrentes utilizando configuraciones de uno y dos workers.

| Métrica | 1 worker | 2 workers |
|---|---:|---:|
| Solicitudes procesadas | 1.447 | 1.431 |
| Fallos | 0 | 0 |
| Solicitudes por segundo | 48,48 | 47,94 |
| Latencia promedio | 6 ms | 5 ms |
| P95 | 22 ms | 14 ms |
| P99 | 28 ms | 20 ms |
| Latencia máxima | 178 ms | 70 ms |

La cantidad de solicitudes procesadas y el throughput fueron prácticamente equivalentes en ambas configuraciones. Por esta razón, los resultados no permiten afirmar que dos workers hayan incrementado el rendimiento global medido en solicitudes por segundo.

Sin embargo, la configuración con dos workers presentó menores latencias en la parte superior de la distribución. El P95 disminuyó de 22 ms a 14 ms, el P99 de 28 ms a 20 ms y la latencia máxima observada pasó de 178 ms a 70 ms.

Bajo las condiciones específicas de este experimento, la principal diferencia observable estuvo por tanto en las latencias de cola y no en el throughput.

Estas pruebas fueron realizadas localmente sobre una misma máquina. La utilización de dos procesos Gunicorn demuestra concurrencia a nivel de procesos, pero no constituye escalamiento horizontal ni demuestra distribución entre servidores o instancias cloud independientes.

### 9.5 Experimentos de balanceo dinámico
Para evaluar las estrategias de distribución de carga se desarrolló un entorno experimental reproducible en Python compuesto por tres nodos simulados, cada uno con una capacidad máxima de 100 unidades.

Se compararon dos estrategias bajo las mismas condiciones:

- **Round Robin:** distribuye las tareas siguiendo un orden circular entre los nodos que disponen de capacidad suficiente.
- **Balanceador adaptativo:** selecciona, entre los nodos disponibles, aquel que presenta el menor porcentaje de carga en el momento de realizar la asignación.

Cada tarea fue representada mediante dos parámetros: una cantidad de carga y una duración expresada en ciclos. Al finalizar la duración correspondiente, la carga de la tarea se libera del nodo. De esta forma, el estado de los recursos cambia durante la simulación y las decisiones posteriores dependen de las asignaciones anteriores.

La evaluación final se realizó mediante tres escenarios:

- **Moderado:** cargas relativamente pequeñas y baja presión sobre la capacidad disponible.
- **Alto:** cargas mayores y utilización elevada de los nodos.
- **Pico:** tareas intensivas y de mayor duración que aproximan los recursos a condiciones de saturación.

Para cada estrategia y escenario se recopilaron las siguientes métricas:

- tareas asignadas;
- tareas rechazadas;
- tasa de rechazo;
- desequilibrio promedio entre nodos;
- desequilibrio máximo;
- carga máxima observada.

El desequilibrio de cada ciclo se calculó como la diferencia entre la carga del nodo más utilizado y la del nodo menos utilizado. El promedio de estas diferencias permite observar qué tan uniforme fue la distribución a lo largo del experimento.

La utilización de los mismos escenarios para ambos algoritmos permite realizar una comparación controlada y reproducible.

Los experimentos mostraron comportamientos diferentes según la intensidad de la carga. En el escenario Moderado ambos algoritmos presentaron resultados equivalentes. En el escenario Alto, el balanceador adaptativo redujo las métricas de desequilibrio. En el escenario Pico, ambos algoritmos presentaron la misma cantidad de tareas rechazadas, mientras que Round Robin obtuvo un menor desequilibrio que la estrategia adaptativa.

Estos resultados se conservaron sin modificar los escenarios para favorecer artificialmente a alguno de los algoritmos. El objetivo de la experimentación fue analizar el comportamiento de las estrategias y sus limitaciones, y no demostrar de antemano la superioridad de una de ellas.

## 10. Resultados y evidencias

### 10.1 Evidencias de despliegue cloud
CloudTask fue desplegado exitosamente como una aplicación web accesible públicamente mediante HTTPS. La implementación utiliza Render para ejecutar el servicio web y proporcionar la base de datos PostgreSQL utilizada en producción.

Durante el proceso de despliegue se verificó que el servicio alcanzara correctamente el estado operativo y que Gunicorn iniciara la aplicación Flask. Los registros de producción mostraron además la configuración automática de un worker de acuerdo con los recursos disponibles en la instancia utilizada.

La integración entre GitHub y Render permitió configurar despliegue automático desde la rama principal del repositorio. Esta funcionalidad fue comprobada mediante diferentes actualizaciones del proyecto: después de realizar un commit y enviarlo al repositorio remoto, Render detectó el cambio, inició un nuevo despliegue y publicó correctamente la nueva versión.

También se comprobó la conexión de CloudTask con PostgreSQL mediante la variable de entorno `DATABASE_URL`, manteniendo separada la configuración de persistencia respecto al código fuente.

Como evidencia del funcionamiento del entorno cloud se conservarán las siguientes figuras en el informe final:

**Figura 1. Aplicación CloudTask ejecutándose en producción.**  
Evidencia del acceso público a la aplicación desplegada mediante HTTPS.

**Figura 2. Servicio web CloudTask en estado operativo en Render.**  
Evidencia del despliegue exitoso de la aplicación y de la ejecución del servicio cloud.

**Figura 3. Despliegue automático desde GitHub.**  
Evidencia de la integración entre el repositorio y Render mediante Auto-Deploy.

**Figura 4. Base de datos PostgreSQL utilizada por CloudTask.**  
Evidencia del servicio de persistencia utilizado por la aplicación en producción.

Las evidencias relacionadas con variables de entorno o configuración sensible serán incorporadas únicamente cuando no expongan credenciales, claves, cadenas de conexión ni otros secretos. Cuando sea necesario mostrar una configuración de este tipo, los valores sensibles serán ocultados antes de incorporarlos al documento.

La arquitectura desplegada demuestra la separación entre aplicación y persistencia, acceso remoto mediante HTTPS y automatización del proceso de despliegue. Sin embargo, debido a las características del plan gratuito utilizado, esta evidencia no se presenta como demostración de alta disponibilidad ni de escalamiento horizontal automático.

### 10.2 Evidencias de seguridad
Las medidas de seguridad implementadas en CloudTask fueron verificadas mediante pruebas automatizadas y comprobaciones HTTP realizadas directamente sobre la aplicación desplegada.

Una de las principales verificaciones se realizó mediante una solicitud al endpoint `/health` utilizando `curl`. La respuesta del servidor confirmó el estado HTTP 200 y permitió inspeccionar los encabezados de seguridad enviados por la aplicación.

Entre los encabezados verificados en producción se encontraron:

- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(), geolocation=()`
- `Content-Security-Policy: default-src 'self'; style-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'`

La respuesta también permitió comprobar que el servicio estaba siendo ejecutado mediante Gunicorn y que el endpoint de salud funcionaba correctamente en producción.

Adicionalmente, las pruebas automatizadas verificaron el funcionamiento de controles relacionados con autenticación, autorización, almacenamiento seguro de contraseñas, protección CSRF, encabezados HTTP y HSTS.

También se comprobó específicamente el cierre de sesión seguro. La ruta `/logout` fue configurada para aceptar únicamente solicitudes POST protegidas mediante CSRF. Una solicitud GET directa sobre esta ruta produjo una respuesta HTTP 405, demostrando que el cierre de sesión no puede ejecutarse mediante dicho método.

Como evidencia de estos controles se incorporarán posteriormente las siguientes figuras:

**Figura 5. Verificación HTTP del endpoint `/health` y encabezados de seguridad.**  
Evidencia de la respuesta HTTP 200 y de los encabezados de protección activos en producción.

**Figura 6. Validación del método HTTP utilizado para el cierre de sesión.**  
Evidencia del rechazo de una solicitud GET sobre `/logout` mediante HTTP 405.

**Figura 7. Pruebas automatizadas de los controles de seguridad.**  
Evidencia de la validación mediante Pytest de autenticación, autorización, CSRF, encabezados de seguridad y HSTS.

Las evidencias seleccionadas para el documento final no mostrarán valores de `SECRET_KEY`, credenciales de PostgreSQL, cookies de sesión, cadenas privadas de conexión ni otros datos sensibles. La clave utilizada por la aplicación fue rotada durante el desarrollo después de una posible exposición y su valor no forma parte de la documentación.

Las comprobaciones realizadas proporcionan evidencia reproducible de los controles implementados dentro del alcance de CloudTask. No obstante, estos resultados no sustituyen una auditoría de seguridad integral ni una prueba de penetración especializada.

### 10.3 Resultados de pruebas automatizadas
La ejecución final de la suite automatizada permitió validar conjuntamente las funcionalidades principales de CloudTask, sus controles de seguridad y los componentes desarrollados para los experimentos de balanceo.

La ejecución se realizó mediante:

`python -m pytest -v`

Pytest recopiló un total de 24 pruebas y todas finalizaron satisfactoriamente.

| Resultado | Cantidad |
|---|---:|
| Pruebas recopiladas | 24 |
| Pruebas aprobadas | 24 |
| Pruebas fallidas | 0 |
| Porcentaje de aprobación | 100 % |
| Tiempo aproximado de ejecución | 3,85 s |

Las primeras 14 pruebas corresponden a la aplicación web y verifican funcionalidades como registro, autenticación, control de acceso, operaciones CRUD sobre tareas, protección CSRF y encabezados de seguridad.

Las 10 pruebas restantes corresponden a los componentes utilizados en los experimentos de balanceo. Estas verifican el comportamiento de los nodos, el control de capacidad y las decisiones realizadas por los algoritmos Round Robin y adaptativo.

El resultado de 24 pruebas aprobadas proporciona evidencia reproducible de que los componentes evaluados presentaban el comportamiento esperado al finalizar la implementación.

Además de validar individualmente las funcionalidades, la ejecución completa se utilizó como prueba de regresión. Esto permitió comprobar que la incorporación posterior de los algoritmos y experimentos de balanceo no introdujera fallos detectables por la suite en las funcionalidades previamente desarrolladas.

**Figura 8. Ejecución final de la suite automatizada con Pytest.**  
La evidencia muestra la recopilación de 24 pruebas, la aprobación de la totalidad de los casos evaluados y la ausencia de pruebas fallidas.

El resultado satisfactorio de la suite no implica ausencia absoluta de defectos en la aplicación. Las pruebas proporcionan cobertura sobre los comportamientos definidos en los casos implementados, mientras que escenarios adicionales podrían requerir nuevas pruebas en futuras versiones.

### 10.4 Resultados de pruebas de carga
Las pruebas realizadas con Locust permitieron observar el comportamiento del servicio bajo incrementos controlados en el número de usuarios concurrentes. Para mantener comparables las ejecuciones, se utilizó el endpoint `/health` y una configuración local de Gunicorn con dos workers.

Los resultados obtenidos fueron los siguientes:

| Usuarios concurrentes | Solicitudes | Fallos | Solicitudes/s | Promedio | P95 | P99 | Máximo |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 151 | 0 | 5,08 | 5 ms | 9 ms | 29 ms | 39 ms |
| 50 | 715 | 0 | 24,02 | 6 ms | 12 ms | 14 ms | 26 ms |
| 100 | 1.431 | 0 | 47,94 | 5 ms | 14 ms | 20 ms | 70 ms |

En los tres escenarios se obtuvo una tasa de fallos del 0 %. A medida que aumentó el número de usuarios concurrentes también aumentó la cantidad de solicitudes procesadas por segundo.

La prueba de 10 usuarios alcanzó aproximadamente 5,08 solicitudes por segundo; con 50 usuarios se alcanzaron 24,02 solicitudes por segundo; y con 100 usuarios se registraron aproximadamente 47,94 solicitudes por segundo.

Las latencias promedio permanecieron entre 5 y 6 ms durante las tres ejecuciones. En el escenario de mayor carga, correspondiente a 100 usuarios concurrentes, el percentil 95 fue de 14 ms, el percentil 99 de 20 ms y la latencia máxima observada fue de 70 ms.

**Figura 9. Resultado de la prueba de carga con 10 usuarios concurrentes.**  
Evidencia de la ejecución realizada con Locust y de las métricas obtenidas bajo el primer nivel de carga.

**Figura 10. Resultado de la prueba de carga con 50 usuarios concurrentes.**  
Evidencia del comportamiento del servicio al incrementar la cantidad de usuarios simulados.

**Figura 11. Resultado de la prueba de carga con 100 usuarios concurrentes.**  
Evidencia del escenario de mayor concurrencia utilizado en las pruebas locales con dos workers.

Los resultados muestran estabilidad del endpoint evaluado dentro de las condiciones del experimento, debido a que no se registraron solicitudes fallidas en ninguno de los tres niveles de carga.

Sin embargo, estas métricas no representan la capacidad máxima de CloudTask ni deben extrapolarse directamente a operaciones que involucren autenticación, consultas complejas o escritura en PostgreSQL. El endpoint `/health` ejecuta una operación ligera y las pruebas fueron realizadas en un entorno local controlado.

Por esta razón, los resultados se utilizan como evidencia experimental del comportamiento bajo la carga definida y no como una prueba de capacidad máxima de la infraestructura de producción.

### 10.5 Comparación de concurrencia
Para complementar las pruebas generales de carga se comparó el comportamiento de CloudTask utilizando uno y dos procesos worker de Gunicorn bajo el mismo escenario de 100 usuarios concurrentes.

Los resultados fueron los siguientes:

| Métrica | 1 worker | 2 workers | Diferencia observada |
|---|---:|---:|---:|
| Solicitudes | 1.447 | 1.431 | -16 |
| Fallos | 0 | 0 | Sin diferencia |
| Solicitudes/s | 48,48 | 47,94 | -0,54 |
| Latencia promedio | 6 ms | 5 ms | -1 ms |
| P95 | 22 ms | 14 ms | -8 ms |
| P99 | 28 ms | 20 ms | -8 ms |
| Latencia máxima | 178 ms | 70 ms | -108 ms |

La comparación evidencia que el throughput fue prácticamente equivalente. La configuración con un worker alcanzó aproximadamente 48,48 solicitudes por segundo y la configuración con dos workers 47,94 solicitudes por segundo. Por tanto, los resultados no permiten afirmar que el segundo worker haya incrementado la cantidad de solicitudes procesadas por unidad de tiempo.

La diferencia más relevante se presentó en las latencias de cola. Al utilizar dos workers, el P95 disminuyó de 22 ms a 14 ms, equivalente a una reducción aproximada del 36,4 %. El P99 pasó de 28 ms a 20 ms, una reducción aproximada del 28,6 %. La latencia máxima disminuyó de 178 ms a 70 ms, aproximadamente un 60,7 %.

Estas reducciones describen únicamente el escenario experimental evaluado y no deben interpretarse como una mejora garantizada para cualquier tipo de carga.

**Figura 12. Comparación de latencias entre uno y dos workers de Gunicorn.**  
La figura permitirá representar gráficamente las diferencias observadas en latencia promedio, P95, P99 y latencia máxima.

**Figura 13. Distribución de solicitudes entre dos procesos worker.**  
La evidencia muestra diferentes valores de `worker_pid` obtenidos mediante el endpoint `/health`, confirmando que las solicitudes fueron atendidas por más de un proceso durante la prueba local.

Los resultados permiten concluir que, en este experimento, incrementar el número de workers no mejoró de forma apreciable el throughput, pero estuvo asociado con menores latencias en la parte superior de la distribución.

Esta prueba representa concurrencia mediante procesos dentro de una misma máquina y no escalamiento horizontal. La distribución entre múltiples instancias cloud requeriría una arquitectura diferente, como la propuesta en la sección de arquitectura escalable.

### 10.6 Resultados del balanceo multiescenario
Para evaluar el comportamiento de los algoritmos bajo diferentes niveles de exigencia se ejecutaron tres escenarios reproducibles: Moderado, Alto y Pico. Round Robin y el balanceador adaptativo fueron evaluados utilizando exactamente las mismas tareas y capacidades.

Los resultados obtenidos fueron los siguientes:

| Escenario | Algoritmo | Asignadas | Rechazadas | Tasa rechazo | Desequilibrio promedio | Desequilibrio máximo | Carga máxima |
|---|---|---:|---:|---:|---:|---:|---:|
| Moderado | Round Robin | 15 | 0 | 0 % | 17,67 | 25 | 25 % |
| Moderado | Adaptativo | 15 | 0 | 0 % | 17,67 | 25 | 25 % |
| Alto | Round Robin | 15 | 0 | 0 % | 41,00 | 60 | 95 % |
| Alto | Adaptativo | 15 | 0 | 0 % | 31,00 | 45 | 90 % |
| Pico | Round Robin | 11 | 4 | 26,67 % | 33,33 | 55 | 100 % |
| Pico | Adaptativo | 11 | 4 | 26,67 % | 43,33 | 95 | 100 % |

En el escenario Moderado no se observaron diferencias entre las estrategias. Ambos algoritmos asignaron las 15 tareas sin rechazos y obtuvieron las mismas métricas de desequilibrio y carga máxima.

En el escenario Alto ambos algoritmos también asignaron las 15 tareas sin rechazos, pero el balanceador adaptativo presentó una distribución más uniforme. El desequilibrio promedio disminuyó de 41 a 31 puntos, equivalente a una reducción aproximada del 24,4 %. El desequilibrio máximo pasó de 60 a 45 puntos, una reducción del 25 %. La carga máxima observada disminuyó de 95 % a 90 %.

El escenario Pico produjo un comportamiento diferente. Ambos algoritmos asignaron 11 tareas y rechazaron 4, obteniendo una tasa de rechazo del 26,67 % y alcanzando una carga máxima del 100 %. Sin embargo, Round Robin presentó un desequilibrio promedio de 33,33 puntos frente a 43,33 del adaptativo. El desequilibrio máximo fue de 55 puntos para Round Robin y de 95 para el balanceador adaptativo.

Por tanto, los experimentos no muestran la superioridad universal de una estrategia. El balanceador adaptativo obtuvo mejores métricas de equilibrio en el escenario Alto, resultados equivalentes en el escenario Moderado y un comportamiento menos uniforme que Round Robin durante el escenario Pico.

Este resultado evidencia una limitación de la heurística utilizada: tomar decisiones utilizando únicamente la carga actual puede resultar insuficiente cuando existen tareas con diferentes intensidades y duraciones y los recursos se aproximan a la saturación.

**Figura 14. Comparación del desequilibrio promedio por escenario.**  
La figura comparará Round Robin y el balanceador adaptativo en los escenarios Moderado, Alto y Pico.

**Figura 15. Comparación del desequilibrio máximo por escenario.**  
La representación permitirá observar especialmente el comportamiento de ambas estrategias durante el escenario Pico.

**Figura 16. Comparación de la carga máxima observada.**  
La figura mostrará el porcentaje máximo de utilización alcanzado por cada estrategia en los tres escenarios.

**Figura 17. Evidencia de ejecución del experimento multiescenario.**  
La evidencia mostrará la salida reproducible generada por `multi_scenario_experiment.py` y almacenada como parte de los resultados del proyecto.

La conservación de resultados favorables y desfavorables permite realizar un análisis más riguroso del prototipo y proporciona información para plantear mejoras futuras en la estrategia de balanceo.

## 11. Análisis y discusión de resultados
Los resultados obtenidos durante el desarrollo y evaluación de CloudTask permiten analizar el proyecto desde cuatro dimensiones principales: funcionamiento de la aplicación, seguridad, rendimiento y distribución experimental de carga.

En primer lugar, la ejecución satisfactoria de las 24 pruebas automatizadas proporciona evidencia reproducible del comportamiento esperado de las funcionalidades incluidas en la suite. Las pruebas cubrieron registro y autenticación de usuarios, operaciones CRUD, restricciones de acceso, protección CSRF, encabezados de seguridad y componentes relacionados con los algoritmos de balanceo. La ejecución conjunta de estas pruebas también permitió utilizarlas como mecanismo de regresión después de incorporar nuevas funcionalidades.

Desde la perspectiva de seguridad, las verificaciones realizadas sobre la aplicación desplegada confirmaron la presencia de controles tanto a nivel de aplicación como de comunicación HTTP. El uso de hashing para contraseñas, variables de entorno para secretos, protección CSRF, restricciones de acceso por usuario, cookies configuradas con atributos de seguridad y encabezados HTTP permite aplicar de manera práctica varios de los principios estudiados para entornos cloud. La verificación directa de estos controles en producción complementa las pruebas automatizadas y evita limitar la evaluación únicamente a una revisión del código fuente.

Las pruebas de carga mostraron que el endpoint `/health` respondió sin fallos en los escenarios evaluados de 10, 50 y 100 usuarios concurrentes. No obstante, estos resultados deben interpretarse dentro de su contexto: el endpoint realiza una operación ligera y las pruebas fueron ejecutadas localmente. Por esta razón, las cifras obtenidas permiten analizar el comportamiento del entorno experimental, pero no representan la capacidad máxima de CloudTask ni constituyen una prueba de rendimiento integral de todas sus operaciones.

La comparación entre uno y dos workers de Gunicorn produjo un resultado particularmente relevante. El throughput permaneció prácticamente equivalente, con aproximadamente 48 solicitudes por segundo en ambas configuraciones. Por tanto, no existe evidencia suficiente para afirmar que el segundo worker aumentara la cantidad de solicitudes procesadas por segundo. Sin embargo, la configuración con dos workers presentó menores valores de P95, P99 y latencia máxima. Esto sugiere que, bajo las condiciones específicas de la prueba, disponer de más de un proceso permitió reducir las latencias extremas aun cuando el throughput permaneció estable.

Los experimentos de balanceo permitieron observar que el comportamiento de una estrategia depende directamente de las características de la carga. En el escenario Moderado, Round Robin y el balanceador adaptativo obtuvieron resultados equivalentes, lo que indica que una estrategia más sensible al estado de los nodos no necesariamente genera ventajas cuando existe capacidad suficiente y las cargas son reducidas.

En el escenario Alto, el balanceador adaptativo presentó mejores métricas de equilibrio. El desequilibrio promedio disminuyó aproximadamente un 24,4 % y el desequilibrio máximo un 25 % respecto a Round Robin. Este comportamiento demuestra que considerar el estado actual de los recursos puede resultar beneficioso bajo determinadas condiciones de utilización elevada.

Sin embargo, el escenario Pico mostró la principal limitación del algoritmo adaptativo desarrollado. Ambos métodos rechazaron la misma cantidad de tareas, pero Round Robin obtuvo un menor desequilibrio promedio y máximo. La selección del nodo menos cargado en cada instante constituye una decisión local y no considera necesariamente la evolución futura de las tareas ya asignadas, especialmente cuando estas poseen cargas y duraciones diferentes.

Este resultado permite identificar una diferencia importante entre reaccionar al estado actual y anticipar el comportamiento futuro del sistema. Una estrategia más avanzada podría incorporar información adicional como duración estimada de las tareas, tendencias de utilización, métricas reales de CPU y memoria o mecanismos predictivos para mejorar las decisiones de asignación.

En conjunto, los experimentos no demuestran que una estrategia sea universalmente superior. En cambio, proporcionan evidencia de que las decisiones de distribución deben adaptarse al comportamiento de la carga y que una heurística aparentemente favorable puede perder eficiencia cuando cambian las condiciones del sistema.

Finalmente, debe diferenciarse la experimentación realizada de la infraestructura productiva actualmente desplegada. CloudTask utiliza una única instancia web en el plan gratuito empleado y no implementa escalamiento horizontal automático. La arquitectura de múltiples instancias y balanceo de tráfico se presenta como una evolución técnicamente posible del proyecto, mientras que los experimentos realizados permiten estudiar y evaluar estos conceptos de forma controlada y reproducible.

## 12. Limitaciones y trabajo futuro
CloudTask fue desarrollado como un prototipo académico funcional orientado a demostrar la aplicación práctica de conceptos de computación en la nube, seguridad, pruebas de software, concurrencia y distribución de carga. Debido a este alcance, existen limitaciones que deben considerarse al interpretar los resultados obtenidos.

La infraestructura de producción utiliza el plan gratuito de Render. El servicio web dispone de recursos limitados y puede entrar en estado de suspensión después de periodos de inactividad. Asimismo, la instancia utilizada no implementa escalamiento horizontal automático y durante las verificaciones realizadas Gunicorn operó con un único worker de acuerdo con los recursos disponibles.

La base de datos PostgreSQL utilizada también corresponde al servicio gratuito seleccionado para el proyecto. Por esta razón, la infraestructura actual no debe considerarse una solución de alta disponibilidad ni una arquitectura preparada para cargas productivas de gran escala.

Las pruebas de rendimiento se realizaron principalmente en un entorno local y utilizaron el endpoint `/health`, cuya operación es considerablemente más ligera que procesos como autenticación, creación de tareas o consultas con mayor interacción con la base de datos. Una evaluación futura debería incorporar escenarios de carga que reproduzcan recorridos completos de usuarios y operaciones de lectura y escritura sobre PostgreSQL.

El sistema de balanceo desarrollado constituye una simulación independiente de la infraestructura productiva. Los nodos utilizados no representan servidores reales y las variables de carga no proceden de métricas de CPU, memoria, red o latencia. Asimismo, la estrategia adaptativa utiliza una heurística basada en el estado actual y no incorpora predicción de demanda futura.

Como evolución de la arquitectura se propone desplegar múltiples instancias independientes de CloudTask detrás de un balanceador de carga y utilizar métricas reales de infraestructura para determinar la distribución de solicitudes y las decisiones de escalamiento.

También podría incorporarse un mecanismo de autoescalado que aumente o reduzca la cantidad de instancias de acuerdo con indicadores como utilización de CPU, memoria, latencia, cantidad de solicitudes o profundidad de colas.

En el componente experimental de balanceo, una evolución podría incorporar duración estimada de tareas, ponderación de recursos, análisis histórico de utilización y mecanismos predictivos. Esto permitiría evaluar estrategias capaces de anticipar condiciones de saturación en lugar de reaccionar únicamente a la carga existente en el instante de asignación.

Desde la perspectiva de seguridad, entre las mejoras futuras se encuentran autenticación multifactor, administración especializada de secretos, rotación automatizada de credenciales, registro centralizado de eventos, monitoreo y alertas, copias de seguridad automatizadas, definición formal de RPO y RTO, auditorías periódicas, herramientas CSPM, protección mediante WAF y un procedimiento formal de respuesta a incidentes.

La persistencia también podría evolucionar mediante estrategias de respaldo, restauración y recuperación ante desastres que permitan establecer objetivos verificables de continuidad del servicio.

Finalmente, una versión posterior del proyecto podría incorporar observabilidad integral mediante métricas, registros y trazas distribuidas, permitiendo relacionar el comportamiento de los usuarios, las decisiones del balanceador, el rendimiento de las instancias y las operaciones de base de datos.

Estas mejoras representan líneas de evolución y no funcionalidades presentes en la versión evaluada. Mantener esta distinción permite establecer con precisión el alcance técnico alcanzado por CloudTask y las capacidades que requerirían una implementación posterior.

## 13. Conclusiones
El desarrollo de CloudTask permitió implementar una aplicación web funcional y desplegarla en un entorno de computación en la nube, integrando persistencia de datos, autenticación de usuarios, gestión de tareas, controles de seguridad, pruebas automatizadas y mecanismos experimentales para el análisis de concurrencia y distribución de carga.

La utilización de Flask, SQLAlchemy, PostgreSQL, Gunicorn, GitHub y Render permitió establecer una arquitectura en la que la aplicación, la persistencia y el proceso de despliegue se encuentran claramente diferenciados. El despliegue mediante HTTPS y la integración de Auto-Deploy demostraron además la posibilidad de mantener un flujo reproducible desde el desarrollo local hasta la publicación de nuevas versiones en la nube.

En materia de seguridad, CloudTask incorporó mecanismos de hashing de contraseñas, autenticación, autorización por usuario, protección CSRF, variables de entorno para información sensible, configuración segura de cookies y encabezados HTTP de seguridad. La validación mediante pruebas automatizadas y comprobaciones directas sobre producción permitió demostrar técnicamente el funcionamiento de estos controles dentro del alcance definido para el proyecto.

La suite automatizada alcanzó 24 pruebas aprobadas de 24 ejecutadas. Estas pruebas permitieron validar funcionalidades de la aplicación, mecanismos de seguridad y componentes asociados con los algoritmos de balanceo, además de proporcionar un mecanismo de regresión durante la evolución del proyecto.

Las pruebas de carga realizadas con Locust mostraron una tasa de fallos del 0 % en los escenarios evaluados de 10, 50 y 100 usuarios concurrentes sobre el endpoint `/health`. La comparación entre uno y dos workers de Gunicorn mostró un throughput prácticamente equivalente, pero menores latencias P95, P99 y máxima con dos procesos bajo las condiciones específicas del experimento. Este resultado permitió diferenciar empíricamente la concurrencia mediante procesos del escalamiento horizontal entre instancias independientes.

Los experimentos de balanceo demostraron que el comportamiento de las estrategias depende de las características de la carga. Round Robin y el algoritmo adaptativo presentaron resultados equivalentes bajo el escenario Moderado. En el escenario Alto, la estrategia adaptativa redujo el desequilibrio promedio aproximadamente un 24,4 % y el desequilibrio máximo un 25 %. Sin embargo, durante el escenario Pico, Round Robin presentó una distribución más uniforme y ambos algoritmos registraron la misma tasa de rechazo del 26,67 %.

Estos resultados muestran que utilizar información dinámica sobre el estado actual de los recursos puede aportar ventajas bajo determinadas condiciones, pero no garantiza una distribución óptima en todos los escenarios. El experimento permitió identificar las limitaciones de una heurística basada únicamente en la carga instantánea y fundamentar la necesidad de estrategias más avanzadas cuando las tareas presentan diferentes intensidades y duraciones.

Finalmente, CloudTask permitió aplicar de manera integrada conceptos de computación en la nube, seguridad de la información, pruebas de software, concurrencia y balanceo dinámico. El proyecto distingue explícitamente entre las capacidades realmente implementadas, los experimentos desarrollados y las características propuestas como evolución futura, proporcionando una base técnica reproducible para continuar estudiando arquitecturas cloud más escalables, observables, resilientes y seguras.

## 14. Referencias bibliográficas
Ministerio de Tecnologías de la Información y las Comunicaciones – MinTIC. (2021). *Guía técnica de computación en la nube (v.1.1).* Bogotá D.C.: MinTIC. https://www.mintic.gov.co/portal/715/articles-58727_recurso_2.pdf

Rajammal, K., & Chinnadurai, M. (2025). Dynamic load balancing in cloud computing using predictive graph networks and adaptive neural scheduling. *Scientific Reports, 15*(1), Artículo 22181. https://doi.org/10.1038/s41598-025-97494-2