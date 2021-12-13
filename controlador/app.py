import urllib

from flask import Flask,render_template,request,flash,redirect,url_for,abort
from flask_bootstrap import Bootstrap
from modelo.DAO import Categoria,db,Usuario, Producto, Carrito, Tarjeta, Pedido
from flask_login import current_user,login_user,logout_user,login_manager,login_required,LoginManager
import json
app=Flask(__name__,template_folder='../vista',static_folder='../static')
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://userShopitesz:Hola.123@127.0.0.1/Shopitesz_v2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='cl4v3'

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))

@app.route('/')
def inicio():
    c=Categoria()
    return render_template('comunes/principal.html',categorias=c.consultaGeneral())

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
@login_required
def nuevaCategoria():
    return render_template('categorias/nuevo.html')

@app.route('/categorias/registrar',methods=['post'])
@login_required
def registrarCategoria():
    c=Categoria()
    c.nombre=request.form['nombre']
    imagen=request.files['foto'].read()
    if imagen:
        c.foto=imagen
    c.insertar()
    flash('Categoria registrada con exito')
    return render_template('categorias/nuevo.html')

@app.route('/categorias/ver/<int:id>')
@login_required
def consultarCategoria(id):
    if current_user.is_authenticated and current_user.is_admin():
        c=Categoria()
        return render_template('categorias/editar.html',cat=c.consultaIndividual(id))
    else:
        abort(404)

@app.route('/categorias/editar',methods=['post'])
@login_required
def editarCategoria():
    c=Categoria()
    c.idCategoria=request.form['id']
    c.nombre=request.form['nombre']
    imagen=request.files['foto'].stream.read()
    if imagen:
        c.foto=imagen
    estatus=request.values.get('estatus','False')
    if estatus=='True':
        c.estatus=True
    else:
        c.estatus=False
    c.actualizar()
    flash('Categoria editada con exito')
    return render_template('categorias/editar.html',cat=c)

@app.route('/categorias/eliminar/<int:id>')
@login_required
def eliminarCategoria(id):
    if current_user.is_authenticated and current_user.is_admin():
        c=Categoria()
        c.eliminar(id)
        return redirect(url_for('categorias'))
    else:
        abort(404)
#fin de seccion de categorias
#Seccion para la administración de usuarios
@app.route('/usuarios/iniciarSesion')
def login():
    if current_user.is_authenticated:
        return render_template('comunes/principal.html')
    else:
        return  render_template('usuarios/login.html')

@app.route('/usuarios/validarSesion',methods=['post'])
def validarSesion():
    email=request.form['email']
    password=request.form['password']
    user=Usuario()
    user=user.validar(email,password)
    if user!=None:
        print(user.nombrecompleto)
        login_user(user)
        c = Categoria()
        return render_template('comunes/principal.html', categorias=c.consultaGeneral())
    else:
        flash('! Datos de Sesión incorrectos !')
        return render_template('usuarios/login.html')

@app.route('/usuarios/nuevo')
def nuevoUsuario():
    return render_template('usuarios/nuevo.html')

@app.route('/usuarios/registrar',methods=['post'])
def registrarUsuario():
    try:
        u = Usuario()
        u.nombrecompleto = request.form['nombrecompleto']
        u.domicilio = request.form['domicilio']
        u.telefono = request.form['telefono']
        u.tipo = request.form['tipo']
        u.password = request.form['password']
        u.sexo = request.form['genero']
        u.email=request.form['email']
        u.insertar()
        flash('! Usuario registrado con exito !')
    except:
        flash('!Error al registrar el usuario!')
    return redirect(url_for('nuevoUsuario'))

@app.route('/usuarios/editar')
def editarUsuario():
    return  render_template('usuarios/editar.html')

@app.route('/usuarios/modificar',methods=['POST'])
def modificarUsuario():
    try:
        u=Usuario()
        u.idUsuario=current_user.idUsuario
        u.nombrecompleto=request.form['nombre']
        u.domicilio=request.form['domicilio']
        u.telefono=request.form['telefono']
        u.tipo=request.form['tipo']
        u.password=request.form['password']
        u.sexo=request.form['sexo']
        u.actualizar()
        login_user(u.consultaIndividual(u.idUsuario))
        flash('! Datos modificados con exito !')
    except:
        flash('!Error al modificar el usuario!')

    return redirect(url_for('editarUsuario'))


@app.route('/usuarios')
def consultaUsuarios():
    return render_template('usuarios/consulta.html')

@app.route('/cerrarSesion')
def cerrarSesion():
    logout_user()
    return redirect(url_for('login'))

@app.route('/usuarios/email/<string:email>',methods=['Get'])
def consultarEmail(email):
    usuario=Usuario()
    return json.dumps(usuario.consultarPorEmail(email))
#Fin de la seccion de usuarios
#Seccion de productos

@app.route('/productos')
def consultaProductos():
    p=Producto()
    return render_template('productos/consulta.html',productos=p.consultaGeneral())

@app.route('/productos/imagen/<int:id>')
def consultarImagenProducto(id):
    p=Producto()
    return p.consultaIndividual(id).foto

@app.route('/productos/categoria/<int:id>')
def consultarPorCategoria(id):
    p=Producto()
    return render_template('productos/consulta.html',productos=p.consultarPorCategoria(id))

@app.route('/productos/editar')
def editarProducto():
    return 'Editando un producto'

@app.route('/productos/nuevo')
def nuevoProducto():
    c=Categoria()
    return render_template('productos/nuevo.html',categorias=c.consultaGeneral())

@app.route('/productos/registrar',methods=['post'])
def registrarProducto():
    idCategoria=request.form['categoria']
    return "Categoria seleccionada:"+str(idCategoria)
#seccion del carrito
@app.route('/carrito/agregar',methods=['post'])
@login_required
def agregarCarrito():
    ojson=request.get_json()
    ojson["idUsuario"]=current_user.idUsuario
    carrito=Carrito()
    salida=carrito.agregar(ojson)
    salida['productos']=current_user.consultarCantidadCarrito()
    #flash('Producto Agregado con Exito')
    return salida

@app.route('/carrito',methods=['get'])
@login_required
def consultarCarrito():
    if current_user.is_authenticated and current_user.is_comprador():
        carrito=Carrito()
        return render_template('carrito/consulta.html',carrito=carrito.consultaGeneral(current_user.idUsuario))
    else:
        abort(404)

@app.route('/carrito/eliminar/<int:id>',methods=['get'])
@login_required
def eliminarCarrito(id):
    if current_user.is_authenticated and current_user.is_comprador():
        try:
            carrito=Carrito()
            carrito.eliminar(id)
            flash('Producto del  carrito eliminado con exito.')
        except:
            flash('Error al eliminar el producto del carrito.')
        return redirect(url_for('consultarCarrito'))
    else:
        abort(404)
#fin seccion de carrito

#seccion tarjetas
@app.route('/tarjetas/<int:id>',methods=['GET'])
@login_required
def consultarTarjeta(id):
    if current_user.is_authenticated and  current_user.is_comprador():
        tarjeta=Tarjeta()
        tarjeta=tarjeta.consultaIndividual(id)
        dict_tarjeta={"idTarjeta":tarjeta.idTarjeta,"saldo":tarjeta.saldo,"banco":tarjeta.emisor}
        return json.dumps(dict_tarjeta)
    else:
        msg={"estatus":"error","mensaje":"Debes iniciar sesion"}
        return json.dumps(msg)
#fin seccion de tarjetas
#seccion de pedidos
@app.route('/pedidos/registrar',methods=['post'])
@login_required
def registrarPedido():
    if current_user.is_authenticated and  current_user.is_comprador():
        ojson=request.get_json()
        ojson["idComprador"]=current_user.idUsuario
        pedido=Pedido()
        print(ojson)
        salida=pedido.agregar(ojson)
        return json.dumps(salida)
    else:
        msg={"estatus":"error","mensaje":"Debes iniciar sesion"}
        return json.dumps(msg)

#fin seccion pedidos
@app.route('/prueba')
def prueba():
    return render_template('comunes/prueba.html')
@app.route('/ruta',methods=['post'])
def ruta():
    fecha=request.form['fecha']
    cad=fecha.split("-")
    cadFecha=cad[2]+"/"+cad[1]+"/"+cad[0]
    return cadFecha
#Seccion de paginas de error
@app.errorhandler(404)
def error_404(e):
    return render_template('comunes/error_404.html'),404
if __name__=='__main__':
    db.init_app(app)
    app.run(debug=True)