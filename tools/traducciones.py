# -*- coding: utf-8 -*-
"""Tabla de traducción ES->EN para la UI del notebook (strings de usuario).
Se aplica a las celdas ES para generar PZ_Colab_EN.ipynb. La lógica no cambia.
"""

TRADUCCIONES = [
    # --- Markdown: índice ---
    (
        "🗺️ **Guía rápida del cuaderno**",
        "🗺️ **Quick Notebook Guide**",
    ),
    (
        "| Celda | Acción |",
        "| Cell | Action |",
    ),
    (
        "| 1 | 🚀 Instalar el servidor (elegir versión b42 / b41) |",
        "| 1 | 🚀 Install the server (choose b42 / b41 version) |",
    ),
    (
        "| 2 | 🔗 Configurar el túnel Playit (solo la 1ª vez) |",
        "| 2 | 🔗 Set up the Playit tunnel (first time only) |",
    ),
    (
        "| 3 | 🔥 Encender el servidor (con watchdog) |",
        "| 3 | 🔥 Start the server (with watchdog) |",
    ),
    (
        "| 3.1 | 📄 Consola del servidor en vivo |",
        "| 3.1 | 📄 Live server console |",
    ),
    (
        "| 3.2 | 🛑 Apagado limpio del servidor |",
        "| 3.2 | 🛑 Clean server shutdown |",
    ),
    (
        "| 4 | 📦 Mods: inyección + descarga Workshop |",
        "| 4 | 📦 Mods: injection + Workshop download |",
    ),
    (
        "| 4.1 | 🩺 Diagnóstico de logs por mod |",
        "| 4.1 | 🩺 Per-mod log diagnostics |",
    ),
    (
        "| 5 | 💾 Backup de saves en Drive |",
        "| 5 | 💾 Saves backup on Drive |",
    ),
    (
        "_Flujo típico: 1 → 2 → 3 → (3.1 opcional) → 3.2 al terminar. Las celdas 4, 4.1 y 5 se usan bajo demanda._",
        "_Typical flow: 1 → 2 → 3 → (3.1 optional) → 3.2 when done. Cells 4, 4.1 and 5 are used on demand._",
    ),
    # --- Markdown: anti-AFK ---
    (
        "🛠️ Script Anti-Abandono para el Navegador",
        "🛠️ Browser Anti-Idle Script",
    ),
    (
        "Este script simula que estás haciendo clic en la página de Colab de forma automática cada 10 minutos para engañar al sistema de inactividad.",
        "This script simulates clicking on the Colab page automatically every 10 minutes to fool the idle-detection system.",
    ),
    (
        "Pasos para activarlo:",
        "Steps to activate it:",
    ),
    (
        "1.   Abre tu cuaderno de Google Colab en el navegador (Chrome, Edge o Firefox).",
        "1.   Open your Google Colab notebook in the browser (Chrome, Edge or Firefox).",
    ),
    (
        "2.   Presiona la tecla F12 (o clic derecho en cualquier parte de la página y selecciona Inspeccionar).",
        "2.   Press the F12 key (or right-click anywhere on the page and select Inspect).",
    ),
    (
        "3.   Ve a la pestaña llamada Consola (Console).",
        "3.   Go to the Console tab.",
    ),
    (
        "4.   Pega el siguiente código y presiona Enter:",
        "4.   Paste the following code and press Enter:",
    ),
    (
        'console.log("Manteniendo servidor activo...");',
        'console.log("Keeping server alive...");',
    ),
    (
        "// Simula un clic en el botón de conectar o de opciones del sistema",
        "// Simulates a click on the connect or system-options button",
    ),
    (
        "setInterval(KeepAlive, 600000); // Se ejecuta automáticamente cada 10 minutos (600,000 ms)",
        "setInterval(KeepAlive, 600000); // Runs automatically every 10 minutes (600,000 ms)",
    ),
    (
        "Verás un mensaje en la consola cada 10 minutos. Mientras dejes esa pestaña del navegador abierta (aunque minimices la ventana), el servidor no se caerá por inactividad.",
        "You'll see a message in the console every 10 minutes. As long as you keep that browser tab open (even minimized), the server won't drop due to inactivity.",
    ),
    # --- Badge: apunta al notebook EN ---
    (
        "PZ_Colab_ES.ipynb",
        "PZ_Colab_EN.ipynb",
    ),
    # --- Celda 1 ---
    ("# @title 1. Instalar Servidor y Dependencias", "# @title 1. Install Server & Dependencies"),
    ("# @markdown ### 🎮 Selección de Versión", "# @markdown ### 🎮 Version Selection"),
    (
        'Version = "b42 estable" # @param ["b42 estable", "b41 legacy", "b42 unstable"]',
        'Version = "b42 stable" # @param ["b42 stable", "b41 legacy", "b42 unstable"]',
    ),
    ('"🚀 INSTALADOR DE SERVIDOR PROJECT ZOMBOID"', '"🚀 PROJECT ZOMBOID SERVER INSTALLER"'),
    ('"1. Preparar sistema y dependencias"', '"1. Prepare system & dependencies"'),
    ('"2. Descargar red Playit.gg"', '"2. Download Playit.gg tunnel agent"'),
    ('"3. Vincular Google Drive"', '"3. Mount Google Drive"'),
    ('"4. Descargar Servidor (SteamCMD)"', '"4. Download Server (SteamCMD)"'),
    ('"   📊 PROGRESO DE DESCARGA:"', '"   📊 DOWNLOAD PROGRESS:"'),
    (
        '"\\n   📊 PROGRESO DE DESCARGA:"',
        '"\\n   📊 DOWNLOAD PROGRESS:"',
    ),
    (
        '"⚠️ Carpeta local antigua de /root/Zomboid renombrada; se reemplaza por el enlace a Drive."',
        '"⚠️ Old local /root/Zomboid folder renamed; replaced by the Drive link."',
    ),
    (
        '"ℹ️ El servidor ya está instalado con la versión seleccionada. Se omite la descarga."',
        '"ℹ️ The server is already installed with the selected version. Skipping download."',
    ),
    (
        '"\\nℹ️ El servidor ya está instalado con la versión seleccionada. Se omite la descarga."',
        '"\\nℹ️ The server is already installed with the selected version. Skipping download."',
    ),
    (
        '"⚠️ Se detectó una versión distinta instalada. Deteniendo servidor y reinstalando..."',
        '"⚠️ A different version is installed. Stopping the server and reinstalling..."',
    ),
    (
        '"💾 Memoria del servidor ajustada a 6 GB (compatible con el límite de Colab)."',
        '"💾 Server memory adjusted to 6 GB (fits within Colab\'s limit)."',
    ),
    (
        '"ℹ️ start-server.sh ya tenía memoria configurada (no se modificó)."',
        '"ℹ️ start-server.sh already had memory configured (not modified)."',
    ),
    (
        '"⚠️ No se encontró start-server.sh tras la instalación."',
        '"⚠️ start-server.sh was not found after installation."',
    ),
    (
        '"📌 Estado guardado en Drive: todas las celdas usarán esta versión."',
        '"📌 State saved on Drive: all cells will use this version."',
    ),
    ('f"⚠️ No se pudo guardar el estado: {e}"', 'f"⚠️ Could not save state: {e}"'),
    (
        '"✅ ¡FASE 1 COMPLETADA CON ÉXITO! Puedes continuar a la Celda 2."',
        '"✅ PHASE 1 COMPLETED! You can continue to Cell 2."',
    ),
    (
        '"⚠️ SteamCMD falló al validar el ejecutable. Intenta correr la celda de nuevo."',
        '"⚠️ SteamCMD failed to validate the executable. Try running the cell again."',
    ),
    (
        '"\\n⚠️ SteamCMD falló al validar el ejecutable. Intenta correr la celda de nuevo."',
        '"\\n⚠️ SteamCMD failed to validate the executable. Try running the cell again."',
    ),
    # --- Variables de parámetros (labels del formulario) ---
    ("pausa_cuando_vacio", "pause_when_empty"),
    ("watchdog_activo", "watchdog_enabled"),
    ("max_reinicios", "max_restarts"),
    ("Limpiar_Lista_Anterior", "clear_previous_list"),
    ("Descargar_Mods", "download_mods"),
    ("Backup_Max_Guardar", "backup_max_keep"),
    # --- Celda 2 ---
    ("# @title 2. Configurar Playit.gg Persistente", "# @title 2. Configure Persistent Playit.gg"),
    ('"❌ Google Drive NO está montado. Ejecuta primero la Celda 1."', '"❌ Google Drive is NOT mounted. Run Cell 1 first."'),
    ('"✅ Configuración persistente enlazada."', '"✅ Persistent config linked."'),
    (
        '"ℹ️ Ya existe un túnel configurado en Drive. Esta celda es OPCIONAL en re-ejecuciones;"',
        '"ℹ️ A tunnel config already exists on Drive. This cell is OPTIONAL on re-runs;"',
    ),
    ('"   úsala solo si necesitas reclamar un túnel nuevo."', '"   use it only if you need to claim a new tunnel."'),
    ('"🚀 Iniciando Playit..."', '"🚀 Starting Playit..."'),
    ('"⚠️ SOLO la primera vez tendrás que reclamar el túnel."', '"⚠️ Only the first time you\'ll need to claim the tunnel."'),
    # --- Celda 3 ---
    ("# @title 3. Iniciar Servidor (Watchdog + Config Avanzada)", "# @title 3. Start Server (Watchdog + Advanced Config)"),
    ("# @markdown ### 🎮 Parámetros del Servidor", "# @markdown ### 🎮 Server Parameters"),
    ("# @markdown _💡 Si cambias el puerto, actualiza el túnel en playit.gg._", "# @markdown _💡 If you change the port, update the tunnel at playit.gg._"),
    ("# @markdown ### 🛡️ Watchdog (auto-reinicio ante crashes)", "# @markdown ### 🛡️ Watchdog (auto-restart on crashes)"),
    ('f"📌 Versión activa: {Version}"', 'f"📌 Active version: {Version}"'),
    (
        '"🛑 Servidor anterior detectado; se detiene antes de continuar."',
        '"🛑 Previous server detected; stopping it before continuing."',
    ),
    ('"🔗 Symlink de saves recreado (runtime nuevo)."', '"🔗 Saves symlink recreated (new runtime)."'),
    ('"🔑 Admin password recuperada del .ini existente."', '"🔑 Admin password recovered from the existing .ini."'),
    (
        'f"🔑 Admin password generada automáticamente: {admin_password}"',
        'f"🔑 Admin password auto-generated: {admin_password}"',
    ),
    (
        '"ℹ️ Primer arranque: .ini base creado con la configuración elegida."',
        '"ℹ️ First run: base .ini created with your settings."',
    ),
    ('f"⚙️ Configuración aplicada en {INI_PATH}"', 'f"⚙️ Settings applied in {INI_PATH}"'),
    (
        'f"⚠️ Puerto cambiado a {port}. Actualiza el túnel en https://playit.gg/account"',
        'f"⚠️ Port changed to {port}. Update the tunnel at https://playit.gg/account"',
    ),
    ('"✅ Túnel Playit encendido en el fondo."', '"✅ Playit tunnel running in the background."'),
    (
        'abortar("❌ No se encontró start-server.sh. Ejecuta primero la Celda 1 (instalación).")',
        'abortar("❌ start-server.sh not found. Run Cell 1 (installation) first.")',
    ),
    ('"🔥 Servidor arrancado en segundo plano."', '"🔥 Server started in the background."'),
    ('f"📄 Consola en vivo: Celda 3.1 (tail de {LOG_PATH})"', 'f"📄 Live console: Cell 3.1 (tail of {LOG_PATH})"'),
    ('"🛑 Apagado limpio: Celda 3.2"', '"🛑 Clean shutdown: Cell 3.2"'),
    (
        'f"🛡️ Watchdog activo: hasta {max_reinicios} reinicios automáticos."',
        'f"🛡️ Watchdog active: up to {max_reinicios} automatic restarts."',
    ),
    # --- Celda 3.1 ---
    ("# @title 3.1 Consola en Vivo del Servidor (tail)", "# @title 3.1 Live Server Console (tail)"),
    (
        "# @markdown _Ejecuta esta celda para ver la consola del servidor en tiempo real._",
        "# @markdown _Run this cell to watch the server console in real time._",
    ),
    (
        "# @markdown _Para detenerla, presiona el botón ⏹ (Interrumpir ejecución)._",
        "# @markdown _To stop it, press the ⏹ button (Interrupt execution)._",
    ),
    ('"⚠️ Todavía no hay log. Ejecuta primero la Celda 3."', '"⚠️ No log yet. Run Cell 3 first."'),
    (
        '"📄 Mostrando últimas 40 líneas + seguimiento en vivo (⏹ para salir)...\\n"',
        '"📄 Showing last 40 lines + live follow (⏹ to exit)...\\n"',
    ),
    # --- Celda 3.2 ---
    ("# @title 3.2 Apagado Limpio del Servidor", "# @title 3.2 Clean Server Shutdown"),
    (
        "# @markdown _Guarda el mundo (save) y apaga el servidor de forma ordenada._",
        "# @markdown _Saves the world and shuts the server down cleanly._",
    ),
    ('"💾 Enviando SAVE..."', '"💾 Sending SAVE..."'),
    ('"🛑 Enviando QUIT..."', '"🛑 Sending QUIT..."'),
    ('"✅ Servidor apagado de forma segura."', '"✅ Server shut down safely."'),
    ('"⚠️ No respondió a tiempo; forzando cierre."', '"⚠️ No response in time; forcing shutdown."'),
    (
        '"⚠️ El proceso del servidor no está accesible en esta sesión (runtime reiniciado?)."',
        '"⚠️ The server process is not accessible in this session (runtime restarted?)."',
    ),
    ('"   Intentando pkill suave..."', '"   Trying graceful pkill..."'),
    ('"✅ Señales de terminación enviadas."', '"✅ Termination signals sent."'),
    # --- Celda 4 ---
    ("# @title 4. Mods Fáciles: Pega URLs o Colecciones", "# @title 4. Easy Mods: Paste URLs or Collections"),
    ("# @markdown ### 📥 Entrada de Mods (uno por línea)", "# @markdown ### 📥 Mod Input (one per line)"),
    (
        "# @markdown _Pega la URL del Workshop o solo el ID numérico. Si es una colección, se expande automáticamente._",
        "# @markdown _Paste the Workshop URL or just the numeric ID. If it's a collection, it expands automatically._",
    ),
    (
        "# @markdown _Formato avanzado si falla la detección automática: `URL|ModIDManual`_",
        "# @markdown _Advanced format if auto-detection fails: `URL|ModIDManual`_",
    ),
    ("# @markdown ### 🧹 Control de Historial", "# @markdown ### 🧹 History Control"),
    (
        "# @markdown _💡 Activa la casilla si quieres borrar los mods viejos del .ini y quedarte **solo** con los que pegues abajo._",
        "# @markdown _💡 Enable it to clear old mods from the .ini and keep **only** the ones you paste below._",
    ),
    ("# @markdown ### 📥 Descargar Mods del Workshop", "# @markdown ### 📥 Download Workshop Mods"),
    (
        "# @markdown _💡 Descarga cada item vía SteamCMD y detecta el Mod ID real leyendo su `mod.info`._",
        "# @markdown _💡 Downloads each item via SteamCMD and detects the real Mod ID from its `mod.info`._",
    ),
    (
        "**▶️ Para confirmar: ejecuta esta celda con el botón ▶ (o Ctrl+Enter). Los campos del formulario se procesan al ejecutar la celda — no hay un botón interno.**",
        "**▶️ To confirm: run this cell with the ▶ button (or Ctrl+Enter). Form fields are processed when the cell runs — there is no internal button.**",
    ),
    (
        'f"📌 Versión detectada desde la Celda 1: {Version.upper()} | Servidor: {server_name}\\n"',
        'f"📌 Version detected from Cell 1: {Version.upper()} | Server: {server_name}\\n"',
    ),
    (
        '"⚠️ No se encontró el estado de la Celda 1 (.pzcolab_state.json). Se asume b42 estable.\\n"',
        '"⚠️ Cell 1 state not found (.pzcolab_state.json). Assuming b42 stable.\\n"',
    ),
    (
        'f"⚠️ Línea ignorada (no parece ID de Workshop): {l.strip()[:60]}"',
        'f"⚠️ Line ignored (doesn\'t look like a Workshop ID): {l.strip()[:60]}"',
    ),
    (
        'f"la página menciona Build 42 pero tu servidor es {Version.upper()}"',
        'f"the page mentions Build 42 but your server is {Version.upper()}"',
    ),
    (
        'f"la página menciona Build 41 pero tu servidor es {Version.upper()}"',
        'f"the page mentions Build 41 but your server is {Version.upper()}"',
    ),
    ('f"      🔗 Requiere: {\', \'.join(reqs)}"', 'f"      🔗 Requires: {\', \'.join(reqs)}"'),
    ('"⚠️ DEPENDENCIAS FALTANTES:"', '"⚠️ MISSING DEPENDENCIES:"'),
    ('"\\n⚠️ DEPENDENCIAS FALTANTES:"', '"\\n⚠️ MISSING DEPENDENCIES:"'),
    (
        'f"   El mod \'{mid}\' requiere \'{req}\', que no está en la lista. Agrégalo o el servidor puede no cargar."',
        'f"   Mod \'{mid}\' requires \'{req}\', which is not in the list. Add it or the server may fail to load."',
    ),
    (
        '"🔎 POSIBLES INCOMPATIBILIDADES DE VERSIÓN (heurístico, verifica en el Workshop):"',
        '"🔎 POSSIBLE VERSION INCOMPATIBILITIES (heuristic, verify on the Workshop):"',
    ),
    (
        '"\\n🔎 POSIBLES INCOMPATIBILIDADES DE VERSIÓN (heurístico, verifica en el Workshop):"',
        '"\\n🔎 POSSIBLE VERSION INCOMPATIBILITIES (heuristic, verify on the Workshop):"',
    ),
    (
        '"   Si el mod no carga, revisa su página para confirmar compatibilidad."',
        '"   If the mod fails to load, check its page to confirm compatibility."',
    ),
    (
        '"ℹ️ No hay mods nuevos para procesar. Para ver los actuales usa la Celda 4.1."',
        '"ℹ️ No new mods to process. To see the current ones, use Cell 4.1."',
    ),
    (
        'f"📂 Colección detectada: {wsid} → expandiendo..."',
        'f"📂 Collection detected: {wsid} → expanding..."',
    ),
    ('f"🧾 Items a procesar: {len(final)}\\n"', 'f"🧾 Items to process: {len(final)}\\n"'),
    (
        '"⚠️ No se encontró la instalación del servidor. Ejecuta la Celda 1 para instalar."',
        '"⚠️ Server installation not found. Run Cell 1 to install."',
    ),
    ('"📥 Descargando mods desde Steam Workshop..."', '"📥 Downloading mods from Steam Workshop..."'),
    ('f"   ✓ {wsid} ya descargado (se omite)."', 'f"   ✓ {wsid} already downloaded (skipped)."'),
    (
        'f"     {\'✅ Descargado\' if ok else \'⚠️ Fallo (revisa el ID o usa el formato URL|ModIDManual)\'}"',
        'f"     {\'✅ Downloaded\' if ok else \'⚠️ Failed (check the ID or use URL|ModIDManual)\'}"',
    ),
    (
        'f"⚠️ No se detectó el Mod ID de {wsid}. Si lo conoces, usa el formato: URL|ModID"',
        'f"⚠️ Could not detect the Mod ID for {wsid}. If you know it, use: URL|ModID"',
    ),
    (
        '"❌ ERROR: No se encontró el archivo INI. Inicia el servidor una vez (Celda 3) para generarlo."',
        '"❌ ERROR: INI file not found. Start the server once (Cell 3) to generate it."',
    ),
    ('"🧹 Historial limpiado. Solo se escribirán los mods pegados.\\n"', '"🧹 History cleared. Only pasted mods will be written.\\n"'),
    ('"⚠️ No hay mods activos para escribir en el servidor."', '"⚠️ No active mods to write to the server."'),
    ('f"📋 MODS EN EL SERVIDOR (Total: {len(combinada)})"', 'f"📋 MODS ON THE SERVER (Total: {len(combinada)})"'),
    (
        'f"✅ .ini actualizado: {INI_PATH}"',
        'f"✅ .ini updated: {INI_PATH}"',
    ),
    ('"   Reinicia el servidor (Celda 3) para aplicar los mods."', '"   Restart the server (Cell 3) to apply the mods."'),
    # --- Celda 4.1 ---
    ("# @title 🔍 4.1 Inspector y Diagnóstico Avanzado de Servidor", "# @title 🔍 4.1 Server Inspector & Advanced Diagnostics"),
    (
        "# @markdown _Muestra tus mods activos y analiza los logs agrupando errores por mod e identificando culpables reales._",
        "# @markdown _Shows your active mods and analyzes logs, grouping errors by mod to find the real culprits._",
    ),
    ('"👁️  MODS CONFIGURADOS EN EL SERVIDOR"', '"👁️  MODS CONFIGURED ON THE SERVER"'),
    ('"❌ No se encontró ningún archivo de configuración .ini."', '"❌ No configuration .ini file found."'),
    ('"⚠️ El archivo .ini no tiene mods configurados."', '"⚠️ The .ini file has no mods configured."'),
    ('"🔍 INICIANDO ESCANEO AVANZADO DE LOGS..."', '"🔍 STARTING ADVANCED LOG SCAN..."'),
    ('"ℹ️ No se encontraron archivos de registro activos."', '"ℹ️ No active log files found."'),
    (
        'f"[Línea {num_linea}] 🌐 Fallo Steam ➡️ {line.strip()}"',
        'f"[Line {num_linea}] 🌐 Steam Failure ➡️ {line.strip()}"',
    ),
    (
        'f"[Línea {num_linea}] 📝 Detalle ➡️ {line.strip()[:90]}..."',
        'f"[Line {num_linea}] 📝 Detail ➡️ {line.strip()[:90]}..."',
    ),
    (
        'f"🔴 Errores de Lua/Crashes Detectados: {len(fallos_criticos)}"',
        'f"🔴 Lua Errors/Crashes Detected: {len(fallos_criticos)}"',
    ),
    ('"👑 MODS O ARCHIVOS MÁS INESTABLES:"', '"👑 MOST UNSTABLE MODS OR FILES:"'),
    (
        'f"   ⚠️ -> \'{mod}\' generó {count} alertas en este arranque."',
        'f"   ⚠️ -> \'{mod}\' triggered {count} alerts on this boot."',
    ),
    ('"📌 Muestra de las primeras líneas de error:"', '"📌 Sample of the first error lines:"'),
    ('"\\n📌 Muestra de las primeras líneas de error:"', '"\\n📌 Sample of the first error lines:"'),
    ('f"   [Línea {num}] Script: {ctx}"', 'f"   [Line {num}] Script: {ctx}"'),
    (
        'f"🌐 Problemas con Steam Workshop: {len(errores_steam)}"',
        'f"🌐 Steam Workshop Issues: {len(errores_steam)}"',
    ),
    (
        'f"\\n🌐 Problemas con Steam Workshop: {len(errores_steam)}"',
        'f"\\n🌐 Steam Workshop Issues: {len(errores_steam)}"',
    ),
    (
        'f"📝 Alertas Menores o Estéticas (No rompen el servidor): {len(alertas_esteticas)}"',
        'f"📝 Minor/Aesthetic Alerts (don\'t break the server): {len(alertas_esteticas)}"',
    ),
    (
        'f"\\n📝 Alertas Menores o Estéticas (No rompen el servidor): {len(alertas_esteticas)}"',
        'f"\\n📝 Minor/Aesthetic Alerts (don\'t break the server): {len(alertas_esteticas)}"',
    ),
    (
        '"   💡 _Nota: Son sonidos faltantes o vallas del mapa original. Ignorables._"',
        '"   💡 _Note: Missing sounds or original map fences. Ignorable._"',
    ),
    ('"🛠️ DIAGNÓSTICO FINAL:"', '"🛠️ FINAL DIAGNOSIS:"'),
    (
        '"   El servidor inició, pero hay mods con scripts obsoletos. Si notas lag visual o items invisibles,"',
        '"   The server started, but some mods have outdated scripts. If you notice visual lag or invisible items,"',
    ),
    (
        '"   revisa los mods indicados en el top de inestabilidad."',
        '"   check the mods listed at the top of the instability ranking."',
    ),
    (
        '"   ¡Estable! El servidor no registra problemas de programación críticos en los mods."',
        '"   Stable! No critical mod scripting issues recorded."',
    ),
    (
        '"✅ ¡SISTEMA 100% LIMPIO! Logs impecables y listos para jugar."',
        '"✅ 100% CLEAN! Spotless logs, ready to play."',
    ),
    # --- Celda 5 ---
    ("# @title 5. Backup de Saves (Drive)", "# @title 5. Saves Backup (Drive)"),
    (
        "# @markdown _Crea un respaldo .tar.gz del mundo y la configuración en tu Google Drive._",
        "# @markdown _Creates a .tar.gz backup of the world and config on your Google Drive._",
    ),
    ('"❌ Drive no montado. Ejecuta primero la Celda 1."', '"❌ Drive not mounted. Run Cell 1 first."'),
    (
        '"📦 Creando backup (según el tamaño del mundo puede tardar unos minutos)..."',
        '"📦 Creating backup (may take a few minutes depending on world size)..."',
    ),
    ('f"✅ Backup creado: {destino} ({tamaño_mb:.1f} MB)"', 'f"✅ Backup created: {destino} ({tamaño_mb:.1f} MB)"'),
    (
        'f"📊 Backups conservados: {len(backups)} (máximo {max_guardar})"',
        'f"📊 Backups kept: {len(backups)} (max {max_guardar})"',
    ),
    ('f"📂 Carpeta de backups: {BACKUP_DIR}"', 'f"📂 Backup folder: {BACKUP_DIR}"'),
]

# Aplicar las más largas primero para evitar colisiones parciales
TRADUCCIONES.sort(key=lambda p: len(p[0]), reverse=True)


def traducir(texto):
    """Aplica la tabla ES->EN a una cadena de código fuente."""
    for es, en in TRADUCCIONES:
        if es in texto:
            texto = texto.replace(es, en)
    return texto
