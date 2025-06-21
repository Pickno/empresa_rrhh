from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '0113'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///empresa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'nicocabra.m@gmail.com'
app.config['MAIL_PASSWORD'] = 'mgygzrjnhrilnoqk'

db = SQLAlchemy(app)
mail = Mail(app)

# Modelo de contacto
class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(100), nullable=False)
    nit = db.Column(db.String(20), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    compania = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    servicio = db.Column(db.String(100), nullable=False)

class Postulacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    perfil = db.Column(db.String(100), nullable=False)
    hoja_vida = db.Column(db.String(200), nullable=False)

@app.route('/')
def home():
    return render_template('dashboard_publico.html')

@app.route('/RRHH')
def Recursos_Humanos():
    return render_template('RRHH.html')

@app.route('/SST')
def Salud_y_Seguridad_en_el_Trabajo():
    return render_template('SST.html')

@app.route('/TI')
def Soporte_Técnico():
    return render_template('TI.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        correo = request.form['correo']
        nit = request.form['nit']
        ciudad = request.form['ciudad']
        compania = request.form['compania']
        telefono = request.form['telefono']
        servicio = request.form['servicio']

        # Guardar en la base de datos
        nuevo_contacto = Contacto(correo=correo, nit=nit, ciudad=ciudad, compania=compania, telefono=telefono, servicio=servicio)
        db.session.add(nuevo_contacto)
        db.session.commit()

        # Enviar correo a la empresa
        mensaje = Message('Nuevo formulario de contacto', 
                  sender='nicocabra.m@gmail.com', 
                  recipients=['nicocabra.m@gmail.com'])
        mensaje.body = f'''
        Correo: {correo}
        NIT: {nit}
        Ciudad: {ciudad}
        Compañía: {compania}
        Teléfono: {telefono}
        Servicio requerido: {servicio}
        '''

        mail.send(mensaje)

        flash('Gracias por contactarnos. Te responderemos pronto.', 'success')
        return redirect('/')

    return render_template('contacto.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/trabaja', methods=['GET', 'POST'])
def trabaja():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        perfil = request.form['perfil']
        archivo = request.files['hoja_vida']
        
        if archivo:
            filename = secure_filename(archivo.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            archivo.save(path)

            nueva_postulacion = Postulacion(
                nombre=nombre,
                correo=correo,
                telefono=telefono,
                perfil=perfil,
                hoja_vida=filename
            )
            db.session.add(nueva_postulacion)
            db.session.commit()

            mensaje = Message('Nueva postulación recibida',
                              sender='nicocabra.m@gmail.com',
                              recipients=['nicocabra.m@gmail.com'])
            mensaje.body = f'''Se ha recibido una nueva postulación:

Nombre: {nombre}
Correo: {correo}
Teléfono: {telefono}
Perfil: {perfil}
Archivo: {filename}
'''
            with app.open_resource(path) as cv:
                mensaje.attach(filename, 'application/octet-stream', cv.read())

            mail.send(mensaje)

            flash('Gracias por postularte. Te contactaremos pronto.', 'success')
            return redirect('/')

    return render_template('trabaja.html')


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == "__main__":
    app.run()



