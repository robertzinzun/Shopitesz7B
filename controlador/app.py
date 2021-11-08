import urllib

from flask import Flask,render_template,request,flash
from flask_bootstrap import Bootstrap
from modelo.DAO import Categoria,db

app=Flask(__name__,template_folder='../vista',static_folder='../static')
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://userShopitesz:Hola.123@127.0.0.1/Shopitesz_v2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='cl4v3'
@app.route('/')
def inicio():
    #return '<H1>Bienvenido a la tienda en linea SHOPITESZ</H1>'
    return render_template('comunes/principal.html')

#Seccion para categorias
@app.route('/categorias')
def categorias():
    c=Categoria()
    categorias=c.consultaGeneral()
    return render_template('categorias/consulta.html',categorias=categorias)

@app.route('/categorias/imagen/<int:id>')
def consultarImagenCategoria(id):
    c=Categoria()
    return c.consultaIndividual(id).foto

@app.route('/categorias/nuevo')
def nuevaCategoria():
    return render_template('categorias/nuevo.html')

@app.route('/categorias/registrar',methods=['post'])
def registrarCategoria():
    c=Categoria()
    c.nombre=request.form['nombre']
    imagen=request.files['foto'].read()
    if imagen:
        c.foto=imagen
    c.insertar()
    flash('Categoria registrada con exito')
    return render_template('categorias/nuevo.html')

#fin de seccion de categorias
@app.route('/carrito')
def carrito():
    return '<p> Consultando el carrito </p>'

#Seccion para la administración de usuarios
@app.route('/usuarios/login',methods=['POST'])
def login():
    email=request.form['email']
    return 'Validando la cuenta del usuario:'+email

@app.route('/usuarios/iniciarSesion')
def iniciarSesion():
    return  render_template('usuarios/login.html')

@app.route('/usuarios/nuevo')
def nuevoUsuario():
    return render_template('usuarios/nuevo.html')

@app.route('/usuarios/registrar',methods=['post'])
def registrarUsuario():
    nombre=request.form['nombrecompleto']
    return 'registrando al usuario:'+nombre

@app.route('/usuarios/editar')
def editarUsuario():
    return  render_template('usuarios/editar.html')

@app.route('/usuarios')
def consultaUsuarios():
    return render_template('usuarios/consulta.html')
#Fin de la seccion de usuarios
#Seccion de productos
@app.route('/productos')
def consultaProductos():
    return render_template('productos/consulta.html')
@app.route('/productos/editar')
def editarProducto():
    return 'Editando un producto'

if __name__=='__main__':
    db.init_app(app)
    app.run(debug=True)