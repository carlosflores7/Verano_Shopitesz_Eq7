/*Creacion de la BD*/

create database shopitesz;
use shopitesz;
create table Categorias(
idCategoria int auto_increment not null,
nombre varchar(60) not null,
imagen mediumblob  null, 
estatus varchar(10) not null, 
constraint pk_categorias primary key(idCategoria),
constraint uk_nombre_categoria unique (nombre)
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
estatus varchar(10) not null,
constraint pk_procuctos primary key(idProducto),
constraint fk_Productos_Categorias foreign key (idCategoria) references Categorias(idCategoria)
);


create table Usuarios(
idUsuario int auto_increment not null, 
nombreCompleto varchar (60) not null,
direccion varchar(200) not null,
telefono char(12) not null,
email varchar(100) not null,
password_hash varchar(256) not null,
tipo varchar(20) not null,
estatus varchar(10) not null,
genero char(1) not null,
constraint fk_usuarios primary key(idUsuario),
constraint uk_email unique (email),
constraint uk_telefono unique (telefono)
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
constraint uk_noTarjeta unique (noTarjeta, banco)
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
constraint fk_Carrito_Producto foreign key (idProducto) references Productos (idProducto)
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
constraint fk_Pedidos_Tarjeta foreign key (idTarjeta) references Tarjetas (idTarjeta)
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
constraint fk_DetallePedidos_Productos foreign key (idProducto) references Productos (idProducto)
);

create table ENVIOS
(
   IDENVIO              int not null auto_increment,
   IDPEDIDO             int,
   IDPAQUETERIA         int,
   FECHAENVIO           date,
   FECHAENTREGA         date,
   NOGUIA               varchar(10),
   PESOPAQUETE          float,
   PRECIOGR             float,
   TOTALPAGAR           float,
   ESTATUS              varchar(10),
   primary key (IDENVIO)
);

create table PAQUETERIAS
(
   IDPAQUETERIA         int not null auto_increment,
   NOMBRE               varchar(50),
   PAGINAWEB            varchar(200),
   PRECIOGR             float,
   TELEFONO             varchar(12),
   ESTATUS              varchar(10),
   primary key (IDPAQUETERIA)
);

alter table ENVIOS add constraint FK_ENVIOS_PEDIDOS foreign key (IDPEDIDO) references PEDIDOS (IDPEDIDO);

alter table ENVIOS add constraint FK_PEDIDOS_PAQUETERIAS foreign key (IDPAQUETERIA) references PAQUETERIAS (IDPAQUETERIA);

/*Crear un usuario para la conexion con la app*/
create user user_shopitesz1 identified by 'Banano0420';
grant select, insert, update, delete on Shopitesz.Categorias to user_shopitesz1; 
grant select, insert, update, delete on Shopitesz.Productos to user_shopitesz1; 
grant select, insert, update, delete on Shopitesz.Usuarios to user_shopitesz1; 
grant select, insert, update, delete on Shopitesz.Tarjetas to user_shopitesz1; 
grant select, insert, update, delete on Shopitesz.Carrito to user_shopitesz1; 
grant select, insert, update, delete on Shopitesz.Pedidos to user_shopitesz1; 
grant select, insert, update, delete on Shopitesz.DetallePedidos to user_shopitesz1;
grant select, insert, update, delete on Shopitesz.ENVIOS to user_shopitesz1; 
grant select, insert, update, delete on Shopitesz.PAQUETERIAS to user_shopitesz1;