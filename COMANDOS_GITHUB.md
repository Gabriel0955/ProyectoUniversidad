# Publicar el proyecto en GitHub

1. Crear un repositorio vacío en GitHub, por ejemplo: `sistema-reservas-canchas`.
2. Abrir una terminal dentro de esta carpeta.
3. Ejecutar:

```bash
git init
git add .
git commit -m "feat: implementar código base y pruebas de reservas"
git branch -M main
git remote add origin https://github.com/USUARIO/sistema-reservas-canchas.git
git push -u origin main
```

## Ramas sugeridas para el equipo

```bash
git checkout -b feature/crear-reserva
git checkout -b feature/consultar-disponibilidad
git checkout -b feature/cancelar-reserva
git checkout -b test/pruebas-unitarias
git checkout -b docs/informe-diagnostico
```

Cada integrante debe realizar commits significativos y descriptivos.
