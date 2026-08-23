# -*- coding: utf-8 -*-
"""Genera PZ_Colab_ES.ipynb (ES) y PZ_Colab_EN.ipynb (EN) de forma programática."""
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
TARGET = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "PZ_Colab_ES.ipynb"

def md(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }

def code(cell_id, source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"id": cell_id},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }

BADGE = md(
    '<a href="https://colab.research.google.com/github/Andresdotdev/PZColab/blob/main/PZ_Colab_ES.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>'
)

INDICE = md('''🗺️ **Guía rápida del cuaderno**

| Celda | Acción |
|---|---|
| 1 | 🚀 Instalar el servidor (elegir versión b42 / b41) |
| 2 | 🔥 Encender servidor + reclamar túnel Playit + consola en vivo + apagado limpio (integrado) |
| 3 | 📦 Mods: inyección + descarga Workshop |
| 3.1 | 🩺 Diagnóstico de logs por mod |
| 4 | 💾 Backup de saves en Drive |

_Flujo típico: 1 → 2 (encender + jugar + apagar). Las celdas 3, 3.1 y 4 se usan bajo demanda._
''')

CELDA_1 = code("cell-instalar", '''# @title 1. Instalar Servidor y Dependencias
# @markdown ---
# @markdown ### 🎮 Selección de Versión
Version = "b42 estable" # @param ["b42 estable", "b41 legacy", "b42 unstable"]

import os
import re
import json
import time
import subprocess
from IPython.display import clear_output

SAVES_PATH = "/content/drive/MyDrive/ZomboidSaves"
STATE_PATH = f"{SAVES_PATH}/.pzcolab_state.json"
SERVER_PATH = "/content/pzserver"

def beta_args(version):
    if version == "b41 legacy":
        return ["-beta", "legacy41"]
    if version == "b42 unstable":
        return ["-beta", "unstable"]
    return []

def mostrar_panel(etapa, progreso_steam=None):
    clear_output(wait=True)
    print("=========================================================")
    print("🚀 INSTALADOR DE SERVIDOR PROJECT ZOMBOID")
    print("=========================================================\\n")
    pasos = [
        "1. Preparar sistema y dependencias",
        "2. Descargar red Playit.gg",
        "3. Vincular Google Drive",
        "4. Descargar Servidor (SteamCMD)",
    ]
    for i, p in enumerate(pasos, start=1):
        if etapa >= i:
            print(f"[✅] {p}")
        elif etapa == i - 1:
            print(f"[⏳] {p}")
        else:
            print(f"[  ] {p}")
    if progreso_steam and etapa == 3:
        print("\\n   📊 PROGRESO DE DESCARGA:")
        for state, pct in progreso_steam.items():
            bar_length = 30
            filled = int(bar_length * pct / 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f"      ► {state:<14} |{bar}| {pct:>5.1f}%")

mostrar_panel(0)

# --- 1. SISTEMA ---
!sudo dpkg --add-architecture i386 > /dev/null 2>&1
!sudo apt update -y > /dev/null 2>&1
!echo steam steam/license note '' | debconf-set-selections
!echo steam steam/question select "I AGREE" | debconf-set-selections
!sudo apt install lib32gcc-s1 lib32stdc++6 steamcmd curl -y > /dev/null 2>&1
!/usr/games/steamcmd +quit > /dev/null 2>&1
mostrar_panel(1)

# --- 2. PLAYIT ---
!curl -sL https://github.com/playit-cloud/playit-agent/releases/download/v0.15.26/playit-linux-amd64 -o /usr/local/bin/playit > /dev/null 2>&1
!chmod +x /usr/local/bin/playit
mostrar_panel(2)

# --- 3. GOOGLE DRIVE ---
if not os.path.exists("/content/drive"):
    from google.colab import drive
    drive.mount('/content/drive')
os.makedirs(SAVES_PATH, exist_ok=True)
if os.path.exists("/root/Zomboid") and not os.path.islink("/root/Zomboid"):
    os.system("mv /root/Zomboid /root/Zomboid.local_$(date +%s)")
    print("⚠️ Carpeta local antigua de /root/Zomboid renombrada; se reemplaza por el enlace a Drive.")
os.system("rm -rf /root/Zomboid")
os.system(f'ln -s "{SAVES_PATH}" /root/Zomboid')
mostrar_panel(3, {"Iniciando...": 0.0})

# --- 4. STEAMCMD (idempotente: no re-descarga si ya está instalado) ---
ya_instalado = os.path.exists(f"{SERVER_PATH}/ProjectZomboid64")
misma_version = False
try:
    with open(STATE_PATH) as f:
        misma_version = json.load(f).get("version") == Version
except Exception:
    pass

if ya_instalado and misma_version:
    mostrar_panel(4)
    print("\\nℹ️ El servidor ya está instalado con la versión seleccionada. Se omite la descarga.")
else:
    if ya_instalado:
        print("⚠️ Se detectó una versión distinta instalada. Deteniendo servidor y reinstalando...")
        os.system("pkill -f ProjectZomboid64 2>/dev/null")
        time.sleep(3)

    cmd_base = ['/usr/games/steamcmd', '+force_install_dir', SERVER_PATH, '+login', 'anonymous', '+app_update', '380870']
    cmd = cmd_base + beta_args(Version) + ['+quit']

    # Intento de descarga con retry: Colab free puede interrumpir por inactividad (~15 min sin output)
    # o rate-limits de Steam. Reintentamos limpiando pzserver.
    intento = 0
    max_intentos = 3
    ok_descarga = False
    while intento < max_intentos and not ok_descarga:
        intento += 1
        # Limpiar parciales del intento anterior
        os.system("rm -rf " + SERVER_PATH + " 2>/dev/null")
        os.makedirs(SERVER_PATH, exist_ok=True)
        if intento > 1:
            print(f"\\n🔄 Reintento de descarga {intento}/{max_intentos} (limpiando estado previo)...")
            time.sleep(5)

        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            progreso = {}
            try:
                for line in process.stdout:
                    line_lower = line.lower()
                    match = re.search(r'(?:stage|update state)\\s+\\(([^)]+)\\)\\s+([a-zA-Z]+),\\s+progress:\\s+([0-9.]+)', line_lower)
                    if match:
                        state = match.group(2).capitalize()
                        try:
                            percent = float(match.group(3))
                        except ValueError:
                            percent = 0.0
                        if percent > 100.0:
                            percent = 100.0
                        progreso[state] = percent
                        mostrar_panel(3, progreso)
            except KeyboardInterrupt:
                # Colab interrumpió: matar el proceso y reintentar
                print("\\n⚠️ Descarga interrumpida (posible pausa de inactividad de Colab).")
                try:
                    process.terminate()
                    process.wait(timeout=30)
                except Exception:
                    pass
                continue
            rc = process.wait()
            if rc != 0:
                print(f"⚠️ SteamCMD salió con código {rc} (rate-limit o red).")
                continue
            ok_descarga = True
        except Exception as e:
            print(f"⚠️ Error en SteamCMD en el intento {intento}: {e}")
            continue

    if not ok_descarga:
        print(f"\\n⚠️ Falló la descarga después de {max_intentos} intentos.")
        print("💡 Solución: Reinicia el runtime de Colab (Desconectar y Reconectar) y vuelve a ejecutar esta celda.")

# --- 4.1 VALIDAR INTEGRIDAD (si falta el ejecutable, validar vía SteamCMD) ---
if ok_descarga and not os.path.exists(f"{SERVER_PATH}/ProjectZomboid64"):
    print("\\n🔎 Validando integridad de archivos con SteamCMD (puede tardar un par de minutos)...")
    cmd_validate = ['/usr/games/steamcmd', '+force_install_dir', SERVER_PATH, '+login', 'anonymous', '+app_update', '380870', 'validate', '+quit']
    try:
        vproc = subprocess.run(cmd_validate, capture_output=True, text=True, timeout=600)
        mostrar_panel(3)
        if vproc.returncode != 0:
            print(f"⚠️ Validación falló (código {vproc.returncode}).")
    except Exception as e:
        print(f"⚠️ No se pudo validar integridad: {e}")

# --- 5. PARCHAR MEMORIA (Colab tiene ~12.7 GB de RAM) ---
START_SH = f"{SERVER_PATH}/start-server.sh"
if os.path.exists(START_SH):
    with open(START_SH) as f:
        contenido = f.read()
    nuevo = re.sub(r'-Xms\\S+', '-Xms6g', contenido)
    nuevo = re.sub(r'-Xmx\\S+', '-Xmx6g', nuevo)
    if nuevo != contenido:
        with open(START_SH, 'w') as f:
            f.write(nuevo)
        print("💾 Memoria del servidor ajustada a 6 GB (compatible con el límite de Colab).")
    else:
        print("ℹ️ start-server.sh ya tenía memoria configurada (no se modificó).")
else:
    print("⚠️ No se encontró start-server.sh tras la instalación.")

# --- 6. GUARDAR ESTADO (sincroniza la versión entre todas las celdas) ---
try:
    with open(STATE_PATH, 'w') as f:
        json.dump({"version": Version, "server_path": SERVER_PATH}, f)
    print("📌 Estado guardado en Drive: todas las celdas usarán esta versión.")
except Exception as e:
    print(f"⚠️ No se pudo guardar el estado: {e}")

# --- FINALIZACIÓN ---
if os.path.exists(f"{SERVER_PATH}/ProjectZomboid64"):
    mostrar_panel(4)
    print("\\n=========================================================")
    print("✅ ¡FASE 1 COMPLETADA CON ÉXITO! Puedes continuar a la Celda 2.")
    print("=========================================================")
else:
    print("\\n⚠️ SteamCMD falló al validar el ejecutable. Intenta correr la celda de nuevo.")
''')

CELDA_3 = code("cell-iniciar", '''# @title 2. Iniciar Servidor + Túnel Playit + Consola (Auto-Apagado)
# @markdown ---
# @markdown ### 🎮 Parámetros del Servidor
server_name = 'PzColab' # @param {type: "string"}
admin_password = '' # @param {type: "string"}
server_password = '' # @param {type: "string"}
port = 16261 # @param {type: "integer"}
max_players = 16 # @param {type: "integer"}
pausa_cuando_vacio = True # @param {type: "boolean"}
# @markdown _💡 Cuanta más memoria, más mods y jugadores caben. Máx. seguro: 8 GB en Colab._
memoria_gb = "6 GB" # @param ["4 GB", "6 GB", "8 GB"]
# @markdown _💡 Si cambias el puerto, actualiza el túnel en playit.gg._
# @markdown
# @markdown ### 🛡️ Watchdog (auto-reinicio ante crashes)
watchdog_activo = True # @param {type: "boolean"}
max_reinicios = 3 # @param {type: "integer"}
# @markdown ### 💾 Backup automático al apagar
Auto_Backup = True # @param {type: "boolean"}
# @markdown _💡 Al detener la celda (⏹), guarda un .tar.gz de tu mundo en Drive antes de apagar._

import os
import re
import json
import time
import sys
import secrets
import threading
import subprocess

SAVES_PATH = "/content/drive/MyDrive/ZomboidSaves"
SERVER_PATH = "/content/pzserver"
LOG_PATH = "/tmp/pzserver.log"
STATE_PATH = f"{SAVES_PATH}/.pzcolab_state.json"
INI_DIR = f"{SAVES_PATH}/Server"
INI_PATH = f"{INI_DIR}/{server_name}.ini"

def abortar(msg):
    print(msg)
    sys.exit()

# --- 0. VERIFICAR PRE-REQUISITOS ---
if not os.path.exists("/content/drive"):
    abortar("❌ Google Drive NO está montado. Ejecuta primero la Celda 1.")

Version = "b42 estable"
if os.path.exists(STATE_PATH):
    try:
        with open(STATE_PATH) as f:
            Version = json.load(f).get("version", "b42 estable")
    except Exception:
        pass
print(f"📌 Versión activa: {Version}")

# --- 0.1 LIMPIAR EJECUCIONES ANTERIORES (re-ejecución segura de la celda) ---
if "pz_proc" in globals() and globals()["pz_proc"] and globals()["pz_proc"].poll() is None:
    if "parada" in globals() and globals()["parada"]:
        globals()["parada"].set()
    print("🛑 Servidor anterior detectado; se detiene antes de continuar.")
    os.system("pkill -f ProjectZomboid64 2>/dev/null")
    time.sleep(5)

# Recrear el symlink de saves si el runtime se reinició
if not os.path.islink("/root/Zomboid"):
    os.makedirs(SAVES_PATH, exist_ok=True)
    os.system("rm -rf /root/Zomboid")
    os.system(f'ln -s "{SAVES_PATH}" /root/Zomboid')
    print("🔗 Symlink de saves recreado (runtime nuevo).")

# --- 1. CONFIGURAR EL .INI (puerto, jugadores, pausa, passwords) ---
os.makedirs(INI_DIR, exist_ok=True)

def set_ini(key, valor):
    linea = f"{key}={valor}"
    if os.path.exists(INI_PATH):
        with open(INI_PATH) as f:
            lines = f.readlines()
        encontrado = False
        for i, l in enumerate(lines):
            if l.startswith(f"{key}="):
                lines[i] = linea + "\\n"
                encontrado = True
                break
        if not encontrado:
            lines.append(linea + "\\n")
        with open(INI_PATH, "w") as f:
            f.writelines(lines)
    else:
        with open(INI_PATH, "w") as f:
            f.write(linea + "\\n")

if not admin_password:
    m = None
    if os.path.exists(INI_PATH):
        with open(INI_PATH) as f:
            m = re.search(r'^AdminPassword=(.*)', f.read(), re.MULTILINE)
    if m and m.group(1).strip():
        admin_password = m.group(1).strip()
        print("🔑 Admin password recuperada del .ini existente.")
    else:
        admin_password = "Pz" + secrets.token_hex(4)
        print(f"🔑 Admin password generada automáticamente: {admin_password}")

if not os.path.exists(INI_PATH):
    with open(INI_PATH, "w") as f:
        f.write(f"Port={port}\\nDefaultPort={port}\\nMaxPlayers={max_players}\\nPauseOnEmpty={str(pausa_cuando_vacio).lower()}\\nPassword={server_password}\\nAdminPassword={admin_password}\\n")
    print("ℹ️ Primer arranque: .ini base creado con la configuración elegida.")
else:
    set_ini("Port", port)
    set_ini("DefaultPort", port)
    set_ini("MaxPlayers", max_players)
    set_ini("PauseOnEmpty", str(pausa_cuando_vacio).lower())
    set_ini("Password", server_password)
    set_ini("AdminPassword", admin_password)
    print(f"⚙️ Configuración aplicada en {INI_PATH}")

if port != 16261:
    print(f"⚠️ Puerto cambiado a {port}. Actualiza el túnel en https://playit.gg/account")

# Guardar el nombre del servidor para que las demás celdas lo usen
try:
    with open(STATE_PATH) as f:
        estado = json.load(f)
    estado["server_name"] = server_name
    with open(STATE_PATH, "w") as f:
        json.dump(estado, f)
except Exception:
    pass

# --- 2. PLAYIT TÚNEL (reclamo inline primera vez / background después) ---
PLAYIT_DRIVE = f"{SAVES_PATH}/playitgg"
PLAYIT_CONFIG = "/root/.config/playit_gg"
playit_proc = None  # global del kernel, persiste entre re-ejecuciones
try:
    playit_proc = globals().get("playit_proc")
except Exception:
    pass

os.system("pkill -f 'playit' 2>/dev/null")

# Enlazar persistencia de config a Drive
if os.path.exists("/content/drive"):
    os.makedirs(PLAYIT_DRIVE, exist_ok=True)
    if os.path.isdir(PLAYIT_CONFIG) or os.path.islink(PLAYIT_CONFIG):
        os.system("rm -rf " + PLAYIT_CONFIG)
    os.system("ln -s " + PLAYIT_DRIVE + " " + PLAYIT_CONFIG)

config_existe = os.path.isdir(PLAYIT_DRIVE) and any(os.scandir(PLAYIT_DRIVE)) if os.path.isdir(PLAYIT_DRIVE) else False
if not config_existe:
    # Primera vez: reclamo foreground del túnel (la celda se pausa)
    print("🚀 Primera ejecución: reclama tu túnel Playit.gg en la ventana que se abre.")
    print("⚠️ Autoriza el enlace y vuelve aquí. La celda se quedará esperando.")
    print("=" * 50)
    get_ipython().system("playit")
    config_existe = os.path.isdir(PLAYIT_DRIVE) and any(os.scandir(PLAYIT_DRIVE)) if os.path.isdir(PLAYIT_DRIVE) else False

if config_existe:
    playit_proc = subprocess.Popen(["playit"], stdout=open("/tmp/playit.log", "a"), stderr=subprocess.STDOUT)
    print("✅ Túnel Playit.gg en segundo plano (handle guardado):", playit_proc.pid)
else:
    print("⚠️ No se pudo reclamar el túnel de Playit.gg. El servidor funciona local pero no es accesible externamente.")

# --- 3. APLICAR MEMORIA CONFIGURADA (parche Xms/Xmx en start-server.sh) ---
START_SH = "/content/pzserver/start-server.sh"
if not os.path.exists(START_SH):
    abortar("❌ No se encontró start-server.sh. Ejecuta primero la Celda 1 (instalación).")

memoria_elegida = int(str(memoria_gb).split()[0])
tope_seguro = 8
try:
    with open("/proc/meminfo") as f:
        for linea in f:
            if linea.startswith("MemTotal:"):
                ram_total_gb = int(linea.split()[1]) // 1024 // 1024
                tope_seguro = min(8, max(4, ram_total_gb - 4))
                break
except Exception:
    pass
memoria_final = min(memoria_elegida, tope_seguro)
if memoria_final < memoria_elegida:
    print(f"⚠️ Elegiste {memoria_elegida} GB pero este runtime permite hasta {tope_seguro} GB. Se aplica {memoria_final} GB.")

with open(START_SH) as f:
    contenido = f.read()
nuevo = re.sub(r'-Xms\\S+', f'-Xms{memoria_final}g', contenido)
nuevo = re.sub(r'-Xmx\\S+', f'-Xmx{memoria_final}g', nuevo)
if nuevo != contenido:
    with open(START_SH, "w") as f:
        f.write(nuevo)
    print(f"💾 Memoria del servidor: {memoria_final} GB (tope seguro de este runtime: {tope_seguro} GB).")

os.system("chmod +x /content/pzserver/start-server.sh 2>/dev/null")

# --- 4. LANZAR SERVIDOR EN SEGUNDO PLANO CON WATCHDOG ---
logf = open(LOG_PATH, "a", buffering=1)
logf.write(f"\\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🚀 INICIO DE SERVIDOR ({Version})\\n")
logf.flush()

parada = threading.Event()

def arrancar():
    return subprocess.Popen(
        ["/content/pzserver/start-server.sh", "-servername", server_name, "-adminpassword", admin_password],
        stdin=subprocess.PIPE, stdout=logf, stderr=subprocess.STDOUT, text=True)

pz_proc = arrancar()
reinicios = 0

def monitor():
    global pz_proc, reinicios
    while True:
        code = pz_proc.poll()
        if code is not None:
            logf.write(f"[{time.strftime('%H:%M:%S')}] ⚠️ El servidor terminó (código {code}).\\n")
            logf.flush()
            if parada.is_set() or not watchdog_activo or reinicios >= max_reinicios:
                logf.write("[...] Watchdog detenido.\\n")
                logf.flush()
                break
            reinicios += 1
            logf.write(f"[{time.strftime('%H:%M:%S')}] 🔄 Reinicio {reinicios}/{max_reinicios} en 8s...\\n")
            logf.flush()
            time.sleep(8)
            pz_proc = arrancar()
        time.sleep(5)

threading.Thread(target=monitor, daemon=True).start()

print("🔥 Servidor arrancado en segundo plano.")
print("📄 Consola en vivo integrada abajo (⏹ para detener y apagar de forma limpia).")
if watchdog_activo:
    print(f"🛡️ Watchdog activo: hasta {max_reinicios} reinicios automáticos.")

# --- 5. CONSOLA EN VIVO + APAGADO LIMPIO (flujo unificado) ---
# El tail se consume con subprocess para que el ⏹ de Colab dispare KeyboardInterrupt
# y entre en el bloque finally => save() -> quit() automático al terminar.
tail_proc = None
try:
    print(f"📖 Streaming de {LOG_PATH} — pulsa ⏹ para detener y apagar de forma limpia.")
    if os.path.exists(LOG_PATH):
        tail_proc = subprocess.Popen(["tail", "-n", "40", "-f", LOG_PATH],
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for linea in tail_proc.stdout:
            print(linea, end="", flush=True)
    else:
        print("⚠️ Aún no hay log. El streaming empezará en cuanto arranque el servidor.")
        time.sleep(20)
except KeyboardInterrupt:
    print("\\n🛑 Interrupción manual detectada: iniciando apagado limpio...")
except Exception as e:
    print(f"\\n⚠️ Error en el tail: {e}")
finally:
    if tail_proc and tail_proc.poll() is None:
        tail_proc.terminate()
        try:
            tail_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            tail_proc.kill()
    # Apagado ordenado del servidor: save -> quit
    if parada is not None:
        parada.set()
    if pz_proc and pz_proc.poll() is None and pz_proc.stdin:
        print("💾 Enviando SAVE...")
        try:
            pz_proc.stdin.write("save\\n")
            pz_proc.stdin.flush()
        except Exception:
            pass
        time.sleep(15)
        print("🛑 Enviando QUIT...")
        try:
            pz_proc.stdin.write("quit\\n")
            pz_proc.stdin.flush()
        except Exception:
            pass
        try:
            pz_proc.wait(timeout=90)
            print("✅ Servidor apagado de forma segura.")
        except subprocess.TimeoutExpired:
            print("⚠️ No respondió a tiempo; forzando cierre.")
            pz_proc.terminate()
    else:
        os.system("pkill -TERM -f ProjectZomboid64 2>/dev/null; sleep 10; pkill -KILL -f ProjectZomboid64 2>/dev/null")
        print("✅ Señales de terminación enviadas.")
    if playit_proc and playit_proc.poll() is None:
        playit_proc.terminate()
        try:
            playit_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            playit_proc.kill()
    if logf and not logf.closed:
        logf.close()
    # --- Auto-backup al apagar (antes del save final) ---
    try:
        if Auto_Backup and os.path.isdir(SAVES_PATH):
            import tarfile, time, glob as _glob
            BACKUP_DIR = f"{SAVES_PATH}_backups"
            os.makedirs(BACKUP_DIR, exist_ok=True)
            # Rotar logs: conservar sólo los 20 archivos más recientes en Logs/, borrar el resto
            LOGS_DIR = os.path.join(SAVES_PATH, "Logs")
            if os.path.isdir(LOGS_DIR):
                logs = sorted(_glob.glob(os.path.join(LOGS_DIR, "*")), key=os.path.getmtime)
                for viejo in logs[:-20]:
                    try:
                        os.remove(viejo)
                    except Exception:
                        pass
            ts = time.strftime("%Y%m%d_%H%M%S")
            destino = f"{BACKUP_DIR}/ZomboidSaves_{ts}_{int(time.time() * 1000) % 100000:05d}.tar.gz"
            # Excluir Logs/ (ya rotados) y el propio backups dir del tar.gz
            def _tar_filter(ti):
                if ti.name.startswith("ZomboidSaves/Logs"):
                    return None
                return ti
            with tarfile.open(destino, "w:gz") as tar:
                tar.add(SAVES_PATH, arcname="ZomboidSaves", recursive=True, filter=_tar_filter)
            # Retención: mantener sólo los 3 backups más recientes
            backups = sorted(_glob.glob(f"{BACKUP_DIR}/ZomboidSaves_*.tar.gz"), key=os.path.getmtime)
            for viejo in backups[:-3]:
                try:
                    os.remove(viejo)
                except Exception:
                    pass
            print(f"💾 Auto-backup creado: {destino}")
    except Exception as e:
        print(f"⚠️ Auto-backup falló: {e}")
    print("🎯 Cierre completo: servidor guardado y túnel detenido.")
''')

ANTI_AFK = md('''🛠️ Script Anti-Abandono para el Navegador
Este script simula que estás haciendo clic en la página de Colab de forma automática cada 10 minutos para engañar al sistema de inactividad.

Pasos para activarlo:

1.   Abre tu cuaderno de Google Colab en el navegador (Chrome, Edge o Firefox).
2.   Presiona la tecla F12 (o clic derecho en cualquier parte de la página y selecciona Inspeccionar).
3.   Ve a la pestaña llamada Consola (Console).
4.   Pega el siguiente código y presiona Enter:
```
function KeepAlive() {
    console.log("Manteniendo servidor activo...");
    // Simula un clic en el botón de conectar o de opciones del sistema
    let connectButton = document.querySelector("#connect") || document.querySelector("colab-connect-button");
    if (connectButton) {
        connectButton.click();
    }
}
setInterval(KeepAlive, 600000); // Se ejecuta automáticamente cada 10 minutos (600,000 ms)
```
Verás un mensaje en la consola cada 10 minutos. Mientras dejes esa pestaña del navegador abierta (aunque minimices la ventana), el servidor no se caerá por inactividad.
''')

CELDA_4 = code("cell-mods", '''# @title 4. Mods Fáciles: Pega URLs o Colecciones
# @markdown ---
# @markdown ### 🧹 Control de Historial
Limpiar_Lista_Anterior = False # @param {type:"boolean"}
# @markdown _💡 Activa la casilla si quieres borrar los mods viejos del .ini y quedarte **solo** con los que pegues abajo._
# @markdown
# @markdown ### 📥 Entrada de Mods (uno por línea)
# @markdown _Pega la URL del Workshop o solo el ID numérico. Si es una colección, se expande automáticamente._
mods_input = "" # @param {type:"raw"}
# @markdown _Formato avanzado si falla la detección automática: `URL|ModIDManual`_
# @markdown
# @markdown ### 📥 Descargar Mods del Workshop
Descargar_Mods = True # @param {type:"boolean"}
# @markdown _💡 Descarga cada item vía SteamCMD y detecta el Mod ID real leyendo su `mod.info`._
# @markdown
# @markdown ### 📦 Resolver Dependencias (require=)
Descargar_Dependencias = True # @param {type:"boolean"}
# @markdown _💡 Si un mod requiere otro (require= en `mod.info`) y falta de descargar, lo busca en Workshop y lo descarga automáticamente (3 pasos, cache por sesión). Los que no encuentre, se reportan para pegarlos manualmente._
# @markdown
# @markdown ### 🗑️ Gestión rápida de mods
Eliminar_Mods = False # @param {type:"boolean"}
# @markdown _💡 Activa para listar tus mods y eliminar uno por número o WSID sin tocar el .ini a mano._
numero_a_eliminar = "" # @param {type:"string"}
# @markdown _📌 Al activar Eliminar_Mods, corre la celda → aparecerá el listado → pega el número o WSID a eliminar._
# @markdown
# @markdown **▶️ Para confirmar: ejecuta esta celda con el botón ▶ (o Ctrl+Enter). Los campos del formulario se procesan al ejecutar la celda — no hay un botón interno.**

import os, re, json, zipfile, subprocess

SAVES_PATH = '/content/drive/MyDrive/ZomboidSaves'
SERVER_PATH = '/content/pzserver'
STATE_PATH = f"{SAVES_PATH}/.pzcolab_state.json"
WS_APP = "108600"
WS_BASE = f"{SERVER_PATH}/steamapps/workshop/content/{WS_APP}"

try:
    with open(STATE_PATH) as f:
        estado = json.load(f)
    Version = estado.get("version")
    server_name = estado.get("server_name", "PzColab")
    if not Version:
        raise ValueError("sin version")
except Exception:
    Version = "b42 estable"
    server_name = "PzColab"
    print("⚠️ No se encontró el estado de la Celda 1 (.pzcolab_state.json). Se asume b42 estable.\\n")

is_b42 = Version.startswith("b42")
INI_PATH = f"{SAVES_PATH}/Server/{server_name}.ini"

print(f"📌 Versión detectada desde la Celda 1: {Version.upper()} | Servidor: {server_name}\\n")

# --- 1. EXTRAER WORKSHOP ID DE CADA LÍNEA ---
def extraer_id(linea):
    linea = linea.strip()
    if not linea:
        return None
    manual = None
    if "|" in linea:
        linea, _, manual = linea.partition("|")
        linea = linea.strip()
        manual = manual.strip() or None
    m = re.search(r'id=(\\d+)', linea) or re.search(r'(\\d{5,})', linea)
    if not m:
        return None
    return (m.group(1), manual)

entradas = []
for l in mods_input.splitlines():
    r = extraer_id(l)
    if r:
        entradas.append(r)
    elif l.strip():
        print(f"⚠️ Línea ignorada (no parece ID de Workshop): {l.strip()[:60]}")

if not entradas:
    print("ℹ️ No hay mods nuevos para procesar. Para ver los actuales usa la Celda 4.1.")
else:
    # --- 2. RESOLVER COLECCIONES + VERIFICAR COMPATIBILIDAD (1 request por item) ---
    try:
        import requests
    except ImportError:
        requests = None

    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PZColab/1.0"}

    def pagina_workshop(wsid):
        if requests is None:
            return None
        try:
            r = requests.get(f"https://steamcommunity.com/sharedfiles/filedetails/?id={wsid}", headers=HEADERS, timeout=20)
            if r.status_code == 200:
                return r.text
        except Exception:
            pass
        return None

    def es_coleccion(pagina):
        return bool(pagina) and "collectionChildren" in pagina

    def hijos_coleccion(wsid):
        if requests is None:
            return []
        for url in (f"https://steamcommunity.com/sharedfiles/filedetails/?id={wsid}&insideModal=1",
                    f"https://steamcommunity.com/sharedfiles/filedetails/?id={wsid}"):
            try:
                r = requests.get(url, headers=HEADERS, timeout=20)
                if r.status_code == 200:
                    m = re.search(r'<div[^>]*class="[^"]*collectionChildren[^"]*"[^>]*>(.*?)</div>', r.text, re.DOTALL)
                    bloque = m.group(1) if m else r.text
                    ids = re.findall(r'sharedfiles/filedetails/\\?id=(\\d+)', bloque)
                    if ids:
                        return list(dict.fromkeys(ids))
            except Exception:
                continue
        return []

    def analizar_compatibilidad(wsid, pagina):
        """Heurístico: avisa si la página del mod menciona una build distinta a la activa."""
        if not pagina:
            return None
        txt = pagina.lower()
        marca41 = bool(re.search(r'\\bb41\\b|build\\s*41', txt))
        marca42 = bool(re.search(r'\\bb42\\b|build\\s*42|42\\.\\d', txt))
        if marca41 and marca42:
            return None
        if marca42 and not is_b42:
            return f"la página menciona Build 42 pero tu servidor es {Version.upper()}"
        if marca41 and is_b42:
            return f"la página menciona Build 41 pero tu servidor es {Version.upper()}"
        return None

    # --- BÚSQUEDA DE WORKSHOP ID POR MOD ID (para resolver dependencias) ---
    deps_cache = {}  # cache por sesión: ModID -> WSID

    def buscar_wsid_por_modid(query):
        if query in deps_cache:
            return deps_cache[query]
        wsid = None
        if requests is not None:
            try:
                url = f"https://steamcommunity.com/workshop/search?searchText={query}&appid={WS_APP}"
                r = requests.get(url, headers=HEADERS, timeout=20)
                if r.status_code == 200:
                    ids = re.findall(r'sharedfiles/filedetails/\\?id=(\\d+)', r.text)
                    if ids:
                        wsid = ids[0]
            except Exception:
                pass
        deps_cache[query] = wsid
        return wsid

    def descargar_ws_item(wsid):
        """Descarga un item del Workshop vía steamcmd. Devuelve True si la carpeta quedó con contenido."""
        carpeta = f"{WS_BASE}/{wsid}"
        if os.path.isdir(carpeta) and list(os.scandir(carpeta)):
            return True
        if not os.path.isdir(WS_BASE):
            os.makedirs(WS_BASE, exist_ok=True)
        cmd = ['/usr/games/steamcmd', '+force_install_dir', SERVER_PATH, '+login', 'anonymous',
               '+workshop_download_item', WS_APP, wsid, '+quit']
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
        except Exception:
            pass
        return os.path.isdir(carpeta) and list(os.scandir(carpeta))

    final = []
    vistos = set()
    def agregar(wsid, manual):
        if wsid not in vistos:
            vistos.add(wsid)
            final.append((wsid, manual))

    avisos_compat = []
    cola = [(wsid, manual, 0) for wsid, manual in entradas]
    while cola:
        wsid, manual, prof = cola.pop(0)
        if manual:
            agregar(wsid, manual)
            continue
        pagina = pagina_workshop(wsid)
        if es_coleccion(pagina) and prof < 3:
            print(f"📂 Colección detectada: {wsid} → expandiendo...")
            for h in hijos_coleccion(wsid):
                cola.append((h, None, prof + 1))
        else:
            agregar(wsid, None)
            aviso = analizar_compatibilidad(wsid, pagina)
            if aviso:
                avisos_compat.append((wsid, aviso))

    print(f"🧾 Items a procesar: {len(final)}\\n")

    # --- 3. DESCARGAR ITEMS (opcional) ---
    if Descargar_Mods:
        if not os.path.exists(SERVER_PATH):
            print("⚠️ No se encontró la instalación del servidor. Ejecuta la Celda 1 para instalar.")
        else:
            print("📥 Descargando mods desde Steam Workshop...")
            for wsid, manual in final:
                carpeta = f"{WS_BASE}/{wsid}"
                if os.path.isdir(carpeta) and list(os.scandir(carpeta)):
                    print(f"   ✓ {wsid} ya descargado (se omite).")
                    continue
                print(f"   → Workshop ID {wsid}...")
                cmd = ['/usr/games/steamcmd', '+force_install_dir', SERVER_PATH, '+login', 'anonymous',
                       '+workshop_download_item', WS_APP, wsid, '+quit']
                r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                ok = r.returncode == 0 and os.path.isdir(carpeta) and list(os.scandir(carpeta))
                print(f"     {'✅ Descargado' if ok else '⚠️ Fallo (revisa el ID o usa el formato URL|ModIDManual)'}")
            print()

    # --- 4. DETECTAR MOD ID REAL DESDE mod.info ---
    def parse_mod_info(txt):
        mid = mname = None
        requires = []
        for line in txt.splitlines():
            line = line.strip()
            if line.startswith("id="):
                mid = line.partition("=")[2].strip()
            elif line.startswith("name="):
                mname = line.partition("=")[2].strip()
            elif line.startswith("require="):
                requires = [x.strip() for x in line.partition("=")[2].split(";") if x.strip()]
        return (mid, mname, requires)

    def detectar(wsid):
        base = f"{WS_BASE}/{wsid}"
        res = []
        if os.path.isdir(base):
            for root, dirs, files in os.walk(base):
                for fn in files:
                    if fn == "mod.info":
                        try:
                            with open(os.path.join(root, fn), encoding="utf-8", errors="ignore") as f:
                                res.append(parse_mod_info(f.read()))
                        except Exception:
                            pass
                    elif fn.lower().endswith(".zip"):
                        try:
                            with zipfile.ZipFile(os.path.join(root, fn)) as z:
                                for nombre in z.namelist():
                                    if nombre.endswith("mod.info"):
                                        res.append(parse_mod_info(z.read(nombre).decode("utf-8", errors="ignore")))
                        except Exception:
                            pass
        return [(mid, mname, requires) for mid, mname, requires in res if mid]

    def clasificar(nombre, mid):
        n = f"{nombre} {mid}".lower()
        if any(k in n for k in ("lib", "tsar", "core", "framework")): return "lib"
        if "ui" in n: return "ui"
        if any(k in n for k in ("car", "vehicle", "bike")): return "car"
        return "qol"

    nuevos = []  # (wsid, mod_id, tipo, nombre)
    requerimientos = {}
    for wsid, manual in final:
        detectados = detectar(wsid)
        if detectados:
            for mid, mname, requires in detectados:
                nuevos.append((wsid, mid, clasificar(mname, mid), mname or mid))
                if requires:
                    requerimientos[mid] = requires
        elif manual:
            nuevos.append((wsid, manual, clasificar(manual, manual), manual))
        else:
            print(f"⚠️ No se detectó el Mod ID de {wsid}. Si lo conoces, usa el formato: URL|ModID")

    # --- 5. MERGE CON HISTORIAL DEL .ini (sin duplicados) ---
    if not os.path.exists(INI_PATH):
        print("❌ ERROR: No se encontró el archivo INI. Inicia el servidor una vez (Celda 2) para generarlo.")
    else:
        with open(INI_PATH, 'r') as f:
            ini_lines = f.readlines()
        ini_content = "".join(ini_lines)

        base = []
        if not Limpiar_Lista_Anterior:
            ws_match = re.search(r'^WorkshopItems=(.*)', ini_content, re.MULTILINE)
            mod_match = re.search(r'^Mods=(.*)', ini_content, re.MULTILINE)
            ws_list = [x.strip() for x in ws_match.group(1).split(';') if x.strip()] if ws_match and ws_match.group(1).strip() else []
            mod_list = [x.strip().replace('\\\\', '') for x in mod_match.group(1).split(';') if x.strip()] if mod_match and mod_match.group(1).strip() else []
            for i in range(min(len(ws_list), len(mod_list))):
                base.append((ws_list[i], mod_list[i], "qol", mod_list[i]))
        else:
            print("🧹 Historial limpiado. Solo se escribirán los mods pegados.\\n")

        combinada = list(nuevos)
        vistos_ws = {m[0] for m in combinada}
        for b in base:
            if b[0] not in vistos_ws:
                vistos_ws.add(b[0])
                combinada.append(b)

        # Orden de carga: librerías primero, luego UI, vehículos y QoL
        peso = {"lib": 0, "ui": 1, "car": 2, "qol": 3}
        combinada.sort(key=lambda m: peso.get(m[2], 3))

        if not combinada:
            print("⚠️ No hay mods activos para escribir en el servidor.")
        else:
            ws_ids = [m[0] for m in combinada]
            mod_ids = [m[1] for m in combinada]
            workshop_str = f"WorkshopItems={';'.join(ws_ids)}\\n"
            mod_str = f"Mods={';'.join([f'\\\\{m}' if is_b42 else m for m in mod_ids])}\\n"

            ws_found, mod_found = False, False
            for idx, line in enumerate(ini_lines):
                if line.startswith("WorkshopItems="):
                    ini_lines[idx] = workshop_str
                    ws_found = True
                elif line.startswith("Mods="):
                    ini_lines[idx] = mod_str
                    mod_found = True
            if not ws_found:
                ini_lines.append(workshop_str)
            if not mod_found:
                ini_lines.append(mod_str)

            with open(INI_PATH, 'w') as f:
                f.writelines(ini_lines)

            # --- 6. REPORTE CON NOMBRES REALES ---
            iconos = {"lib": "📚", "ui": "🖥️", "car": "🚗", "qol": "⚙️"}
            totales = {}
            for m in combinada:
                totales[m[2]] = totales.get(m[2], 0) + 1
            print("=" * 60)
            print(f"📋 MODS EN EL SERVIDOR (Total: {len(combinada)})")
            print(f"📊 Resumen: {totales.get('lib', 0)} lib · {totales.get('ui', 0)} ui · {totales.get('car', 0)} car · {totales.get('qol', 0)} qol")
            print("=" * 60)
            for wsid, mid, tipo, nombre in combinada:
                print(f"   {iconos.get(tipo, '⚙️')} {nombre} ({tipo}) | Workshop: {wsid}")
                reqs = requerimientos.get(mid)
                if reqs:
                    print(f"      🔗 Requiere: {', '.join(reqs)}")
            print("-" * 60)

            faltantes = []
            # Mod IDs disponibles en el filesystem (descargados previamente, aunque no estén en la lista)
            ids_en_filesystem = set()
            wsids_existentes = set()
            if os.path.isdir(WS_BASE):
                for wsid_dir in os.listdir(WS_BASE):
                    wsids_existentes.add(wsid_dir)
                    for mid, mname, requires in detectar(wsid_dir):
                        ids_en_filesystem.add(mid)
            ids_configurados = {m[1] for m in combinada} | ids_en_filesystem
            for mid, reqs in requerimientos.items():
                for req in reqs:
                    if req not in ids_configurados:
                        faltantes.append((mid, req))
            if faltantes:
                if Descargar_Dependencias and os.path.isdir(WS_BASE):
                    print("\\n🔎 Resolviendo dependencias faltantes vía Workshop (máx. 3 pasos)...")
                    pasada = 0
                    while faltantes and pasada < 3:
                        pasada += 1
                        nuevos_wsids = []
                        for mid, req in faltantes:
                            wsid = buscar_wsid_por_modid(req)
                            if wsid:
                                # Si ya está descargado en el filesystem, no volver a descargar, solo enlazarlo
                                if wsid in wsids_existentes:
                                    print(f"   🔗 {req} -> Workshop {wsid} (ya descargado, se enlaza)")
                                    if wsid not in vistos_ws:
                                        nuevos_wsids.append(wsid)
                                else:
                                    print(f"   🔗 {req} -> Workshop {wsid} (descargando, paso {pasada})...")
                                    if descargar_ws_item(wsid):
                                        nuevos_wsids.append(wsid)
                                        wsids_existentes.add(wsid)
                                    else:
                                        print(f"   ⚠️ Falló la descarga de {req} (Workshop {wsid}).")
                            else:
                                print(f"   ⚠️ '{req}' no encontrado en Workshop. Agrégalo manualmente si existe.")
                        # Reanalizar las dependencias recién descargadas/enlazadas
                        if nuevos_wsids:
                            for wsid in nuevos_wsids:
                                for mid2, mname2, requires2 in detectar(wsid):
                                    nuevos.append((wsid, mid2, clasificar(mname2, mid2), mname2 or mid2))
                                    if requires2:
                                        requerimientos[mid2] = requires2
                        # Rehacer merge con los mods nuevos + historial
                        combinada = list(nuevos)
                        vistos_ws = {m[0] for m in combinada}
                        for b in base:
                            if b[0] not in vistos_ws:
                                vistos_ws.add(b[0])
                                combinada.append(b)
                        peso = {"lib": 0, "ui": 1, "car": 2, "qol": 3}
                        combinada.sort(key=lambda m: peso.get(m[2], 3))
                        # Reescribir .ini con la combinada actualizada
                        ws_ids = [m[0] for m in combinada]
                        mod_ids = [m[1] for m in combinada]
                        workshop_str = f"WorkshopItems={';'.join(ws_ids)}\\n"
                        mod_str = f"Mods={';'.join([f'\\\\{m}' if is_b42 else m for m in mod_ids])}\\n"
                        ws_found, mod_found = False, False
                        for idx, line in enumerate(ini_lines):
                            if line.startswith("WorkshopItems="):
                                ini_lines[idx] = workshop_str; ws_found = True
                            elif line.startswith("Mods="):
                                ini_lines[idx] = mod_str; mod_found = True
                        if not ws_found:
                            ini_lines.append(workshop_str)
                        if not mod_found:
                            ini_lines.append(mod_str)
                        with open(INI_PATH, 'w') as f:
                            f.writelines(ini_lines)
                        # Reevaluar faltantes (ya descargados pasan a ids_en_filesystem)
                        for wsid in nuevos_wsids:
                            for mid, mname, requires in detectar(wsid):
                                ids_en_filesystem.add(mid)
                        ids_configurados = {m[1] for m in combinada} | ids_en_filesystem
                        faltantes = []
                        for mid, reqs in requerimientos.items():
                            for req in reqs:
                                if req not in ids_configurados:
                                    faltantes.append((mid, req))
                if faltantes:
                    print("\\n⚠️ DEPENDENCIAS FALTANTES:")
                    for mid, req in faltantes:
                        print(f"   El mod '{mid}' requiere '{req}', que no está en la lista. Agrégalo o el servidor puede no cargar.")

            if avisos_compat:
                print("\\n🔎 POSIBLES INCOMPATIBILIDADES DE VERSIÓN (heurístico, verifica en el Workshop):")
                for wsid, motivo in avisos_compat:
                    print(f"   ⚠️ Workshop {wsid}: {motivo}")
                print("   Si el mod no carga, revisa su página para confirmar compatibilidad.")

            print(f"✅ .ini actualizado: {INI_PATH}")
            print("   Reinicia el servidor (Celda 2) para aplicar los mods.")

# --- 7. GESTIÓN RÁPIDA: ELIMINAR MODS (independiente de pegar mods) ---
if Eliminar_Mods and os.path.exists(INI_PATH):
    def _parse_mod_info(txt):
        mid = mname = None
        for line in txt.splitlines():
            line = line.strip()
            if line.startswith("id="):
                mid = line.partition("=")[2].strip()
            elif line.startswith("name="):
                mname = line.partition("=")[2].strip()
        return (mid, mname)

    def _detectar_mods(wsid):
        res = []
        base = f"{WS_BASE}/{wsid}"
        if os.path.isdir(base):
            for root, dirs, files in os.walk(base):
                for fn in files:
                    if fn == "mod.info":
                        try:
                            with open(os.path.join(root, fn), encoding="utf-8", errors="ignore") as f:
                                mid, mname = _parse_mod_info(f.read())
                                if mid:
                                    res.append((mid, mname))
                        except Exception:
                            pass
                    elif fn.lower().endswith(".zip"):
                        try:
                            with zipfile.ZipFile(os.path.join(root, fn)) as z:
                                for nombre in z.namelist():
                                    if nombre.endswith("mod.info"):
                                        mid, mname = _parse_mod_info(z.read(nombre).decode("utf-8", errors="ignore"))
                                        if mid:
                                            res.append((mid, mname))
                        except Exception:
                            pass
        return res

    with open(INI_PATH, 'r') as f:
        ini_lines2 = f.readlines()
    ini2 = "".join(ini_lines2)
    ws_m = re.search(r'^WorkshopItems=(.*)', ini2, re.MULTILINE)
    mod_m = re.search(r'^Mods=(.*)', ini2, re.MULTILINE)
    ws_list2 = [x.strip() for x in ws_m.group(1).split(';') if x.strip()] if ws_m and ws_m.group(1).strip() else []
    mod_list2 = [x.strip().replace('\\\\', '') for x in mod_m.group(1).split(';') if x.strip()] if mod_m and mod_m.group(1).strip() else []
    nombre_por_wsid = {}
    for wsid in ws_list2:
        for mid, mname in _detectar_mods(wsid):
            nombre_por_wsid[wsid] = (mname or mid)
    print("-" * 60)
    print("🗑️ MODS ACTIVOS (usa el número o el WSID para eliminar):")
    print("-" * 60)
    for i, wsid in enumerate(ws_list2):
        nom = nombre_por_wsid.get(wsid, mod_list2[i] if i < len(mod_list2) else wsid)
        print(f"  [{i}] 📦 {nom} | Workshop: {wsid}")
    print("-" * 60)
    blanco = numero_a_eliminar.strip()
    if blanco:
        indice_a_borrar = None
        if blanco.isdigit() and int(blanco) < len(ws_list2):
            indice_a_borrar = int(blanco)
        elif blanco in ws_list2:
            indice_a_borrar = ws_list2.index(blanco)
        if indice_a_borrar is not None:
            borrado = ws_list2.pop(indice_a_borrar)
            if indice_a_borrar < len(mod_list2):
                mod_list2.pop(indice_a_borrar)
            print(f"🗑️  Elimando: {nombre_por_wsid.get(borrado, borrado)} (WSID: {borrado})")
            nuevo_ws = ';'.join(ws_list2)
            nuevo_mod = ';'.join([f'\\\\{m}' if is_b42 else m for m in mod_list2])
            for idx, line in enumerate(ini_lines2):
                if line.startswith("WorkshopItems="):
                    ini_lines2[idx] = f"WorkshopItems={nuevo_ws}\\n"
                elif line.startswith("Mods="):
                    ini_lines2[idx] = f"Mods={nuevo_mod}\\n"
            with open(INI_PATH, 'w') as f:
                f.writelines(ini_lines2)
            print(f"✅ {borrado} eliminado del .ini. Reinicia el servidor (Celda 2).")
        else:
            print("⚠️ Número o WSID inválido. Revisa la lista y vuelve a intentarlo.")
''')


CELDA_4_1 = code("cell-diagnostico", '''# @title 🔍 4.1 Inspector y Diagnóstico Avanzado de Servidor
# @markdown _Muestra tus mods activos y analiza los logs agrupando errores por mod e identificando culpables reales._

import os, re, json

SAVES_PATH = '/content/drive/MyDrive/ZomboidSaves'
try:
    with open(f"{SAVES_PATH}/.pzcolab_state.json") as f:
        server_name = json.load(f).get("server_name", "PzColab")
except Exception:
    server_name = "PzColab"
INI_PATH = f"{SAVES_PATH}/Server/{server_name}.ini"

# --- PARTE 1: LECTURA DE MODS ---
print("=========================================================")
print("👁️  MODS CONFIGURADOS EN EL SERVIDOR")
print("=========================================================")

if not os.path.exists(INI_PATH):
    print("❌ No se encontró ningún archivo de configuración .ini.")
else:
    with open(INI_PATH, 'r') as f:
        content = f.read()

    ws_match = re.search(r'^WorkshopItems=(.*)', content, re.MULTILINE)
    mod_match = re.search(r'^Mods=(.*)', content, re.MULTILINE)

    ws_list = [x.strip() for x in ws_match.group(1).split(';') if x.strip()] if ws_match and ws_match.group(1).strip() else []
    mod_list = [x.strip().replace('\\\\', '') for x in mod_match.group(1).split(';') if x.strip()] if mod_match and mod_match.group(1).strip() else []
    total_mods = min(len(ws_list), len(mod_list))

    def nombre_amigable(wsid, fallback):
        base = f"/content/pzserver/steamapps/workshop/content/108600/{wsid}"
        if os.path.isdir(base):
            for root, dirs, files in os.walk(base):
                if "mod.info" in files:
                    try:
                        with open(os.path.join(root, "mod.info"), encoding="utf-8", errors="ignore") as f:
                            for line in f:
                                if line.strip().startswith("name="):
                                    return line.partition("=")[2].strip() or fallback
                    except Exception:
                        pass
        return fallback

    if total_mods > 0:
        for i in range(total_mods):
            mid = mod_list[i]
            tag = "📦 Mod"
            if "lib" in mid.lower() or "tsar" in mid.lower(): tag = "📚 Lib"
            elif "ui" in mid.lower(): tag = "🖥️ UI"
            elif "car" in mid.lower() or "vehicle" in mid.lower(): tag = "🚗 Car"
            print(f"[{i+1:>2}] {tag} ➡️ {nombre_amigable(ws_list[i], mid):<28} | Workshop: {ws_list[i]}")
    else:
        print("⚠️ El archivo .ini no tiene mods configurados.")
print("=========================================================\\n")

# --- PARTE 2: DIAGNÓSTICO INTELIGENTE ---
print("🔍 INICIANDO ESCANEO AVANZADO DE LOGS...")
print("=========================================================")

log_files = []
for subdir in ("Server", "Logs"):
    base = os.path.join(SAVES_PATH, subdir)
    if not os.path.isdir(base):
        continue
    for root, dirs, files in os.walk(base):
        for file in files:
            if file.endswith('.txt') and ('debuglog' in file.lower() or 'console' in file.lower()):
                log_files.append(os.path.join(root, file))

if not log_files:
    print("ℹ️ No se encontraron archivos de registro activos.")
else:
    ULTIMO_LOG = max(log_files, key=os.path.getmtime)
    print(f"📖 Analizando incidencias en: MIdrive/{ULTIMO_LOG.replace('/content/drive/MyDrive/', '')}\\n")

    with open(ULTIMO_LOG, 'r', encoding='utf-8', errors='ignore') as f:
        log_lines = f.readlines()

    fallos_criticos = []
    alertas_esteticas = []
    errores_steam = []
    problemas_memoria = []
    errores_servidor = []
    fallos_guardado = []

    # Diccionario para contar qué mods están dando más guerra
    mods_culpables = {}

    for idx, line in enumerate(log_lines):
        line_lower = line.lower()
        num_linea = idx + 1

        # 1. DETECTAR CRASHES O ERRORES LUA
        if "lua error" in line_lower or "stack trace" in line_lower or "call stack" in line_lower:
            # Rastrear contexto (buscar el nombre del mod culpable en las 4 líneas cercanas)
            contexto = "Desconocido (Script interno)"
            for k in range(max(0, idx-2), min(len(log_lines), idx+3)):
                match_mod = re.search(r'(media/lua/[^\\s]+|mods/([^/\\s]+))', log_lines[k])
                if match_mod:
                    contexto = match_mod.group(1)
                    break

            fallos_criticos.append((num_linea, line.strip(), contexto))
            mods_culpables[contexto] = mods_culpables.get(contexto, 0) + 1

        # 2. DETECTAR FALLOS DE STEAM WORKSHOP
        elif "workshop" in line_lower and ("fail" in line_lower or "error" in line_lower or "rejected" in line_lower):
            errores_steam.append(f"[Línea {num_linea}] 🌐 Fallo Steam ➡️ {line.strip()}")

        # 3. DETECTAR PROBLEMAS DE MEMORIA
        elif ("outofmemory" in line_lower or "out of memory" in line_lower or "gc overhead" in line_lower
              or "heap space" in line_lower or "could not reserve enough space" in line_lower
              or "insufficient memory" in line_lower):
            problemas_memoria.append(f"[Línea {num_linea}] 🧠 ➡️ {line.strip()[:110]}")

        # 4. DETECTAR ERRORES GENERALES DEL SERVIDOR (puertos, assert, steam)
        elif ("failed to bind" in line_lower or "address already in use" in line_lower
              or "assertion failed" in line_lower or "illegal worker thread" in line_lower
              or ("steam" in line_lower and ("timeout" in line_lower or "not responding" in line_lower))):
            errores_servidor.append(f"[Línea {num_linea}] ⚠️ ➡️ {line.strip()[:110]}")

        # 5. DETECTAR FALLOS AL GUARDAR
        elif "failed to save" in line_lower or ("save" in line_lower and ("corrupt" in line_lower or "failed" in line_lower)):
            fallos_guardado.append(f"[Línea {num_linea}] 💾 ➡️ {line.strip()[:110]}")

        # 6. FILTRAR ALERTAS MENORES (Evita alarmar por sonidos o vallas rotas)
        elif "missing" in line_lower and ("thumpsound" in line_lower or "tile" in line_lower or "media/sound" in line_lower):
            alertas_esteticas.append(f"[Línea {num_linea}] 📝 Detalle ➡️ {line.strip()[:90]}...")

    # --- DESPLIEGUE DEL REPORTE RESUMIDO ---
    if fallos_criticos or errores_steam or alertas_esteticas or problemas_memoria or errores_servidor or fallos_guardado:

        if problemas_memoria:
            print(f"🧠 PROBLEMAS DE MEMORIA: {len(problemas_memoria)}")
            for err in problemas_memoria[:3]: print(f"   {err}")
            print("   💡 Sube la memoria en la Celda 3 (máx 8 GB) o reduce MaxPlayers/mods pesados.")
            print("-" * 60)

        if errores_servidor:
            print(f"⚠️ ERRORES DEL SERVIDOR: {len(errores_servidor)}")
            for err in errores_servidor[:3]: print(f"   {err}")
            print("-" * 60)

        if fallos_guardado:
            print(f"💾 FALLOS DE GUARDADO: {len(fallos_guardado)}")
            for err in fallos_guardado[:3]: print(f"   {err}")
            print("-" * 60)

        if fallos_criticos:
            print(f"🔴 Errores de Lua/Crashes Detectados: {len(fallos_criticos)}")
            print("👑 MODS O ARCHIVOS MÁS INESTABLES:")
            for mod, count in sorted(mods_culpables.items(), key=lambda x: x[1], reverse=True)[:3]:
                print(f"   ⚠️ -> '{mod}' generó {count} alertas en este arranque.")
            print("\\n📌 Muestra de las primeras líneas de error:")
            for num, _, ctx in fallos_criticos[:4]:
                print(f"   [Línea {num}] Script: {ctx}")
            print("-" * 60)

        if errores_steam:
            print(f"\\n🌐 Problemas con Steam Workshop: {len(errores_steam)}")
            for err in errores_steam[:3]: print(f"   {err}")
            print("-" * 60)

        if alertas_esteticas:
            print(f"\\n📝 Alertas Menores o Estéticas (No rompen el servidor): {len(alertas_esteticas)}")
            print("   💡 _Nota: Son sonidos faltantes o vallas del mapa original. Ignorables._")
            for err in alertas_esteticas[:3]: print(f"   {err}")
            print("-" * 60)

        print("\\n🛠️ DIAGNÓSTICO FINAL:")
        if fallos_criticos:
            print("   El servidor inició, pero hay mods con scripts obsoletos. Si notas lag visual o items invisibles,")
            print("   revisa los mods indicados en el top de inestabilidad.")
        elif problemas_memoria:
            print("   El servidor se quedó sin memoria. Aumenta la memoria en la Celda 3 (máx 8 GB) o reduce jugadores/mods.")
        elif errores_servidor:
            print("   Hay errores de red/puerto o del propio servidor. Revisa las líneas señaladas arriba.")
        elif fallos_guardado:
            print("   Hubo fallos al guardar el mundo. Verifica el espacio en Drive y usa la Celda 3.2 para un apagado limpio.")
        else:
            print("   ¡Estable! El servidor no registra problemas de programación críticos en los mods.")
    else:
        print("✅ ¡SISTEMA 100% LIMPIO! Logs impecables y listos para jugar.")

print("=========================================================")
''')

CELDA_5 = code("cell-backup", '''# @title 5. Backup de Saves (Drive)
# @markdown _Crea un respaldo .tar.gz del mundo y la configuración en tu Google Drive._
Backup_Max_Guardar = 3 # @param {type: "integer"}
# @markdown _💡 Retención: se conservan los últimos N backups._
# @markdown
# @markdown ### ♻️ Restaurar un backup
Restaurar_Backup = False # @param {type: "boolean"}
# @markdown _💡 Activa para listar tus backups y restaurar uno (reemplaza tu save actual)._
numero_backup = 0 # @param {type: "integer"}
# @markdown _📌 Usa el número que aparece al listar (0 = más reciente, 1 = anterior...)._

import os, glob, time, tarfile

SAVES_PATH = "/content/drive/MyDrive/ZomboidSaves"
BACKUP_DIR = "/content/drive/MyDrive/ZomboidSaves_backups"

def _rotar_logs():
    """Conservar sólo los 20 logs más recientes, borrar el resto."""
    LOGS_DIR = os.path.join(SAVES_PATH, "Logs")
    if os.path.isdir(LOGS_DIR):
        logs = sorted(glob.glob(os.path.join(LOGS_DIR, "*")), key=os.path.getmtime)
        for viejo in logs[:-20]:
            try:
                os.remove(viejo)
            except Exception:
                pass

def _tar_filter(ti):
    if ti.name.startswith("ZomboidSaves/Logs"):
        return None
    return ti

if not os.path.exists("/content/drive"):
    print("❌ Drive no montado. Ejecuta primero la Celda 1.")
else:
    os.makedirs(BACKUP_DIR, exist_ok=True)
    if Restaurar_Backup:
        backups = sorted(glob.glob(f"{BACKUP_DIR}/ZomboidSaves_*.tar.gz"), key=os.path.getmtime, reverse=True)
        if not backups:
            print("📭 No hay backups disponibles para restaurar.")
        else:
            print("📋 Backups disponibles (más reciente primero):")
            for i, b in enumerate(backups):
                sz = os.path.getsize(b) / (1024 * 1024)
                print(f"  [{i}] {os.path.basename(b)} ({sz:.1f} MB)")
            idx = max(0, min(numero_backup, len(backups) - 1))
            eleccion = backups[idx]
            ts = time.strftime("%Y%m%d_%H%M%S")
            respaldo_previo = f"{BACKUP_DIR}/previo_a_restore_{ts}.tar.gz"
            print(f"⚠️  RESTAURACIÓN: {os.path.basename(eleccion)} reemplazará tu save actual.")
            print(f"   Se guarda un backup de seguridad en: {os.path.basename(respaldo_previo)}")
            with tarfile.open(respaldo_previo, "w:gz") as tar:
                tar.add(SAVES_PATH, arcname="ZomboidSaves", recursive=True, filter=_tar_filter)
            with tarfile.open(eleccion, "r:gz") as tar:
                tar.extractall(path=os.path.dirname(SAVES_PATH), filter="data")
            print(f"✅ Restore completado: {os.path.basename(eleccion)} → {SAVES_PATH}")
            print("   Reinicia el servidor (Celda 2) para aplicar.")
    else:
        if not os.path.isdir(SAVES_PATH):
            os.makedirs(SAVES_PATH, exist_ok=True)
        _rotar_logs()
        ts = time.strftime("%Y%m%d_%H%M%S")
        destino = f"{BACKUP_DIR}/ZomboidSaves_{ts}_{int(time.time() * 1000) % 100000:05d}.tar.gz"
        print("📦 Creando backup (según el tamaño del mundo puede tardar unos minutos)...")
        with tarfile.open(destino, "w:gz") as tar:
            tar.add(SAVES_PATH, arcname="ZomboidSaves", recursive=True, filter=_tar_filter)
        tamaño_mb = os.path.getsize(destino) / (1024 * 1024)
        print(f"✅ Backup creado: {destino} ({tamaño_mb:.1f} MB)")

        backups = sorted(glob.glob(f"{BACKUP_DIR}/ZomboidSaves_*.tar.gz"), key=os.path.getmtime)
        max_guardar = max(1, Backup_Max_Guardar)
        for viejo in backups[:-max_guardar]:
            os.remove(viejo)
        print(f"📊 Backups conservados: {len(backups)} (máximo {max_guardar})")
        print(f"📂 Carpeta de backups: {BACKUP_DIR}")
''')

cells = [
    BADGE,
    INDICE,
    CELDA_1,
    CELDA_3,
    CELDA_4,
    CELDA_4_1,
    CELDA_5,
    ANTI_AFK,
]

# --- Versión EN: se deriva de la ES aplicando la tabla de traducción ---
from traducciones import traducir

cells_en = []
for c in cells:
    nuevo_src = traducir("".join(c["source"]))
    if c["cell_type"] == "code":
        cells_en.append(code(c["metadata"]["id"], nuevo_src))
    else:
        cells_en.append(md(nuevo_src))

# --- VALIDAR sintaxis de cada celda de código ---
# Los magics de IPython (! y %) no son Python válido: se reemplazan por 'pass'
# conservando el número de líneas para reportar errores correctamente.
def pythonify(src):
    out = []
    for linea in src.splitlines():
        if linea.lstrip().startswith(("!", "%")):
            indent = linea[: len(linea) - len(linea.lstrip())]
            out.append(indent + "pass")
        else:
            out.append(linea)
    return "\n".join(out)

def validar(conjunto, nombre):
    print(f"--- Validación {nombre} ---")
    for c in conjunto:
        if c["cell_type"] == "code":
            src = "".join(c["source"])
            try:
                compile(pythonify(src), c["metadata"]["id"], "exec")
            except SyntaxError as e:
                print(f"❌ SYNTAX ERROR en celda {c['metadata']['id']} (línea {e.lineno}): {e.msg}")
                print(src.splitlines()[max(0, (e.lineno or 1) - 1)])
                sys.exit(1)
            print(f"✅ Celda {c['metadata']['id']} OK ({len(c['source'])} líneas)")

validar(cells, "ES (PZ_Colab_ES.ipynb)")
validar(cells_en, "EN (PZ_Colab_EN.ipynb)")

def armar_notebook(conjunto):
    return {
        "cells": conjunto,
        "metadata": {
            "colab": {
                "provenance": [],
                "authorship_tag": "ABX9TyOK4967SsJq9nglXPaeJNpq",
                "include_colab_link": True
            },
            "kernelspec": {
                "display_name": "Python 3",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 0
    }

TARGET_EN = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else ROOT / "PZ_Colab_EN.ipynb"

with open(TARGET, "w", encoding="utf-8") as f:
    json.dump(armar_notebook(cells), f, ensure_ascii=False, indent=1)

with open(TARGET_EN, "w", encoding="utf-8") as f:
    json.dump(armar_notebook(cells_en), f, ensure_ascii=False, indent=1)

print(f"\n✅ Notebook ES generado: {TARGET}")
print(f"✅ Notebook EN generado: {TARGET_EN}")
