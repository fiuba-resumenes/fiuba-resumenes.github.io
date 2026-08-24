"""Configuracion por materia para armar.py.

Cada apunte comparte el shell y el vocabulario de fragmentos; lo unico que
cambia es lo de aca: identidad, paleta y como se agrupan los capitulos.
Agregar una materia es agregar una entrada, no copiar el script.

La paleta usa los mismos nombres de token que el shell, asi que su CSS
funciona sin tocarlo. Los neutros (ink) se mantienen parejos entre materias;
lo que cambia es el acento y el tinte del fondo, para que cada apunte se
reconozca de un vistazo sin dejar de ser la misma familia.

"autores" son usuarios de GitHub, uno o varios. Sin eso el build falla. El
orden no importa: se ordenan alfabeticamente al armar.
"""

REDES = {
    "clave": "redes",
    "autores": ["echepereza", "flopeztancredi"],
    "salida": "redes/index.html",
    "prefijo_ls": "rd",          # namespace de localStorage
    "titulo_tab": "Redes (75.43) - Apunte completo",
    "marca": "Redes",
    "h1": "Redes",
    "hero": ("Apunte de la materia 75.43 (FIUBA) sobre Kurose y Ross: de la "
             "arquitectura de Internet a la capa de red, con los mecanismos "
             "explicados de punta a punta."),
    "descripcion": "Apunte completo de Redes (75.43, FIUBA).",
    "theme_color": "#a06520",
    "favicon_hex": "a06520",
    "grupos": [
        ("Fundamentos", [
            ("r01", "01", "Internet, borde, núcleo y retardos"),
        ]),
        ("Capas", [
            ("r02", "02", "Capa de aplicación"),
            ("r03", "03", "Capa de transporte"),
            ("r04", "04", "Capa de red: plano de datos"),
        ]),
        ("Para el final", [
            ("r99", "R", "Resumen integrador"),
        ]),
    ],
    "paleta_light": """:root {
      color-scheme: light;
      --bg: #fdf9f3;
      --surface: #ffffff;
      --surface-2: #f7efe2;
      --ink: #2b2318;
      --muted: #736750;
      --line: #ece0cd;
      --accent: #a06520;
      --accent-2: #fbf0df;
      --accent-ink: #7a4a12;
      --warm: #96591c;
      --warm-bg: #fdf2e1;
      --danger: #a63a56;
      --danger-bg: #fdebf0;
      --blue: #276b93;
      --blue-bg: #e6f2f8;
      --ok: #35704a;
      --ok-bg: #e9f5ec;
      --exam: #a83a7d;
      --exam-bg: #fceaf4;
      --hl-yellow: #ffe08a;
      --hl-mint: #a8e6c8;
      --hl-pink: #ffc1d2;
      --hl-blue: #cdc4ff;
      --shadow: 0 18px 55px rgba(88, 62, 25, .09);
      --radius: 18px;
      --sidebar: 292px;
    }""",
    "paleta_dark": """html[data-theme="dark"] {
      color-scheme: dark;
      --bg: #1a1610;
      --surface: #241f17;
      --surface-2: #302819;
      --ink: #faf5ec;
      --muted: #bdb098;
      --line: #453a27;
      --accent: #f0b766;
      --accent-2: #3b2c19;
      --accent-ink: #ffe3bb;
      --warm: #f0b766;
      --warm-bg: #3b2c19;
      --danger: #f097ad;
      --danger-bg: #3f2029;
      --blue: #7ec8e8;
      --blue-bg: #16323f;
      --ok: #86cf9b;
      --ok-bg: #1a2f21;
      --exam: #e79ac9;
      --exam-bg: #3a1f31;
      --hl-yellow: #6f5a18;
      --hl-mint: #1f5c40;
      --hl-pink: #6e3549;
      --hl-blue: #443577;
      --shadow: 0 18px 55px rgba(0, 0, 0, .3);
    }""",
}

EBT = {
    "clave": "ebt",
    "autores": ["echepereza", "flopeztancredi"],
    # La URL escribe el nombre entero, como las otras tres. /ebt/ queda como
    # redireccion. El prefijo de localStorage sigue siendo "ebt" a proposito:
    # es el mismo origen, asi que mover la ruta no le borra las notas a nadie.
    "salida": "empresas-de-base-tecnologica/index.html",
    "prefijo_ls": "ebt",
    "titulo_tab": "Empresas de Base Tecnológica 1 - Apunte completo",
    "marca": "Empresas de Base Tecnológica",
    # nombre bajo el icono al instalar la PWA (opcional, si "marca" es larga)
    "nombre_corto": "EBT 1",
    "h1": "Empresas de Base Tecnológica",
    "hero": ("Apunte de EBT 1 (FIUBA), las dos mitades de la materia: economía "
             "(valor, contabilidad, finanzas y evaluación de proyectos) y "
             "derecho (vínculos jurídicos, contratos, sociedades y regímenes)."),
    "descripcion": "Apunte completo de Empresas de Base Tecnológica 1 (FIUBA).",
    "theme_color": "#33704b",
    "favicon_hex": "33704b",
    # Los uids no son correlativos con el numero de display: e11 y e12 llegaron
    # despues (merge con el apunte de echepereza) y las notas de los lectores
    # viven en localStorage bajo el uid, asi que renumerar uids las borraria.
    "grupos": [
        ("Economía", [
            ("e01", "01", "Contexto y conceptos económicos"),
            ("e02", "02", "Valor y cadena de valor"),
            ("e03", "03", "Contabilidad"),
            ("e04", "04", "Finanzas y valor tiempo del dinero"),
            ("e05", "05", "Evaluación de proyectos"),
            ("e11", "06", "Costos y rentabilidad"),
        ]),
        ("Derecho", [
            ("e06", "07", "Derecho: conceptos y ramas"),
            ("e07", "08", "Vínculos y actos jurídicos"),
            ("e08", "09", "Contratos"),
            ("e09", "10", "Sociedades"),
            ("e10", "11", "Regímenes de promoción"),
            ("e12", "12", "Derecho laboral"),
        ]),
        ("Para el final", [
            ("e98", "R", "Repaso final y machete"),
            ("e99", "P", "Ejercicios resueltos"),
        ]),
    ],
    "paleta_light": """:root {
      color-scheme: light;
      --bg: #f6fbf7;
      --surface: #ffffff;
      --surface-2: #eaf4ed;
      --ink: #1c2a21;
      --muted: #5c6f63;
      --line: #d9e9de;
      --accent: #33704b;
      --accent-2: #e5f3ea;
      --accent-ink: #24563a;
      --warm: #96591c;
      --warm-bg: #fdf2e1;
      --danger: #a63a56;
      --danger-bg: #fdebf0;
      --blue: #276b93;
      --blue-bg: #e6f2f8;
      --ok: #35704a;
      --ok-bg: #e9f5ec;
      --exam: #a83a7d;
      --exam-bg: #fceaf4;
      --hl-yellow: #ffe08a;
      --hl-mint: #a8e6c8;
      --hl-pink: #ffc1d2;
      --hl-blue: #cdc4ff;
      --shadow: 0 18px 55px rgba(24, 60, 38, .08);
      --radius: 18px;
      --sidebar: 292px;
    }""",
    "paleta_dark": """html[data-theme="dark"] {
      color-scheme: dark;
      --bg: #111a14;
      --surface: #19241d;
      --surface-2: #223026;
      --ink: #eef7f1;
      --muted: #9fb3a7;
      --line: #2f4237;
      --accent: #86cf9b;
      --accent-2: #1a2f21;
      --accent-ink: #d5f0de;
      --warm: #f0b766;
      --warm-bg: #3b2c19;
      --danger: #f097ad;
      --danger-bg: #3f2029;
      --blue: #7ec8e8;
      --blue-bg: #16323f;
      --ok: #86cf9b;
      --ok-bg: #1a2f21;
      --exam: #e79ac9;
      --exam-bg: #3a1f31;
      --hl-yellow: #6f5a18;
      --hl-mint: #1f5c40;
      --hl-pink: #6e3549;
      --hl-blue: #443577;
      --shadow: 0 18px 55px rgba(0, 0, 0, .3);
    }""",
}

MATERIAS = {"redes": REDES, "ebt": EBT}
