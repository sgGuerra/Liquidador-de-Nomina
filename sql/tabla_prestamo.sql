create table if not exists prestamos (
  id_prestamo serial not null,
  id_empleado varchar(11) not null,
  monto float not null,
  numero_de_cuotas int not null,
  fecha_inicio date not null default current_date,
  tasa_interes float not null,
  primary key(id_prestamo),
  foreign key (id_empleado) references empleados(cedula)
);

