# FIUBA Resúmenes

Apuntes de Ingeniería en Informática (FIUBA), de varios autores y abiertos a
contribuciones: **https://fiuba-resumenes.github.io**

Este repo es solo la portada (`index.html`) y las redirecciones legacy. Cada
materia vive en su propio repo bajo el org
[fiuba-resumenes](https://github.com/fiuba-resumenes), servido como GitHub
Pages "project site" en `fiuba-resumenes.github.io/<materia>/` (mismo
dominio, otro repo: no hace falta ni tocar `sync-worker/`). Todos comparten
el mismo motor de armado, [fiuba-resumenes/motor](https://github.com/fiuba-resumenes/motor).

Sitio estático puro, sin Jekyll (`.nojekyll`). Todo lo que se publica es HTML
autocontenido: sin build en el servidor, sin dependencias, sin CDN.

## Qué hay

| materia | se lee en | vive en | lo escribió |
|---|---|---|---|
| Redes (75.43) | [/redes](https://fiuba-resumenes.github.io/redes/) | repo [redes](https://github.com/fiuba-resumenes/redes) | echepereza, flopeztancredi |
| Empresas de Base Tecnológica 1 | [/empresas-de-base-tecnologica](https://fiuba-resumenes.github.io/empresas-de-base-tecnologica/) | repo [empresas-de-base-tecnologica](https://github.com/fiuba-resumenes/empresas-de-base-tecnologica) | echepereza, flopeztancredi |
| Empresas de Base Tecnológica 2 | [/empresas-de-base-tecnologica-2](https://fiuba-resumenes.github.io/empresas-de-base-tecnologica-2/) | repo [empresas-de-base-tecnologica-2](https://github.com/fiuba-resumenes/empresas-de-base-tecnologica-2) | echepereza, flopeztancredi |
| Ciencia de Datos | [/ciencia-de-datos](https://fiuba-resumenes.github.io/ciencia-de-datos/) | repo [ciencia-de-datos](https://github.com/fiuba-resumenes/ciencia-de-datos) | echepereza, flopeztancredi |
| Sistemas Distribuidos (75.74) | [/sistemas-distribuidos](https://fiuba-resumenes.github.io/sistemas-distribuidos/) | repo [sistemas-distribuidos](https://github.com/fiuba-resumenes/sistemas-distribuidos) | flopeztancredi |
| Aprendizaje Automático (75.06) | [/aprendizaje-automatico](https://fiuba-resumenes.github.io/aprendizaje-automatico/) | repo [aprendizaje-automatico](https://github.com/fiuba-resumenes/aprendizaje-automatico) | flopeztancredi |
| Programación Concurrente | [echepereza.github.io/programacion-concurrente](https://echepereza.github.io/programacion-concurrente/) | repo [programacion-concurrente](https://github.com/echepereza/programacion-concurrente) | echepereza |

Todas las materias salvo Programación Concurrente ya están bajo el org.
Sistemas Distribuidos ya usa el motor compartido; a Aprendizaje Automático
le falta convertir su HTML monolítico a fragmentos. Redes y EBT eran
markdown servido con just-the-docs; las URLs viejas siguen vivas,
`docs/redes/` y `docs/ebt/` (y `/ebt/`) redirigen. Las URLs viejas de
Sistemas Distribuidos y Aprendizaje Automático en `flopeztancredi.github.io`
también redirigen, con una banda que pide sincronizar las notas antes de
pasarse.

## Cómo contribuir a una materia

Cada repo de materia trae su propio `README.md` con los pasos exactos. En
general: fragmentos HTML según el contrato del motor
([contrato-fragmento.md](https://github.com/fiuba-resumenes/motor/blob/main/motor_apuntes/contrato-fragmento.md)),
`pip install -r requirements.txt`, `python3 armar.py`, commitear fragmento y
output juntos. El CI de cada repo revisa que coincidan.

## El motor compartido

[fiuba-resumenes/motor](https://github.com/fiuba-resumenes/motor) es un
paquete Python versionado (instalable con
`pip install "motor-apuntes @ git+https://github.com/fiuba-resumenes/motor@vX.Y.Z"`)
del que depende cada repo de materia, con una versión fija. Arma el apunte
sobre un shell compartido (búsqueda, resaltador, notas, tema oscuro,
sincronización entre dispositivos), genera la PWA (manifest, service worker,
íconos) y valida el contrato de fragmentos. Una mejora ahí no rompe todas
las materias de un día para el otro: cada repo sube el pin cuando quiere.

## Sincronizar entre dispositivos

Cada apunte agrega un botón "Sincronizar" al panel lateral. **Sin cuenta ni
login**, modelo tipo Brave: una frase de 12 palabras es identidad y clave a
la vez. El endpoint (`sync-worker/`, un Worker de Cloudflare) solo ve un
identificador y un blob cifrado: no puede leer nada. El que no configura
nada sigue con todo en localStorage del dispositivo.

Ver `sync-worker/README.md` para desplegarlo o cambiar los orígenes
permitidos (CORS).

## Colores

Cada materia tiene su acento, el mismo en la portada y en su apunte, en
versión clara y oscura. En la portada están inline en cada tarjeta de
`index.html` (`--c`, `--c-ink`, `--c-bg` para el tema claro, `--c-d` y
`--c-d-bg` para el oscuro); en cada apunte salen de la paleta declarada en
su propio repo.

Los contrastes están verificados contra WCAG AA en los dos temas.
