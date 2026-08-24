#!/usr/bin/env python3
"""Rasteriza los iconos PNG de la PWA de cada materia.

armar.py genera en cada build todo lo que es texto (icon.svg, manifest,
sw.js), pero los PNG que piden iOS y el instalador de Chrome necesitan
ImageMagick, y el build no debe depender de herramientas externas: se
rasterizan aca UNA vez y van commiteados (armar.py solo valida que existan).
Correr de nuevo solo si cambia favicon_hex de una materia o el glifo.

Uso:
    python3 gen_iconos.py           # todas las materias
    python3 gen_iconos.py ebt       # una sola
"""
import subprocess
import sys
from pathlib import Path

from armar import REPO, icono_svg
from materias import MATERIAS

# apple-touch-icon: iOS no aplica mascara, pero el fondo a sangre completa
# del icono ya lo deja opaco y cuadrado, que es lo que espera.
TAMANOS = {"icon-192.png": 192, "icon-512.png": 512, "apple-touch-icon.png": 180}


def main(argv) -> int:
    claves = argv or list(MATERIAS)
    malas = [c for c in claves if c not in MATERIAS]
    if malas:
        print(f"!! materia desconocida: {malas}. Hay: {list(MATERIAS)}",
              file=sys.stderr)
        return 1
    for clave in claves:
        cfg = MATERIAS[clave]
        out_dir = (REPO / cfg["salida"]).parent
        out_dir.mkdir(parents=True, exist_ok=True)
        svg = out_dir / "icon.svg"
        svg.write_text(icono_svg(cfg["favicon_hex"]), encoding="utf-8")
        for nombre, lado in TAMANOS.items():
            # densidad para que el SVG (viewBox de 64 a 96 dpi) se renderice
            # ya al tamano final, sin reescalar un raster chico
            subprocess.run(
                ["magick", "-background", "none",
                 "-density", str(lado * 96 // 64), str(svg),
                 "-resize", f"{lado}x{lado}", str(out_dir / nombre)],
                check=True)
            print(f"{out_dir.relative_to(REPO)}/{nombre}: {lado}x{lado}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
