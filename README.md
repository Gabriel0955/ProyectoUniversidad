# Sistema de Reservas de Canchas Deportivas

Proyecto académico correspondiente a la **Fase 2 - Código base e informe de diagnóstico** de la asignatura Diseño de Software.

## Casos de uso implementados

1. Crear una reserva.
2. Consultar disponibilidad de una cancha.
3. Cancelar una reserva.

## Tecnologías

- Python 3.10 o superior.
- Programación orientada a objetos.
- pytest para pruebas unitarias.
- Repositorio en memoria para evitar dependencias externas.

## Estructura

```text
src/reservas/
  models.py          Entidades de dominio.
  repository.py      Persistencia en memoria.
  notification.py    Simulación de notificaciones.
  service.py         Casos de uso del sistema.
tests/
  test_reservation_service.py
docs/
  Informe_Diagnostico_Malos_Olores.pdf
```

## Preparación del entorno

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Instalar pytest:

```bash
python -m pip install pytest
```

## Ejecutar pruebas

Desde la raíz del repositorio:

```bash
python -m pytest
```

Resultado esperado: **7 pruebas aprobadas**.

## Ejecutar demostración

Windows PowerShell:

```bash
$env:PYTHONPATH="src"
python MAIN.py
```

Linux/macOS:

```bash
PYTHONPATH=src python MAIN.py
```

## Diagnóstico

La versión base contiene oportunidades de mejora identificadas de manera explícita para la siguiente fase de refactorización. El informe se encuentra en `docs/Informe_Diagnostico_Malos_Olores.pdf`.

## Flujo Git recomendado

```bash
git init
git add .
git commit -m "feat: implementar casos de uso base de reservas"
git branch -M main
git remote add origin URL_DEL_REPOSITORIO
git push -u origin main
```

Los integrantes deben trabajar con ramas por funcionalidad o por integrante y realizar commits descriptivos.
