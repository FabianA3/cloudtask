from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# Crear el formulario de registro
class RegistroForm(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(),
            Length(min=2, max=100)
        ]
    )

    email = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(),
            Length(min=8, max=128)
        ]
    )

    confirmar_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    submit = SubmitField("Crear cuenta")

# Crear el formulario de inicio de sesión
class LoginForm(FlaskForm):
    email = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Iniciar sesión")

# Crear el formulario de tareas
class TareaForm(FlaskForm):
    titulo = StringField(
        "Título",
        validators=[
            DataRequired(),
            Length(min=3, max=150)
        ]
    )

    descripcion = TextAreaField(
        "Descripción",
        validators=[
            Length(max=1000)
        ]
    )

    prioridad = SelectField(
        "Prioridad",
        choices=[
            ("Baja", "Baja"),
            ("Media", "Media"),
            ("Alta", "Alta")
        ],
        validators=[DataRequired()]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("Pendiente", "Pendiente"),
            ("En progreso", "En progreso"),
            ("Completada", "Completada")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Guardar tarea")