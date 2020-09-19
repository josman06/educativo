from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(30), unique=True, nullable=False)
    contraseña = db.Column(db.String(66), nullable=False)

class Archivos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    materia = db.Column(db.String(15), nullable=False)

    def __init__(self, nombre, materia):
        self.nombre = nombre
        self.materia = materia

class Casos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    año = db.Column(db.String(4), nullable=False)
    tribunal = db.Column(db.String(30), nullable=True)
    nombre = db.Column(db.String(300), nullable=False)
    hechos = db.Column(db.Text, nullable=False)

    def __init__(self, año, tribunal, nombre, hechos):
        self.año = año
        self.tribunal = tribunal
        self.nombre = nombre
        self.hechos = hechos

class Temas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_caso = db.Column(db.Integer, db.ForeignKey('casos.id'), nullable=False)
    tema = db.Column(db.String(50), nullable=False)

    def __init__(self, id_caso, tema):
        self.id_caso = id_caso
        self.tema = tema

#Funciones SqlAlchemy

# Definición de la funcion Consultar_Caso_Id(); obtener un casos específico por Id y los temas vinculados con el caso.
def Consultar_Caso_Id(id):
    query = db.session.query(Casos).get(id)
    query2 = db.session.query(Temas).filter(Temas.id_caso==id)
    data = [(query.id,query.año,query.tribunal,query.nombre,query.hechos)]
    data2 = []
    for x in query2:
        data2.append((x.tema, x.id))
    return data,data2

# Definición de la función Consultar_Temas_Tema(tema); obtener todos los casos relacionados con un tema en especifico.
def Consultar_Temas_Tema(tema):
    query = db.session.query(Casos.id, Casos.nombre).join(Temas).filter(Temas.tema == tema)
    data = []
    for x in query:
        data.append((x.id, x.nombre))
    return data

# Definición de la función Consultar_Casos_Temas(); obtener todos los casos y temas almacenados en la bd para cargar los elementos select HTML.
def Consultar_Casos_Temas():
    query_casos = db.session.query(Casos.id, Casos.nombre)
    query_temas = db.session.query(Temas.tema).distinct()
    data_casos = []
    data_temas = []
    caso = (0, "- Selecciona un caso -")
    data_temas.append("- Selecciona un tema -",)
    data_casos.append(caso)
    for x in query_casos:
        caso = None
        caso = x.id, x.nombre
        data_casos.append(caso)
    for x in query_temas:
        data_temas.append(x.tema)

    return data_casos, data_temas

# Definición de la función Consultar_Usuario(); consultar usuario para permitir el acceso al administrador.
def Consultar_Usuario(nombre):
    query = db.session.query(Usuario).filter(Usuario.usuario == nombre).first()
    return query

# Definición de la función Consultar_Archivo(); consultar archivo dependiendo de la materia.
def Consultar_Archivo(nombre):
    query = db.session.query(Archivos).filter(Archivos.materia == nombre).all()
    data= []
    for x in query:
        data.append((x.nombre, x.id))
    return query

