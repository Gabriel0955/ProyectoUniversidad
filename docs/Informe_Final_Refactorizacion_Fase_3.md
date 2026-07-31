# FASE 3 - Codigo refactorizado e informe final

Sistema de Reservas de Canchas Deportivas

## 1. Contexto

Este informe corresponde a la Fase 3 del proyecto integrador de Diseno de Software. La Fase 1 definio el diseno UML del sistema mediante el enfoque 4+1, con las clases Cliente, Cancha, Horario, Reserva, ServicioReserva, RepositorioReserva y Notificador. La Fase 2 implemento una version funcional minima y documento malos olores como metodo largo, lista de parametros, codigo duplicado, obsesion por primitivos, numeros magicos y clase con exceso de responsabilidades.

En esta fase se refactorizo el codigo manteniendo los casos de uso principales:

- Crear reserva.
- Consultar disponibilidad.
- Cancelar reserva.

El objetivo fue mejorar el diseno sin alterar el comportamiento observable del sistema. Despues de cada refactorizacion se ejecutaron las pruebas unitarias y se creo un commit independiente.

## 2. Evidencia de pruebas

Comando usado despues de cada refactorizacion:

```bash
python -m pytest
```

Resultado final:

```text
7 passed
```

Las pruebas existentes cubren la creacion exitosa de reservas, rechazo de conflictos, consulta de disponibilidad, cancelacion, reserva desconocida y correo invalido.

## 3. Refactorizaciones realizadas

| No. | Commit | Nivel cubierto | Refactorizacion | Olor atendido | Resultado |
| --- | --- | --- | --- | --- | --- |
| 1 | `9530008` | Metodos | Se extrajeron metodos privados de validacion en `ReservationService`. | Metodo largo y codigo duplicado. | `create_reservation`, `check_availability` y `cancel_reservation` quedaron mas pequenos y legibles. |
| 2 | `a1fa5a6` | Datos | Se introdujo `ReservationRequest` como objeto de datos. | Lista larga de parametros. | La creacion puede recibir una estructura unica y el metodo publico anterior se conserva como fachada. |
| 3 | `c0079fe` | Datos | Se introdujo `TimeSlot` como objeto de valor para inicio, duracion, fin y solapamiento. | Obsesion por primitivos y calculos repetidos de fechas. | La regla de solapamiento paso del repositorio al dominio. |
| 4 | `aeaca8f` | Clases/objetos y condicionales | Se introdujo `ReservationStatus` y `Reservation.cancel()`. | Strings magicos y manipulacion externa del estado. | La reserva controla su propia transicion a cancelada. |
| 5 | `d4adbc5` | Clases/objetos | Se extrajo `ReservationValidator`. | Clase de servicio con demasiadas responsabilidades. | Las validaciones de entrada quedaron en una clase especializada e inyectable. |
| 6 | `1cc9d63` | Condicionales | Se agrego `has_active_conflict()` y `Reservation.is_confirmed()`. | Condicionales compuestos y consultas poco expresivas. | El servicio expresa la regla como disponibilidad/conflicto y el repositorio encapsula el filtro. |

## 4. Cobertura de los cuatro niveles solicitados

### 4.1 Nivel de metodos

El metodo `create_reservation` concentraba validaciones, construccion de objetos, verificacion de conflictos, persistencia y notificacion. La primera refactorizacion extrajo validaciones y redujo el tamano del metodo. Luego, parte del flujo se movio a `create_reservation_from_request`, mejorando la claridad de la API interna.

### 4.2 Nivel de clases/objetos

La clase `ReservationService` tenia responsabilidades de caso de uso y validacion. Con `ReservationValidator`, el servicio conserva la orquestacion y delega las reglas de entrada. Ademas, `Reservation` ahora encapsula la cancelacion, por lo que el servicio ya no cambia directamente `status` ni concatena notas de cancelacion.

### 4.3 Nivel de datos

La lista de parametros de `create_reservation` se redujo mediante `ReservationRequest`. Tambien se reemplazo el par primitivo `start_at` y `duration_hours` por `TimeSlot`, que representa el concepto del dominio equivalente a Horario en el diseno UML de Fase 1.

### 4.4 Nivel de condicionales

Los condicionales sobre strings de estado y calculos de solapamiento se movieron a metodos con nombre. `Reservation.is_confirmed()` reemplaza comparaciones directas con literales y `has_active_conflict()` permite expresar la disponibilidad como una consulta booleana.

## 5. Evolucion del diseno

El diseno evoluciono sin cambiar el alcance funcional planteado en Fase 1:

- `Horario` se implementa ahora como `TimeSlot`, objeto de valor encargado de calcular `end_at` y detectar solapamientos.
- `Reserva` aumento su cohesion porque controla su estado mediante `cancel()`.
- `ServicioReserva` mantiene el rol de orquestador de casos de uso, pero ya no concentra todas las validaciones.
- `ReservationValidator` se agrego como colaborador especializado.
- `ReservationStatus` reemplaza literales de texto para evitar errores por strings magicos.
- `ReservationRequest` documenta los datos necesarios para crear una reserva y facilita extender el caso de uso sin agrandar la firma publica.

El diagrama actualizado se encuentra en:

```text
docs/diagrama_clases_actualizado_fase_3.puml
```

## 6. Relacion con principios de diseno

- Responsabilidad unica: `ReservationService`, `ReservationValidator`, `Reservation` y `TimeSlot` tienen responsabilidades mas separadas.
- Abierto/cerrado: la validacion y la representacion del horario pueden evolucionar con menor impacto en el servicio.
- Inversion de dependencias: se conserva la dependencia del servicio hacia repositorio y notificador inyectados.
- Alta cohesion: reglas de estado pertenecen a `Reservation` y reglas de tiempo pertenecen a `TimeSlot`.
- Bajo acoplamiento: el servicio depende de operaciones expresivas en sus colaboradores, no de detalles internos.

## 7. Estado final

La implementacion final mantiene los tres casos de uso de la Fase 1 y conserva las pruebas unitarias aprobadas. La historia de Git contiene seis commits independientes de refactorizacion, lo que permite revisar cada diff antes/despues y comprobar que el sistema se mantuvo funcional durante todo el proceso.

## 8. Comandos utiles de verificacion

```bash
git log --oneline -6
python -m pytest
```

Salida esperada de commits:

```text
1cc9d63 refactor: simplificar condicionales de disponibilidad
d4adbc5 refactor: extraer validador de reservas
aeaca8f refactor: encapsular cambios de estado de reserva
c0079fe refactor: introducir objeto de valor para horario
a1fa5a6 refactor: introducir objeto de solicitud de reserva
9530008 refactor: extraer metodos de validacion del servicio de reservas
```
