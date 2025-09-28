create table if not exists cargos(
    id serial,
    cargo_empleado varchar(255),
    bonificacion float,
    primary key(id)
);