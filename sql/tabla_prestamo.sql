create table if not exists prestamos (
  id_prestamo serial not null,
  id_empleado varchar(11) not null,
  valor_prestamo float,
  cuotas int,
  primary key(id_prestamo),
  foreign key (id_empleado) references empleado(cedula)
);