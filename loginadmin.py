from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(UserMixin):

    def __init__(self, usuario, contraseña, is_admin=False):
        self.usuario = usuario
        self.contraseña = generate_password_hash(contraseña)
        self.is_admin = is_admin

    def set_password(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)

    def check_password(self, contraseña):
        return check_password_hash(self.password, contraseña)

    def __repr__(self):
        return '<User {}>'.format(self.email)

