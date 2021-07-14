/*Creacion de la BD*/

create database shopitesz;
use shopitesz;
create table Categorias(
idCategoria int auto_increment not null,
nombre varchar(60) not null,
imagen mediumblob  null, 
estatus varchar(10) not null, 
constraint pk_categorias primary key(idCategoria),
constraint uk_nombre_categoria unique (nombre),
constraint chk_estatus check (estaus in('Activa','Inactiva'))
);

create table Productos(
idProducto int auto_increment not null,
idCategoria int not null,
nombre varchar(100) not null,
descripcion varchar(200) not null,
precioVenta float not null,
existencia int not null,
foto mediumblob null,
especificaciones mediumblob null,
estatus varchar(10),
constraint pk_procuctos primary key(idProducto),
constraint fk_Productos_Categorias foreign key (idCategoria) references Categorias(idCategoria),
constraint uk_nombre_categoria unique (nombre),
constraint chk_estatus check (estaus in('Activa','Inactiva'))
);


create table Usuarios(
idUsuario int auto_increment not null, 
nombreCompleto varchar (60) not null,
direccion varchar(200) not null,
telefono char(12) not null,
email varchar(100) not null,
passwordd varchar(20) not null,
tipo varchar(10) not null,
estatus varchar(10) not null,
constraint fk_usuarios primary key(idUsuario),
constraint uk_email unique (email),
constraint uk_telefono unique (telefono),
constraint chk_estatus check (estaus in('Activa','Inactiva')),
constraint chk_tipo check (tipo in('Cliente','Vendedor'))
);

create table Tarjetas (
idTarjeta int auto_increment not null,
idUsuario int not null, 
noTarjeta varchar (16) not null,
saldo float not null,
banco char(50) not null,
estatus varchar(10) not null,
constraint fk_Tarjetas primary key(idTarjeta),
constraint fk_Tarjetas_Usuarios foreign key (idUsuario) references Usuarios (idUsuario),
constraint uk_noTarjeta unique (noTarjeta),
constraint chk_estatus check (estaus in('Activa','Inactiva')),
constraint chk_saldo check(saldo<0)
);

create table Carrito (
idCarrito int auto_increment not null,
idUsuario int not null, 
idProducto int not null,
fecha date not null,
cantidad int not null,
estatus varchar(10) not null,
constraint fk_Carrito primary key(idCarrito),
constraint fk_Carrito_Usuarios foreign key (idUsuario) references Usuarios (idUsuario),
constraint fk_Carrito_Producto foreign key (idProducto) references Productos (idProducto),
constraint chk_estatus check (estaus in('Activa','Inactiva'))
);

create table Pedidos (
idPedido int auto_increment not null,
idComprador int not null, 
idVendedor int not null,
idTarjeta int not null,
fechaRegistro date not null,
fechaAtencion date null,
fechaRecepcion date null,
fechaCierre date  null,
total float not null,
estatus varchar(10) not null,
constraint fk_Pedidos primary key(idPedido),
constraint fk_Pedidos_Comprador foreign key (idComprador) references Usuarios (idUsuario),
constraint fk_Pedidos_Vendedor foreign key (idVendedor) references Usuarios (idUsuario),
constraint fk_Pedidos_Tarjeta foreign key (idTarjeta) references Tarjetas (idTarjeta),
constraint chk_estatus check (estaus in('Activa','Inactiva'))
);

create table DetallePedidos (
idDetalle int auto_increment not null,
idPedido int not null,
idProducto int not null, 
precio float not null,
cantidadPedida int not null,
cantidadEnviada int not null,
cantidadAceptada int null,
cantidadRechazada int null,
subtotal float not null,
estatus varchar(10) not null,
comentario varchar(200) not null,
constraint fk_DetallePedidos primary key(idDetalle),
constraint fk_DetallesPedidos_Pedidos foreign key (idPedido) references Pedidos (idPedido),
constraint fk_DetallePedidos_Productos foreign key (idProducto) references Productos (idProducto),
constraint chk_estatus check (estaus in('Activa','Inactiva'))
);
