create table if not exists historial_pagos_prestamo (
  id_pago serial not null,
  id_prestamo int not null,
  fecha_pago date not null default current_date,
  monto_pagado float not null,
  saldo_anterior float not null,
  saldo_restante float not null,
  primary key(id_pago),
  foreign key (id_prestamo) references prestamos(id_prestamo)
);
