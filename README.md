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

## Sincronizar entre dispositivos

`fuentes/sync.html` es un módulo que los builders inyectan antes de `</body>`.
Agrega el botón "Sincronizar" al panel lateral.

**Sin cuenta ni login**, modelo tipo Brave: se genera una frase de 12 palabras
que es identidad y clave a la vez. De esa frase salen, por derivaciones
independientes, la clave AES-GCM y el identificador del registro. El endpoint
(`sync-worker/`, un Worker de Cloudflare) solo ve un identificador y un blob
cifrado: no puede leer nada. Cada lector tiene su frase, así que no hay estado
compartido, y el que no configura nada sigue con todo en localStorage.

- Se sincroniza contenido, no interfaz. La regla es por sufijo
  (`-highlights-v1`, `-study-notes-v1`, `-prepared-topics-v1`), así que una
  materia nueva entra sola. El tema y los paneles plegados quedan por
  dispositivo.
- Gana la versión más nueva, clave por clave, con marca de tiempo propia. Antes
  de pisar algo local se guarda una copia y el diálogo ofrece "Deshacer", que
  toca solo ese dispositivo y deja el servidor intacto.
- La primera vez en un dispositivo que ya tenía notas, pregunta cuál lado
  conservar en vez de elegir solo.
- Sin nada configurado hay copia a un archivo JSON, que además es el respaldo
  que si no no existe.
- `fuentes/lista-frases.txt` son las 256 palabras. Cambiarla invalida las
  frases ya repartidas.

Mientras `ENDPOINT` en `fuentes/sync.html` diga `SIN_CONFIGURAR`, el diálogo
avisa que no está configurado y ofrece solo la copia en archivo. Para
habilitarlo, ver `sync-worker/README.md`.

Está en los cuatro apuntes, incluido el de Aprendizaje Automático, que vive en
su repo y lo lleva inyectado en el HTML porque no tiene build.

## Elegir qué se imprime

`fuentes/imprimir.html`, inyectado igual que el módulo de sincronización. El
botón PDF abre un diálogo con un tilde por capítulo, agrupados como la barra
lateral, con la estimación de páginas de cada uno y del total. Lo destildado se
oculta solo en `@media print`: la pantalla no se toca.

Arregla además un defecto que tenía la impresión. El CSS del shell trata de
mostrar el contenido de los `<details>` cerrados con
`details:not([open]) > .details-body { display: block }`, y Chrome ya no lo
respeta, así que la autoevaluación de Sistemas Distribuidos salía impresa con
las 71 preguntas y **ninguna** respuesta: 3.574 palabras en lugar de 45.000. El
módulo los abre de verdad en `beforeprint` y los cierra en `afterprint`. Por eso
el apunte pasó de 214 a 300 páginas impresas: antes faltaban las respuestas.

Los coeficientes de la estimación salen de imprimir los tres apuntes con Chrome
y ajustar por mínimos cuadrados (496 palabras por página de texto, 0,271 páginas
por figura o tabla). Error medido: +0,1%, +4,6% y -5,6%. **Si se toca el CSS de
impresión hay que volver a medirlos.**

## Colores

Cada materia tiene su acento, el mismo en la portada y en su apunte, en versión
clara y oscura. En la portada están inline en cada tarjeta de `index.html`
(`--c`, `--c-ink`, `--c-bg` para el tema claro, `--c-d` y `--c-d-bg` para el
oscuro); en los apuntes salen de la paleta de `fuentes/materias.py`.

Los contrastes están verificados contra WCAG AA en los dos temas: el par más
justo es el acento sobre la tarjeta en claro, con 4,65:1.
