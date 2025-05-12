create table if not exists empleados(
  cedula varchar(11) not null,
  nombres varchar(25) not null,
  apellidos varchar(30) not null,
  cargo int not null,
  salario_base float not null,
  prestamos int,
  horas_extras int,
  primary key(cedula),
  foreign key (cargo) references cargos(id)
);


