# Apuntes FIUBA

Portada de mis apuntes de Ingeniería en Informática: **https://flopeztancredi.github.io**

`index.html` es la portada, un archivo estático sin dependencias que Jekyll copia
tal cual (no tiene front matter, así que el tema no lo toca).

## Qué hay

Los apuntes completos viven cada uno en su repo, con su propio deploy, y la
portada linkea hacia afuera:

| materia | repo | se lee en |
|---|---|---|
| Sistemas Distribuidos (75.74) | [sistemas-distribuidos](https://github.com/flopeztancredi/sistemas-distribuidos) | [/sistemas-distribuidos](https://flopeztancredi.github.io/sistemas-distribuidos/) |
| Aprendizaje Automático (75.06) | [aprendizaje-automatico](https://github.com/flopeztancredi/aprendizaje-automatico) | [/aprendizaje-automatico](https://flopeztancredi.github.io/aprendizaje-automatico/) |

Los más viejos siguen en este repo, en markdown servido con
[just-the-docs](https://just-the-docs.com):

- `docs/redes/`: Redes (75.43), sobre Kurose.
- `docs/ebt/`: Empresas de Base Tecnológica 1.

## Por qué los completos no están acá

Cada uno es un HTML autocontenido de más de un mega, con su propio CSS, JS,
buscador, resaltador y panel de notas. Meterlos dentro de Jekyll sería pelear el
tema del sitio contra el del apunte, romper las URLs que ya circularon, y atar
varias materias al mismo deploy. Esta portada los reúne sin mudarlos.

## Colores

Cada materia tiene su acento, el mismo que usa su apunte, en versión clara y
oscura. Están inline en cada tarjeta de `index.html` (`--c`, `--c-ink` y `--c-bg`
para el tema claro, `--c-d` y `--c-d-bg` para el oscuro). Agregar una materia es
copiar una tarjeta y cambiarle esos cinco valores.

Los contrastes están verificados contra WCAG AA en los dos temas: el par más
justo es el acento sobre la tarjeta en claro, con 4,65:1.
