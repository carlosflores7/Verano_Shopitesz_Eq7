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

@app.route("/login", methods=['POST'])
def login():
    correo=request.form['correo']
    return "Validando al usuario "+correo

@app.route("/productos")
def consultarProductos():
    return render_template("productos/consultaGeneral.html")

@app.route("/categorias")
def categorias():
    return render_template("productos/categorias.html")

@app.route("/carrito")
def carrito():
    return render_template("usuarios/carrito.html")

if __name__== '__main__':
    app.run(debug=True)
