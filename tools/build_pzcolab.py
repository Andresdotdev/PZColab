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
| 2 | 🔗 Configurar el túnel Playit (solo la 1ª vez) |
| 3 | 🔥 Encender el servidor (con watchdog) |
| 3.1 | 📄 Consola del servidor en vivo |
| 3.2 | 🛑 Apagado limpio del servidor |
| 4 | 📦 Mods: inyección + descarga Workshop |
| 4.1 | 🩺 Diagnóstico de logs por mod |
| 5 | 💾 Backup de saves en Drive |

_Flujo típico: 1 → 2 → 3 → (3.1 opcional) → 3.2 al terminar. Las celdas 4, 4.1 y 5 se usan bajo demanda._
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

    os.makedirs(SERVER_PATH, exist_ok=True)
    cmd = ['/usr/games/steamcmd', '+force_install_dir', SERVER_PATH, '+login', 'anonymous', '+app_update', '380870'] + beta_args(Version) + ['+quit']

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    progreso = {}
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
    process.wait()

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

CELDA_2 = code("cell-playit", '''# @title 2. Configurar Playit.gg Persistente

import os

PLAYIT_DRIVE = "/content/drive/MyDrive/ZomboidSaves/playitgg"
PLAYIT_CONFIG = "/root/.config/playit_gg"

if not os.path.exists("/content/drive"):
    print("❌ Google Drive NO está montado. Ejecuta primero la Celda 1.")
else:
    # Matar instancias anteriores
    !pkill -f playit 2>/dev/null

    # Crear carpeta persistente
    os.makedirs(PLAYIT_DRIVE, exist_ok=True)

    # Si no existe config local, enlazar Drive
    if os.path.exists(PLAYIT_CONFIG):
        !rm -rf {PLAYIT_CONFIG}

    !ln -s {PLAYIT_DRIVE} {PLAYIT_CONFIG}

    print("✅ Configuración persistente enlazada.")

    ya_configurado = any(os.scandir(PLAYIT_DRIVE)) if os.path.isdir(PLAYIT_DRIVE) else False
    if ya_configurado:
        print("ℹ️ Ya existe un túnel configurado en Drive. Esta celda es OPCIONAL en re-ejecuciones;")
        print("   úsala solo si necesitas reclamar un túnel nuevo.")

    print("🚀 Iniciando Playit...")
    print("⚠️ SOLO la primera vez tendrás que reclamar el túnel.")
    print("=" * 50)

    !playit
''')

CELDA_3 = code("cell-iniciar", '''# @title 3. Iniciar Servidor (Watchdog + Config Avanzada)
# @markdown ---
# @markdown ### 🎮 Parámetros del Servidor
server_name = 'PzColab' # @param {type: "string"}
admin_password = '' # @param {type: "string"}
server_password = '' # @param {type: "string"}
port = 16261 # @param {type: "integer"}
max_players = 16 # @param {type: "integer"}
pausa_cuando_vacio = True # @param {type: "boolean"}
# @markdown _💡 Si cambias el puerto, actualiza el túnel en playit.gg._
# @markdown
# @markdown ### 🛡️ Watchdog (auto-reinicio ante crashes)
watchdog_activo = True # @param {type: "boolean"}
max_reinicios = 3 # @param {type: "integer"}

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

# --- 2. PLAYIT EN SEGUNDO PLANO ---
os.system("pkill -f playit 2>/dev/null")
os.system("nohup playit > /tmp/playit.log 2>&1 &")
print("✅ Túnel Playit encendido en el fondo.")

# --- 3. LANZAR SERVIDOR EN SEGUNDO PLANO CON WATCHDOG ---
if not os.path.exists("/content/pzserver/start-server.sh"):
    abortar("❌ No se encontró start-server.sh. Ejecuta primero la Celda 1 (instalación).")

os.system("chmod +x /content/pzserver/start-server.sh 2>/dev/null")

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
print(f"📄 Consola en vivo: Celda 3.1 (tail de {LOG_PATH})")
print("🛑 Apagado limpio: Celda 3.2")
if watchdog_activo:
    print(f"🛡️ Watchdog activo: hasta {max_reinicios} reinicios automáticos.")
''')

CELDA_3_1 = code("cell-consola", '''# @title 3.1 Consola en Vivo del Servidor (tail)
# @markdown _Ejecuta esta celda para ver la consola del servidor en tiempo real._
# @markdown _Para detenerla, presiona el botón ⏹ (Interrumpir ejecución)._

import os

LOG_PATH = "/tmp/pzserver.log"

if not os.path.exists(LOG_PATH):
    print("⚠️ Todavía no hay log. Ejecuta primero la Celda 3.")
else:
    print("📄 Mostrando últimas 40 líneas + seguimiento en vivo (⏹ para salir)...\\n")
    get_ipython().system(f"tail -n 40 -f {LOG_PATH}")
''')

CELDA_3_2 = code("cell-apagar", '''# @title 3.2 Apagado Limpio del Servidor
# @markdown _Guarda el mundo (save) y apaga el servidor de forma ordenada._

import os
import time
import subprocess

try:
    pz_proc
except NameError:
    pz_proc = None
try:
    parada
except NameError:
    parada = None

if pz_proc and pz_proc.poll() is None and pz_proc.stdin:
    if parada:
        parada.set()
    print("💾 Enviando SAVE...")
    pz_proc.stdin.write("save\\n")
    pz_proc.stdin.flush()
    time.sleep(15)
    print("🛑 Enviando QUIT...")
    pz_proc.stdin.write("quit\\n")
    pz_proc.stdin.flush()
    try:
        pz_proc.wait(timeout=90)
        print("✅ Servidor apagado de forma segura.")
    except subprocess.TimeoutExpired:
        print("⚠️ No respondió a tiempo; forzando cierre.")
        pz_proc.terminate()
else:
    print("⚠️ El proceso del servidor no está accesible en esta sesión (runtime reiniciado?).")
    print("   Intentando pkill suave...")
    os.system("pkill -TERM -f ProjectZomboid64 2>/dev/null; sleep 10; pkill -KILL -f ProjectZomboid64 2>/dev/null")
    print("✅ Señales de terminación enviadas.")
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
        print("❌ ERROR: No se encontró el archivo INI. Inicia el servidor una vez (Celda 3) para generarlo.")
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
            ids_configurados = {m[1] for m in combinada}
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
            print("   Reinicia el servidor (Celda 3) para aplicar los mods.")
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

        # 3. FILTRAR ALERTAS MENORES (Evita alarmar por sonidos o vallas rotas)
        elif "missing" in line_lower and ("thumpsound" in line_lower or "tile" in line_lower or "media/sound" in line_lower):
            alertas_esteticas.append(f"[Línea {num_linea}] 📝 Detalle ➡️ {line.strip()[:90]}...")

    # --- DESPLIEGUE DEL REPORTE RESUMIDO ---
    if fallos_criticos or errores_steam or alertas_esteticas:

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
        else:
            print("   ¡Estable! El servidor no registra problemas de programación críticos en los mods.")
    else:
        print("✅ ¡SISTEMA 100% LIMPIO! Logs impecables y listos para jugar.")

print("=========================================================")
''')

CELDA_5 = code("cell-backup", '''# @title 5. Backup de Saves (Drive)
# @markdown _Crea un respaldo .tar.gz del mundo y la configuración en tu Google Drive._
Backup_Max_Guardar = 3 # @param {type: "integer"}

import os, glob, time, tarfile

SAVES_PATH = "/content/drive/MyDrive/ZomboidSaves"
BACKUP_DIR = "/content/drive/MyDrive/ZomboidSaves_backups"

if not os.path.exists("/content/drive"):
    print("❌ Drive no montado. Ejecuta primero la Celda 1.")
else:
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    destino = f"{BACKUP_DIR}/ZomboidSaves_{ts}.tar.gz"
    print("📦 Creando backup (según el tamaño del mundo puede tardar unos minutos)...")
    with tarfile.open(destino, "w:gz") as tar:
        tar.add(SAVES_PATH, arcname="ZomboidSaves", recursive=True)
    tamaño_mb = os.path.getsize(destino) / (1024 * 1024)
    print(f"✅ Backup creado: {destino} ({tamaño_mb:.1f} MB)")

    backups = sorted(glob.glob(f"{BACKUP_DIR}/ZomboidSaves_*.tar.gz"))
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
    CELDA_2,
    CELDA_3,
    CELDA_3_1,
    CELDA_3_2,
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
