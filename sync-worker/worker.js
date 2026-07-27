// Guarda bytes cifrados y nada mas.
//
// El cliente deriva de la frase del lector dos cosas distintas: la clave de
// cifrado y el identificador del registro. Este worker solo ve el
// identificador y un texto opaco. No hay cuentas, no hay sesiones, no hay
// forma de listar registros ajenos: hay que saber el identificador exacto,
// que son 128 bits derivados de una frase de 96 bits de entropia.
//
// Deploy: ver README.md, son tres comandos.

const ORIGENES = ['https://flopeztancredi.github.io'];
const MAX_BYTES = 512 * 1024;
const ID_VALIDO = /^[a-f0-9]{32}$/;
const UN_ANIO = 60 * 60 * 24 * 365;

function cabeceras(origen) {
  // Se refleja el origen solo si esta en la lista; si no, se responde con el
  // canonico, que hace que el navegador del que se cuelgue igual lo bloquee.
  const permitido = ORIGENES.includes(origen) ? origen : ORIGENES[0];
  return {
    'Access-Control-Allow-Origin': permitido,
    'Access-Control-Allow-Methods': 'GET, PUT, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
    'Vary': 'Origin',
  };
}

export default {
  async fetch(req, env) {
    const cors = cabeceras(req.headers.get('Origin') || '');

    if (req.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: cors });
    }

    const ruta = new URL(req.url).pathname.match(/^\/d\/([^/]+)$/);
    if (!ruta || !ID_VALIDO.test(ruta[1])) {
      return new Response('identificador invalido', { status: 400, headers: cors });
    }
    const clave = 'b:' + ruta[1];

    if (req.method === 'GET') {
      const valor = await env.DATOS.get(clave);
      if (valor === null) {
        return new Response('', { status: 404, headers: cors });
      }
      return new Response(valor, {
        status: 200,
        headers: { ...cors, 'Content-Type': 'text/plain', 'Cache-Control': 'no-store' },
      });
    }

    if (req.method === 'PUT') {
      const cuerpo = await req.text();
      if (cuerpo.length > MAX_BYTES) {
        return new Response('demasiado grande', { status: 413, headers: cors });
      }
      // Un anio de vida, y cada escritura lo renueva: los registros que nadie
      // vuelve a tocar se limpian solos en vez de acumularse para siempre.
      await env.DATOS.put(clave, cuerpo, { expirationTtl: UN_ANIO });
      return new Response(null, { status: 204, headers: cors });
    }

    return new Response('metodo no permitido', { status: 405, headers: cors });
  },
};
