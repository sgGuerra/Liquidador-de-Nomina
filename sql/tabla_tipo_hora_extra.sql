create table if not exists tipos_horas_extra(
    tipo_hora_id varchar(20),
    nombre_tipo_hora varchar(50) not null,
    primary key(tipo_hora_id)
);