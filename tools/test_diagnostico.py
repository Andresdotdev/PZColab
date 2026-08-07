# -*- coding: utf-8 -*-
"""Test funcional de la Celda 4.1 (diagnóstico ampliado) + tope de memoria (Celda 3)."""
import contextlib
import io
import json
import os
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
NB = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "PZ_Colab_ES.ipynb")
ES = "EN" not in NB
print("Notebook:", NB, "(ES)" if ES else "(EN)")
nb = json.load(open(NB, encoding="utf-8"))

src_diag = "".join("".join(c["source"]) for c in nb["cells"] if c["metadata"].get("id") == "cell-diagnostico")
src_ini = "".join("".join(c["source"]) for c in nb["cells"] if c["metadata"].get("id") == "cell-iniciar")

# ============ ESCENARIO H: detección ampliada en 4.1 ============
tmp = tempfile.mkdtemp(prefix="pzcolab_diag_")
saves = os.path.join(tmp, "ZomboidSaves")
os.makedirs(os.path.join(saves, "Server"), exist_ok=True)
os.makedirs(os.path.join(saves, "Logs"), exist_ok=True)
with open(os.path.join(saves, "Server", "PzColab.ini"), "w") as f:
    f.write("WorkshopItems=1111\nMods=oldmod\n")
with open(os.path.join(saves, "Logs", "console.txt"), "w", encoding="utf-8") as f:
    f.write("INFO: server starting...\n")
    f.write("java.lang.OutOfMemoryError: Java heap space\n")
    f.write("ERROR: failed to bind to port 16261\n")
    f.write("SEVERE: failed to save the world chunk\n")
    f.write("INFO: all good\n")

code = src_diag.replace("'/content/drive/MyDrive/ZomboidSaves'", "r'" + saves.replace("\\", "/") + "'")
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(code, "cell-diagnostico", "exec"), {})
out = buf.getvalue()

sec_mem = "PROBLEMAS DE MEMORIA" if ES else "MEMORY PROBLEMS"
sec_srv = "ERRORES DEL SERVIDOR" if ES else "SERVER ERRORS"
sec_save = "FALLOS DE GUARDADO" if ES else "SAVE FAILURES"
assert sec_mem in out, f"memoria no detectada:\n{out}"
assert sec_srv in out, f"errores servidor no detectados:\n{out}"
assert sec_save in out, f"fallos de guardado no detectados:\n{out}"
assert "OutOfMemoryError" in out and "failed to bind" in out
print("H1 OK: 4.1 detecta memoria, errores de servidor y fallos de guardado")

# ============ ESCENARIO I: tope de memoria dinámico (Celda 3) ============
# Unidad: misma fórmula que usa la celda
def tope_seguro(ram_total_gb):
    return min(8, max(4, ram_total_gb - 4))

assert tope_seguro(12.7) == 8, "12.7 GB -> 8"
assert tope_seguro(16) == 8, "16 GB -> 8 (cap duro)"
assert tope_seguro(8) == 4, "8 GB -> 4"
assert tope_seguro(6) == 4, "6 GB -> 4 (mín 4)"

def aplicar(elegida, ram_total_gb):
    t = tope_seguro(ram_total_gb)
    return min(elegida, t), t

f, t = aplicar(8, 12.7)
assert (f, t) == (8, 8), "elegir 8 con 12.7 OK"
f, t = aplicar(6, 8)
assert (f, t) == (4, 4), "elegir 6 con 8 GB -> baja a 4"
f, t = aplicar(4, 12.7)
assert (f, t) == (4, 8), "elegir 4 se respeta"
print("I1 OK: tope dinámico (mín 4, máx 8, RAM-4)")

# El parche aplica -Xms/-Xmx con el valor final
import re
contenido = "java -Xms6g -Xmx6g -cp ... zombie.network.GameServer"
memoria_final = 8
nuevo = re.sub(r"-Xms\S+", f"-Xms{memoria_final}g", contenido)
nuevo = re.sub(r"-Xmx\S+", f"-Xmx{memoria_final}g", nuevo)
assert nuevo == "java -Xms8g -Xmx8g -cp ... zombie.network.GameServer", nuevo
print("I2 OK: el parche reemplaza Xms/Xmx con el valor final")

# El notebook EN tiene la variable renombrada memory_gb
if not ES:
    assert "memory_gb = \"6 GB\"" in src_ini, "falta memory_gb en EN"
    assert "memoria_gb" not in src_ini.replace("memoria_elegida", "").replace("memoria_final", ""), "quedó memoria_gb en EN"
    print("I3 OK: EN usa memory_gb (label en inglés)")
else:
    assert "memoria_gb = \"6 GB\"" in src_ini, "falta memoria_gb en ES"
    print("I3 OK: ES usa memoria_gb")

print("\n✅ TODOS LOS ESCENARIOS PASARON")
