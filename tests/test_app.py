import pytest
import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "clave-exclusiva-para-pruebas"

from app import app
from app import db, Usuario, Tarea

@pytest.fixture
def app_test():
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app_test):
    return app_test.test_client()

def crear_usuario(nombre="Usuario Test", email="test@cloudtask.com", password="Password123"):
    usuario = Usuario(
        nombre=nombre,
        email=email
    )
    usuario.set_password(password)

    db.session.add(usuario)
    db.session.commit()

    return usuario


def iniciar_sesion(client, email="test@cloudtask.com", password="Password123"):
    return client.post(
        "/login",
        data={
            "email": email,
            "password": password
        },
        follow_redirects=True
    )



def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
    assert response.get_json()["service"] == "CloudTask"


def test_registro_usuario(client, app_test):
    response = client.post(
        "/registro",
        data={
            "nombre": "Usuario Test",
            "email": "test@cloudtask.com",
            "password": "Password123",
            "confirmar_password": "Password123"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    with app_test.app_context():
        usuario = Usuario.query.filter_by(email="test@cloudtask.com").first()

        assert usuario is not None
        assert usuario.nombre == "Usuario Test"
        assert usuario.password_hash != "Password123"
        assert usuario.check_password("Password123")


def test_registro_email_duplicado(client):
    datos = {
        "nombre": "Usuario Test",
        "email": "duplicado@cloudtask.com",
        "password": "Password123",
        "confirmar_password": "Password123"
    }

    client.post("/registro", data=datos, follow_redirects=True)

    response = client.post(
        "/registro",
        data=datos,
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Ya existe una cuenta registrada con este correo." in response.data


def test_login_correcto(client, app_test):
    with app_test.app_context():
        crear_usuario()

    response = client.post(
        "/login",
        data={
            "email": "test@cloudtask.com",
            "password": "Password123"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Bienvenido, Usuario Test" in response.data


def test_login_password_incorrecta(client, app_test):
    with app_test.app_context():
        crear_usuario()

    response = client.post(
        "/login",
        data={
            "email": "test@cloudtask.com",
            "password": "PasswordIncorrecta123"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Correo o contrase" in response.data
    assert b"Bienvenido, Usuario Test" not in response.data


def test_dashboard_requiere_autenticacion(client):
    response = client.get("/dashboard")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_crear_tarea(client, app_test):
    with app_test.app_context():
        crear_usuario()

    iniciar_sesion(client)

    response = client.post(
        "/tareas/nueva",
        data={
            "titulo": "Tarea de prueba",
            "descripcion": "Creada mediante pytest",
            "prioridad": "Alta",
            "estado": "Pendiente"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    with app_test.app_context():
        tarea = Tarea.query.filter_by(titulo="Tarea de prueba").first()

        assert tarea is not None
        assert tarea.descripcion == "Creada mediante pytest"
        assert tarea.prioridad == "Alta"
        assert tarea.estado == "Pendiente"
        assert tarea.usuario_id is not None


def test_editar_tarea(client, app_test):
    with app_test.app_context():
        usuario = crear_usuario()

        tarea = Tarea(
            titulo="Tarea original",
            descripcion="Descripción original",
            prioridad="Baja",
            estado="Pendiente",
            usuario_id=usuario.id
        )

        db.session.add(tarea)
        db.session.commit()
        tarea_id = tarea.id

    iniciar_sesion(client)

    response = client.post(
        f"/tareas/{tarea_id}/editar",
        data={
            "titulo": "Tarea actualizada",
            "descripcion": "Descripción actualizada",
            "prioridad": "Alta",
            "estado": "Completada"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    with app_test.app_context():
        tarea = db.session.get(Tarea, tarea_id)

        assert tarea.titulo == "Tarea actualizada"
        assert tarea.descripcion == "Descripción actualizada"
        assert tarea.prioridad == "Alta"
        assert tarea.estado == "Completada"


def test_eliminar_tarea(client, app_test):
    with app_test.app_context():
        usuario = crear_usuario()

        tarea = Tarea(
            titulo="Tarea para eliminar",
            descripcion="Esta tarea debe ser eliminada",
            prioridad="Media",
            estado="Pendiente",
            usuario_id=usuario.id
        )

        db.session.add(tarea)
        db.session.commit()
        tarea_id = tarea.id

    iniciar_sesion(client)

    response = client.post(
        f"/tareas/{tarea_id}/eliminar",
        follow_redirects=True
    )

    assert response.status_code == 200

    with app_test.app_context():
        tarea = db.session.get(Tarea, tarea_id)

        assert tarea is None


def test_usuario_no_puede_editar_tarea_ajena(client, app_test):
    with app_test.app_context():
        usuario_1 = crear_usuario(
            nombre="Usuario Uno",
            email="usuario1@cloudtask.com"
        )

        usuario_2 = crear_usuario(
            nombre="Usuario Dos",
            email="usuario2@cloudtask.com"
        )

        tarea = Tarea(
            titulo="Tarea privada",
            descripcion="Pertenece al usuario uno",
            prioridad="Alta",
            estado="Pendiente",
            usuario_id=usuario_1.id
        )

        db.session.add(tarea)
        db.session.commit()
        tarea_id = tarea.id

    iniciar_sesion(
        client,
        email="usuario2@cloudtask.com",
        password="Password123"
    )

    response = client.get(
        f"/tareas/{tarea_id}/editar"
    )

    assert response.status_code == 404


def test_usuario_no_puede_eliminar_tarea_ajena(client, app_test):
    with app_test.app_context():
        usuario_1 = crear_usuario(
            nombre="Usuario Uno",
            email="usuario1@cloudtask.com"
        )

        crear_usuario(
            nombre="Usuario Dos",
            email="usuario2@cloudtask.com"
        )

        tarea = Tarea(
            titulo="Tarea privada",
            descripcion="No debe ser eliminada por otro usuario",
            prioridad="Alta",
            estado="Pendiente",
            usuario_id=usuario_1.id
        )

        db.session.add(tarea)
        db.session.commit()
        tarea_id = tarea.id

    iniciar_sesion(
        client,
        email="usuario2@cloudtask.com",
        password="Password123"
    )

    response = client.post(
        f"/tareas/{tarea_id}/eliminar"
    )

    assert response.status_code == 404

    with app_test.app_context():
        tarea = db.session.get(Tarea, tarea_id)
        assert tarea is not None


def test_csrf_rechaza_post_sin_token(client, app_test):
    app_test.config["WTF_CSRF_ENABLED"] = True

    response = client.post(
        "/login",
        data={
            "email": "test@cloudtask.com",
            "password": "Password123"
        }
    )

    assert response.status_code == 400

    app_test.config["WTF_CSRF_ENABLED"] = False



def test_encabezados_seguridad(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert "default-src 'self'" in response.headers["Content-Security-Policy"]
    assert response.headers["Permissions-Policy"] == "camera=(), microphone=(), geolocation=()"


def test_hsts_en_produccion(client):
    os.environ["APP_ENV"] = "production"

    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["Strict-Transport-Security"] == \
        "max-age=31536000; includeSubDomains"

    os.environ.pop("APP_ENV", None)