create table if not exists cargos(
    id serial,
    cargo_empleado varchar(255),
    salario_base float not null,
    bonificacion float,
    primary key(id)
);