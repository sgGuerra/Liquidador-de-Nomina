create table if not exists historial_nomina (
  id serial not null,
  cedula varchar(11) not null,
  fecha_calculo timestamp not null default current_timestamp,
  salario_bruto float not null,
  deducciones float not null,
  impuestos float not null,
  auxilio_transporte float not null,
  neto float not null,
  primary key(id),
  foreign key (cedula) references empleados(cedula)
);
