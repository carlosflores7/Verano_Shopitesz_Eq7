from flask import Flask,render_template,request,redirect,url_for,flash
from flask_bootstrap import Bootstrap
from modelo.Dao import db,Categoria,Producto
from flask_login import login_required,login_user,logout_user,current_user,login_manager
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user_shopitesz1:Banano0420@localhost/shopitesz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='Cl4v3'

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
    producto = Producto()
    return render_template("productos/consultaGeneral.html",productos=producto.consultaGeneral())


#CRUD de Categorias
@app.route('/Categorias')
def consultaCategorias():
    cat=Categoria()
    return render_template('productos/categorias.html',categorias=cat.consultaGeneral())

@app.route('/Categorias/consultarImagen/<int:id>')
def consultarImagenCategoria(id):
    cat=Categoria()
    return cat.consultarImagen(id)


@app.route('/Categorias/nueva')
@login_required
def nuevaCategoria():
    if current_user.is_authenticated and current_user.is_admin():
        return render_template('categorias/agregar.html')
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Categorias/agregar',methods=['post'])
@login_required
def agregarCategoria():
    if current_user.is_authenticated and current_user.is_admin():
        try:
            cat=Categoria()
            cat.nombre=request.form['nombre']
            cat.imagen=request.files['imagen'].stream.read()
            cat.estatus='Activa'
            cat.agregar()
            flash('¡ Categoria agregada con exito !')
        except:
            flash('¡ Error al agregar la categoria !')
        return redirect(url_for('consultaCategorias'))
    else:
        return redirect(url_for('mostrar_login'))


@app.route('/Categorias/<int:id>')
@login_required
def consultarCategoria(id):
    if current_user.is_authenticated and current_user.is_admin():
        cat=Categoria()
        return render_template('categorias/editar.html',cat=cat.consultaIndividuall(id))
    else:
        return redirect(url_for('mostrar_login'))


@app.route('/Categorias/editar',methods=['POST'])
@login_required
def editarCategoria():
    if current_user.is_authenticated and current_user.is_admin():
        try:
            cat=Categoria()
            cat.idCategoria=request.form['id']
            cat.nombre=request.form['nombre']
            imagen=request.files['imagen'].stream.read()
            if imagen:
                cat.imagen=imagen
            cat.estatus=request.values.get("estatus","Inactiva")
            cat.editar()
            flash('¡ Categoria editada con exito !')
        except:
            flash('¡ Error al editar la categoria !')

        return redirect(url_for('consultaCategorias'))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Categorias/eliminar/<int:id>')
@login_required
def eliminarCategoria(id):
    if current_user.is_authenticated and current_user.is_admin():
        try:
            categoria=Categoria()
            #categoria.eliminar(id)
            categoria.eliminacionLogica(id)
            flash('Categoria eliminada con exito')
        except:
            flash('Error al eliminar la categoria')
        return redirect(url_for('consultaCategorias'))
    else:
        return redirect(url_for('mostrar_login'))

#Fin del crud de categorias


@app.route("/carrito")
def carrito():
    return render_template("usuarios/carrito.html")

@app.route('/tarjetas')
def Tarjetas():
    return render_template('Usuarios/tarjetas.html')

@app.route('/tarjetas/registrada')
def Tarjetasregistradas():
    return render_template('Usuarios/tarjetaregistrada.html')



@app.route('/verperfil')
def verperfil():
    return render_template('usuarios/VerPerfil.html')

@app.route('/verperfil/modificar')
def modificarperfil():
    return render_template('usuarios/modificarperfilcl.html')

@app.route("/pedidosclt")
def consultarPedidos():
    #return "Retorna la lista de productos"
    return render_template("pedidosclt/pedidocl.html")

@app.route("/pedidosclt/pedidosdetalle")
def detallesPeddidos():
    return render_template("pedidosclt/pedidocliente.html")

@app.route("/pedidosclt/pedidospedir")
def pedidospedir():
    return render_template("pedidosclt/pedidopedircl.html")

@app.route("/pedidosclt/pedidosclvarios")
def pedidosclvarios():
    return render_template("pedidosclt/pedidosclvarios.html")

@app.route("/pedidosclt/pedidoscluno")
def pedidoscluno():
    return render_template("pedidosclt/pedidoscluno.html")

@app.route("/vendedorpedido/pedidosad")
def vendedorpedidos():
    return render_template("vendedorpedido/pedidosadministrados.html")

@app.route("/vendedorpedido/aceptarpedido")
def vendedorpedidosaceptar():
    return render_template("vendedorpedido/aceptarpedido.html")

@app.route("/vendedorpedido/pedidovendidosad")
def vendedorpedidosadministrados():
    return render_template("vendedorpedido/pedidosvendedoradministrativos.html")

@app.route("/vendedorpedido/pedidovendidaduno")
def vendedorpedidosaduno():
    return render_template("vendedorpedido/pedidosaduno.html")

@app.route("/vendedorpedido/pedidovendidadvarios")
def vendedorpedidosadvarios():
    return render_template("vendedorpedido/pedidosadvarios.html")

if __name__== '__main__':
    app.run(debug=True)
