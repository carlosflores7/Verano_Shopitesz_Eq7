from flask import Flask,render_template,request
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def inicio():
    #return "Hola mundo"
    return render_template("principal.html")

@app.route("/validarSesion")
def validarSesion():
    return render_template("usuarios/login.html")

@app.route("/registrarCuenta")
def registrarCuenta():
    return render_template("usuarios/registrarCuenta.html")

@app.route("/login")
def login():
    return render_template('usuarios/Login.html')

@app.route("/productos")
def consultarProductos():
    return render_template("productos/consultaGeneral.html")

@app.route("/categorias")
def categorias():
    return render_template("productos/categorias.html")

@app.route("/carrito")
def carrito():
    return render_template("usuarios/carrito.html")

@app.route('/tarjetas')
def Tarjetas():
    return render_template('Usuarios/tarjetas.html')


@app.route('/verperfil')
def verperfil():
    return render_template('usuarios/VerPerfil.html')

@app.route("/pedidosclt")
def consultarPedidos():
    #return "Retorna la lista de productos"
    return render_template("pedidosclt/pedidocl.html")

@app.route("/pedidosclt/pedidosdetalle")
def detallesPeddidos():
    return render_template("pedidosclt/pedidocliente.html")

@app.route("/vendedorpedido/pedidosad")
def vendedorpedidos():
    return render_template("vendedorpedido/pedidosadministrados.html")

@app.route("/vendedorpedido/pedidovendidosad")
def vendedorpedidosadministrados():
    return render_template("vendedorpedido/pedidosvendedoradministrativos.html")

if __name__== '__main__':
    app.run(debug=True)
