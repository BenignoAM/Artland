from flask import Flask, render_template, session, url_for, request, redirect, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models.entities.User import User
from models.ModelUser import ModelUser
from werkzeug.security import generate_password_hash
from flask_mysqldb import MySQL
from config import config
import smtplib
import base64
import dateutil.parser as dparser
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

artlandApp = Flask(__name__)
db = MySQL(artlandApp)
login_manager_app = LoginManager(artlandApp)


@login_manager_app.user_loader
def loader_user(id):
    return ModelUser.get_by_id(db, id)

@artlandApp.route('/')
def index():
    return render_template('home.html')

@artlandApp.route('/perfil/<string:id>', methods = ['GET', 'POST'])
def perfil(id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT p.idpublicacion, p.idusuario, p.comentariop, p.imagenp, p.fechahorap, u.nombre, u.fotou FROM publicacion p INNER JOIN usuario u ON p.idusuario = u.id WHERE p.idusuario = %s ", (id,))
    resultado = cursor.fetchall()
    publicaciones = []

    for row in resultado:
        publi = list(row)
        cursor.execute("SELECT c.idcomentario, c.idusuario, c.idpublicacion, c.comentariou, c.fechahorac, u.nombre, u.fotou FROM comentarios c INNER JOIN usuario u ON c.idusuario = u.id WHERE c.idpublicacion = %s", (row[0],))
        comentarios = cursor.fetchall()
        publi.append(comentarios)
        publicaciones.append(publi)

    now = current_user.fechareg
    dt_1  = now.strftime("%m/%d/%Y")
    tempVal = (dparser.parse(dt_1,fuzzy=True).date()).strftime('%d %B %Y')

    current_user.fechareg = ("Artista en Artland desde: {}".format(tempVal))

    return render_template('perfil.html', publicacion=publicaciones)

@artlandApp.route('/perfila/<string:id>', methods = ['GET', 'POST'])
def perfila(id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT p.idpublicacion, p.idusuario, p.comentariop, p.imagenp, p.fechahorap, u.nombre, u.fotou FROM publicacion p INNER JOIN usuario u ON p.idusuario = u.id WHERE p.idusuario = %s ", (id,))
    resultado = cursor.fetchall()
    publicaciones = []

    for row in resultado:
        publi = list(row)
        cursor.execute("SELECT c.idcomentario, c.idusuario, c.idpublicacion, c.comentariou, c.fechahorac, u.nombre, u.fotou FROM comentarios c INNER JOIN usuario u ON c.idusuario = u.id WHERE c.idpublicacion = %s", (row[0],))
        comentarios = cursor.fetchall()
        publi.append(comentarios)
        publicaciones.append(publi)

    now = current_user.fechareg
    dt_1  = now.strftime("%m/%d/%Y")
    tempVal = (dparser.parse(dt_1,fuzzy=True).date()).strftime('%d %B %Y')

    current_user.fechareg = ("Artista en Artland desde: {}".format(tempVal))

    return render_template('perfiladmin.html', publicacion=publicaciones)

@artlandApp.route('/usuario', methods = ['GET', 'POST'])
def usuario():
    cursor = db.connection.cursor()
    cursor.execute("SELECT p.idpublicacion, p.idusuario, p.comentariop, p.imagenp, p.fechahorap, u.nombre, u.fotou FROM publicacion p INNER JOIN usuario u ON p.idusuario = u.id")
    resultado = cursor.fetchall()
    publicaciones = []

    for row in resultado:
        publi = list(row)
        cursor.execute("SELECT c.idcomentario, c.idusuario, c.idpublicacion, c.comentariou, c.fechahorac, u.nombre, u.fotou FROM comentarios c INNER JOIN usuario u ON c.idusuario = u.id WHERE c.idpublicacion = %s", (row[0],))
        comentarios = cursor.fetchall()
        publi.append(comentarios)
        publicaciones.append(publi)


    return render_template('usuario.html', publicacion=publicaciones)

@artlandApp.route('/usuarioa', methods = ['GET', 'POST'])
def usuarioa():
    cursor = db.connection.cursor()
    cursor.execute("SELECT p.idpublicacion, p.idusuario, p.comentariop, p.imagenp, p.fechahorap, u.nombre, u.fotou FROM publicacion p INNER JOIN usuario u ON p.idusuario = u.id")
    resultado = cursor.fetchall()
    publicaciones = []

    for row in resultado:
        publi = list(row)
        cursor.execute("SELECT c.idcomentario, c.idusuario, c.idpublicacion, c.comentariou, c.fechahorac, u.nombre, u.fotou FROM comentarios c INNER JOIN usuario u ON c.idusuario = u.id WHERE c.idpublicacion = %s", (row[0],))
        comentarios = cursor.fetchall()
        publi.append(comentarios)
        publicaciones.append(publi)

    return render_template('usuarioadmin.html', publicacion=publicaciones)

@artlandApp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre   = request.form['nombre']
        correo   = request.form['correo']
        clave    = request.form['clave']
        fechanac = request.form['fechanac']
        fotou    = request.files['fotou']
        foto     = base64.b64encode(fotou.read())
        claveCifrada = generate_password_hash(clave)

        try:
            regUser = db.connection.cursor()
            regUser.execute("INSERT INTO usuario (nombre, correo, clave, fechanac, fotou) VALUES (%s, %s, %s, %s, %s)", (nombre, correo, claveCifrada, fechanac, foto))
            db.connection.commit()
        except:
            flash('')
            return render_template('registro.html')

        usuario = User(None, nombre, correo, clave, None, fechanac, None, None)
        usuarioAut = ModelUser.login(db, usuario)
        login_user(usuarioAut)

        sender = 'artlandwebapp@gmail.com'
        rec = correo

        conexion = smtplib.SMTP (host='smtp.gmail.com', port=587)
        conexion.ehlo()
        conexion.starttls()
        conexion.login(user='artlandwebapp@gmail.com', password='vqgdcuahyvawdczr')
        mensaje = MIMEMultipart ("alternatives")
        mensaje['Subject'] = 'Te lo agradecemos'
        mensaje['From'] = sender
        mensaje['To'] = rec

        text = "¡Gracias!"
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body{
                background-image: url(/static/img/fondoV.jpg);
            }
            
            .form-registro {
                width: 100%;
                background-color: #c9ece5;
                padding: 30px;
                margin: auto;
                margin-top: 20px;
                border-radius: 15px;
                font-family: Georgia, 'Times New Roman', Times, serif;
                color: black;
                box-shadow: 7px 13px 37px #000;
            }
            
            .form-registro h4 {
                font-size: 25px;
                margin-bottom: 18px;
                color: black;
                font-family:  "Gill Sans Extrabold", Helvetica, sans-serif;
                text-align: center;
            }
            
            
            .form-registro p{
                height: 40px;
                text-align: center;
                font-size: 18px;
            }
            
            .form-registro a{
                color: black;
                text-decoration: underline;
            }
            
            .form-registro .botons {
                display: inline-flex;
                align-items: center;
                text-align: center;
                justify-content: center;
                width: 100%;
                background: #000000;
                border: none;
                cursor: pointer;
                padding: 13px;
                color: black;
                margin: 16px 0;
                font-size: 17px;
            }
            
        </style>
        <title>Formulario</title>
        </head>
        <body>
        <section class="form-registro">
            <h4>Registro Exitoso</h4>
            
            <p>¡Gracias por unirte a nuestra Red!</p>
            <p>Pulsa el siguiente botón para completar la confirmación de tu cuenta</p>
            <br>
            <p>Si tu no creaste esta cuenta, ignora este correo</p>
            
        </section>
        </body>
        </html>
        """
        textpart = MIMEText(text, 'plain')
        htmlpart = MIMEText(html, 'html')
        mensaje.attach(textpart)
        mensaje.attach(htmlpart)

        conexion.sendmail('artlandwebapp@gmail.com', correo, mensaje.as_string())
        conexion.quit()
        return redirect(url_for('usuario'))
    else:
        return render_template('registro.html')

@artlandApp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = User(0, None, request.form['correo'], request.form['clave'], None, None, None, None)
        usuarioAut = ModelUser.login(db, usuario)
        if usuarioAut is not None:
            if usuarioAut.clave:
                login_user(usuarioAut)
                if usuarioAut.perfil == 'A':
                    return redirect(url_for('sUsuario'))
                else:
                    return redirect(url_for('usuario'))
            else:
                flash('La contraseña es incorrecta, intente de nuevo')
                return redirect(request.url)
        else:
            flash('El usuario no se ha encontrado, verifique los datos proporcionados')
            return redirect(request.url)
    else:
        return render_template('login.html')

@artlandApp.route('/logout')
def logout():
    logout_user()
    return render_template('home.html')

@artlandApp.route('/sUsuario', methods = ['GET', 'POST'])
def sUsuario():
    selUsuario = db.connection.cursor()
    selUsuario.execute("SELECT * FROM usuario")
    u = selUsuario.fetchall()
    return render_template('admin.html', usuario = u)

@artlandApp.route('/uUsuario/<int:id>', methods = ['GET', 'POST'])
def uUsuario(id):
    if request.method == 'POST':
        nombre   = request.form['nombre']
        correo   = request.form['correo']
        fechanac = request.form['fechanac']
        perfil = request.form['perfil']
        actUsuario = db.connection.cursor()
        actUsuario.execute("UPDATE usuario SET nombre = %s, correo = %s, fechanac = %s, perfil = %s WHERE id = %s", (nombre, correo, fechanac, perfil, id))
        db.connection.commit()
        flash('Usuario actualizado exitosamente')
        return redirect(url_for('sUsuario'))
    else:
        return redirect(request.url)

@artlandApp.route('/dUsuario/<string:id>', methods = ['GET', 'POST'])
def dUsuario(id):
    if request.method == 'POST':
        delUsuario = db.connection.cursor()
        delUsuario.execute("DELETE FROM usuario WHERE id = %s", [id])
        db.connection.commit()
        flash('Usuario eliminado exitosamente')
        return redirect(url_for('sUsuario'))
    else:
        return redirect(request.url)

@artlandApp.route('/iUsuario', methods=['GET', 'POST'])
def iUsuario():
    if request.method == 'POST':
        nombre   = request.form['nombre']
        correo   = request.form['correo']
        clave    = request.form['clave']
        fechanac = request.form['fechanac']
        perfil = request.form['perfil']
        fotou = request.files['fotou']
        foto = base64.b64encode(fotou.read())
        claveCifrada = generate_password_hash(clave)

        regUser = db.connection.cursor()
        regUser.execute("INSERT INTO usuario (nombre, correo, clave, perfil, fechanac, fotou) VALUES (%s, %s, %s, %s, %s, %s)", (nombre, correo, claveCifrada, perfil, fechanac, foto))
        db.connection.commit()

        conexion = smtplib.SMTP(host = 'smtp.gmail.com', port = 587)
        conexion.ehlo()
        conexion.starttls()
        conexion.login(user = 'artlandwebapp@gmail.com', password='awrfjpxfcggovmzl')
        mensaje = 'Prueba 1'
        conexion.sendmail(from_addr='artlandwebapp@gmail.com', to_addrs= correo, msg= mensaje)
        conexion.quit()
        flash('Usuario agregado exitosamente')
        return redirect(url_for('sUsuario'))
    else:
        return redirect(request.url)

@artlandApp.route('/cpUsuario/<string:id>', methods = ['GET', 'POST'])
def cpUsuario(id):
    if request.method == 'POST':
        usuario = User(0, None, request.form['correo'], request.form['clave'], None, None, None, None)
        usuarioAut = ModelUser.login(db, usuario)
        if usuarioAut.clave:
            clave = request.form['clavenueva']
            claveCifrada  = generate_password_hash(clave)

            actUsuario = db.connection.cursor()
            actUsuario.execute("UPDATE usuario SET clave = %s WHERE id = %s", (claveCifrada, id))
            db.connection.commit()
            flash('Contraseña actualizada exitosamente')
            return redirect(url_for('perfil', id=id))
        else:
            return redirect(request.url) 
    else:
        flash('La contraseña es incorrecta, intente de nuevo')
        return redirect(url_for('perfil', id=id))

@artlandApp.route('/cpaUsuario/<string:id>', methods = ['GET', 'POST'])
def cpaUsuario(id):
    if request.method == 'POST':
        usuario = User(0, None, request.form['correo'], request.form['clave'], None, None, None, None)
        usuarioAut = ModelUser.login(db, usuario)
        if usuarioAut.clave:
            clave = request.form['clavenueva']
            claveCifrada  = generate_password_hash(clave)

            actUsuario = db.connection.cursor()
            actUsuario.execute("UPDATE usuario SET clave = %s WHERE id = %s", (claveCifrada, id))
            db.connection.commit()
            flash('Contraseña actualizada exitosamente')
            return redirect(url_for('perfila', id=id))
        else:
            return redirect(request.url) 
    else:
        flash('La contraseña es incorrecta, intente de nuevo')
        return redirect(url_for('perfila', id=id))

@artlandApp.route('/upUsuario/<string:id>', methods = ['GET', 'POST'])
def upUsuario(id):
    if request.method == 'POST':
        nombre   = request.form['nombre']
        correo   = request.form['correo']
        fechanac = request.form['fechanac']
        actUsuario = db.connection.cursor()
        actUsuario.execute("UPDATE usuario SET nombre = %s, correo = %s, fechanac = %s WHERE id = %s", (nombre, correo, fechanac, id))
        db.connection.commit()
        flash('Usuario actualizado exitosamente')
        return redirect(url_for('perfil', id=id))
    else:
        return redirect(request.url)

@artlandApp.route('/upaUsuario/<string:id>', methods = ['GET', 'POST'])
def upaUsuario(id):
    if request.method == 'POST':
        nombre   = request.form['nombre']
        correo   = request.form['correo']
        fechanac = request.form['fechanac']
        actUsuario = db.connection.cursor()
        actUsuario.execute("UPDATE usuario SET nombre = %s, correo = %s, fechanac = %s WHERE id = %s", (nombre, correo, fechanac, id))
        db.connection.commit()
        flash('Usuario actualizado exitosamente')
        return redirect(url_for('perfila', id=id))
    else:
        return redirect(request.url)

@artlandApp.route('/cUsuario/<string:id>', methods = ['GET', 'POST'])
def cUsuario(id):
    if request.method == 'POST':
        usuario = User(0, None, request.form['correo'], request.form['clave'], None, None, None, None)
        usuarioAut = ModelUser.login(db, usuario)
        if usuarioAut.clave:
            clave = request.form['clavenueva']
            claveCifrada  = generate_password_hash(clave)

            actUsuario = db.connection.cursor()
            actUsuario.execute("UPDATE usuario SET clave = %s WHERE id = %s", (claveCifrada, id))
            db.connection.commit()
            flash('Contraseña actualizada exitosamente')
            return redirect(url_for('sUsuario'))
        else:
            return redirect(request.url) 
    else:
        flash('La contraseña es incorrecta, intente de nuevo')
        return redirect(url_for('sUsuario'))

@artlandApp.route('/uaFoto/<string:id>', methods = ['GET', 'POST'])
def uaFoto(id):
    if request.method == 'POST':
        fotou = request.files['fotou']
        foto = base64.b64encode(fotou.read())

        actUsuario = db.connection.cursor()
        actUsuario.execute("UPDATE usuario SET fotou = %s WHERE id = %s", (foto, id))
        db.connection.commit()
        flash('Foto actualizada exitosamente')
        return redirect(url_for('perfila', id=id))
    else:
        return redirect(request.url)

@artlandApp.route('/uFoto/<string:id>', methods = ['GET', 'POST'])
def uFoto(id):
    if request.method == 'POST':
        fotou = request.files['fotou']
        foto = base64.b64encode(fotou.read())

        actUsuario = db.connection.cursor()
        actUsuario.execute("UPDATE usuario SET fotou = %s WHERE id = %s", (foto, id))
        db.connection.commit()
        flash('Foto actualizada exitosamente')
        return redirect(url_for('perfil', id=id))
    else:
        return redirect(request.url)

@artlandApp.route('/aFoto/<string:id>', methods = ['GET', 'POST'])
def aFoto(id):
    if request.method == 'POST':
        fotou = request.files['fotou']
        foto = base64.b64encode(fotou.read())

        actUsuario = db.connection.cursor()
        actUsuario.execute("UPDATE usuario SET fotou = %s WHERE id = %s", (foto, id))
        db.connection.commit()
        flash('Foto actualizada exitosamente')
        return redirect(url_for('sUsuario'))
    else:
        return redirect(request.url) 

@artlandApp.route('/sPubli', methods = ['GET', 'POST'])
def sPubli():
    selPubli = db.connection.cursor()
    selPubli.execute("SELECT * FROM publicacion")
    p = selPubli.fetchall()

    selUsuario = db.connection.cursor()
    selUsuario.execute("SELECT id FROM usuario")
    u = selUsuario.fetchall()
    return render_template('admin2.html', publicacion = p, usuario = u)

@artlandApp.route('/publicar', methods=['GET', 'POST'])
def publicar():
    if request.method == 'POST':
        comentariop   = request.form['comentariop']
        idusuario     = request.form['idusuario']
        imagenp   = request.files['imagenp']
        imagen = base64.b64encode(imagenp.read())

        regUser = db.connection.cursor()
        regUser.execute("INSERT INTO publicacion (idusuario, comentariop, imagenp) VALUES (%s, %s, %s)", (idusuario, comentariop, imagen))
        db.connection.commit()

        flash('Publicacion exitosa')
        return redirect(url_for('perfila', id=idusuario))
    else:
        return redirect(request.url)

@artlandApp.route('/publicaru', methods=['GET', 'POST'])
def publicaru():
    if request.method == 'POST':
        comentariop   = request.form['comentariop']
        idusuario     = request.form['idusuario']
        imagenp   = request.files['imagenp']
        imagen = base64.b64encode(imagenp.read())

        regUser = db.connection.cursor()
        regUser.execute("INSERT INTO publicacion (idusuario, comentariop, imagenp) VALUES (%s, %s, %s)", (idusuario, comentariop, imagen))
        db.connection.commit()

        flash('Publicacion exitosa')
        return redirect(url_for('perfil', id=idusuario))
    else:
        return redirect(request.url)

@artlandApp.route('/dPubli/<string:idpublicacion>', methods = ['GET', 'POST'])
def dPubli(idpublicacion):
    if request.method == 'POST':
        delUsuario = db.connection.cursor()
        delUsuario.execute("DELETE FROM publicacion WHERE idpublicacion = %s", [idpublicacion])
        db.connection.commit()
        flash('Publicación eliminada exitosamente')
        return redirect(url_for('sPubli'))
    else:
        return redirect(request.url)

@artlandApp.route('/uPubli/<string:idpublicacion>', methods = ['GET', 'POST'])
def uPubli(idpublicacion):
    if request.method == 'POST':
        comentariop   = request.form['comentariop']
        idusuario     = request.form['idusuario']

        actUsuario = db.connection.cursor()
        actUsuario.execute("UPDATE publicacion SET idusuario = %s, comentariop = %s WHERE idpublicacion = %s", (idusuario, comentariop, idpublicacion))
        db.connection.commit()
        flash('Publicacion actualizada exitosamente')
        return redirect(url_for('sPubli'))
    else:
        return redirect(request.url)

@artlandApp.route('/uPublif/<string:idpublicacion>', methods = ['GET', 'POST'])
def uPublif(idpublicacion):
    if request.method == 'POST':
        imagenp   = request.files['imagenp']
        imagen = base64.b64encode(imagenp.read())

        actUsuario = db.connection.cursor()
        actUsuario.execute("UPDATE publicacion SET imagenp = %s WHERE idpublicacion = %s", (imagen, idpublicacion))
        db.connection.commit()
        flash('Publicacion actualizada exitosamente')
        return redirect(url_for('sPubli'))
    else:
        return redirect(request.url)

@artlandApp.route('/iPubli', methods=['GET', 'POST'])
def iPubli():
    if request.method == 'POST':
        comentariop   = request.form['comentariop']
        idusuario     = request.form['idusuario']
        imagenp   = request.files['imagenp']
        imagen = base64.b64encode(imagenp.read())

        regUser = db.connection.cursor()
        regUser.execute("INSERT INTO publicacion (idusuario, comentariop, imagenp) VALUES (%s, %s, %s)", (idusuario, comentariop, imagen))
        db.connection.commit()

        flash('Publicacion agregada exitosamente')
        return redirect(url_for('sPubli'))
    else:
        return redirect(request.url)

@artlandApp.route('/uPubliu/<string:idpublicacion>', methods = ['GET', 'POST'])
def uPubliu(idpublicacion):
    if request.method == 'POST':
        comentariop   = request.form['comentariop']
        idusuario = current_user.id

        actUsuario = db.connection.cursor()
        actUsuario.execute("UPDATE publicacion SET comentariop = %s WHERE idpublicacion = %s", (comentariop, idpublicacion))
        db.connection.commit()
        flash('Publicacion actualizada exitosamente')
        return redirect(url_for('perfil', id=idusuario))
    else:
        return redirect(request.url)

@artlandApp.route('/uPublifu/<string:idpublicacion>', methods = ['GET', 'POST'])
def uPublifu(idpublicacion):
    if request.method == 'POST':
        imagenp   = request.files['imagenp']
        imagen = base64.b64encode(imagenp.read())
        idusuario = current_user.id

        actUsuario = db.connection.cursor()
        actUsuario.execute("UPDATE publicacion SET imagenp = %s WHERE idpublicacion = %s", (imagen, idpublicacion))
        db.connection.commit()
        flash('Publicacion actualizada exitosamente')
        return redirect(url_for('perfil', id=idusuario))
    else:
        return redirect(request.url)

@artlandApp.route('/uPublia/<string:idpublicacion>', methods = ['GET', 'POST'])
def uPublia(idpublicacion):
    if request.method == 'POST':
        comentariop   = request.form['comentariop']
        idusuario = current_user.id

        actUsuario = db.connection.cursor()
        actUsuario.execute("UPDATE publicacion SET comentariop = %s WHERE idpublicacion = %s", (comentariop, idpublicacion))
        db.connection.commit()
        flash('Publicacion actualizada exitosamente')
        return redirect(url_for('perfila', id=idusuario))
    else:
        return redirect(request.url)

@artlandApp.route('/uPublifa/<string:idpublicacion>', methods = ['GET', 'POST'])
def uPublifa(idpublicacion):
    if request.method == 'POST':
        imagenp   = request.files['imagenp']
        imagen = base64.b64encode(imagenp.read())
        idusuario = current_user.id

        actUsuario = db.connection.cursor()
        actUsuario.execute("UPDATE publicacion SET imagenp = %s WHERE idpublicacion = %s", (imagen, idpublicacion))
        db.connection.commit()
        flash('Publicacion actualizada exitosamente')
        return redirect(url_for('perfila', id=idusuario))
    else:
        return redirect(request.url)

@artlandApp.route('/dPubliu/<string:idpublicacion>', methods = ['GET', 'POST'])
def dPubliu(idpublicacion):
    if request.method == 'POST':
        delUsuario = db.connection.cursor()
        idusuario = current_user.id
        delUsuario.execute("DELETE FROM publicacion WHERE idpublicacion = %s", [idpublicacion])
        db.connection.commit()
        flash('Publicación eliminada exitosamente')
        return redirect(url_for('perfil', id=idusuario))
    else:
        return redirect(request.url)

@artlandApp.route('/dPublia/<string:idpublicacion>', methods = ['GET', 'POST'])
def dPublia(idpublicacion):
    if request.method == 'POST':
        delUsuario = db.connection.cursor()
        idusuario = current_user.id
        delUsuario.execute("DELETE FROM publicacion WHERE idpublicacion = %s", [idpublicacion])
        db.connection.commit()
        flash('Publicación eliminada exitosamente')
        return redirect(url_for('perfila', id=idusuario))
    else:
        return redirect(request.url)

@artlandApp.route('/sComen', methods = ['GET', 'POST'])
def sComen():
    sComen = db.connection.cursor()
    sComen.execute("SELECT * FROM comentarios")
    c = sComen.fetchall()

    selUsuario = db.connection.cursor()
    selUsuario.execute("SELECT id FROM usuario")
    u = selUsuario.fetchall()

    selPubli = db.connection.cursor()
    selPubli.execute("SELECT idpublicacion FROM publicacion")
    p = selPubli.fetchall()
    return render_template('admin3.html', comentarios = c, usuario = u, publicaciones = p)

@artlandApp.route('/comentar/<string:idpublicacion>', methods=['GET', 'POST'])
def comentar(idpublicacion):
    if request.method == 'POST':
        idusuario     = current_user.id
        comentariou   = request.form['comentariou']

        regComen = db.connection.cursor()
        regComen.execute("INSERT INTO comentarios (idusuario, idpublicacion, comentariou) VALUES (%s, %s, %s)", (idusuario, idpublicacion, comentariou))
        db.connection.commit()

        flash('Comentario agregado exitosamente')
        return redirect(url_for('perfila', id=idusuario))
    else:
        return redirect(request.url)

@artlandApp.route('/comentarha/<string:idpublicacion>', methods=['GET', 'POST'])
def comentarha(idpublicacion):
    if request.method == 'POST':
        idusuario     = current_user.id
        comentariou   = request.form['comentariou']

        regComen = db.connection.cursor()
        regComen.execute("INSERT INTO comentarios (idusuario, idpublicacion, comentariou) VALUES (%s, %s, %s)", (idusuario, idpublicacion, comentariou))
        db.connection.commit()

        flash('Comentario agregado exitosamente')
        return redirect(url_for('usuarioa', id=idusuario))
    else:
        return redirect(request.url)

@artlandApp.route('/comentarhu/<string:idpublicacion>', methods=['GET', 'POST'])
def comentarhu(idpublicacion):
    if request.method == 'POST':
        idusuario     = current_user.id
        comentariou   = request.form['comentariou']

        regComen = db.connection.cursor()
        regComen.execute("INSERT INTO comentarios (idusuario, idpublicacion, comentariou) VALUES (%s, %s, %s)", (idusuario, idpublicacion, comentariou))
        db.connection.commit()

        flash('Comentario agregado exitosamente')
        return redirect(url_for('usuario', id=idusuario))
    else:
        return redirect(request.url)

@artlandApp.route('/dComena/<string:idcomentario>', methods = ['GET', 'POST'])
def dComena(idcomentario):
    if request.method == 'POST':
        delUsuario = db.connection.cursor()
        idusuario = current_user.id
        delUsuario.execute("DELETE FROM comentarios WHERE idcomentario = %s", [idcomentario])
        db.connection.commit()
        flash('Comentario eliminado exitosamente')
        return redirect(url_for('perfila', id=idusuario))
    else:
        return redirect(request.url)

@artlandApp.route('/comentaru/<string:idpublicacion>', methods=['GET', 'POST'])
def comentaru(idpublicacion):
    if request.method == 'POST':
        idusuario     = current_user.id
        comentariou   = request.form['comentariou']

        regComen = db.connection.cursor()
        regComen.execute("INSERT INTO comentarios (idusuario, idpublicacion, comentariou) VALUES (%s, %s, %s)", (idusuario, idpublicacion, comentariou))
        db.connection.commit()

        flash('Comentario agregado exitosamente')
        return redirect(url_for('perfil', id=idusuario))
    else:
        return redirect(request.url)

@artlandApp.route('/dComenu/<string:idcomentario>', methods = ['GET', 'POST'])
def dComenu(idcomentario):
    if request.method == 'POST':
        delUsuario = db.connection.cursor()
        idusuario = current_user.id
        delUsuario.execute("DELETE FROM comentarios WHERE idcomentario = %s", [idcomentario])
        db.connection.commit()
        flash('Comentario eliminado exitosamente')
        return redirect(url_for('perfil', id=idusuario))
    else:
        return redirect(request.url)

@artlandApp.route('/icomentario', methods=['GET', 'POST'])
def icomentario():
    if request.method == 'POST':
        idusuario     = request.form['idusuario']
        idpublicacion = request.form['idpublicacion']
        comentariou   = request.form['comentariou']

        regComen = db.connection.cursor()
        regComen.execute("INSERT INTO comentarios (idusuario, idpublicacion, comentariou) VALUES (%s, %s, %s)", (idusuario, idpublicacion, comentariou))
        db.connection.commit()

        flash('Comentario agregado exitosamente')
        return redirect(url_for('sComen'))
    else:
        return redirect(request.url)

@artlandApp.route('/ucomentario/<string:idcomentario>', methods = ['GET', 'POST'])
def ucomentario(idcomentario):
    if request.method == 'POST':
        comentariou   = request.form['comentariou']
        idusuario     = request.form['idusuario']
        idpublicacion = request.form['idpublicacion']

        actUsuario = db.connection.cursor()
        actUsuario.execute("UPDATE comentarios SET idusuario = %s, idpublicacion = %s, comentariou = %s  WHERE idcomentario = %s", (idusuario, idpublicacion, comentariou, idcomentario))
        db.connection.commit()
        flash('Comentario actualizada exitosamente')
        return redirect(url_for('sComen'))
    else:
        return redirect(request.url)

@artlandApp.route('/dcomentario/<string:idcomentario>', methods = ['GET', 'POST'])
def dcomentario(idcomentario):
    if request.method == 'POST':
        delUsuario = db.connection.cursor()
        idusuario = current_user.id
        delUsuario.execute("DELETE FROM comentarios WHERE idcomentario = %s", [idcomentario])
        db.connection.commit()
        flash('Comentario eliminado exitosamente')
        return redirect(url_for('sComen'))
    else:
        return redirect(request.url)

if __name__ == '__main__':
    artlandApp.config.from_object(config['development'])
    artlandApp.run(port=3000)