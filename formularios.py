from html import escape
from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import StringField, SubmitField, PasswordField, SelectField, HiddenField, Field, TextAreaField
from wtforms.validators import DataRequired, Length, Optional
from wtforms.widgets import html_params, HTMLString
from flask_wtf.file import FileField, FileRequired, FileAllowed

class InlineButtonWidget(object):
    def __init__(self, class_=None):
        self.class_ = class_

    def __call__(self, field, **kwargs):
        kwargs.setdefault('type', 'submit')
        kwargs["class"] = self.class_
        title = kwargs.pop('title', field.description or '')
        params = html_params(title=title, **kwargs)

        html = '<button %s>%s</button>'

        return HTMLString(html % (params, escape(field.label.text)))

class InlineButton(Field):
    widget = InlineButtonWidget()

    def __init__(self, label=None, validators=None, text='Save', **kwargs):
        super(InlineButton, self).__init__(label, validators, **kwargs)
        self.text = text

    def _value(self):
        if self.data:
            return u''.join(self.data)
        else:
            return u''

class FrmAcceso(FlaskForm):
    usuario = StringField('usuario', validators=[DataRequired(), Length(max=20)], render_kw={"placeholder": "usuario"})
    contraseña = PasswordField('contraseña', validators=[DataRequired(), Length(max=20)], render_kw={"placeholder": "contraseña"})
    submit = SubmitField('Acceder')

class FrmCmbCasos(FlaskForm):
    caso = SelectField('caso', choices=[], validators=[DataRequired()])
    text = Markup('<i class="icon solid fa-search"></i>')
    # This class_ param it's applied in the class of the button in HTML.
    submit = SubmitField(text, widget=InlineButtonWidget(class_="small btn-default primary"))

class FrmCmbTemas(FlaskForm):
    tema = SelectField('tema', validators=[DataRequired()])
    text = Markup('<i></i>')
    # This class_ param it's applied in the class of the button in HTML.
    submit = SubmitField(text, widget=InlineButtonWidget(class_="small btn-default primary icon solid fa-search"))

class FrmMateria(FlaskForm):
    nombre = SelectField('nombre', choices=["- Selecciona una materia -", "Comparado", "Internacional", "Teoría"], validators=[DataRequired()])
    text = Markup('<i></i>')
    # This class_ param it's applied in the class of the button in HTML.
    submit = SubmitField(text, widget=InlineButtonWidget(class_="small btn-default primary icon solid fa-search"))

class FrmNuevo(FlaskForm):
    text = Markup('<i>Agregar nuevo registro</i>')
    # This class_ param it's applied in the class of the button in HTML.
    submit = SubmitField(text, widget=InlineButtonWidget(class_="small btn-default primary icon solid fa-file"))

class FrmActualizar(FlaskForm):
    text = Markup('<i>Actualizar registro</i>')
    # This class_ param it's applied in the class of the button in HTML.
    submit = SubmitField(text, widget=InlineButtonWidget(class_="small btn-default primary icon solid fa-pen"))

class FrmCasos(FlaskForm):
    idcaso = HiddenField('Id')
    año = StringField('Año:', validators=[DataRequired(), Length(max=4)])
    tribunal = StringField('Tribunal:', validators=[Length(max=30)])
    nombre = StringField('Nombre y clasificación:', validators=[DataRequired(), Length(max=300)])
    hechos = TextAreaField('Hechos y consideraciones:', render_kw={"rows": 8}, validators=[DataRequired()])

class FrmCasosEliminar(FlaskForm):
    idcaso = HiddenField('Id', validators=[Optional()])
    año = StringField('Año:', validators=[Optional(), Length(max=4)])
    tribunal = StringField('Tribunal:', validators=[Optional(), Length(max=30)])
    nombre = StringField('Nombre y clasificación:', validators=[Optional(), Length(max=300)])
    hechos = TextAreaField('Hechos y consideraciones:', render_kw={"rows": 8}, validators=[Optional()])
    text = Markup('<i class="icon solid fa-trash-alt">Eliminar</i>')
    # This class_ param it's applied in the class of the button in HTML.
    submit = SubmitField(text, widget=InlineButtonWidget(class_="small btn-default primary"))

class FrmTemas(FlaskForm):
    id = HiddenField('Id')
    tema = StringField('Tema:', validators=[DataRequired(), Length(max=100)])
    caso = StringField('Nombre y clasificación:', validators=[DataRequired(), Length(max=300)])

class FrmTemasEliminar(FlaskForm):
    id = HiddenField('Id', validators=[Optional()])
    caso = StringField('Caso', validators=[Optional(), Length(max=300)])
    tema = StringField('Tema:', validators=[Optional(), Length(max=50)])
    text = Markup('<i class="icon solid fa-trash-alt">Eliminar</i>')
    # This class_ param it's applied in the class of the button in HTML.
    submit = SubmitField(text, widget=InlineButtonWidget(class_="small btn-default primary"))

class FrmArchivosEliminar(FlaskForm):
    id = HiddenField('Id', validators=[Optional()])
    nombre = StringField('Nombre:', validators=[Optional(), Length(max=100)])
    materia = StringField('Materia:', validators=[Optional(), Length(max=15)])
    text = Markup('<i class="icon solid fa-trash-alt">Eliminar</i>')
    # This class_ param it's applied in the class of the button in HTML.
    submit = SubmitField(text, widget=InlineButtonWidget(class_="small btn-default primary"))

class FrmArchivos(FlaskForm):
    id = HiddenField('Id')
    nombre = StringField('Nombre:', validators=[DataRequired(), Length(max=100)])
    materia = SelectField('Materia', choices=["- Selecciona una materia -", "Comparado", "Internacional", "Teoría"], validators=[DataRequired()])

class FrmSubir(FlaskForm):
    materia = SelectField('Materia:', choices=["- Selecciona una materia -", "comparado", "internacional", "teoria"], validators=[DataRequired()])
    nombre = FileField('Archivo:', validators=[FileRequired(), FileAllowed(['pdf', 'pptx'], 'Subir solo .pdf y .pptx')])
    text = Markup('<i class="icon solid fa-file">Subir archivo</i>')
    # This class_ param it's applied in the class of the button in HTML.
    submit = SubmitField(text, widget=InlineButtonWidget(class_="small btn-default primary"))
