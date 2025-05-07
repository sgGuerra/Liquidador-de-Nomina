create table horas_extras (
  id_hora_extra serial not null,
  id_empleado varchar(11),
  id_tipo_hora varchar(20),
  primary key(id_hora_extra),
  foreign key(id_empleado) references empleado(cedula) ,
  foreign key(id_tipo_hora) references tipos_horas_extra(tipo_hora_id)
);