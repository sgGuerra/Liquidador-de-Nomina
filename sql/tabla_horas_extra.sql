create table if not exists horas_extras (
  id_hora_extra serial not null,
  id_empleado varchar(11) not null,
  id_tipo_hora varchar(20) not null,
  numero_de_horas int not null,
  fecha_registro date not null default current_date,
  primary key(id_hora_extra),
  foreign key(id_empleado) references empleados(cedula),
  foreign key(id_tipo_hora) references tipos_horas_extra(tipo_hora_id)
);