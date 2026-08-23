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
* **Memoria configurable:** elige 4 / 6 / 8 GB de RAM del servidor en la Celda 2 — el cuaderno re-aplica el parche `-Xms/-Xmx` en cada arranque y **limita automáticamente** el valor según la RAM real del runtime (nunca más de 8 GB en Colab).
* **Túnel Playit + Consola en Vivo + Apagado Automático (unificado):** la Celda 2 enciende el servidor con watchdog, reclama o reutiliza tu túnel Playit.gg persistente, muestra la consola en vivo debajo y almacena el mundo guardándolo (`save` + `quit`) de forma ordenada al detener la celda con ⏹.
* **Inyector de Mods Fácil + Colecciones:** Pega la URL del Workshop (o solo el ID) de cada mod — uno por línea — o una colección entera de Steam y el sistema la expande. Descarga cada item vía SteamCMD, **detecta automáticamente el Mod ID real** leyendo el `mod.info`, los clasifica (Librerías, UI, Vehículos, QoL) y los escribe en el `.ini` sin duplicados.
* **Descarga automática de dependencias:** cuando un mod declara un `require=` faltante (en su `mod.info`), la Celda 4 busca el ID de Workshop de la dependencia y la descarga **automáticamente** (cache por sesión, hasta 3 pasadas para deps transitivas). Las dependencias no encontradas en el Workshop se reportan para pegarlas manualmente.
* **Borrado rápido de mods (Celda 4):** lista tus mods activos y elimina uno por número o ID de Workshop directamente — no hace falta editar el `.ini` a mano. Ideal para desactivar un mod que el diagnóstico (Celda 3.1) marcó como inestable.
* **Watchdog de Crashes:** Auto-reinicio del servidor ante fallos (número de reintentos configurable).
* **Backup + Auto-respaldo:** al apagar (Celda 2, ⏹) y al usar la Celda 5, se crea un `.tar.gz` de los saves en `MyDrive/ZomboidSaves_backups` con retención de las 3 últimas copias y rotación de `Logs/` (máx. 20 archivos) para mantener el backup pequeño (≈ dentro del tope de 1 GB de Drive). Incluye **restauración interactiva** con backup de seguridad previo.
* **🛠️ Diagnóstico Avanzado de Logs:** Un script analizador único que escanea los archivos de registro (`DebugLog-server.txt`) para detectar *crashes*, errores de Lua y fallos de Steam Workshop, señalando qué mod específico está causando inestabilidad en el servidor.
* **Anti-AFK:** Script integrado para la consola del navegador que previene la desconexión por inactividad en Google Colab.

## 🚀 Uso Rápido

1. Sube o abre el cuaderno interactivo (`PZ_Colab_ES.ipynb`) en Google Colab.
2. Ejecuta la **Celda 1** para elegir la versión e instalar el servidor y conectar tu Google Drive.
3. Ejecuta la **Celda 2** para encender el servidor, reclamar tu túnel Playit.gg (la primera vez autoriza el enlace; en ejecuciones posteriores se reutiliza la config de Drive), ver la consola en vivo y apagar el servidor de forma ordenada (con guardado automático) al detener la celda con ⏹. ¡Tus amigos pueden conectarse usando la IP y puerto que te asigne Playit!

### Versiones disponibles (Celda 1)

| Opción | Rama SteamCMD | Descripción |
|---|---|---|
| `b42 estable` | Sin beta (por defecto) | Versión estable actual de Project Zomboid. **Recomendada.** |
| `b41 legacy` | `-beta legacy41` | Versión antigua 41.x, para servidores con mods legacy. |
| `b42 unstable` | `-beta unstable` | Rama inestable de la Build 42, para testeo de nuevas features. |

La versión elegida se guarda en `MyDrive/ZomboidSaves/.pzcolab_state.json` y es leída automáticamente por las demás celdas (no hace falta repetir la selección). Re-ejecutar la **Celda 1** es rápido: si el servidor ya está instalado con la misma versión, omite la descarga; si cambiaste de versión, reinstala automáticamente y detiene el servidor activo.

### Gestión de Mods (Celda 3)

Pega cada mod en su propia línea — la **URL del Workshop** o **solo el ID numérico**:

```
https://steamcommunity.com/sharedfiles/filedetails/?id=2902678
2861456062
https://steamcommunity.com/sharedfiles/filedetails/?id=2750177123
```

También acepta **URLs de colecciones de Steam** (se expanden automáticamente). Al ejecutar, la celda descarga cada item con SteamCMD, **detecta el Mod ID real desde su `mod.info`** (no hace falta saberlo), los clasifica (Librerías → UI → Vehículos → QoL) y actualiza el `.ini` sin duplicados, conservando el historial. El reporte final muestra los **nombres reales** de los mods.

Si algún mod falla la detección automática, usa el formato avanzado `URL|ModIDManual` en la misma línea.

La celda también avisa de **posibles incompatibilidades de build** (b41 vs b42) escaneando la página del Workshop de cada mod, y de **dependencias requeridas faltantes** (`require=` en `mod.info`) antes de reiniciar el servidor — el reporte muestra el nombre real, el tipo y las dependencias de cada mod.

> **Bonus:** si un mod declara un `require=` faltante que encuentra en el Workshop, la Celda 4 lo descarga **automáticamente** (cache por sesión, hasta 3 pasadas para deps transitivas). Las dependencias no encontradas se listan en un reporte "DEPENDENCIAS FALTANTES" para pegarlas a mano. Desactívalo desmarcando `Descargar_Dependencias`.

#### Borrado rápido de mods

Para desactivar un mod que ya no quieres (por ejemplo, el que el diagnóstico marcó como inestable), usa la sección de **gestión rápida** en la parte superior de la Celda 4: marca `Eliminar_Mods`, lee la lista numerada de mods activos y escribe su **número o ID de Workshop** en `numero_a_eliminar`. La celda reescribe `WorkshopItems`/`Mods` en el `.ini` in situ — no necesitas editarlo a mano.



### Operación del servidor

* **Celda 1 — Instalación:** instala SteamCMD, dependencias del sistema y el servidor, monta Drive y enlaza `/root/Zomboid` → `MyDrive/ZomboidSaves`.
* **Celda 2 — Servidor + Consola + Auto-Apagado (unificado):** enciende el servidor con watchdog, reclama o reutiliza el túnel Playit.gg, muestra la consola en vivo debajo y **guarda el mundo y apaga de forma ordenada** (con respaldo automático) al detener la celda con ⏹.
* **Celda 3 — Mods Fáciles:** pega URLs o colecciones del Workshop (ver arriba).
* **Celda 3.1 — Diagnóstico de errores:** escanea logs y agrupa errores por mod.
* **Celda 4 — Backup + Restauración:** crea un `.tar.gz` de tus saves en `MyDrive/ZomboidSaves_backups` con retención de 3 copias, rota `Logs/` y ofrece restaurar un backup (guarda de seguridad previo).
* **Anti-AFK (al final del cuaderno):** script para la consola del navegador que evita la desconexión por inactividad mientras el servidor corre.

## 🧠 Diagnóstico de Errores

Si el servidor presenta problemas al arrancar, ejecuta la herramienta **3.1 Inspector y Diagnóstico Avanzado**. Este bloque analizará el historial de Google Drive y te entregará un reporte visual en consola indicando:
- Número exacto de errores críticos de Lua.
- Nombre del Mod/Script culpable del fallo.
- Alertas de conexión con Steam.
- **Problemas de memoria** (con sugerencia de subir la memoria en la Celda 2 o reducir jugadores/mods), **errores de servidor/puerto** y **fallos al guardar**.

## ⚠️ Notas Importantes

* **Playit.gg:** la versión del agente está fijada en `v0.15.26` a propósito (compatibilidad con consola de Colab). No actualizar.
* **Límites de Colab:** las sesiones gratuitas duran hasta 12 horas y tienen un timeout por inactividad (~90 min). Usa el script Anti-AFK del cuaderno y reinicia el servidor al reconectar el runtime.
* **Cambio de puerto:** si cambias el puerto UDP en la Celda 2, recuerda actualizar el túnel correspondiente en tu panel de [Playit.gg](https://playit.gg/account).

## 🤝 Contribuciones y Pruebas de Comunidad

Las contribuciones (Pull Requests) son bienvenidas. Este proyecto busca ser una base sólida para que la comunidad hispanohablante de desarrolladores y jugadores de Project Zomboid pueda realizar pruebas de estrés de mods, mapas y configuraciones en entornos multijugador sin coste de infraestructura local.

Si encuentras algún *bug* o tienes ideas para optimizar el consumo de RAM/CPU en el entorno de Colab, no dudes en abrir un *Issue*.

## 📄 Licencia
Este proyecto está bajo la Licencia MIT. Eres libre de usarlo, modificarlo y distribuirlo para tus propias pruebas.
