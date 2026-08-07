# 🧟‍♂️ PZColab - Servidor de Project Zomboid en Google Colab

[![Licencia: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Abrir en Colab](https://img.shields.io/badge/Abrir%20En-Colab-orange.svg?logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/Andresdotdev/PZColab/blob/main/PZ_Colab_ES.ipynb)

**Read this in: [English 🇬🇧](README.md)**


PZColab es un entorno de despliegue automatizado diseñado para ejecutar un servidor dedicado de **Project Zomboid** directamente en **Google Colab**, compatible con la **Build 41 (legacy)** y la **Build 42 estable**.

Este proyecto está pensado como una herramienta open-source para facilitar el testing de comunidad, permitiendo levantar servidores multijugador de forma rápida, gratuita y con persistencia de datos, sin necesidad de configuraciones de red complejas gracias a la integración con Playit.gg.

## ✨ Características Principales

* **Despliegue en 1 Clic:** Instalación automatizada de dependencias del sistema, SteamCMD y el servidor base de PZ.
* **Versiones seleccionables:** **b42 estable** (recomendada), **b41 legacy** y **b42 unstable** — el selector es único y sincronizado entre celdas mediante un archivo de estado en Drive.
* **Túnel de Red Integrado:** Configuración automática de [Playit.gg](https://playit.gg/) para asignar IPs públicas sin necesidad de abrir puertos (Port Forwarding).
* **Persistencia en la Nube:** Enlace directo con Google Drive (`/MyDrive/ZomboidSaves`) para asegurar que el mundo, las configuraciones y los perfiles de los jugadores no se pierdan al cerrar la sesión.
* **Ajuste automático de memoria:** El script ajusta `-Xms/-Xmx` del servidor a 6 GB, compatible con el límite de RAM de Colab (~12.7 GB).
* **Inyector de Mods Fácil + Colecciones:** Pega la URL del Workshop (o solo el ID) de cada mod — uno por línea — o una colección entera de Steam y el sistema la expande. Descarga cada item vía SteamCMD, **detecta automáticamente el Mod ID real** leyendo el `mod.info`, los clasifica (Librerías, UI, Vehículos, QoL) y los escribe en el `.ini` sin duplicados.
* **Watchdog de Crashes:** Auto-reinicio del servidor ante fallos (número de reintentos configurable).
* **Apagado Limpio:** Envía `save` y `quit` al servidor para que el mundo se guarde de forma ordenada.
* **Consola en Vivo:** Celda de `tail` para ver la consola del servidor en tiempo real.
* **Backup de Saves:** Genera respaldos `.tar.gz` en Drive con retención configurable.
* **🛠️ Diagnóstico Avanzado de Logs:** Un script analizador único que escanea los archivos de registro (`DebugLog-server.txt`) para detectar *crashes*, errores de Lua y fallos de Steam Workshop, señalando qué mod específico está causando inestabilidad en el servidor.
* **Anti-AFK:** Script integrado para la consola del navegador que previene la desconexión por inactividad en Google Colab.

## 🚀 Uso Rápido

1. Sube o abre el cuaderno interactivo (`PZ_Colab_ES.ipynb`) en Google Colab.
2. Ejecuta la **Celda 1** para elegir la versión e instalar el servidor y conectar tu Google Drive.
3. Ejecuta la **Celda 2** para generar y reclamar tu enlace persistente de Playit.gg (Solo es necesario configurarlo la primera vez).
4. Ejecuta la **Celda 3** para encender el servidor. ¡Tus amigos pueden conectarse usando la IP y puerto que te asigne Playit!

### Versiones disponibles (Celda 1)

| Opción | Rama SteamCMD | Descripción |
|---|---|---|
| `b42 estable` | Sin beta (por defecto) | Versión estable actual de Project Zomboid. **Recomendada.** |
| `b41 legacy` | `-beta legacy41` | Versión antigua 41.x, para servidores con mods legacy. |
| `b42 unstable` | `-beta unstable` | Rama inestable de la Build 42, para testeo de nuevas features. |

La versión elegida se guarda en `MyDrive/ZomboidSaves/.pzcolab_state.json` y es leída automáticamente por las demás celdas (no hace falta repetir la selección). Re-ejecutar la **Celda 1** es rápido: si el servidor ya está instalado con la misma versión, omite la descarga; si cambiaste de versión, reinstala automáticamente y detiene el servidor activo.

### Gestión de Mods (Celda 4)

Pega cada mod en su propia línea — la **URL del Workshop** o **solo el ID numérico**:

```
https://steamcommunity.com/sharedfiles/filedetails/?id=2902678
2861456062
https://steamcommunity.com/sharedfiles/filedetails/?id=2750177123
```

También acepta **URLs de colecciones de Steam** (se expanden automáticamente). Al ejecutar, la celda descarga cada item con SteamCMD, **detecta el Mod ID real desde su `mod.info`** (no hace falta saberlo), los clasifica (Librerías → UI → Vehículos → QoL) y actualiza el `.ini` sin duplicados, conservando el historial. El reporte final muestra los **nombres reales** de los mods.

Si algún mod falla la detección automática, usa el formato avanzado `URL|ModIDManual` en la misma línea.

> 💡 Si la contraseña de admin se deja vacía en la Celda 3, se recupera del `.ini` existente o se genera una automáticamente (se muestra en consola).

### Operación del servidor

* **Celda 3.1 — Consola en vivo:** muestra la salida del servidor en tiempo real (detener con el botón ⏹).
* **Celda 3.2 — Apagado limpio:** guarda el mundo y apaga el servidor ordenadamente.
* **Celda 5 — Backup:** crea un `.tar.gz` de tus saves en `MyDrive/ZomboidSaves_backups` con retención de las N últimas copias.
* **Anti-AFK (al final del cuaderno):** script para la consola del navegador que evita la desconexión por inactividad mientras el servidor corre.

## 🧠 Diagnóstico de Errores

Si el servidor presenta problemas al arrancar, ejecuta la herramienta **4.1 Inspector y Diagnóstico Avanzado**. Este bloque analizará el historial de Google Drive y te entregará un reporte visual en consola indicando:
- Número exacto de errores críticos de Lua.
- Nombre del Mod/Script culpable del fallo.
- Alertas de conexión con Steam.

## ⚠️ Notas Importantes

* **Playit.gg:** la versión del agente está fijada en `v0.15.26` a propósito (compatibilidad con consola de Colab). No actualizar.
* **Límites de Colab:** las sesiones gratuitas duran hasta 12 horas y tienen un timeout por inactividad (~90 min). Usa el script Anti-AFK del cuaderno y reinicia el servidor al reconectar el runtime.
* **Cambio de puerto:** si cambias el puerto UDP en la Celda 3, recuerda actualizar el túnel correspondiente en tu panel de [Playit.gg](https://playit.gg/account).

## 🤝 Contribuciones y Pruebas de Comunidad

Las contribuciones (Pull Requests) son bienvenidas. Este proyecto busca ser una base sólida para que la comunidad hispanohablante de desarrolladores y jugadores de Project Zomboid pueda realizar pruebas de estrés de mods, mapas y configuraciones en entornos multijugador sin coste de infraestructura local.

Si encuentras algún *bug* o tienes ideas para optimizar el consumo de RAM/CPU en el entorno de Colab, no dudes en abrir un *Issue*.

## 📄 Licencia
Este proyecto está bajo la Licencia MIT. Eres libre de usarlo, modificarlo y distribuirlo para tus propias pruebas.
