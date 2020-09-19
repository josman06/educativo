# Importar librerias
from config import Desarrollo
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from flask import Flask, flash, render_template, redirect, url_for, session, request, send_from_directory
from formularios import  FrmAcceso, FrmCmbCasos, FrmCmbTemas, FrmMateria, FrmNuevo, FrmActualizar, FrmSubir, \
    FrmCasos, FrmCasosEliminar,  FrmTemas, FrmTemasEliminar, FrmArchivos, FrmArchivosEliminar
from modelo import db, Casos, Temas, Archivos, Consultar_Caso_Id,Consultar_Temas_Tema, Consultar_Usuario, \
    Consultar_Casos_Temas, Consultar_Archivo
import os

# Definición de un objeto app de Flaskc
app = Flask(__name__)
#Instanciar el objeto del ambiente dearrollo
app.config.from_object("config.Desarrollo")
csrf = CSRFProtect()

#********************* Definición de rutas (URL's) y funciones *******************************************

#Indicamos la ruta para la página principal y su función presentación()
@app.route("/")
def presentacion():
    # Llamada a la función Consultar_Casos_Temas(), e instanciar las Clases para llenar los elementos select
    query_casos, query_temas = Consultar_Casos_Temas()
    cmb_casos = FrmCmbCasos()
    cmb_casos.caso.choices = query_casos
    cmb_temas = FrmCmbTemas()
    cmb_temas.tema.choices = query_temas
    # Devolvemos las variables de las consultas
    return render_template("/publico/presentacion.html",cmb_casos=cmb_casos, cmb_temas=cmb_temas)

#Indicamos la ruta para la página sobremi y su función sobremi()
@app.route("/sobremi")
def sobremi():
    # Llamada a la función Consultar_Casos_Temas(), e instanciar las Clases para llenar los elementos select
    query_casos, query_temas = Consultar_Casos_Temas()
    cmb_casos = FrmCmbCasos()
    cmb_casos.caso.choices = query_casos
    cmb_temas = FrmCmbTemas()
    cmb_temas.tema.choices = query_temas
    # Devolvemos las variables de las consultas
    return render_template("/publico/sobremi.html", cmb_casos=cmb_casos, cmb_temas=cmb_temas)

#Indicamos la ruta para la página internacional y su función consultarinternacional(); Obtener todos los archivos relacionados con la materia derecho internacional.
@app.route("/internacional")
def consultarinternacional():
    # Llamada a la función Consultar_Casos_Temas(), e instanciar las Clases para llenar los elementos select
    query_casos, query_temas = Consultar_Casos_Temas()
    cmb_casos = FrmCmbCasos()
    cmb_casos.caso.choices = query_casos
    cmb_temas = FrmCmbTemas()
    cmb_temas.tema.choices = query_temas
    data= Consultar_Archivo('internacional')
    # Devolvemos las variables de las consultas
    return render_template("/publico/internacional.html", data=data, cmb_casos=cmb_casos, cmb_temas=cmb_temas)

#Indicamos la ruta para la página teoria y su función consultateoria(); Obtener todos los archivos relacionados con la materia teoría del derecho.
@app.route("/teoria")
def consultateoria():
    # Llamada a la función Consultar_Casos_Temas(), e instanciar las Clases para llenar los elementos select
    query_casos, query_temas = Consultar_Casos_Temas()
    cmb_casos = FrmCmbCasos()
    cmb_casos.caso.choices = query_casos
    cmb_temas = FrmCmbTemas()
    cmb_temas.tema.choices = query_temas
    data= Consultar_Archivo('teoria')
    # Devolvemos las variables de las consultas
    return render_template("/publico/teoria.html", data=data, cmb_casos=cmb_casos, cmb_temas=cmb_temas)

#Indicamos la ruta para la página comparado y su función consultarcomparado(); Obtener todos los archivos relacionados con la materia derecho comparado.
@app.route("/comparado")
def consultarcomparado():
    # Llamada a la función Consultar_Casos_Temas(), e instanciar las Clases para llenar los elementos select
    query_casos, query_temas = Consultar_Casos_Temas()
    cmb_casos = FrmCmbCasos()
    cmb_casos.caso.choices = query_casos
    cmb_temas = FrmCmbTemas()
    cmb_temas.tema.choices = query_temas
    data= Consultar_Archivo('comparado')
    # Devolvemos las variables de las consultas
    return render_template("/publico/comparado.html", data=data, cmb_casos=cmb_casos, cmb_temas=cmb_temas)

#Indicamos la ruta para la página casos y su función casos(); Obtener el caso especifico para ser desplegado
@app.route("/casos", methods=['GET','POST'])
def casos():
    # Llamada a la función Consultar_Casos_Temas(), e instanciar las Clases para llenar los elementos select
    query_casos, query_temas = Consultar_Casos_Temas()
    cmb_casos = FrmCmbCasos()
    cmb_casos.caso.choices = query_casos
    cmb_temas = FrmCmbTemas()
    cmb_temas.tema.choices = query_temas
    if request.method == 'GET':
        if request.args:
            valor=str(request.args.get('caso'))
            # Llamada a la función Consultar_Caso_Id(id); enviando como parámetro el id del caso
            caso,temas_vin = Consultar_Caso_Id(int(valor))
        # Devolvemos las variables de las consultas
        return render_template("/publico/casos.html", cmb_casos=cmb_casos, cmb_temas=cmb_temas, caso=caso, temas_vin=temas_vin)
    if cmb_casos.validate_on_submit():
        idcaso = cmb_casos.caso.data
        if int(idcaso) != 0:
            # Llamada a la función Consultar_Caso_Id(id); enviando como parámetro el id del caso
            caso, temas_vin = Consultar_Caso_Id(idcaso)
            return render_template("/publico/casos.html", cmb_casos=cmb_casos, cmb_temas=cmb_temas, caso=caso, temas_vin=temas_vin)
        else:
            flash('¡ Selecciona un caso !')
            # Devolvemos las variables de las consultas
            return render_template("/publico/casos.html", cmb_casos=cmb_casos, cmb_temas=cmb_temas)

#Indicamos la ruta para la página temas y su función temas()
@app.route("/temas", methods=['POST'])
def temas():
    # Llamada a la función Consultar_Casos_Temas(), e instanciar las Clases para llenar los elementos select
    query_casos, query_temas = Consultar_Casos_Temas()
    cmb_casos = FrmCmbCasos()
    cmb_casos.caso.choices = query_casos
    cmb_temas = FrmCmbTemas()
    cmb_temas.tema.choices = query_temas
    if cmb_temas.validate_on_submit():
        tema = cmb_temas.tema.data
        if tema != '- Selecciona un tema -':
            # Llamada a la función Consultar_Temas_Tema(); enviando como parámetro el nombre del tema
            casos = Consultar_Temas_Tema(tema)
            return render_template("/publico/temas.html", cmb_casos=cmb_casos, cmb_temas=cmb_temas, casos=casos, tema=tema)
        else:
            flash('¡ Selecciona un tema !')
            # Devolvemos las variables de las consultas
            return render_template("/publico/temas.html", cmb_casos=cmb_casos, cmb_temas=cmb_temas)

@app.route("/salir")
def salir():
    # Eliminar sesión
    session.pop("username", None)
    flash("Sesión cerrada.")
    # Llamada a la función Consultar_Casos_Temas(), e instanciar las Clases para llenar los elementos select
    query_casos, query_temas = Consultar_Casos_Temas()
    cmb_casos = FrmCmbCasos()
    cmb_casos.caso.choices = query_casos
    cmb_temas = FrmCmbTemas()
    cmb_temas.tema.choices = query_temas
    # Devolvemos las variables de las consultas
    return render_template("/publico/presentacion.html", cmb_casos=cmb_casos, cmb_temas=cmb_temas)


#Indicamos la ruta para la página acceso y su función acceso()
@app.route("/acceso", methods=['GET', 'POST'])
def acceso():
    datos = FrmAcceso()
    if request.method == 'POST':
        if datos.validate_on_submit():
            usuario= datos.usuario.data
            # Llamada a la función Consultar_Usuario(), verificar si el usuario existe
            user = Consultar_Usuario(usuario)
            if user and check_password_hash(user.contraseña, datos.contraseña.data):
                session["username"] = usuario
                flash("Inicio de sesión exitoso")
                return render_template("/admin/administracion.html")
            else:
                flash("¡ El usuario no exite o los datos son incorectos !")

    return render_template("/admin/acceso.html", datos=datos)

@app.route("/administracion", methods=['GET', 'POST'])
def administracion():
    if "username" in session:
        archivo = FrmSubir()
        if archivo.validate_on_submit():
            if archivo.materia.data != "- Selecciona una materia -":
                f = archivo.nombre.data
                materia = archivo.materia.data
                filename = secure_filename(f.filename)
                f.save(os.path.join(os.path.abspath("./static/" + materia ), filename))
                flash('Archivo cargado con exito')
                return render_template("/admin/administracion.html")
            else:
                flash('¡ Selecciona una materia !')
                # Devolvemos las variables de las consultas
                return render_template("/admin/administracion.html")
    return render_template("/admin/administracion.html", archivo=archivo)

##################### Admin Casos ########################################

@app.route("/administracion/casos", methods=['GET', 'POST'])
def casosadmin():
    if "username" in session:
        #Llamada a la función Consultar_Casos_Temas(), e instanciar las funciones para llenar los elementos select
        query_casos, query_temas = Consultar_Casos_Temas()
        cmb_casos = FrmCmbCasos()
        cmb_casos.caso.choices = query_casos
        datos = FrmCasosEliminar()
        nuevo = FrmNuevo()
        actualizar = FrmActualizar()
        if cmb_casos.validate_on_submit():
            idcaso = cmb_casos.caso.data
            if int(idcaso) != 0:
                # Llamada a la función Consultar_Caso_Id(); enviando como parámetro el id del caso
                caso, temas_vin = Consultar_Caso_Id(idcaso)
                datos.idcaso.data = caso[0][0]
                datos.año.data = caso[0][1]
                datos.tribunal.data = caso[0][2]
                datos.nombre.data = caso[0][3]
                datos.hechos.data = caso[0][4]
                return render_template("/admin/casosadmin.html", cmb_casos=cmb_casos, datos=datos)
            else:
                flash('¡ Selecciona un caso !')
                return render_template("/admin/casosadmin.html", cmb_casos=cmb_casos)
        elif datos.validate_on_submit() and request.method == 'POST':
            data = Casos.query.get(int(datos.idcaso.data))
            db.session.delete(data)
            db.session.commit()
            flash('Registro eliminado')
            query_casos, query_temas = Consultar_Casos_Temas()
            cmb_casos = FrmCmbCasos()
            cmb_casos.caso.choices = query_casos
            return render_template("/admin/casosadmin.html", cmb_casos=cmb_casos, nuevo=nuevo, actualizar=actualizar)

        return render_template("/admin/casosadmin.html", cmb_casos=cmb_casos, nuevo=nuevo, actualizar=actualizar)

@app.route("/administracion/casos/agregar", methods=['GET', 'POST'])
def casosagregar():
    if "username" in session:
        #Llamada a la función Consultar_Casos_Temas(), e instanciar las funciones para llenar los elementos select
        query_casos, query_temas = Consultar_Casos_Temas()
        cmb_casos = FrmCmbCasos()
        cmb_casos.caso.choices = query_casos
        nuevo = FrmNuevo()
        actualizar = FrmActualizar()
        agregar = FrmCasos()
        if agregar.validate_on_submit() and request.method == 'POST':
            año = agregar.año.data
            tribunal = agregar.tribunal.data
            nombre = agregar.nombre.data
            hechos = agregar.hechos.data
            data = Casos(año, tribunal, nombre, hechos)
            db.session.add(data)
            db.session.commit()
            flash('Registro agregado')
            query_casos, query_temas = Consultar_Casos_Temas()
            cmb_casos = FrmCmbCasos()
            cmb_casos.caso.choices = query_casos
            return render_template("/admin/casosadmin.html", cmb_casos=cmb_casos, nuevo=nuevo, actualizar=actualizar)
            # Devolvemos las variables de las consultas
        return render_template("/admin/casosagregar.html", cmb_casos=cmb_casos, agregar=agregar)

@app.route("/administracion/casos/actualizar", methods=['GET', 'POST'])
def casosactualizar():
    if "username" in session:
        #Llamada a la función Consultar_Casos_Temas(), e instanciar las funciones para llenar los elementos select
        query_casos, query_temas = Consultar_Casos_Temas()
        cmb_casos = FrmCmbCasos()
        cmb_casos.caso.choices = query_casos
        datos = FrmCasos()
        nuevo = FrmNuevo()
        actualizar = FrmActualizar()
        if cmb_casos.validate_on_submit() and request.method =='POST':
            idcaso = cmb_casos.caso.data
            if int(idcaso) != 0:
                # Llamada a la función Consultar_Caso_Id(); enviando como parámetro el id del caso
                caso, temas_vin = Consultar_Caso_Id(idcaso)
                datos.idcaso.data = caso[0][0]
                datos.año.data = caso[0][1]
                datos.tribunal.data = caso[0][2]
                datos.nombre.data = caso[0][3]
                datos.hechos.data = caso[0][4]
                return render_template("/admin/casosactualizar.html", cmb_casos=cmb_casos, datos=datos)
            else:
                flash('¡ Selecciona un caso !')
                return render_template("/admin/casosadmin.html", cmb_casos=cmb_casos)
        elif datos.validate_on_submit() and request.method =='POST':
            data = Casos.query.get(int(datos.idcaso.data))
            data.año = datos.año.data
            data.tribunal = datos.tribunal.data
            data.nombre = datos.nombre.data
            data.hechos = datos.hechos.data
            db.session.commit()
            flash('Registro actualizado')
            query_casos, query_temas = Consultar_Casos_Temas()
            cmb_casos = FrmCmbCasos()
            cmb_casos.caso.choices = query_casos
            return render_template("/admin/casosadmin.html", cmb_casos=cmb_casos, nuevo=nuevo, actualizar=actualizar)

        return render_template("/admin/casosactualizar.html", cmb_casos=cmb_casos)

######################## Admin Temas #####################################

@app.route("/administracion/temas", methods=['GET', 'POST'])
def temasadmin():
    if "username" in session:
        #Llamada a la función Consultar_Casos_Temas(), e instanciar las funciones para llenar los elementos select
        query_casos, query_temas = Consultar_Casos_Temas()
        cmb_casos = FrmCmbCasos()
        cmb_casos.caso.choices = query_casos
        datos = FrmTemasEliminar()
        nuevo = FrmNuevo()
        actualizar = FrmActualizar()
        if cmb_casos.validate_on_submit():
            idcaso = cmb_casos.caso.data
            if int(idcaso) != 0:
                # Llamada a la función Consultar_Caso_Id(); enviando como parámetro el id del caso
                caso, temas_vin = Consultar_Caso_Id(idcaso)
                data = []
                for x in temas_vin:
                    datos = FrmTemasEliminar()
                    datos.id.data = x[1]
                    datos.caso.data = caso[0][3]
                    datos.tema.data = x[0]
                    data.append(datos)
                return render_template("/admin/temasadmin.html", cmb_casos=cmb_casos, datos=datos, data=data)
            else:
                flash('¡ Selecciona un caso !')
                # Devolvemos las variables de las consultas
                return render_template("/admin/temasadmin.html", cmb_casos=cmb_casos)
        elif datos.validate_on_submit() and request.method == 'POST':
            data = Temas.query.get(int(datos.id.data))
            db.session.delete(data)
            db.session.commit()
            flash('Registro eliminado')
            query_casos, query_temas = Consultar_Casos_Temas()
            cmb_casos = FrmCmbCasos()
            cmb_casos.caso.choices = query_casos
            return render_template("/admin/temasadmin.html", cmb_casos=cmb_casos, nuevo=nuevo, actualizar=actualizar)

        return render_template("/admin/temasadmin.html", cmb_casos=cmb_casos, nuevo=nuevo, actualizar=actualizar)

@app.route("/administracion/temas/agregar", methods=['GET', 'POST'])
def temasagregar():
    if "username" in session:
        #Llamada a la función Consultar_Casos_Temas(), e instanciar las funciones para llenar los elementos select
        query_casos, query_temas = Consultar_Casos_Temas()
        cmb_casos = FrmCmbCasos()
        cmb_casos.caso.choices = query_casos
        nuevo = FrmNuevo()
        actualizar = FrmActualizar()
        agregar = FrmTemas()
        agregar.caso.choices = query_casos
        if agregar.validate_on_submit():
            if agregar.caso.data != "0":
                id_caso = agregar.caso.data
                tema = agregar.tema.data
                data = Temas(id_caso, tema)
                db.session.add(data)
                db.session.commit()
                flash('Registro agregado')
                return render_template("/admin/temasadmin.html", cmb_casos=cmb_casos, nuevo=nuevo, actualizar=actualizar)
            else:
                flash('¡ Selecciona un caso !')
                # Devolvemos las variables de las consultas
                return render_template("/admin/temasagregar.html", agregar=agregar)
        # Devolvemos las variables de las consultas
        return render_template("/admin/temasagregar.html", agregar=agregar)

@app.route("/administracion/temas/actualizar", methods=['GET', 'POST'])
def temasactualizar():
    if "username" in session:
        #Llamada a la función Consultar_Casos_Temas(), e instanciar las funciones para llenar los elementos select
        query_casos, query_temas = Consultar_Casos_Temas()
        cmb_casos = FrmCmbCasos()
        cmb_casos.caso.choices = query_casos
        nuevo = FrmNuevo()
        actualizar = FrmActualizar()
        datos = FrmTemas()
        if cmb_casos.validate_on_submit():
            idcaso = cmb_casos.caso.data
            if datos.caso.data != "0":
                # Llamada a la función Consultar_Caso_Id(); enviando como parámetro el id del caso
                caso, temas_vin = Consultar_Caso_Id(idcaso)
                data = []
                for x in temas_vin:
                    datos = FrmTemas()
                    datos.id.data = x[1]
                    datos.caso.choices = query_casos
                    datos.caso.data = caso[0][3]
                    datos.tema.data = x[0]
                    data.append(datos)
                return render_template("/admin/temasactualizar.html", cmb_casos=cmb_casos, datos=datos, data=data)
            else:
                flash('¡ Selecciona un caso !')
                return render_template("/admin/temasadmin.html", cmb_casos=cmb_casos)

        if datos.validate_on_submit():
            if datos.caso.data != "- Selecciona un caso -":
                data = Temas.query.get(int(datos.id.data))
                data.tema = datos.tema.data
                data.caso = datos.caso.data
                db.session.commit()
                flash('Registro actualizado')
                return render_template("/admin/temasadmin.html",  cmb_casos=cmb_casos, nuevo=nuevo,actualizar=actualizar)
            else:
                flash('¡ Selecciona un caso !')
                return render_template("/admin/temasactualizar.html",  cmb_casos=cmb_casos)

        return render_template("/admin/temasactualizar.html",  cmb_casos=cmb_casos)

########################### Admin Archivos ###############################

@app.route("/administracion/archivos", methods=['GET', 'POST'])
def archivosadmin():
    if "username" in session:
        cmb_materia = FrmMateria()
        datos = FrmArchivosEliminar()
        nuevo = FrmNuevo()
        actualizar = FrmActualizar()
        if cmb_materia.validate_on_submit():
            materia = cmb_materia.nombre.data
            if materia != "- Selecciona una materia -":
                # Llamada a la función Consultar_Caso_Id(); enviando como parámetro el id del caso
                archivos = Consultar_Archivo(materia)
                data = []
                for x in archivos:
                    datos = FrmArchivosEliminar()
                    datos.id.data = x.id
                    datos.nombre.data = x.nombre
                    datos.materia.data = x.materia
                    data.append(datos)
                return render_template("/admin/archivosadmin.html", cmb_materia=cmb_materia, datos=datos, data=data)
            else:
                flash('¡ Selecciona una materia !')
                # Devolvemos las variables de las consultas
                return render_template("/admin/archivosadmin.html", cmb_materia=cmb_materia, nuevo=nuevo, actualizar=actualizar)
        elif datos.validate_on_submit() and request.method == 'POST':
            data = Archivos.query.get(int(datos.id.data))
            print(data)
            db.session.delete(data)
            db.session.commit()
            flash('Registro eliminado')
            return render_template("/admin/archivosadmin.html", cmb_materia=cmb_materia, nuevo=nuevo, actualizar=actualizar)

        return render_template("/admin/archivosadmin.html", cmb_materia=cmb_materia, nuevo=nuevo, actualizar=actualizar)

@app.route("/administracion/archivos/agregar", methods=['GET', 'POST'])
def archivosagregar():
    if "username" in session:
        nuevo = FrmNuevo()
        cmb_materia = FrmMateria()
        actualizar = FrmActualizar()
        agregar = FrmArchivos()
        if agregar.validate_on_submit():
            if agregar.materia.data != "- Selecciona una materia -":
                nombre = agregar.nombre.data
                materia = agregar.materia.data
                data = Archivos(nombre, materia)
                db.session.add(data)
                db.session.commit()
                flash('Registro agregado')
                return render_template("/admin/archivosadmin.html", cmb_materia=cmb_materia, nuevo=nuevo, actualizar=actualizar)
            else:
                flash('¡ Selecciona una materia !')
                # Devolvemos las variables de las consultas
                return render_template("/admin/archivosagregar.html", agregar=agregar)
        # Devolvemos las variables de las consultas
        return render_template("/admin/archivosagregar.html", agregar=agregar)

@app.route("/administracion/archivos/actualizar", methods=['GET', 'POST'])
def archivosactualizar():
    if "username" in session:
        nuevo = FrmNuevo()
        actualizar = FrmActualizar()
        datos = FrmArchivos()
        cmb_materia = FrmMateria()
        if cmb_materia.validate_on_submit():
            materia = cmb_materia.nombre.data
            if materia != "- Selecciona una materia -":
                # Llamada a la función Consultar_Caso_Id(); enviando como parámetro el id del caso
                archivos = Consultar_Archivo(materia)
                data = []
                for x in archivos:
                    datos = FrmArchivos()
                    datos.id.data = x.id
                    datos.nombre.data = x.nombre
                    datos.materia.data = materia
                    data.append(datos)
                return render_template("/admin/archivosactualizar.html", cmb_materia=cmb_materia, datos=datos, data=data)
            else:
                flash('¡ Selecciona una materia !', 'combo')
                # Devolvemos las variables de las consultas
                return render_template("/admin/archivosadmin.html", cmb_materia=cmb_materia, nuevo=nuevo, actualizar=actualizar)
        if datos.validate_on_submit() and request.method =='POST':
            if datos.materia.data != "- Selecciona una materia -":
                data = Archivos.query.get(int(datos.id.data))
                data.nombre = datos.nombre.data
                data.materia = datos.materia.data
                db.session.commit()
                flash('Registro actualizado')
                return render_template("/admin/archivosadmin.html", cmb_materia=cmb_materia, nuevo=nuevo, actualizar=actualizar)
            else:
                flash('¡ Selecciona una materia !')
                # Devolvemos las variables de las consultas
                return render_template("/admin/archivosactualizar.html", cmb_materia=cmb_materia)

        return render_template("/admin/archivosactualizar.html", cmb_materia=cmb_materia)


def allowed_file(filename):

    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


#Indicamos la ruta para la página de error 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404_pagina_no_disponible.html"), 404

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run()

