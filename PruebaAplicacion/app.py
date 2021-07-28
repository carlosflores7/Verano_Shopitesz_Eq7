import datetime
from datetime import timedelta

from flask import Flask,render_template,request,redirect,url_for,flash,session,abort
from flask_bootstrap import Bootstrap
from modelo.Dao import db,Categoria,Producto,Usuario ,Tarjeta, Envio, Paqueteria, Pedido, Carrito, DetallePedidos
from flask_login import login_required,login_user,logout_user,current_user,LoginManager
import json
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user_shopitesz1:Banano0420@localhost/shopitesz'#usuario BRUNO
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='Cl4v3'

#Implementación de la gestion de usuarios con flask-login
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='mostrar_login'
login_manager.login_message='¡ Tu sesión expiró !'
login_manager.login_message_category="info"
#Implementación de la gestion de usuarios con flask-login
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='mostrar_login'
login_manager.login_message='¡ Tu sesión expiró !'
login_manager.login_message_category="info"

@app.before_request
def before_request():
    session.permanent=True
    #app.permanent_session_lifetime=timedelta(minutes=10)

@app.route("/")
def inicio():
    #return "Bienvenido a la tienda en linea Shopitesz"
    return render_template('principal.html')

#Inicio del CRUD de usuarios
@app.route('/Usuarios/iniciarSesion')
def mostrar_login():
    if current_user.is_authenticated:
        return render_template('principal.html')
    else:
        return render_template('usuarios/login.html')

@login_manager.user_loader
def cargar_usuario(id):
    return Usuario.query.get(int(id))

@app.route('/Usuarios/nuevo')
def nuevoUsuario():
    if current_user.is_authenticated and not current_user.is_admin():
        abort(404)
    else:
        return render_template('usuarios/registrarCuenta.html')

@app.route('/Usuarios/agregar',methods=['post'])
def agregarUsuario():
    if current_user.is_authenticated and not current_user.is_admin():
        return render_template('principal.html')
    else:
        try:
            usuario = Usuario()
            usuario.nombreCompleto = request.form['nombre']
            usuario.telefono = request.form['telefono']
            usuario.direccion = request.form['direccion']
            usuario.email = request.form['email']
            usuario.genero = request.form['genero']
            usuario.password = request.form['password']
            usuario.tipo = request.values.get("tipo", "Comprador")
            usuario.estatus = 'Activo'
            usuario.agregar()
            flash('¡ Usuario registrado con éxito !')
        except:
            flash('¡ Error al agregar al usuario !')
    return render_template('usuarios/registrarCuenta.html')

@app.route("/Usuarios/validarSesion",methods=['POST'])
def login():
    if not current_user.is_authenticated:
        correo = request.form['correo']
        password = request.form['password']
        usuario = Usuario()
        user = usuario.validar(correo, password)
        if user != None:
            login_user(user)
            if current_user.is_active():
                return render_template('principal.html')
            else:
                logout_user()
                flash('Cuenta inactiva')
                return redirect(url_for('mostrar_login'))
        else:
            flash('Nombre de usuario o contraseña incorrectos')
            return render_template('usuarios/login.html')
    else:
        abort(404)

@app.route('/Usuarios/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect(url_for('mostrar_login'))

@app.route('/Usuarios/verPerfil')
@login_required
def verperfil():
    return render_template('usuarios/VerPerfil.html')

@app.route('/Usuarios/editarPerfil',methods=['POST'])
@login_required
def editarPerfil():
    try:
        usuario = Usuario()
        usuario.idUsuario = request.form['ID']
        usuario.nombreCompleto = request.form['nombre']
        usuario.direccion = request.form['direccion']
        usuario.telefono = request.form['telefono']
        usuario.email = request.form['email']
        if request.form['password'] != '':
            usuario.password = request.form['password']

        usuario.tipo = request.form['tipo']
        if request.form['bandera'] == 'admin':
            usuario.estatus = request.form['estatus']
        else:
            usuario.estatus = 'Activo'
        usuario.genero = request.form['genero']
        usuario.editar()
        flash('¡ Usuario modificado con exito !')
    except:
        flash('¡ Error al modificar al usuario !')
    if request.form['bandera'] == 'admin':
        return redirect(url_for('verUsuarios'))
    else:
        return redirect(url_for('verperfil'))

@app.route('/Usuarios/eliminar/<int:id>')
@login_required
def eliminarPerfil(id):
    if current_user.is_authenticated and current_user.idUsuario == id:
        try:
            usuario = Usuario()
            usuario.eliminacionLogica(id)
            logout_user()
            flash('Usuario eliminado con exito')
        except:
            flash('Error al eliminar el usuario')
        return redirect(url_for('inicio'))
    else:
        abort(404)

@app.route('/Usuarios/todos')
@login_required
def verUsuarios():
    if current_user.is_admin():
        usuarios = Usuario()
        return render_template('usuarios/consultaGeneral.html', usuarios=usuarios.consultaGeneral())
    else:
        abort(404)

@app.route('/Usuarios/<int:id>')
@login_required
def usuarioIndividual(id):
    if current_user.is_admin():
        usuario = Usuario()
        return render_template('usuarios/consultaIndividual.html',usuario=usuario.consultaIndividual(id))
    else:
        abort(404)

#Fin del CRUD de usuarios

#CRUD Tarjetas
@app.route('/Usuarios/verTarjetas/<int:id>')
@login_required
def verTarjetas(id):
    tar=Tarjeta()
    return render_template("/tarjetas/tarjetaregistrada.html",Tarjetas=tar.consultaGeneral(id))

@app.route('/usuarios/agregarNuevaTarjeta/<int:id>')
@login_required
def agregarTarjeta(id):
    if current_user.is_authenticated :
        return render_template("/tarjetas/tarjetas.html")

@app.route("/tarjetas/agregar/<int:id>",methods=['post'])
@login_required
def subirtarjeta(id):
    try:
        if current_user.is_authenticated:
                try:
                    tar=Tarjeta()
                    tar.idUsuario=request.form['ID']
                    tar.noTarjeta=request.form['noTarjeta']
                    tar.saldo=request.form['Saldo']
                    tar.banco=request.form['Banco']
                    tar.estatus =request.form['Estatus']
                    tar.agregar()
                    flash('!tarjeta agregada con exito¡')
                except:
                    flash('! Error al agregar tarjeta¡')
                return render_template("/tarjetas/tarjetaregistrada.html",Tarjetas=tar.consultaGeneral(id))
        else:
            return redirect(url_for('mostrar_login'))
    except:
        #abort(500)
        return render_template("/")

@app.route('/Tarjeta/<int:id>')
@login_required
def EditarTarjetas(id):
    if current_user.is_authenticated():
        tar=Tarjeta()
        return render_template('tarjetas/editar.html', tar=tar.consulta(id))
    else:
        return redirect(url_for('mostrar_login'))
@app.route('/tarjeta/editar/<int:id>',methods=['POST'])
@login_required
def editandoTarjeta(id):
    if current_user.is_authenticated:
        try:
            tar=Tarjeta()
            tar.idTarjeta=request.form['ID']
            tar.idUsuario=request.form['IDU']
            tar.noTarjeta=request.form['noTarjeta']
            tar.saldo=request.form['Saldo']
            tar.banco=request.form['Banco']
            tar.estatus=request.form['Estatus']
            tar.editar()
            flash('! Tarjeta editada con exito')
        except:
            flash('! Error al editar el producto')
        return render_template("/tarjetas/tarjetaregistrada.html",Tarjetas=tar.consultaGeneral(id))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/tarjeta/eliminar/<int:id>')
@login_required
def eliminarTarjeta(id):
    if  current_user.is_authenticated():
        try:
            tar=Tarjeta()
            tar.eliminar(id)
            flash('Tarjeta Eliminada')
        except:
            flash('Error al eliminar tarjeta')
        return redirect((url_for('verperfil')))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/tarjeta/saldo')
@login_required
def saldoTarjeta():
    if current_user.is_authenticated and current_user.is_comprador():
        tarjeta = Tarjeta()
        tarjeta = tarjeta.consultaGeneral(current_user.idUsuario)
        for t in tarjeta:
            dict_tarjeta = {"idTarjeta": t.idTarjeta, "saldo": t.saldo}
        return json.dumps(dict_tarjeta)
    else:
        msg = {"estatus": "error", "mensaje": "Debes iniciar sesion"}
        return json.dumps(msg)
#Fin CRUD Tarjetas

#fin de manejo de usuarios


#incio de CRUD DE PRODUCTOS
@app.route("/productos")
def consultarProductos():
    #return "Retorna la lista de productos"
    producto=Producto()
    return render_template("productos/consultaGeneral.html",productos=producto.consultaGeneral())

@app.route('/productos/consultarImagen/<int:id>')
def consultarImagenProducto(id):
    prod=Producto()
    return prod.consultarImagen(id)

@app.route('/productos/consultarEspecificaciones/<int:id>')
def consultarEspecificionesProducto(id):
    prod=Producto()
    return prod.consultarEspecificaciones(id)

@app.route('/productos/consultarNombre/<int:id>')
def consultarNombreProducto(id):
    prod=Producto()
    return prod.consultarNombre(id)


@app.route('/productos/nuevo')
@login_required
def nuevoProducto():
    if current_user.is_authenticated and current_user.is_admin():
            cat = Categoria()
            return render_template('productos/agregar.html',cat=cat.consultaGeneral())
    else:
        #abort(404)
        return
@app.route("/productos/agregar",methods=['post'])
@login_required
def agregarProducto():
    try:
        if current_user.is_authenticated:
            if current_user.is_admin():
                try:
                    prod=Producto()
                    prod.idCategoria=request.form['Categoria']
                    prod.nombre=request.form['nombre']
                    prod.descripcion=request.form['descripcion']
                    prod.precioVenta=request.form['precioventa']
                    prod.existencia=request.form['existencia']
                    prod.foto=request.files['foto'].stream.read()
                    prod.especificaciones=request.files['especificaciones'].stream.read()
                    prod.estatus ='Activo'
                    prod.agregar()
                    flash('!Producto agregado con exito!')
                except:
                    flash('! Error al agregar producto !')
                return redirect(url_for('consultarProductos'))
            else:
                #abort(404)
                return
        else:
            return redirect(url_for('mostrar_login'))
    except:
        #abort(500)
        return

@app.route('/productos/<int:id>')
@login_required
def consultaProductos(id):
    if current_user.is_authenticated and current_user.is_admin:
        prod=Producto()
        cat=Categoria()
        return render_template('productos/editar.html',prod=prod.consultaIndividuall(id),cat=cat.consultaGeneral())
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/productos/editar',methods=['POST'])
@login_required
def editarProducto():
    if current_user.is_authenticated and current_user.is_admin:
        try:
            prod=Producto()
            prod.idProducto = request.form['id']
            prod.idCategoria=request.form['Categoria']
            prod.nombre=request.form['nombre']
            prod.descripcion = request.form['descripcion']
            prod.precioVenta = request.form['precioVenta']
            prod.existencia = request.form['existencia']
            especificaciones=request.files['especificaciones'].stream.read()
            foto=request.files['foto'].stream.read()
            if foto:
                prod.foto = foto
            if especificaciones:
                prod.especificaciones = especificaciones
            prod.estatus = request.form['estatus']
            prod.editar()
            flash('! Producto editado con éxito !')
        except:
            flash('! Error al editar el producto !')

        return redirect(url_for('consultarProductos'))
    else:
        return redirect(url_for('mostrar_login'))


@app.route('/productos/eliminar/<int:id>')
@login_required
def eliminarProductos(id):
    if current_user.is_authenticated and current_user.is_admin:
        try:
            prod=Producto()
            prod.eliminacionLogica(id)
            flash('Producto eliminado con exito')
        except:
            flash('Error al eliminar el producto')

        return redirect(url_for('consultarProductos'))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/productos/eliminacionfisica/<int:id>')
@login_required
def eliminacionfisicaproducto(id):
    if  current_user.is_authenticated and current_user.is_admin:
        try:
            prod=Producto()
            prod.eliminar(id)
            flash('Producto eliminado')
        except:
            flash('Error al eliminar Producto')
        return redirect((url_for('consultarProductos')))
    else:
        return redirect(url_for('mostrar_login'))

@app.route("/productos/categorias")
def productosPorCategoria():
    categoria=Categoria()
    return render_template('productos/productosPorCategoria.html',categorias=categoria.consultaGeneral())

@app.route("/productos/categoria/<int:id>")
def consultarProductosPorCategoria(id):
    producto=Producto()
    if id==0:
        lista=producto.consultaGeneral()
    else:
        lista=producto.consultarProductosPorCategoria(id)
    #print(lista)
    listaProductos=[]
    #Generacion de un diccionario para convertir los datos a JSON
    for prod in lista:
        prod_dic={'idProducto':prod.idProducto,'nombre':prod.nombre,'descripcion':prod.descripcion,'precio':prod.precioVenta,'existencia':prod.existencia}
        listaProductos.append(prod_dic)
    #print(listaProductos)
    var_json=json.dumps(listaProductos)
    return var_json

@app.route('/producto/<int:id>')
def consultarProducto(id):
    if current_user.is_authenticated and  current_user.is_comprador():
        prod=Producto()
        prod=prod.consultaIndividuall(id)
        dict_producto={"idProducto":prod.idProducto,"nombre":prod.nombre,"descripcion":prod.descripcion,"precio":prod.precioVenta,"existencia":prod.existencia}
        return json.dumps(dict_producto)
    else:
        msg={"estatus":"error","mensaje":"Debes iniciar sesion"}
        return json.dumps(msg)

@app.route('/productos/foto/<int:id>')
def consultarFotoPorducto(id):
    prod=Producto()
    return prod.consultarFoto(id)

#Fin Cru de productos

#CRUD de DetallesPedidos

@app.route('/Pedidos/verpedidos/detallespedidos/<int:id>')
@login_required
def verDetallesPedido(id):
    detallepedido=DetallePedidos()
    detallepedido = detallepedido.consultaGeneral(id)
    for c in detallepedido:
        idUsuario = c.pedido.idComprador
        idVendedor = c.pedido.idVendedor
    if current_user.is_authenticated and (current_user.is_comprador() or current_user.is_vendedor()) and (current_user.idUsuario==idUsuario or current_user.idUsuario==idVendedor):
        return render_template("/pedidosclt/consultaDetallespedido.html",detallepedido=detallepedido)
    else:
        abort(404)

@app.route('/Pedidos/verpedidos/detallespedidos/en/<int:id>')
@login_required
def editarDetallesPedidos(id):
    detallepedido=DetallePedidos()
    if current_user.is_authenticated and (current_user.is_comprador() or current_user.is_vendedor()):
        return render_template("pedidosclt/editarDetallespedido.html",detallepedido=detallepedido.consultaIndividual(id))
    else:
        abort(404)

@app.route('/Pedidos/verpedidos/detallespedidos/editarPedidos',methods=['POST'])
@login_required
def modDetallesPedidos():
    if current_user.is_authenticated and current_user.is_comprador() or current_user.is_vendedor():
        try:
            detallepedido=DetallePedidos()
            detallepedido.idDetalle = request.form['idDetalle']
            detallepedido.idPedido = request.form['idPedido']
            detallepedido.idProducto = request.form['idProducto']
            detallepedido.precio = request.form['precio']
            detallepedido.cantidadPedida = request.form['cantidadPedida']
            detallepedido.cantidadEnviada = request.form['cantidadEnviada']
            detallepedido.cantidadAceptada = request.form['cantidadAceptada']
            detallepedido.cantidadRechazada = request.form['cantidadRechazada']
            detallepedido.subtotal = request.form['subtotal']
            detallepedido.comentario = request.form['comentario']
            detallepedido.estatus = request.form['estatus']
            detallepedido.editar()
            flash('! Detalles Pedido editada con exito')
            return redirect(url_for('mostrar_login'))
        except:
            flash('! Error al editar Detalles Pedido ')



#Fin CRUD de detallesPedidos


#CRUD DE CARRITO

@app.route('/Usuarios/verCarrito/<int:id>')
@login_required
def verCarrito(id):
    if current_user.is_comprador() and current_user.idUsuario==id:
        carrito = Carrito()
        prod = Producto()
        return render_template("/usuarios/carrito.html", carrito=carrito.consultaGeneral(id),prod=prod.consultaGeneral(), total=carrito.total(id))
    else:
        abort(404)

@app.route('/Usuarios/verCarrito/ed/<int:id>')
@login_required
def editarCarrrito(id):
    carrito=Carrito()
    if current_user.is_authenticated and current_user.is_comprador():
        return render_template("usuarios/carritoEditar.html",carrito=carrito.consultaIndividual(id),total=0)
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Usuarios/verCarrito/editar',methods=['POST'])
@login_required
def editarCarritoBien():
    if  current_user.is_authenticated and current_user.is_comprador():
        try:
            carrito = Carrito()
            carrito.idCarrito = request.form['idCarrito']
            carrito.idUsuario = request.form['idUsuario']
            carrito.idProducto = request.form['idProducto']
            carrito.fecha = request.form['fecha']
            carrito.cantidad = request.form['cantidad']
            carrito.estatus = request.form['estatus']
            carrito.editar()
            flash('! Carrito editado con exito')
            return redirect(url_for('mostrar_login'))
        except:
            flash('! Error al editar el Producto ')


@app.route('/Usuarios/verCarrito/eliminacionfisica/<int:id>')
@login_required
def eliminacionfisicaCarrito(id):
    if  current_user.is_authenticated and current_user.is_comprador:
        try:
            carrito=Carrito()
            carrito.eliminar(id)
            flash('carrito eliminado')
        except:
            flash('Error al eliminar Producto')
        return redirect((url_for('mostrar_login')))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/carrito/agregar/<data>',methods=['get'])
def agregarProductoCarrito(data):
    msg=''
    if current_user.is_authenticated and current_user.is_comprador():
        datos=json.loads(data)
        carrito=Carrito()
        carrito.idProducto=datos['idProducto']
        carrito.idUsuario=current_user.idUsuario
        carrito.cantidad=datos['cantidad']
        carrito.agregar()
        msg={'estatus':'ok','mensaje':'Producto agregado a la cesta.'}
    else:
        msg = {"estatus": "error", "mensaje": "Debes iniciar sesion"}
    return json.dumps(msg)

@app.route('/carrito/pagar')
@login_required
def pagarCarrito():
    if current_user.is_comprador():
        carrito = Carrito()
        tarjeta = Tarjeta()
        producto = Producto()
        tarjeta = tarjeta.consultaGeneral(current_user.idUsuario)
        total = 0

        idTarjeta = 0
        for t in tarjeta:
            idTarjeta = t.idTarjeta

        if idTarjeta == 0:
            flash('No tienes una tarjeta asociada')
            return redirect(url_for('mostrar_login'))
        pedido = Pedido()

        carrito = carrito.consultaGeneral(current_user.idUsuario)
        for c in carrito:
            producto = producto.consultaIndividuall(c.idProducto)
            total += (producto.precioVenta * c.cantidad)
            if producto.existencia < c.cantidad:
                flash('No hay suficiente producto de ' + producto.nombre)
                return redirect(url_for('mostrar_login'))

        pedido.idComprador = current_user.idUsuario
        pedido.idVendedor = 3
        pedido.idTarjeta = idTarjeta
        pedido.fechaRegistro = datetime.date.today()
        pedido.total = total
        if total==0:
            abort(404)
        for t in tarjeta:
            if total>t.saldo:
                flash('No tienes saldo suficiente')
                return redirect(url_for('mostrar_login'))
        pedido.estatus = 'PENDIENTE'
        pedido.agregar()

        for c in carrito:
            producto = producto.consultaIndividuall(c.idProducto)
            detalle = DetallePedidos()
            detalle.idPedido = pedido.idPedido
            detalle.idProducto = producto.idProducto
            detalle.precio = producto.precioVenta
            detalle.cantidadPedida = c.cantidad
            detalle.cantidadEnviada = c.cantidad
            detalle.cantidadAceptada = 0
            detalle.cantidadRechazada = 0
            detalle.subtotal = producto.precioVenta * c.cantidad
            detalle.estatus = 'pendiente'
            detalle.comentario = ''
            detalle.agregar()
            producto.existencia = producto.existencia - c.cantidad
            c.eliminar(c.idCarrito)
            for t in tarjeta:
                t.saldo = t.saldo - pedido.total
                t.editar()
            flash('Pago realizado con éxito')
    else:
        abort(404)
    return redirect(url_for('mostrar_login'))
#FIN DE CRUD CARRITO


#CRUD de Categorias
@app.route('/Categorias')
def consultaCategorias():
    cat=Categoria()
    return render_template('categorias/consultaGeneral.html',categorias=cat.consultaGeneral())

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
    try:
        if current_user.is_authenticated:
            if current_user.is_admin():
                try:
                    cat = Categoria()
                    cat.nombre = request.form['nombre']
                    cat.imagen = request.files['imagen'].stream.read()
                    cat.estatus = 'Activa'
                    cat.agregar()
                    flash('¡ Categoria agregada con exito !')
                except:
                    flash('¡ Error al agregar la categoria !')
                return redirect(url_for('consultaCategorias'))
            else:
               # abort(404)
                return

        else:
            return redirect(url_for('mostrar_login'))
    except:
        #abort(500)
        return

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

#Crud de envios

@app.route("/Envios")
@login_required
def consultarEnvios():
    envio= Envio()
    if current_user.is_authenticated and current_user.is_vendedor():
        return render_template("envios/consultaGeneral.html",envio=envio.consultaGeneral())
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Envios/<int:id>')
@login_required
def editarEnvio(id):
    envio = Envio()
    paq = Paqueteria()

    if current_user.is_authenticated and current_user.is_vendedor():
        return render_template("envios/editar.html",envio=envio.consultaIndividual(id),paq=paq.consultaGeneral())
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Envios/nueva')
@login_required
def nuevoEnvio():
    paq = Paqueteria()
    ped = Pedido()
    if current_user.is_authenticated and current_user.is_vendedor():
        return render_template('envios/agregar.html',paq=paq.consultaGeneral(),ped=ped.consultaGeneral())
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Envios/agregar',methods=['post'])
@login_required
def agregarEnvio():
        if current_user.is_authenticated and current_user.is_vendedor():
                try:
                    envio = Envio()
                    envio.IDPEDIDO = request.form['IDPEDIDO']
                    envio.IDPAQUETERIA = request.form['IDPAQUETERIA']
                    envio.FECHAENVIO = request.form['FECHAENVIO']
                    envio.FECHAENTREGA = request.form['FECHAENTREGA']
                    envio.NOGUIA = request.form['NOGUIA']
                    envio.PESOPAQUETE = request.form['PESOPAQUETE']
                    envio.PRECIOGR = request.form['PRECIOGR']
                    envio.TOTALPAGAR = request.form['TOTALPAGAR']
                    envio.ESTATUS = "PENDIENTE"
                    envio.agregar()
                    flash('¡ Envio Registrado con exito !')
                    return redirect(url_for('consultarEnvios'))
                except:
                    flash('¡ Error al agregar la categoria !')




@app.route('/Envios/editar',methods=['POST'])
@login_required
def modEnvio():
    if  current_user.is_authenticated and current_user.is_vendedor():
        try:
            envio = Envio()
            envio.IDENVIO = request.form['IDENVIO']
            envio.IDPEDIDO = request.form['IDPEDIDO']
            envio.IDPAQUETERIA = request.form['IDPAQUETERIA']
            envio.FECHAENVIO = request.form['FECHAENVIO']
            envio.FECHAENTREGA = request.form['FECHAENTREGA']
            envio.NOGUIA = request.form['NOGUIA']
            envio.PESOPAQUETE = request.form['PESOPAQUETE']
            envio.PRECIOGR = request.form['PRECIOGR']
            envio.TOTALPAGAR = request.form['TOTALPAGAR']
            envio.ESTATUS = request.form['ESTATUS']
            envio.editar()
            flash('! Envio editado con exito')
            return redirect(url_for('consultarEnvios'))
        except:
            flash('! Error al editar el Envio ')



#Fin de crud de envios

#CRUD DE PEDIDOS

@app.route('/Pedidos/verpedidos/<int:id>')
@login_required
def verPedidos(id):
    pedido=Pedido()
    if current_user.is_authenticated and (current_user.is_comprador() or current_user.is_vendedor()) and current_user.idUsuario==id:
        return render_template("pedidosclt/consulta.html",pedido=pedido.consultaGeneral(id))
    else:
        abort(404)

@app.route('/Pedidos/verpedidos/en/<int:id>')
@login_required
def editarPedidos(id):
    pedido = Pedido()
    pedido = pedido.consultaIndividual(id)
    if current_user.is_authenticated and (current_user.is_comprador() or current_user.is_vendedor()) and (current_user.idUsuario==pedido.idComprador or current_user.idUsuario==pedido.idVendedor):
        return render_template("pedidosclt/editarPedido.html",pedido=pedido)
    else:
        abort(404)

@app.route('/Pedidos/editarPedidos',methods=['post'])
@login_required
def modPedidos():
    if current_user.is_authenticated and (current_user.is_comprador() or current_user.is_vendedor()):
        try:
            ped=Pedido()
            ped.idPedido = request.form['idPedido']
            ped.idComprador = request.form['idComprador']
            ped.idVendedor = request.form['idVendedor']
            ped.idTarjeta = request.form['idTarjeta']
            ped.fechaRegistro = request.form['fechaRegistro']
            ped.fechaAtencion = request.form['fechaAtencion']
            ped.fechaRecepcion = request.form['fechaRecepcion']
            ped.fechaCierre = request.form['fechaCierre']
            ped.total = request.form['total']
            ped.estatus = request.form['ESTATUS']
            ped.editar()
            flash('! Pedido editada con exito')
            return redirect(url_for('inicio'))
        except:
            flash('! Error al editar el pedido ')
        return redirect(url_for('inicio'))
#FIN DE CRUD DE PEDIDOS



#CRUD de paquterias

@app.route("/Paqueterias")
@login_required
def consultarPaqueterias():
    paqueteria = Paqueteria()
    if current_user.is_authenticated and current_user.is_admin():
        return render_template("paqueterias/consultaGeneral.html",paqueteria=paqueteria.consultaGeneral())
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Paqueterias/<int:id>')
@login_required
def editarPaqueterias(id):
    paqueteria = Paqueteria()
    if current_user.is_authenticated and current_user.is_admin():
        return render_template("paqueterias/editar.html",paqueteria=paqueteria.consultaIndividual(id))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Paqueterias/nueva')
@login_required
def nuevaPaqueteria():
    if current_user.is_authenticated and current_user.is_admin():
        return render_template('paqueterias/agregar.html')
    else:
        return redirect(url_for('mostrar_login'))


@app.route('/Paqueterias/agregar',methods=['post'])
@login_required
def agregarPaqueteria():
        if current_user.is_authenticated and current_user.is_admin():
                try:
                    paqueteria = Paqueteria()
                    paqueteria.NOMBRE = request.form['NOMBRE']
                    paqueteria.PAGINAWEB = request.form['PAGINAWEB']
                    paqueteria.PRECIOGR = request.form['PRECIOGR']
                    paqueteria.TELEFONO = request.form['TELEFONO']
                    paqueteria.ESTATUS = "Activo"
                    paqueteria.agregar()
                    flash('¡ Paqueteria Registrado con exito !')
                    return redirect(url_for('consultarPaqueterias'))
                except:
                    flash('¡ Error al agregar la categoria !')

@app.route('/Paqueterias/editar',methods=['POST'])
@login_required
def modPaqueterias():
    if  current_user.is_authenticated and current_user.is_admin():
        try:
            paqueteria = Paqueteria()
            paqueteria.IDPAQUETERIA = request.form['IDPAQUETERIA']
            paqueteria.NOMBRE = request.form['NOMBRE']
            paqueteria.PAGINAWEB = request.form['PAGINAWEB']
            paqueteria.PRECIOGR = request.form['PRECIOGR']
            paqueteria.TELEFONO = request.form['TELEFONO']
            paqueteria.ESTATUS = request.form['ESTATUS']
            paqueteria.editar()
            flash('! Paqueteria editada con exito')
            return redirect(url_for('consultarPaqueterias'))
        except:
            flash('! Error al editar la Paqueteria ')

#FIN DE CRUD de paqueterias

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

#error
@app.errorhandler(404)
def error_404(e):
    return render_template("comunes/error_404.html"),404

@app.errorhandler(405)
def error_405(e):
    return render_template("comunes/error_405.html"),405

if __name__=='__main__':
    db.init_app(app)#Inicializar la BD - pasar la configuración de la url de la BD
    app.run(debug=True)