# -*- coding: utf-8 -*-
"""Test funcional de la nueva Celda 4 (mods fáciles + colecciones)."""
import contextlib
import io
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

# item 556677: mod "b42-only" (para test de compatibilidad)
item_f = os.path.join(WS, "556677", "mods", "coolmod")
os.makedirs(item_f)
with open(os.path.join(item_f, "mod.info"), "w", encoding="utf-8") as f:
    f.write("id=coolmod\nname=Cool Mod\n")

# item 556678: mod con dependencia requerida que NO está en la lista
item_g = os.path.join(WS, "556678", "mods", "gmod")
os.makedirs(item_g)
with open(os.path.join(item_g, "mod.info"), "w", encoding="utf-8") as f:
    f.write("id=gmod\nname=G Mod\nrequire=otromod\n")

# item 556680: mod (b42) que requiere ZombieBuddy con backslash
item_h = os.path.join(WS, "556680", "mods", "zbmod")
os.makedirs(item_h)
with open(os.path.join(item_h, "mod.info"), "w", encoding="utf-8") as f:
    f.write("id=zbmod\nname=ZB Mod\nrequire=\\ZombieBuddy\n")

# item 556681: mod (b42) con require genérico con backslash (\otromod)
item_h3 = os.path.join(WS, "556681", "mods", "zbmod2")
os.makedirs(item_h3)
with open(os.path.join(item_h3, "mod.info"), "w", encoding="utf-8") as f:
    f.write("id=zbmod2\nname=ZB Mod 2\nrequire=\\otromod\n")

# NOTA: item 556679 (otromod) NO se crea aquí; el fake_subprocess_run lo crea
# al simular la descarga via steamcmd, para testear la auto-descarga de deps.

INI = os.path.join(saves, "Server", "PzColab.ini")
os.makedirs(os.path.dirname(INI), exist_ok=True)
with open(INI, "w") as f:
    f.write("Port=16261\nWorkshopItems=1111\nMods=\\oldmod\nPauseOnEmpty=true\n")

# --- Fake requests para las colecciones + compatibilidad ---
def fake_requests_get(url, headers=None, timeout=None):
    r = types.SimpleNamespace()
    if "id=9999" in url and "insideModal" in url:
        r.status_code = 200
        r.text = '<div class="collectionChildren"><a href="https://steamcommunity.com/sharedfiles/filedetails/?id=2902678"></a><a href="https://steamcommunity.com/sharedfiles/filedetails/?id=12345"></a></div>'
    elif "id=9999" in url:
        r.status_code = 200
        r.text = '<div class="collectionChildren"></div>'
    elif "id=556677" in url:
        r.status_code = 200
        r.text = '<div class="workshopItemTitle">Cool Mod</div><div class="workshopItemDescription">This mod requires Build 42!</div>'
    elif "searchText=otromod" in url or "search_text=otromod" in url:
        r.status_code = 200
        r.text = '<div class="collectionChildren"></div><a href="https://steamcommunity.com/sharedfiles/filedetails/?id=556679">Otro Mod</a>'
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
    # Simular contenido del workshop item 556679 (otromod) al ser descargado
    if wsid == "556679":
        sub = os.path.join(carpeta, "mods", "otromod")
        os.makedirs(sub, exist_ok=True)
        with open(os.path.join(sub, "mod.info"), "w", encoding="utf-8") as f:
            f.write("id=otromod\nname=Otro Mod\n")
    # Simular contenido del item de ZombieBuddy (framework Java, WSID fijo)
    if wsid == "3619862853":
        sub = os.path.join(carpeta, "mods", "zombiebuddy")
        os.makedirs(sub, exist_ok=True)
        with open(os.path.join(sub, "mod.info"), "w", encoding="utf-8") as f:
            f.write("id=ZombieBuddy\nname=ZombieBuddy\n")
    return types.SimpleNamespace(returncode=0)

fake_subprocess = types.ModuleType("subprocess")
fake_subprocess.run = fake_subprocess_run
fake_subprocess.DEVNULL = -3
sys.modules["subprocess"] = fake_subprocess

# --- Preparar el código de la celda para inyectar parámetros de test ---
code = src.replace('mods_input = ""', "mods_input = _INPUT")
vars_params = (["Limpiar_Lista_Anterior", "Descargar_Mods", "Descargar_Dependencias", "Incluir_ZombieBuddy"] if ES else ["clear_previous_list", "download_mods", "resolve_dependencies", "include_zombie_buddy"])
for var in vars_params:
    code = code.replace(var, "_LIMP" if "clear" in var or "Limpiar" in var else "_DESC" if "download" in var or "Descargar_Mods" in var else "_ZB" if "zombie" in var.lower() else "_DEP")
code = code.replace("_LIMP = False", "_LIMP = _LIMP")
code = code.replace("_DESC = True", "_DESC = _DESC")
code = code.replace("_DEP = True", "_DEP = _DEP")
code = code.replace("_ZB = False", "_ZB = _ZB")
code = code.replace("'/content/drive/MyDrive/ZomboidSaves'", "r'" + saves.replace("\\", "/") + "'")
code = code.replace("'/content/pzserver'", "r'" + server.replace("\\", "/") + "'")

ns = {}

def correr(input_, limpiar=False, descargar=True, deps=True, zb=False):
    ns.clear()
    ns["_INPUT"] = input_
    ns["_LIMP"] = limpiar
    ns["_DESC"] = descargar
    ns["_DEP"] = deps
    ns["_ZB"] = zb
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(code, "cell-mods", "exec"), ns)
    return buf.getvalue()

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

# ============ ESCENARIO F: compatibilidad de versión (b41 vs página b42) ============
# el estado quedó en b41 legacy desde el escenario C
aviso_compat = "POSIBLES INCOMPATIBILIDADES" if ES else "POSSIBLE VERSION INCOMPATIBILITIES"
out = correr("556677")
assert aviso_compat in out, f"sin aviso de compatibilidad:\n{out}"
assert "Build 42" in out, f"el motivo no menciona Build 42:\n{out}"
assert "coolmod" in open(INI).read()
print("F1 OK: aviso de compatibilidad heurístico (página b42 + servidor b41)")

# unit test de analizar_compatibilidad
ns.clear()
ns["re"] = re
ns["is_b42"] = False
exec(compile("def analizar_compatibilidad(pagina):\n"
             "    if not pagina:\n        return None\n"
             "    txt = pagina.lower()\n"
             "    marca41 = bool(re.search(r'\\bb41\\b|build\\s*41', txt))\n"
             "    marca42 = bool(re.search(r'\\bb42\\b|build\\s*42|42\\.\\d', txt))\n"
             "    if marca41 and marca42:\n        return None\n"
             "    if marca42 and not is_b42:\n        return 'conflicto b42'\n"
             "    if marca41 and is_b42:\n        return 'conflicto b41'\n"
             "    return None\n", "unit", "exec"), ns)
ac = ns["analizar_compatibilidad"]
assert ac("<html>Build 42 only</html>") == "conflicto b42"
assert ac("<html>works on b41 and b42</html>") is None
assert ac("<html>no markers</html>") is None
ns["is_b42"] = True
assert ac("<html>Build 41 legacy</html>") == "conflicto b41"
print("F2 OK: analizar_compatibilidad unitario (b41, b42, ambos, ninguno)")

# ============ ESCENARIO G: dependencias requeridas (require= en mod.info) ============
# G1: auto-descarga de la dependencia "otromod" (requerida por gmod) vía Workshop
aviso_resolviendo = "Resolviendo dependencias" if ES else "Resolving missing dependencies"
aviso_deps = "DEPENDENCIAS FALTANTES" if ES else "MISSING DEPENDENCIES"
out = correr("556678", deps=True)
assert aviso_resolviendo in out, f"sin reporte de resolucion de deps:\n{out}"
assert "otromod -> Workshop 556679" in out, f"no resolvio otromod:\n{out}"
ini = open(INI).read()
assert "otromod" in ini.replace("\\", ""), f"otromod no fue agregado al ini:\n{ini}"
assert aviso_deps not in out, f"no deberia haber faltantes tras auto-descarga:\n{out}"
print("G1 OK: dependencia autodescargada desde Workshop y añadida al .ini (sin faltantes)")

# G2: con Desccargar_Dependencias=False, la dependencia sale como faltante -> fallback a reporte
# Reset de estado: borrar otromod del ini y del filesystem para simular "no descargado"
with open(INI, "w") as f:
    f.write("Port=16261\nWorkshopItems=556678;1111\nMods=\\gmod;\\oldmod\nPauseOnEmpty=true\n")
import shutil
dep_root = os.path.join(WS, "556679")
if os.path.isdir(dep_root):
    shutil.rmtree(dep_root)
out = correr("556678", deps=False)
assert aviso_deps in out, f"sin aviso de faltantes (modo deps=False):\n{out}"
assert "otromod" in out, f"no menciona la dependencia faltante:\n{out}"
print("G2 OK: con deps=False, dependencia faltante reportada (fallback manual)")

# ============ ESCENARIO H: ZombieBuddy (framework Java) ============
zb_req_msg = "ZOMBIEBUDDY REQUERIDO" if ES else "ZOMBIEBUDDY REQUIRED"
zb_on_msg = "ZOMBIEBUDDY ACTIVO" if ES else "ZOMBIEBUDDY ACTIVE"
ZB_WSID = "3619862853"
dep_zb = os.path.join(WS, ZB_WSID)

# H1: check ON -> WSID fijo (sin búsqueda web), descargado, en el .ini y aviso con links
with open(INI, "w") as f:
    f.write("Port=16261\nWorkshopItems=556680;1111\nMods=\\zbmod;\\oldmod\nPauseOnEmpty=true\n")
if os.path.isdir(dep_zb):
    shutil.rmtree(dep_zb)
out = correr("556680", deps=True, zb=True)
assert "ZombieBuddy -> Workshop " + ZB_WSID in out, f"no usó el WSID fijo de ZombieBuddy:\n{out}"
ini = open(INI).read()
assert ZB_WSID in ini, f"ZombieBuddy no fue agregado al ini:\n{ini}"
assert "ZombieBuddy" in ini.replace("\\", ""), f"Mod ID ZombieBuddy ausente:\n{ini}"
assert zb_on_msg in out, f"sin aviso ZOMBIEBUDDY ACTIVO:\n{out}"
assert "windows_installer" in out and "#zombiebuddy" in out, f"faltan links de instalación:\n{out}"
print("H1 OK: check ON -> require=\\ZombieBuddy resuelto con WSID fijo + Mods/.ini + links")

# H2: check OFF -> no se agrega nada y se avisa cómo activarlo
with open(INI, "w") as f:
    f.write("Port=16261\nWorkshopItems=556680;1111\nMods=\\zbmod;\\oldmod\nPauseOnEmpty=true\n")
if os.path.isdir(dep_zb):
    shutil.rmtree(dep_zb)
out = correr("556680", deps=True, zb=False)
assert zb_req_msg in out, f"sin aviso de ZombieBuddy requerido:\n{out}"
assert ZB_WSID not in open(INI).read(), f"no debía agregarse ZombieBuddy con el check OFF:\n{open(INI).read()}"
print("H2 OK: check OFF -> no se agrega y se indica activar la casilla")

# H3: require genérico con backslash b42 (\otromod) también se resuelve
out = correr("556681", deps=True, zb=False)
assert "otromod -> Workshop 556679" in out, f"no se resolvió require con backslash:\n{out}"
print("H3 OK: require=\\otromod (backslash b42) resuelto vía Workshop")

print("\n✅ TODOS LOS ESCENARIOS PASARON")
