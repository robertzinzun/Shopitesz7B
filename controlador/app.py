from flask import Flask,render_template,request
from flask_bootstrap import Bootstrap

app=Flask(__name__,template_folder='../vista',static_folder='../static')
Bootstrap(app)

@app.route('/')
def inicio():
    #return '<H1>Bienvenido a la tienda en linea SHOPITESZ</H1>'
    return render_template('comunes/index.html')

@app.route('/categorias')
def categorias():
    return '<h1>Listado de categorias </h1>'

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
    app.run(debug=True)