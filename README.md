# Apuntes FIUBA

Portada de mis apuntes de Ingeniería en Informática: **https://flopeztancredi.github.io**

Sitio estático puro, sin Jekyll (`.nojekyll`). Todo lo que se publica es HTML
autocontenido: sin build en el servidor, sin dependencias, sin CDN.

## Qué hay

| materia | se lee en | vive en |
|---|---|---|
| Sistemas Distribuidos (75.74) | [/sistemas-distribuidos](https://flopeztancredi.github.io/sistemas-distribuidos/) | repo [sistemas-distribuidos](https://github.com/flopeztancredi/sistemas-distribuidos) |
| Aprendizaje Automático (75.06) | [/aprendizaje-automatico](https://flopeztancredi.github.io/aprendizaje-automatico/) | repo [aprendizaje-automatico](https://github.com/flopeztancredi/aprendizaje-automatico) |
| Redes (75.43) | [/redes](https://flopeztancredi.github.io/redes/) | este repo |
| Empresas de Base Tecnológica 1 | [/empresas-de-base-tecnologica](https://flopeztancredi.github.io/empresas-de-base-tecnologica/) | este repo |

Redes y EBT eran markdown servido con just-the-docs. Se convirtieron al mismo
formato que los otros dos: un solo HTML por materia, con buscador, resaltador,
panel de notas y diagramas SVG propios (las 11 imágenes que había se redibujaron).
Las URLs viejas siguen vivas: `docs/redes/` y `docs/ebt/` son redirecciones.

## Cómo se arma

```
python3 fuentes/armar.py redes    # -> redes/index.html
python3 fuentes/armar.py ebt      # -> empresas-de-base-tecnologica/index.html
```

- `fuentes/shell.html`: el cascarón compartido (CSS, buscador, notas, temas).
- `fuentes/materias.py`: lo único que cambia por materia (identidad, paleta,
  agrupación de capítulos). Agregar una materia es agregar una entrada.
- `fuentes/redes/`, `fuentes/ebt/`: un fragmento HTML por capítulo.
- `fuentes/md/`: el markdown original, conservado como fuente.

El build valida antes de escribir: ids únicos, anclas que resuelven, todo
`var(--token)` definido, cero recursos externos. `fuentes/lint_fragmentos.py`
revisa cada fragmento contra `fuentes/contrato-fragmento.md`.

## Colores

Cada materia tiene su acento, el mismo en la portada y en su apunte, en versión
clara y oscura. En la portada están inline en cada tarjeta de `index.html`
(`--c`, `--c-ink`, `--c-bg` para el tema claro, `--c-d` y `--c-d-bg` para el
oscuro); en los apuntes salen de la paleta de `fuentes/materias.py`.

Los contrastes están verificados contra WCAG AA en los dos temas: el par más
justo es el acento sobre la tarjeta en claro, con 4,65:1.
