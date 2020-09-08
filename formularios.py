from html import escape

from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import StringField, SubmitField, PasswordField, SelectField, HiddenField, Field
from wtforms.validators import DataRequired, Length
from wtforms.widgets import html_params, HTMLString


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



class loginform(FlaskForm):
    usuario = StringField('usuario', validators=[DataRequired(), Length(max=20)], render_kw={"placeholder": "usuario"})
    contraseña = PasswordField('contraseña', validators=[DataRequired(), Length(max=20)], render_kw={"placeholder": "contraseña"})
    submit = SubmitField('Acceder')


class Caso(FlaskForm):
    frmcasos = HiddenField('frmcasos')
    caso = SelectField('caso', choices=[], validators=[DataRequired()])
    text = Markup('<i class="icon solid fa-search"></i>')
    # This class_ param it's applied in the class of the button in HTML.
    submit = SubmitField(text, widget=InlineButtonWidget(class_="btn small btn-default primary"))

class Tema(FlaskForm):
    tema = SelectField('tema', validators=[DataRequired()])
    text = Markup('<i class=""></i>')
    # This class_ param it's applied in the class of the button in HTML.
    submit = SubmitField(text, widget=InlineButtonWidget(class_="btn small btn-default primary icon solid fa-search"))