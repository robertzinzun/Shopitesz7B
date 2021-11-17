from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,Boolean,BLOB
from flask_login import UserMixin

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
        db.session.commit()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

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