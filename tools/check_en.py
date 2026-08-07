# -*- coding: utf-8 -*-
"""Detección de strings en español que no se tradujeron en la versión EN."""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
NB_EN = str(ROOT / "PZ_Colab_EN.ipynb")
nb = json.load(open(NB_EN, encoding="utf-8"))

# Palabras/claves típicas de la UI española
patrones = re.compile(
    r"(celda|ejecuta|ejecut|presiona|versi[oó]n|servidor|configur|archivo|puerto|contrase[nñ]a|"
    r"historial|guardad|guardar|descarg|crear|encontrad|encontró|encontrar|carpeta|memoria|"
    r"instalad|completad|fall[oó]|recuperad|generad|arranque|primer|aplicad|cambiad|actualiza|"
    r"encendid|activ[oa]|reinicio|reiniciar|mostrand|mostrar|enviand|enviar|intentand|se[ñn]al|"
    r"colecci[oó]n|l[íi]nea|ignorad|procesar|actuales|fallo|detect[oó]|conoces|limpiad|escribir|"
    r"reinicia|aplicar|menores|nota:|revisa|indicad|arriba|abajo|saves|somos|solo|uso|usa|"
    r"m[áa]s|d[éa]|puede|tendr[áa]s|asegura|todav[íi]a|nuev|borrar|casilla|pegues|pegad|"
    r"verificac|compatible|l[íi]mite|puedes|continuar|vuelvas|re-ejecuciones|reclamar|vincular)",
    re.IGNORECASE,
)

def check_cell(cell, path):
    if cell["cell_type"] != "code":
        return
    src = "".join(cell["source"])
    for i, line in enumerate(src.splitlines(), 1):
        s = line.strip()
        if s.startswith("#") or not s:
            continue
        # solo nos interesan strings literales dentro de print/abortar/comentarios @
        if ("@" not in s and "print" not in s and "abortar" not in s):
            continue
        if s.startswith("# @title") or s.startswith("# @markdown"):
            if patrones.search(s):
                print(f"{path}:{i} (ui): {s[:110]}")
            continue
        if patrones.search(s):
            print(f"{path}:{i}: {s[:110]}")

for cell in nb["cells"]:
    cid = cell["metadata"].get("id", "(md)")
    check_cell(cell, cid)

print("--- fin del chequeo (vacío = todo traducido) ---")
