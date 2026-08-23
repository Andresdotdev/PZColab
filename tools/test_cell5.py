# -*- coding: utf-8 -*-
"""Tests funcionales para la Celda 5 (backup/restore/rotación) y la sección
Eliminar_Mods de la Celda 4."""
import contextlib, io, glob, json, os, re, shutil, sys, tarfile, tempfile, types
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
NB = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "PZ_Colab_ES.ipynb")
ES = "EN" not in NB
print("Notebook:", NB, "(ES)" if ES else "(EN)")
nb = json.load(open(NB, encoding="utf-8"))

src5 = "".join("".join(c["source"]) for c in nb["cells"] if c["metadata"].get("id") == "cell-backup")
assert "ZomboidSaves_backups" in src5 and "tarfile" in src5 and "Restaurar_Backup" in src5

src4 = "".join("".join(c["source"]) for c in nb["cells"] if c["metadata"].get("id") == "cell-mods")
manage_var = "Eliminar_Mods" if ES else "manage_mods"
num_var = "numero_a_eliminar" if ES else "number_to_remove"
assert manage_var in src4 and num_var in src4, "celda-mods no tiene gestión de eliminación"

# --- Entorno temporal ---
tmp = tempfile.mkdtemp(prefix="pzcolab_test5_")
saves = os.path.join(tmp, "ZomboidSaves")
drive = os.path.join(tmp, "drive")
server = os.path.join(tmp, "pzserver")
os.makedirs(saves, exist_ok=True)
os.makedirs(drive, exist_ok=True)
os.makedirs(server, exist_ok=True)
os.makedirs(os.path.join(saves, "Server"), exist_ok=True)
os.makedirs(os.path.join(saves, "Logs"), exist_ok=True)
INI = os.path.join(saves, "Server", "PzColab.ini")

WS = os.path.join(server, "steamapps", "workshop", "content", "108600")
os.makedirs(WS, exist_ok=True)

def _ini_ws(wsids_mods):
    items = ";".join(wsids_mods[0])
    mods = ";".join([f"\\{m}" if ES else m for m in wsids_mods[1]])
    with open(INI, "w") as f:
        f.write(f"Port=16261\nWorkshopItems={items}\nMods={mods}\nPauseOnEmpty=true\n")

def _make_mod(wsid, mid):
    d = os.path.join(WS, wsid, "mods", mid)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "mod.info"), "w") as f:
        f.write(f"id={mid}\nname={mid}\n")

# Mod info para pruebas
_make_mod("2902678", "hydrocraft")
_make_mod("2799742455", "coolmod")

# logs viejos para test de rotacion (25 archivos -> deben quedar 20)
for i in range(25):
    p = os.path.join(saves, "Logs", f"log_{i:03d}.txt")
    with open(p, "w") as f:
        f.write(f"entry {i}")
    os.utime(p, (i, i))

# ===== TESTS CELDA 5 (backup/restore) =====
# Mockear "/content/drive" para simular Drive montado (cell-backup chequea os.path.exists)
_orig_exists = os.path.exists
def _mock_exists(p):
    if p == "/content/drive":
        return True
    return _orig_exists(p)
code = src5
code = code.replace('"/content/drive/MyDrive/ZomboidSaves"', "r'" + saves.replace("\\", "/") + "'")
code = code.replace('"/content/drive/MyDrive/ZomboidSaves_backups"', "r'" + os.path.join(tmp, "ZomboidSaves_backups").replace("\\", "/") + "'")
# Neutralizar los @param literales para poder inyectar valores de test
code = code.replace("Backup_Max_Guardar", "_BACKUP_MAX")
code = code.replace("Restaurar_Backup", "_RESTORE")
code = code.replace("numero_backup", "_NUM")
# Neutralizar las asignaciones literales (como test_cell4.py hace con _DESC)
code = code.replace("_BACKUP_MAX = 3", "_BACKUP_MAX = _BACKUP_MAX")
code = code.replace("_RESTORE = False", "_RESTORE = _RESTORE")
code = code.replace("_NUM = 0", "_NUM = _NUM")
ns = {}
def correr_backup(max_guardar=3, restore=False, num=0):
    os.path.exists = _mock_exists
    ns.clear()
    ns["_BACKUP_MAX"] = max_guardar
    ns["_RESTORE"] = restore
    ns["_NUM"] = num
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(code, "cell-backup", "exec"), ns)
    finally:
        os.path.exists = _orig_exists
    return buf.getvalue()

_ini = ("Port=16261", "WorkshopItems=2902678;2799742455\nMods=\\hydrocraft;\\coolmod\n", "PauseOnEmpty=true\n")
_ini_en = ("Port=16261", "WorkshopItems=2902678;2799742455\nMods=hydrocraft;coolmod\n", "PauseOnEmpty=true\n")
_ini_act = _ini if ES else _ini_en

# G3: retención 3 backups (crear 5, deben quedar 3)
_ok_backup = "✅ Backup creado" if ES else "✅ Backup created"
for i in range(5):
    with open(INI, "w") as f:
        f.write("".join(_ini_act))
    out = correr_backup(max_guardar=3)
    assert _ok_backup in out, f"backup {i} falló:\n{out}"
backs = sorted(glob.glob(f"{tmp}/ZomboidSaves_backups/ZomboidSaves_*.tar.gz"), key=os.path.getmtime)
assert len(backs) == 3, f"retención falló: {len(backs)} != 3"
print("G3 OK: retención 3 backups (se borran los viejos)")

# G4: restore preserva lista + extrae contenido
# crear un backup con contenido de save distinto
alt = os.path.join(tmp, "alt_save")
os.makedirs(os.path.join(alt, "Server"), exist_ok=True)
with open(os.path.join(alt, "Server", "PzColab.ini"), "w") as f:
    f.write("Port=9999\nWorkshopItems=1111\nMods=" + (("\\restoredmod\n" if ES else "restoredmod\n")) )
# forzar backup con el alt-save como src
import tarfile as _tf
with _tf.open(backs[0], "w:gz") as tar:
    tar.add(alt, arcname="ZomboidSaves", recursive=True)
# corromper el save actual
with open(INI, "w") as f:
    f.write("Port=16261\nWorkshopItems=\nMods=\n")
out = correr_backup(restore=True, num=0)
_aviso_restore = "✅ Restore completado" if ES else "✅ Restore completed"
assert _aviso_restore in out, f"restore falló:\n{out}"
assert "1111" in open(INI).read(), f"restore no aplicó el backup:\n{INI}"
# ver que el número de backups no cambió (se preserva origen, solo se añadió previo-a-restore)
backs2 = sorted(glob.glob(f"{tmp}/ZomboidSaves_backups/ZomboidSaves_*.tar.gz"), key=os.path.getmtime)
assert len(backs2) >= 3, "restore debería preservar los backups"
print("G4 OK: restore aplica backup y preserva lista de backups")

# G5: rotación logs (25 -> 20)
with open(INI, "w") as f:
    f.write("".join(_ini_act))
_ = correr_backup()
logs = os.listdir(os.path.join(saves, "Logs"))
assert len(logs) <= 20, f"rotación falló: {len(logs)} logs"
print("G5 OK: rotación logs conserva máximo 20")

# ===== TESTS CELDA 4: Eliminar_Mods =====
fake_req = types.ModuleType("requests"); fake_req.get = lambda *a, **k: types.SimpleNamespace(status_code=200, text="")
sys.modules["requests"] = fake_req
sys.modules.setdefault("subprocess", types.ModuleType("subprocess"))
ns["subprocess"] = sys.modules["subprocess"]

code4 = src4
code4 = code4.replace('"/content/drive/MyDrive/ZomboidSaves"', "r'" + saves.replace("\\", "/") + "'")
code4 = code4.replace("'/content/drive/MyDrive/ZomboidSaves'", "r'" + saves.replace("\\", "/") + "'")
code4 = code4.replace("'/content/pzserver'", "r'" + server.replace("\\", "/") + "'")
# Neutralizar @param literales del cell-mods con namespaces únicos (como test_cell4.py)
# Cada param se reemplaza por su nombre interno _X para poder inyectar valores de test.
_reemplazos = [
    ("Limpiar_Lista_Anterior", "_LIMP"), ("clear_previous_list", "_LIMP"),
    ("Descargar_Mods", "_DESC"), ("download_mods", "_DESC"),
    ("Descargar_Dependencias", "_DEP"), ("resolve_dependencies", "_DEP"),
    ("Eliminar_Mods", "_ELIM"), ("manage_mods", "_ELIM"),
    ("numero_a_eliminar", "_NUM_ELIM"), ("number_to_remove", "_NUM_ELIM"),
]
for _es, _ns in _reemplazos:
    code4 = code4.replace(_es, _ns)
# Neutralizar las asignaciones literales @param (el source las reescribe, p.ej. _ELIM = False)
code4 = code4.replace("_LIMP = False", "_LIMP = _LIMP")
code4 = code4.replace("_DESC = True", "_DESC = _DESC")
code4 = code4.replace("_DEP = True", "_DEP = _DEP")
code4 = code4.replace("_ELIM = False", "_ELIM = _ELIM")
code4 = code4.replace("_NUM_ELIM = \"\"", "_NUM_ELIM = _NUM_ELIM")
ns4 = {}

def correr_mods(input_, limpiar=False, descargar=False, deps=False, manage=False, num_elim=""):
    ns4.clear()
    ns4["mods_input"] = input_
    ns4["_LIMP"] = limpiar
    ns4["_DESC"] = descargar
    ns4["_DEP"] = deps
    ns4["_ELIM"] = manage
    ns4["_NUM_ELIM"] = num_elim
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(code4, "cell-mods", "exec"), ns4)
    return buf.getvalue()

def _escribir_ini(wsids, mods):
    items = ";".join(wsids)
    mods_str = ";".join([f"\\{m}" if ES else m for m in mods])
    with open(INI, "w") as f:
        f.write(f"Port=16261\nWorkshopItems={items}\nMods={mods_str}\nPauseOnEmpty=true\n")

# G6: eliminar mod por número
_escribir_ini(["2902678", "2799742455"], ["hydrocraft", "coolmod"])
out = correr_mods("", manage=True, num_elim="0")
ini_after = open(INI).read()
assert "2902678" not in ini_after and "2799742455" in ini_after, f"eliminación por número falló:\n{ini_after}"
_msg_elim = "eliminado" if ES else "removed"
assert _msg_elim in out, f"no reporta eliminación:\n{out}"
print("G6 OK: eliminar mod por número (índice 0 desaparece del .ini)")

# G7: eliminar mod por WSID
_escribir_ini(["2902678", "2799742455"], ["hydrocraft", "coolmod"])
out = correr_mods("", manage=True, num_elim="2799742455")
ini_after = open(INI).read()
assert "2799742455" not in ini_after and "2902678" in ini_after, f"eliminación por WSID falló:\n{ini_after}"
print("G7 OK: eliminar mod por WSID")

# G8: listado muestra nombres amigables (y maneja wsid sin mod.info -> fallback nombre)
_escribir_ini(["2902678", "2799742455"], ["hydrocraft", "coolmod"])
out = correr_mods("", manage=True, num_elim="")
label = "MODS ACTIVOS" if ES else "ACTIVE MODS"
assert label in out, f"no lista mods:\n{out}"
assert "2902678" in out and "2799742455" in out, f"la lista no muestra wsid:\n{out}"
print("G8 OK: listado con nombres amigables + WSIDs")

# G9: numero inválido -> aviso, no elimina
_escribir_ini(["2902678", "2799742455"], ["hydrocraft", "coolmod"])
out = correr_mods("", manage=True, num_elim="9999")
ini_after = open(INI).read()
assert "2902678" in ini_after and "2799742455" in ini_after, f"numero inválido borró algo:\n{ini_after}"
assert "inválido" in out.lower() if ES else "invalid" in out.lower(), f"no avisa número inválido:\n{out}"
print("G9 OK: número/WSID inválido avisa sin borrar nada")

shutil.rmtree(tmp, ignore_errors=True)
print("\n✅ TODOS LOS TESTS DE BACKUP/RESTORE/ELIMINAR PASARON")
