import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistroForm, LoginForm, TareaForm

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "clave-desarrollo-cloudtask"
)

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

if os.environ.get("APP_ENV") == "production":
    app.config["SESSION_COOKIE_SECURE"] = True

# Base de datos: SQLite en desarrollo y PostgreSQL en producción
database_url = os.environ.get(
    "DATABASE_URL",
    "sqlite:///cloudtask.db"
)

# Compatibilidad con URLs de PostgreSQL
if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Inicializar LoginManager
login_manager = LoginManager(app)
login_manager.login_view = "login"

#creación de modelo usuario
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(
            password,
            method="pbkdf2:sha256:600000"
    )

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Usuario {self.email}>"

# Crear el cargador de usuarios
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))

#creación de modelo tareas
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    prioridad = db.Column(db.String(20), nullable=False, default="Media")
    estado = db.Column(db.String(30), nullable=False, default="Pendiente")
    fecha_creacion = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now()
    )
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Tarea {self.titulo}>"






@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/health")
def health():
    return {
        "status": "ok",
        "service": "CloudTask",
        "worker_pid": os.getpid()
    }, 200

# funcion registro
@app.route("/registro", methods=["GET", "POST"])
def registro():
    form = RegistroForm()

    if form.validate_on_submit():
        usuario_existente = Usuario.query.filter_by(
            email=form.email.data.lower().strip()
        ).first()

        if usuario_existente:
            flash("Ya existe una cuenta registrada con este correo.", "error")
            return render_template("registro.html", form=form)

        nuevo_usuario = Usuario(
            nombre=form.nombre.data.strip(),
            email=form.email.data.lower().strip()
        )

        nuevo_usuario.set_password(form.password.data)

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Cuenta creada correctamente.", "success")
        return redirect(url_for("login"))

    return render_template("registro.html", form=form)

# funcion login
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.check_password(form.password.data):
            login_user(usuario)
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for("dashboard"))

        flash("Correo o contraseña incorrectos.", "error")

    return render_template("login.html", form=form)

@app.route("/dashboard")
@login_required
def dashboard():
    tareas = Tarea.query.filter_by(
        usuario_id=current_user.id
    ).order_by(Tarea.fecha_creacion.desc()).all()

    return render_template(
        "dashboard.html",
        tareas=tareas
    )

@app.route("/tareas/nueva", methods=["GET", "POST"])
@login_required
def nueva_tarea():
    form = TareaForm()

    if form.validate_on_submit():
        nueva = Tarea(
            titulo=form.titulo.data.strip(),
            descripcion=form.descripcion.data.strip() if form.descripcion.data else None,
            prioridad=form.prioridad.data,
            estado=form.estado.data,
            usuario_id=current_user.id
        )

        db.session.add(nueva)
        db.session.commit()

        flash("Tarea creada correctamente.", "success")
        return redirect(url_for("dashboard"))

    return render_template("nueva_tarea.html", form=form)

@app.route("/tareas/<int:tarea_id>/editar", methods=["GET", "POST"])
@login_required
def editar_tarea(tarea_id):
    tarea = Tarea.query.filter_by(
        id=tarea_id,
        usuario_id=current_user.id
    ).first_or_404()

    form = TareaForm(obj=tarea)

    if form.validate_on_submit():
        tarea.titulo = form.titulo.data.strip()
        tarea.descripcion = (
            form.descripcion.data.strip()
            if form.descripcion.data
            else None
        )
        tarea.prioridad = form.prioridad.data
        tarea.estado = form.estado.data

        db.session.commit()

        flash("Tarea actualizada correctamente.", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "editar_tarea.html",
        form=form,
        tarea=tarea
    )

@app.route("/tareas/<int:tarea_id>/eliminar", methods=["POST"])
@login_required
def eliminar_tarea(tarea_id):
    tarea = Tarea.query.filter_by(
        id=tarea_id,
        usuario_id=current_user.id
    ).first_or_404()

    db.session.delete(tarea)
    db.session.commit()

    flash("Tarea eliminada correctamente.", "success")
    return redirect(url_for("dashboard"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("inicio"))

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def error_interno(error):
    db.session.rollback()
    return render_template("500.html"), 500

@app.after_request
def agregar_encabezados_seguridad(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'"
    return response

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(
        debug=os.environ.get("FLASK_DEBUG") == "1"
    )