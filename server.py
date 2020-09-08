# Importar librerias
import mysql.connector
from flask import Flask, flash, render_template, redirect, url_for, session, request
import formularios

# Definición de un objeto app de Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '5c063bbb907989439184fce0bf7887074cca1049'


# Definición de la función dbconexion(); para hacer la conexión a la BD Mysql
def dbconexion():
    try:
        config = {
        'user': 'root',
        'password': 'Kesit023',
        'host': '127.0.0.1',
        'auth_plugin': 'mysql_native_password',
        'raise_on_warnings': True,
        'database': 'casos'
        }
        #**Especifica que se envia como parametro un dic
        conexion = mysql.connector.connect(**config)

    except (conexion.err.OperationalError, config.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)
    #Devolvemos la conexión
    return conexion

# Definición de la función obtenerdatos(); obtener todos los casos y temas almacenados en la bd para cargar los elementos select HTML.
def obtenerdatos():
    conexion = dbconexion()
    try:
        with conexion.cursor() as cursor:
            query = ("SELECT id,nombre FROM casos;")
            cursor.execute(query)
            casos = [(0, "- Selecciona un caso -")]
            casos += cursor.fetchall()
            query = ("SELECT DISTINCT tema FROM temas order by tema;")
            cursor.execute(query)
            temas = [("- Selecciona un tema -")]
            for tema in cursor:
                temas += tema
            cursor.close()
    finally:
        conexion.close()
        #Devolvemos las variables de las consultas
    return (casos, temas)

# Definición de la funcion consultarcaso(); obtener un casos específico y los temas vinculados con el caso.
def consultarcaso(valor):
    conexion = dbconexion()
    try:
        with conexion.cursor() as cursor:
            if isinstance(valor, int):
                query = ("SELECT * FROM casos where id=" + str(valor) + ";")
            else:
                query = ("SELECT * FROM casos where nombre='" + valor + "';")
            cursor.execute(query)
            print(query)
            caso = cursor.fetchall()

            if isinstance(valor, int):
                query = ("SELECT temas.tema FROM casos INNER JOIN temas ON temas.id_caso = casos.id where temas.id_caso=" + str(valor) + ";")
            else:
                query = ("SELECT temas.tema FROM casos INNER JOIN temas ON temas.id_caso = casos.id where nombre='" + valor + "';")

            cursor.execute(query)
            temas = cursor.fetchall()
            cursor.close()
    finally:
        conexion.close()
        # Devolvemos las variables de las consultas
    return (caso, temas)

# Definición de la función consultartemas(<parametro>); obtener todos los casos relacionados con un tema en especifico.
def consultartemas(nombre):
    conexion = dbconexion()
    try:
        with conexion.cursor() as cursor:
            query = ("SELECT nombre FROM casos INNER JOIN temas ON temas.id_caso = casos.id where tema='" + nombre + "';")
            cursor.execute(query)
            temas = cursor.fetchall()
            cursor.close()
    finally:
        conexion.close()
        # Devolvemos la variable de la consulta
    return (temas)

#Indicamos la ruta para la página principal y su función presentación()
@app.route("/")
def presentacion():
    # Llamada a la función obtenerdatos, e instanciar las Clases para llenar los elementos select
    query_casos, query_temas = obtenerdatos()
    cmb_casos = formularios.Caso()
    cmb_casos.caso.choices = query_casos
    cmb_temas = formularios.Tema()
    cmb_temas.tema.choices = query_temas
    # Devolvemos las variables de las consultas
    return render_template("presentacion.html",cmb_casos=cmb_casos, cmb_temas=cmb_temas)

#Indicamos la ruta para la página sobremi y su función sobremi()
@app.route("/sobremi")
def sobremi():
    # Llamada a la función obtenerdatos, e instanciar las Clases para llenar los elementos select
    query_casos, query_temas = obtenerdatos()
    cmb_casos = formularios.Caso()
    cmb_casos.caso.choices = query_casos
    cmb_temas = formularios.Tema()
    cmb_temas.tema.choices = query_temas
    # Devolvemos las variables de las consultas
    return render_template("sobremi.html", cmb_casos=cmb_casos, cmb_temas=cmb_temas)

#Indicamos la ruta para la página internacional y su función consultarinternacional(); Obtener todos los archivos relacionados con la materia derecho internacional.
@app.route("/internacional")
def consultarinternacional():
    # Llamada a la función obtenerdatos, e instanciar las Clases para llenar los elementos select
    query_casos, query_temas = obtenerdatos()
    cmb_casos = formularios.Caso()
    cmb_casos.caso.choices = query_casos
    cmb_temas = formularios.Tema()
    cmb_temas.tema.choices = query_temas
    conexion = dbconexion()
    try:
        with conexion.cursor() as cursor:
            #Consultar los archivos por materia internacional
            query = ("SELECT nombre FROM archivos where materia='internacional';")
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
    finally:
        conexion.close()
    # Devolvemos las variables de las consultas
    return render_template("internacional.html", data=data, cmb_casos=cmb_casos, cmb_temas=cmb_temas)

#Indicamos la ruta para la página teoria y su función consultateoria(); Obtener todos los archivos relacionados con la materia teoría del derecho.
@app.route("/teoria")
def consultateoria():
    # Llamada a la función obtenerdatos, e instanciar las Clases para llenar los elementos select
    query_casos, query_temas = obtenerdatos()
    cmb_casos = formularios.Caso()
    cmb_casos.caso.choices = query_casos
    cmb_temas = formularios.Tema()
    cmb_temas.tema.choices = query_temas
    conexion = dbconexion()
    try:
        with conexion.cursor() as cursor:
            #Consultar los archivos por materia teoría
            query = ("SELECT nombre FROM archivos where materia='teoría';")
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
    finally:
        conexion.close()
    # Devolvemos las variables de las consultas
    return render_template("teoria.html", data=data, cmb_casos=cmb_casos, cmb_temas=cmb_temas)

#Indicamos la ruta para la página comparado y su función consultarcomparado(); Obtener todos los archivos relacionados con la materia derecho comparado.
@app.route("/comparado")
def consultarcomparado():
    # Llamada a la función obtenerdatos, e instanciar las Clases para llenar los elementos select
    query_casos, query_temas = obtenerdatos()
    cmb_casos = formularios.Caso()
    cmb_casos.caso.choices = query_casos
    cmb_temas = formularios.Tema()
    cmb_temas.tema.choices = query_temas
    conexion = dbconexion()
    # print(os.path.abspath(__file__))
    # contenido = os.listdir('/ApoyoEdu/static/comparado')
    try:
        with conexion.cursor() as cursor:
            #Consultar los archivos por materia comparado
            query = ("SELECT nombre FROM archivos where materia='comparado';")
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
    finally:
        conexion.close()
    # Devolvemos las variables de las consultas
    return render_template("comparado.html", data=data, cmb_casos=cmb_casos, cmb_temas=cmb_temas)

#Indicamos la ruta para la página casos y su función casos(); Obtener el caso especifico para ser desplegado
@app.route("/casos", methods=['GET','POST'])
def casos():
    # Llamada a la función obtenerdatos, e instanciar las Clases para llenar los elementos select
    query_casos, query_temas = obtenerdatos()
    cmb_casos = formularios.Caso()
    cmb_casos.caso.choices = query_casos
    cmb_temas = formularios.Tema()
    cmb_temas.tema.choices = query_temas
    if request.method == 'GET':
        if request.args:
            valor=str(request.args.get('caso'))
            # Llamada a la función consultarcaso; enviando como parámetro el nombre del caso
            caso, temas_vin = consultarcaso(valor)

        # Devolvemos las variables de las consultas
        return render_template("casos.html", cmb_casos=cmb_casos, cmb_temas=cmb_temas, caso=caso, temas_vin=temas_vin)

    if cmb_casos.validate_on_submit():
        idcaso = cmb_casos.caso.data
        if int(idcaso) != 0:
            # Llamada a la función consultarcaso; enviando como parámetro el id del caso
            caso, temas_vin = consultarcaso(int(idcaso))
            return render_template("casos.html", cmb_casos=cmb_casos, cmb_temas=cmb_temas, caso=caso, temas_vin=temas_vin)
        else:
            flash('¡ Selecciona un caso !')

            # Devolvemos las variables de las consultas
            return render_template("casos.html", cmb_casos=cmb_casos, cmb_temas=cmb_temas)

#Indicamos la ruta para la página temas y su función temas()
@app.route("/temas", methods=['POST'])
def temas():
    # Llamada a la función obtenerdatos, e instanciar las Clases para llenar los elementos select
    query_casos, query_temas = obtenerdatos()
    cmb_casos = formularios.Caso()
    cmb_casos.caso.choices = query_casos
    cmb_temas = formularios.Tema()
    cmb_temas.tema.choices = query_temas

    if cmb_temas.validate_on_submit():
        tema = cmb_temas.tema.data
        if tema != '- Selecciona un tema -':
            # Llamada a la función consultartemas; enviando como parámetro el nombre del tema
            casos = consultartemas(tema)
            return render_template("temas.html", cmb_casos=cmb_casos, cmb_temas=cmb_temas, casos=casos, tema=tema)
        else:
            flash('¡ Selecciona un tema !')

            # Devolvemos las variables de las consultas
            return render_template("temas.html", cmb_casos=cmb_casos, cmb_temas=cmb_temas)


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    msg='Inicio de seción'
    conexion = dbconexion()
    # Llamada a la función obtenerdatos
    casos, temas = obtenerdatos()
    datos = formularios.loginform()
    try:
        if request.method == 'POST':
            if datos.validate_on_submit():
                usuario = datos.usuario.data
                contraseña = datos.contraseña.data
                with conexion.cursor() as cursor:
                    # Consultar si el usuario existe en la bd para permitir los accesos.
                    query = ("SELECT * FROM usuario where usuario='" + usuario + "' and contraseña='" + contraseña + "';")
                    cursor.execute(query)
                    data = cursor.fetchall()
                    cursor.close()
                if data:
                    print("hola admin")
                    return render_template('adminprincipal.html',usuario=usuario, casos=casos, temas=temas)
                else:
                    flash("El usuario no exite o los datos son incorectos")
    # except:  # catch *all* exceptions
    #     e = sys.exc_info()[0]
    #     write_to_page("<p>Error: %s</p>" % e)
    finally:
        conexion.close()
    # Devolvemos las variables de las consultas
    return render_template("admin.html", datos=datos, msg=msg)

@app.route("/adminprincipal<string:usuario>", methods=['POST'])
def adminprincipal(usuario):
    data= None
    vinculados = None
    casos, temas = obtenerdatos()
    if request.form['casos']:
        caso = request.form['casos']
        data, vinculados = consultarcaso(caso)
        print(data)
    # Devolvemos las variables de las consultas
    return render_template("adminprincipal.html", usuario=usuario, casos=casos, temas=temas, data=data, vinculados=vinculados)

@app.route("/agregar<string:usuario>", methods=['POST'])
def agregar(usuario):
    data= None
    vinculados = None
    casos, temas = obtenerdatos()
    if request.method == 'POST':
        # id=request.form['id']
        año=request.form['año']
        tribunal = request.form['tribunal']
        nombre = request.form['nombre']
        hechos = request.form['hechos']
        conexion = dbconexion()
        data= [tribunal,nombre,hechos]
        print(data)
        try:
            with conexion.cursor() as cursor:
                query = ('INSERT INTO casos (tribunal,nombre,hechos) VALUES (%s,%s,%s)',data)
                #query =("UPDATE casos SET año=%s, tribunal=%s, nombre=%s, hechos=%s WHERE id=%s", (año, tribunal, nombre, hechos, id))
                cursor.execute(query)
                #data = cursor.fetchall()
                #conexion.commit()
                cursor.close()
        except Exception as e:
            print(e)
        finally:
            conexion.close()

    # Devolvemos las variables de las consultas
    return render_template("adminprincipal.html", usuario=usuario, casos=casos, temas=temas)

@app.route("/admincasos<string:usuario>", methods=['GET', 'POST'])
def admincasos(usuario):
    casos, temas = obtenerdatos()
    caso = request.form['casos']
    print(caso)
    if caso != []:
        data, vinculados = consultarcaso(caso)
        print(data)
        print(vinculados)
    # try:
    #     conn = mysql.connect()
    #     cursor = conn.cursor(pymysql.cursors.DictCursor)
    #     cursor.execute("SELECT * FROM temas")
    #     rows = cursor.fetchall()
    #     table = Results(rows)
    #     return render_template('users.html', table=table)
    # except Exception as e:
    #     print(e)
    # finally:
    #     cursor.close()
    #     conn.close()

    # Devolvemos las variables de las consultas
    return render_template("admincasos.html", usuario=usuario, casos=casos, temas=temas, data=data,vinculados=vinculados)

# db=MySQL(app)
#
# class Casos(db.Model):
#     año = db.Column(db.SmallInt(), nullable=False, primary_key=True)
#     año = db.Column(db.String(4), unique=True, nullable=False, primary_key=True)
#     tribunal = db.Column(db.String(30), unique=True, nullable=False, primary_key=True)
#     tribunal = db.Column(db.String(30), unique=True, nullable=False, primary_key=True)


if __name__ == "__main__":
    app.run(host='localhost', debug=True)

