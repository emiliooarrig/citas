from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import Usuarios, Citas, session as db_session
import os

def register_routes(app):

    app.secret_key = os.urandom(24)  # Clave secreta configurada para usar sesiones y flash

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            # Capturar datos solo si el formulario es enviado
            usuario = request.form['usuario']
            contrasena = request.form['contrasena']

            # Verificar si el usuario existe
            verificar_user = db_session.query(Usuarios).filter(Usuarios.nombre == usuario).first()

            if not verificar_user:
                flash("El usuario no existe")
                return redirect(url_for('index'))

            # Validar la contraseña
            if check_password_hash(verificar_user.password, contrasena):
                # Iniciar sesión guardando el ID de usuario en la sesión
                session['user_id'] = verificar_user.id_user
                flash("Inicio de sesión exitoso", "success")
                return redirect(url_for('citas'))
            else:
                flash("Contraseña incorrecta", "error")
                return redirect(url_for('index'))

        # Renderizar la plantilla solo si es un acceso `GET`
        return render_template('index.html')

    @app.route('/citas')
    def citas():
        # Validar que el usuario haya iniciado sesión antes de acceder
        if 'user_id' not in session:
            flash("Debes iniciar sesión para acceder a esta página")
            return redirect(url_for('index'))
        
        user_id = session['user_id']
        usuario = db_session.query(Usuarios).filter(Usuarios.id_user == user_id).first()

        #Recuperamos todas las citas que hay en la bd
        citas = db_session.query(Citas.fecha, Citas.titulo, Citas.descripcion, 
                                 Citas.hora, Citas.fecha_creacion, Citas.id_date, 
                                 Citas.lugar, Usuarios.nombre).join(Usuarios, Usuarios.id_user == Citas.user_id).all();
        return render_template('citas.html', nombre_usuario=usuario.nombre, citas=citas)

    @app.route('/logout')
    def logout():
        # Cerrar sesión eliminando la clave 'user_id' de la sesión
        session.pop('user_id', None)
        flash("Sesión cerrada", "success")
        return redirect(url_for('index'))

    @app.route('/registrar_user', methods=['GET', 'POST'])
    def registrar_user():
        if request.method == 'POST':
            usuario = request.form['usuario']
            contrasena = request.form['contrasena']
            confirmar_contrasena = request.form['confirmarContrasena']

            # Validar contraseñas
            if contrasena != confirmar_contrasena:
                flash('Las contraseñas no coinciden')
                return redirect(url_for('registrar_user'))

            # Comprobar si el usuario ya existe
            usuario_existente = db_session.query(Usuarios).filter_by(nombre=usuario).first()
            if usuario_existente:
                flash('El usuario ya existe, elige otro')
                return redirect(url_for('registrar_user'))

            # Crear nuevo usuario
            nuevo_usuario = Usuarios(nombre=usuario, password=generate_password_hash(contrasena))
            db_session.add(nuevo_usuario)
            db_session.commit()

            flash('Usuario registrado exitosamente')
            return redirect(url_for('index'))

        return render_template("registrar_user.html")

    @app.route('/agregar_date', methods=['GET', 'POST'])
    def agregar_date():

        if request.method == 'POST':
            titulo = request.form['titulo']
            descripcion = request.form.get('descripcion')  # Campo opcional
            fecha = request.form['fecha']
            hora = request.form['hora']
            lugar = request.form['lugar']
            #Recuperamos el usuario que esta en la sesión
            id_usuario = session['user_id'] 

        # Crear nueva cita
            nueva_cita = Citas(
                user_id=id_usuario, 
                titulo=titulo,
                descripcion=descripcion,
                fecha=fecha,
                hora=hora,
                lugar=lugar,
                fecha_creacion=datetime.now()
            )

            db_session.add(nueva_cita)
            db_session.commit()
            flash('Cita guardada exitosamente')
            return redirect(url_for('citas'))

        return render_template("agregar_date.html")
    
    @app.route('/editar_cita/<int:id_cita>', methods=['GET', 'POST'])
    def editar_cita(id_cita):

        cita = db_session.query(Citas).filter_by(id_date=id_cita).first()
        if request.method == 'POST':
            titulo = request.form['titulo']
            descripcion = request.form['descripcion']
            fecha = request.form['fecha']
            hora = request.form['hora']
            lugar = request.form['lugar']

            cita.titulo = titulo
            cita.descripcion = descripcion
            cita.hora = hora
            cita.fecha = fecha
            cita.lugar = lugar
            db_session.commit()
            flash("Cita editada exitosamente! ")
            return redirect(url_for('citas'))
        
        return render_template('editar_cita.html', cita=cita)
    
    @app.route("/eliminar_cita/<int:id_cita>")
    def eliminar_cita(id_cita):
        cita = db_session.query(Citas).filter_by(id_date=id_cita).first()
        if cita:
            db_session.delete(cita)
            db_session.commit()
            flash("Cita eliminada correctamente")
        else:
            flash("Cita no eliminada")

        return redirect(url_for("citas"))
    
    @app.route("/editar_perfil")
    def editar_perfil():
        #recuperamos el id del usuario usando la sesion.
        id_usuario = session['user_id']

        #Hacemos query para recuperar la informacion del usuario.
        cita = db_session.query(Usuarios).filter(Usuarios.id_user == id_usuario).first()

        if request.method == 'POST':
            cita = db_session.query
        return render_template("editar_perfil.html", usuario = cita)
    
