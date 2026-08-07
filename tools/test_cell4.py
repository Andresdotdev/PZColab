# -*- coding: utf-8 -*-
"""Test funcional de la nueva Celda 4 (mods fáciles + colecciones)."""
import json
import os
import re
import sys
import tempfile
import zipfile
import types
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
NB = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "PZ_Colab_ES.ipynb")
ES = "EN" not in NB
print("Notebook:", NB, "(ES)" if ES else "(EN)")
nb = json.load(open(NB, encoding="utf-8"))
src = "".join("".join(c["source"]) for c in nb["cells"] if c["metadata"].get("id") == "cell-mods")

assert "!@param {type:\"raw\"}" not in src  # sanidad
assert "mods_input" in src and "collectionChildren" in src and "mod.info" in src

# --- Preparar entorno simulado ---
tmp = tempfile.mkdtemp(prefix="pzcolab_test_")
saves = os.path.join(tmp, "ZomboidSaves")
server = os.path.join(tmp, "pzserver")
os.makedirs(saves, exist_ok=True)
os.makedirs(server, exist_ok=True)

with open(os.path.join(saves, ".pzcolab_state.json"), "w") as f:
    json.dump({"version": "b42 estable" if ES else "b42 stable", "server_name": "PzColab"}, f)

WS = os.path.join(server, "steamapps", "workshop", "content", "108600")
os.makedirs(WS, exist_ok=True)

# item 2902678 con mods/hydrocraft/mod.info
item1 = os.path.join(WS, "2902678", "mods", "hydrocraft")
os.makedirs(item1)
with open(os.path.join(item1, "mod.info"), "w", encoding="utf-8") as f:
    f.write("id=hydrocraft\nname=Hydrocraft - Big Crafting Overhaul\nposter=poster.png\n")

# item 12345 como zip con mod.info dentro
item2 = os.path.join(WS, "12345")
os.makedirs(item2)
with zipfile.ZipFile(os.path.join(item2, "mod.zip"), "w") as z:
    z.writestr("mod.info", "id=tsarslib\nname=Tsar's Common Library\n")

# item 9999: colección (HTML simulado)
item3 = os.path.join(WS, "9999")
os.makedirs(item3)
with open(os.path.join(item3, "mod.info"), "w") as f:
    f.write("id=colection\nname=Fake Collection\n")

INI = os.path.join(saves, "Server", "PzColab.ini")
os.makedirs(os.path.dirname(INI), exist_ok=True)
with open(INI, "w") as f:
    f.write("Port=16261\nWorkshopItems=1111\nMods=\\oldmod\nPauseOnEmpty=true\n")

# --- Fake requests para las colecciones ---
def fake_requests_get(url, headers=None, timeout=None):
    r = types.SimpleNamespace()
    if "id=9999" in url and "insideModal" in url:
        r.status_code = 200
        r.text = '<div class="collectionChildren"><a href="https://steamcommunity.com/sharedfiles/filedetails/?id=2902678"></a><a href="https://steamcommunity.com/sharedfiles/filedetails/?id=12345"></a></div>'
    elif "id=9999" in url:
        r.status_code = 200
        r.text = '<div class="collectionChildren"></div>'
    else:
        r.status_code = 200
        r.text = "<html>normal mod page</html>"
    return r

fake_requests = types.ModuleType("requests")
fake_requests.get = fake_requests_get
sys.modules["requests"] = fake_requests

# Fake subprocess: simula la descarga de steamcmd creando la carpeta del item
def fake_subprocess_run(cmd, **kwargs):
    wsid = cmd[cmd.index("108600") + 1]
    carpeta = os.path.join(WS, wsid)
    os.makedirs(carpeta, exist_ok=True)
    with open(os.path.join(carpeta, ".downloaded"), "w") as f:
        f.write("ok")
    return types.SimpleNamespace(returncode=0)

fake_subprocess = types.ModuleType("subprocess")
fake_subprocess.run = fake_subprocess_run
fake_subprocess.DEVNULL = -3
sys.modules["subprocess"] = fake_subprocess

# --- Preparar el código de la celda para inyectar parámetros de test ---
code = src.replace('mods_input = ""', "mods_input = _INPUT")
vars_params = (["Limpiar_Lista_Anterior", "Descargar_Mods"] if ES else ["clear_previous_list", "download_mods"])
for var in vars_params:
    code = code.replace(var, "_LIMP" if "clear" in var or "Limpiar" in var else "_DESC")
code = code.replace("_LIMP = False", "_LIMP = _LIMP")
code = code.replace("_DESC = True", "_DESC = _DESC")
code = code.replace("'/content/drive/MyDrive/ZomboidSaves'", "r'" + saves.replace("\\", "/") + "'")
code = code.replace("'/content/pzserver'", "r'" + server.replace("\\", "/") + "'")

ns = {}

def correr(input_, limpiar=False, descargar=True):
    ns.clear()
    ns["_INPUT"] = input_
    ns["_LIMP"] = limpiar
    ns["_DESC"] = descargar
    exec(compile(code, "cell-mods", "exec"), ns)

# ============ ESCENARIO A: mod individual + fallback manual + historial (b42) ============
correr("https://steamcommunity.com/sharedfiles/filedetails/?id=2902678\n2861456062|manualmod\nlinea-basura")

ini = open(INI).read()
assert "WorkshopItems=2902678;2861456062;1111" in ini, f"INI ws erróneo:\n{ini}"
assert "Mods=\\hydrocraft;\\manualmod;\\oldmod" in ini, f"INI mods erróneo:\n{ini}"
print("A1 OK: merge dedup + formato b42 (\\id) + fallback manual + historial")
assert "linea-basura" not in ns.get("salida", "")

# ============ ESCENARIO B: colección se expande (con zip) ============
correr("https://steamcommunity.com/sharedfiles/filedetails/?id=9999")
ini = open(INI).read()
assert "WorkshopItems=12345;2902678" in ini, f"Colección no expandida:\n{ini}"
assert "Mods=\\tsarslib;\\hydrocraft" in ini, f"mods de colección erróneos:\n{ini}"
print("B1 OK: colección expandida + Mod ID detectado dentro de ZIP + orden lib primero")

# ============ ESCENARIO C: b41 legacy (sin backslash) ============
with open(os.path.join(saves, ".pzcolab_state.json"), "w") as f:
    json.dump({"version": "b41 legacy", "server_name": "PzColab"}, f)
with open(INI, "w") as f:
    f.write("WorkshopItems=1111\nMods=oldmod\n")
correr("2902678")
ini = open(INI).read()
assert "Mods=hydrocraft;oldmod" in ini and "\\hydrocraft" not in ini, f"b41 erróneo:\n{ini}"
print("C1 OK: formato b41 sin backslash")

# ============ ESCENARIO D: limpiar historial ============
correr("2902678", limpiar=True)
ini = open(INI).read()
assert "1111" not in ini and "oldmod" not in ini, f"historial no limpiado:\n{ini}"
print("D1 OK: Limpiar_Lista_Anterior funciona")

# ============ ESCENARIO E: extraer_id unitario ============
ns.clear()
ns["re"] = re
exec(compile("def extraer_id(linea):\n"
             "    linea = linea.strip()\n"
             "    if not linea:\n        return None\n"
             "    manual = None\n"
             "    if '|' in linea:\n        linea, _, manual = linea.partition('|')\n"
             "        linea = linea.strip(); manual = manual.strip() or None\n"
             "    m = re.search(r'id=(\\d+)', linea) or re.search(r'(\\d{5,})', linea)\n"
             "    if not m:\n        return None\n"
             "    return (m.group(1), manual)\n", "unit", "exec"), ns)
f = ns["extraer_id"]
assert f("https://steamcommunity.com/sharedfiles/filedetails/?id=2902678") == ("2902678", None)
assert f("2861456062") == ("2861456062", None)
assert f("https://steamcommunity.com/sharedfiles/filedetails/?id=2750177123|mycustommod") == ("2750177123", "mycustommod")
assert f("") is None and f("cosas raras") is None
print("E1 OK: extraer_id cubre URL, número, fallback manual y basura")

print("\n✅ TODOS LOS ESCENARIOS PASARON")
