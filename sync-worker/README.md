# Endpoint de sincronización

Guarda los datos de sync de los apuntes. Es lo mínimo posible: un `GET` y un
`PUT` sobre un identificador, con el cuerpo opaco.

**No ve el contenido.** El navegador deriva de la frase del lector dos cosas
distintas, con derivaciones independientes: la clave de cifrado y el
identificador del registro. Acá llega el identificador y un blob AES-GCM. No hay
cuentas, ni sesiones, ni forma de listar registros ajenos.

## Estado

Desplegado en **https://apuntes-sync.flopeztancredi.workers.dev**, cuenta
`b363001b04e9e88b1c6e64566df1bf6e`, namespace KV `DATOS`
(`7486e87fdd7d48baab2bc6c246d5b271`). Esa URL ya está en `ENDPOINT`, en
`fuentes/sync.html`.

## Volver a desplegar

Tres comandos:

```
npx wrangler login
npx wrangler kv namespace create DATOS
npx wrangler deploy
```

El segundo imprime un `id`: copialo a `wrangler.toml`, en `kv_namespaces`, antes
de correr el tercero.

Si cambiara la URL, va en `fuentes/sync.html`, en la constante `ENDPOINT`, y
después se rearman los apuntes:

```
python3 fuentes/armar.py
python3 ../distribuidos/apunte/fuentes/adaptar_estetica.py
```

## Límites

El plan gratuito da 100.000 pedidos por día y 1 GB en KV. Cada lector hace unos
pocos pedidos por sesión y su registro pesa kilobytes, así que no se acerca ni
de lejos.

Los registros vencen al año y cada escritura renueva el plazo: lo que nadie
vuelve a abrir se limpia solo.

## Probarlo sin desplegar

```
npx wrangler dev
curl -X PUT --data 'hola' http://localhost:8787/d/00000000000000000000000000000000
curl http://localhost:8787/d/00000000000000000000000000000000
```
