from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,Boolean,BLOB,ForeignKey,Float,Date
from flask_login import UserMixin
from sqlalchemy.orm import relationship
import datetime
import json

db=SQLAlchemy()
class Categoria(db.Model):
    __tablename__='Categorias'
    idCategoria=Column(Integer,primary_key=True)
    nombre=Column(String(60),unique=True)
    estatus=Column(Boolean,default=True)
    foto=Column(BLOB,nullable=True)

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self,id):
        return self.query.get(id)

    def eliminar(self,id):
        obj=self.consultaIndividual(id)
        db.session.delete(obj)
        # obj.estatus=False ='I'
        # db.session.merge(obj)
        db.session.commit()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def consultarPagina(self,pagina):
        paginacion=self.query.order_by(Categoria.idCategoria.asc()).paginate(pagina,per_page=5,error_out=False)
        return paginacion
    def generarDatosExcel(self):
        datos={'Id':None,'Nombre':None}
        ids=[]
        nombres=[]
        lista=self.consultaGeneral()
        for c in lista:
            ids.append(c.idCategoria)
            nombres.append(c.nombre)
        datos['Id']=ids
        datos['Nombre']=nombres
        return datos
class Usuario(UserMixin,db.Model):
    __tablename__='Usuarios'
    idUsuario=Column(Integer,primary_key=True)
    nombrecompleto=Column(String(60),nullable=False)
    domicilio=Column(String(200),nullable=False)
    telefono=Column(String(12),nullable=False)
    email=Column(String(100),unique=True)
    password=Column(String(20),nullable=False)
    tipo=Column(String(10),nullable=False,default='Comprador')
    estatus=Column(Boolean,default=True)
    sexo=Column(String(1),nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
            return self.estatus

    def is_admin(self):
        if self.tipo=='Administrador':
            return True
        else:
            return False

    def is_comprador(self):
        if self.tipo=='Comprador':
            return True
        else:
            return False

    def is_vendedor(self):
        if self.tipo=='Vendedor':
            return True
        else:
            return False

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.idUsuario

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def eliminar(self, id):
        obj = self.consultaIndividual(id)
        db.session.delete(obj)
        db.session.commit()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def validar(self,email,password):
        usuario=None
        usuario=self.query.filter(Usuario.email==email,Usuario.password==password,Usuario.estatus==True).first()
        return usuario

    def consultarPorEmail(self,email):
        salida={"estatus":"","mensaje":""}
        usuario=None
        usuario=self.query.filter(Usuario.email==email).first()
        if usuario!=None:
            salida['estatus']='Error'
            salida['mensaje']='La cuenta:'+email+' ya se encuentra registrada.'
        else:
            salida['estatus'] = 'Ok'
            salida['mensaje'] = 'La cuenta:' + email + ' esta libre.'
        return salida
    def consultarCantidadCarrito(self):
        return len(self.carrito)

class Producto(db.Model):
    __tablename__='Productos'
    idProducto=Column(Integer,primary_key=True)
    idCategoria=Column(Integer,ForeignKey('Categorias.idCategoria'))
    nombre=Column(String(50),nullable=False)
    decripcion=Column(String(100),nullable=True)
    precio=Column(Float,nullable=False,default=1)
    existencia=Column(Integer,nullable=False,default=1)
    color=Column(String(25),nullable=False)
    marca=Column(String(50),nullable=False)
    costoEnvio=Column(Float,nullable=False)
    estatus=Column(Boolean,nullable=False,default=True)
    foto=Column(BLOB,nullable=False)
    categoria=relationship('Categoria',lazy='select')

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def consultarPorCategoria(self,id):
        return self.query.filter(Producto.idCategoria==id).all()

class Carrito(db.Model):
    __tablename__='Carrito'
    idCarrito=Column(Integer,primary_key=True)
    idUsuario=Column(Integer,ForeignKey('Usuarios.idUsuario'))
    idProducto=Column(Integer,ForeignKey('Productos.idProducto'))
    fecha=Column(Date,default=datetime.date.today())
    cantidad=Column(Integer,nullable=False,default=1)
    estatus=Column(String,nullable=False,default=True)
    producto=relationship('Producto',backref='carrito',lazy='select')
    usuario=relationship('Usuario',backref='carrito',lazy='select')

    def agregar(self,ojson):
        salida={"estatus":"","mensaje":""}
        try:
            self.from_json(ojson)
            db.session.add(self)
            db.session.commit()
            salida["estatus"] = "Ok"
            salida["mensaje"] = "Producto agregado con exito"
        except:
            salida["estatus"]="Error"
            salida["mensaje"]="Error al agregar el producto a la cesta"
        return salida
    def from_json(self,ojson):
        self.idUsuario=ojson["idUsuario"]
        self.idProducto = ojson["idProducto"]
        self.cantidad=ojson["cantidad"]

    def consultaGeneral(self,idUsuario):
        return self.query.filter(Carrito.idUsuario==idUsuario).all()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def eliminar(self, id):
        obj = self.consultaIndividual(id)
        db.session.delete(obj)
        db.session.commit()

class Tarjeta(db.Model):
    __tablename__ = 'Tarjetas'
    idTarjeta = Column(Integer, primary_key=True)
    idUsuario= Column(Integer,ForeignKey('Usuarios.idUsuario'))
    noTarjeta = Column(String, nullable=False)
    saldo = Column(Float, nullable=False)
    emisor = Column(String, nullable=False)
    cvc = Column(String,nullable=False)
    anioVigencia=Column(Integer,nullable=False)
    mesVigencia=Column(Integer,nullable=False)
    estatus = Column(Boolean, default=True)
    tipo=Column(String(20),nullable=False)
    usuario=relationship('Usuario',backref='tarjetas',lazy='select')

    def consultaIndividual(self,id):
        return self.query.filter(Tarjeta.idTarjeta== id).first()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

class Pedido(db.Model):
    __tablename__ = 'Pedidos'
    idPedido = Column(Integer, primary_key=True)
    idComprador = Column(Integer, ForeignKey('Usuarios.idUsuario'), nullable=False)
    idVendedor = Column(Integer, ForeignKey('Usuarios.idUsuario'), nullable=True)
    idTarjeta = Column(Integer, ForeignKey('Tarjetas.idTarjeta'),nullable=False)
    fechaRegistro = Column(String, nullable=False,default=datetime.date.today)
    fechaAtencion = Column(String, nullable=True)
    fechaCierre = Column(String, nullable=True)
    costesEnvio = Column(Float, default=0)
    subtotal=Column(Float,default=0)
    totalPagar = Column(Float, default=0)
    estatus = Column(String, nullable=False,default='Proceso')
    valoracion=Column(Integer,default=0)
    comentario=Column(String(200),default='Sin comentarios')
    productos=relationship('DetallePedido',backref='pedido',lazy='select')
    def agregar(self,ojson):
        salida={"estatus":"","mensaje":""}
        try:
            self.from_json(ojson)
            db.session.add(self)
            db.session.commit()
            t=Tarjeta()
            t=t.consultaIndividual(self.idTarjeta)
            t.saldo=t.saldo-self.totalPagar
            t.actualizar()
            salida["estatus"] = "Ok"
            salida["mensaje"] = "Pedido agregado con exito"
        except:
            salida["estatus"]="Error"
            salida["mensaje"]="Error al agregar el producto a la cesta"
        return salida

    def from_json(self,ojson):
        self.idTarjeta=ojson["idTarjeta"]
        self.idComprador=ojson["idComprador"]
        self.costesEnvio=ojson["envio"]
        self.subtotal=ojson["subtotal"]
        self.totalPagar=ojson["total"]
        self.productos=[]
        for p in ojson["carrito"]:
            dp=json.loads(p)
            prod=DetallePedido()
            prod.idProducto=dp.get("idProducto")
            prod.cantidad = dp.get("cantidad")
            prod.precio = dp.get("precio")
            prod.subtotal=dp.get("subtotal")
            self.productos.append(prod)


class DetallePedido(db.Model):
    __tablename__='DetallesPedidos'
    idDetalle=Column(Integer,primary_key=True)
    idPedido=Column(Integer,ForeignKey('Pedidos.idPedido'))
    idProducto=Column(Integer,ForeignKey('Productos.idProducto'))
    precio=Column(Float,nullable=False)
    cantidad=Column(Integer,nullable=False)
    subtotal=Column(Float,nullable=False)