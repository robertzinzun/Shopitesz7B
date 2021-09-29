from flask import Flask,render_template

app=Flask(__name__)

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

if __name__=='__main__':
    app.run(debug=True)