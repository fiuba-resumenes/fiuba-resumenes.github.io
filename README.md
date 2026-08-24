# FIUBA Resúmenes

Apuntes de Ingeniería en Informática (FIUBA), de varios autores y abiertos a
contribuciones: **https://fiuba-resumenes.github.io**

Sitio estático puro, sin Jekyll (`.nojekyll`). Todo lo que se publica es HTML
autocontenido: sin build en el servidor, sin dependencias, sin CDN.

## Qué hay

| materia | se lee en | vive en | lo escribió |
|---|---|---|---|
| Sistemas Distribuidos (75.74) | [/sistemas-distribuidos](https://flopeztancredi.github.io/sistemas-distribuidos/) | repo [sistemas-distribuidos](https://github.com/flopeztancredi/sistemas-distribuidos) | flopeztancredi |
| Aprendizaje Automático (75.06) | [/aprendizaje-automatico](https://flopeztancredi.github.io/aprendizaje-automatico/) | repo [aprendizaje-automatico](https://github.com/flopeztancredi/aprendizaje-automatico) | flopeztancredi |
| Redes (75.43) | [/redes](https://fiuba-resumenes.github.io/redes/) | este repo | echepereza, flopeztancredi |
| Empresas de Base Tecnológica 1 | [/empresas-de-base-tecnologica](https://fiuba-resumenes.github.io/empresas-de-base-tecnologica/) | este repo | echepereza, flopeztancredi |
| Empresas de Base Tecnológica 2 | [/empresas-de-base-tecnologica-2](https://fiuba-resumenes.github.io/empresas-de-base-tecnologica-2/) | este repo | echepereza, flopeztancredi |
| Programación Concurrente | [echepereza.github.io/programacion-concurrente](https://echepereza.github.io/programacion-concurrente/) | repo [programacion-concurrente](https://github.com/echepereza/programacion-concurrente) | echepereza |
| Ciencia de Datos | [/ciencia-de-datos](https://fiuba-resumenes.github.io/ciencia-de-datos/) | este repo | echepereza, flopeztancredi |

Redes y EBT eran markdown servido con just-the-docs. Se convirtieron al mismo
formato que los otros dos: un solo HTML por materia, con buscador, resaltador,
panel de notas y diagramas SVG propios (las 11 imágenes que había se redibujaron).
Las URLs viejas siguen vivas: `docs/redes/` y `docs/ebt/` son redirecciones.
EBT 2 y Ciencia de Datos se portaron después desde los repos de echepereza al
mismo formato, con sus figuras redibujadas sobre los tokens de cada materia.

## Cómo se arma

```
python3 fuentes/armar.py redes    # -> redes/index.html
python3 fuentes/armar.py ebt      # -> empresas-de-base-tecnologica/index.html
python3 fuentes/armar.py ebt2     # -> empresas-de-base-tecnologica-2/index.html
python3 fuentes/armar.py cdd      # -> ciencia-de-datos/index.html
```

- `fuentes/shell.html`: el cascarón compartido (CSS, buscador, notas, temas).
- `fuentes/materias.py`: lo único que cambia por materia (identidad, paleta,
  agrupación de capítulos). Agregar una materia es agregar una entrada.
- `fuentes/redes/`, `fuentes/ebt/`, `fuentes/ebt2/`, `fuentes/cdd/`: un
  fragmento HTML por capítulo.
- `fuentes/md/`: el markdown original, conservado como fuente.

Dos carpetas opcionales por materia extienden los fragmentos sin tocar el
build (hoy las usa EBT; cualquier materia puede sumarlas):

- `fuentes/<materia>/figuras/`: figuras generadas por script (gráficos con
  datos, tarjetas, tablas calculadas). Un fragmento las inserta con el
  marcador `<!--FIG:nombre-->` y `armar.py` inyecta
  `figuras/nombre.html` en ese lugar. Se generan con
  `fuentes/gen_figuras_<materia>.py` y el resultado va commiteado: el script
  se corre solo cuando se cambia una figura. Los SVG usan los alias de
  tokens del contrato (nada de colores fijos), así que heredan la paleta de
  la materia y el modo oscuro.
- `fuentes/<materia>/attachments/`: imágenes (PNG con nombre descriptivo).
  Los fragmentos las referencian como `<img src="img/nombre.png">` y el
  build copia a `<salida>/img/` solo las que se usan.

El build valida antes de escribir: ids únicos, anclas que resuelven, todo
`var(--token)` definido, cero recursos externos, cada `<!--FIG:-->` con su
archivo (sin colores hardcodeados y con SVG accesible) y cada `<img>` con su
archivo en `attachments/` (avisa si sobran). `fuentes/lint_fragmentos.py`
revisa cada fragmento contra `fuentes/contrato-fragmento.md`.

### PWA

Cada apunte es instalable y funciona offline. No hay nada que configurar por
materia: `armar.py` genera en cada build el `manifest.webmanifest` (identidad
y colores salen de `materias.py`), el `icon.svg` (mismo glifo que el favicon)
y el `sw.js`, que precachea el apunte completo. La versión del cache es el
hash del contenido: el service worker solo cambia cuando cambia algo, y ahí
el navegador renueva el cache en la visita siguiente.

Lo único que no genera el build son los PNG del ícono (los piden iOS y el
instalador de Chrome): los rasteriza `fuentes/gen_iconos.py` con ImageMagick
y van commiteados. Se corre una sola vez por materia nueva, o si cambia su
`favicon_hex`; el build falla avisando si faltan.

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

Está en todos los apuntes, incluido el de Aprendizaje Automático, que vive en
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

## Autores

Cada apunte firma al pie de su barra lateral: logo de GitHub y usuario,
enlazado al perfil. La portada no firma.

`fuentes/autoria.py` arma el bloque y lo inyecta, y es el mismo módulo en los
tres builders. Los autores van en la entrada de la materia, en
`fuentes/materias.py`:

```python
"autores": ["echepereza", "flopeztancredi"],
```

Si falta, el build falla. El usuario se valida contra el formato de GitHub
antes de entrar a la URL.

Se ordenan alfabéticamente al armar, así que da igual cómo se declaren: ninguno
es más autor que el otro. Si alguien le agrega algo a un resumen existente, se
suma a la lista.

En los otros dos repos: `AUTORES`, arriba de `fuentes/adaptar_estetica.py`
para Sistemas Distribuidos, y escrito en el HTML para Aprendizaje Automático,
que no tiene build.

## Colores

Cada materia tiene su acento, el mismo en la portada y en su apunte, en versión
clara y oscura. En la portada están inline en cada tarjeta de `index.html`
(`--c`, `--c-ink`, `--c-bg` para el tema claro, `--c-d` y `--c-d-bg` para el
oscuro); en los apuntes salen de la paleta de `fuentes/materias.py`.

Los contrastes están verificados contra WCAG AA en los dos temas: el par más
justo es el acento sobre la tarjeta en claro, con 4,65:1.
