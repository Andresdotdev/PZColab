# 🧟‍♂️ PZColab - Project Zomboid Cloud Server

PZColab es un entorno de despliegue automatizado diseñado para ejecutar un servidor dedicado de **Project Zomboid** (compatible con Build 41 y la rama inestable Build 42 MP) directamente en **Google Colab**. 

Este proyecto está pensado como una herramienta open-source para facilitar el testing de comunidad, permitiendo levantar servidores multijugador de forma rápida, gratuita y con persistencia de datos, sin necesidad de configuraciones de red complejas gracias a la integración con Playit.gg.

## ✨ Características Principales

* **Despliegue en 1 Clic:** Instalación automatizada de dependencias del sistema, SteamCMD y el servidor base de PZ.
* **Túnel de Red Integrado:** Configuración automática de [Playit.gg](https://playit.gg/) para asignar IPs públicas sin necesidad de abrir puertos (Port Forwarding).
* **Persistencia en la Nube:** Enlace directo con Google Drive (`/MyDrive/ZomboidSaves`) para asegurar que el mundo, las configuraciones y los perfiles de los jugadores no se pierdan al cerrar la sesión.
* **Inyector de Mods Compacto:** Interfaz integrada para añadir mods de Steam Workshop (hasta 10 slots a la vez) directamente modificando el archivo `.ini` del servidor de forma segura.
* **🛠️ Diagnóstico Avanzado de Logs:** Un script analizador único que escanea los archivos de registro (`DebugLog-server.txt`) para detectar *crashes*, errores de Lua y fallos de Steam Workshop, señalando qué mod específico está causando inestabilidad en el servidor.
* **Anti-AFK:** Script integrado para la consola del navegador que previene la desconexión por inactividad en Google Colab.

## 🚀 Uso Rápido

1. Sube o abre el cuaderno interactivo (`PZ-Colab.ipynb`) en Google Colab.
2. Ejecuta la **Celda 1** para instalar el servidor y conectar tu Google Drive.
3. Ejecuta la **Celda 2** para generar y reclamar tu enlace persistente de Playit.gg (Solo es necesario configurarlo la primera vez).
4. Ejecuta la **Celda 3** para encender el servidor. ¡Tus amigos pueden conectarse usando la IP y puerto que te asigne Playit!

### Gestión de Mods (Celda 4)
Para instalar mods, simplemente introduce el `Workshop ID` y el `Mod ID` en los slots disponibles de la celda 4. El inyector se encargará de clasificarlos (Librerías, UI, Vehículos, QoL) y escribirlos correctamente en el archivo de configuración sin duplicados.

## 🧠 Diagnóstico de Errores

Si el servidor presenta problemas al arrancar, ejecuta la herramienta **4.1 Inspector y Diagnóstico Avanzado**. Este bloque analizará el historial de Google Drive y te entregará un reporte visual en consola indicando:
- Número exacto de errores críticos de Lua.
- Nombre del Mod/Script culpable del fallo.
- Alertas de conexión con Steam.

## 🤝 Contribuciones y Pruebas de Comunidad

Las contribuciones (Pull Requests) son bienvenidas. Este proyecto busca ser una base sólida para que la comunidad hispanohablante de desarrolladores y jugadores de Project Zomboid pueda realizar pruebas de estrés de mods, mapas y configuraciones en entornos multijugador sin coste de infraestructura local. 

Si encuentras algún *bug* o tienes ideas para optimizar el consumo de RAM/CPU en el entorno de Colab, no dudes en abrir un *Issue*.

## 📄 Licencia
Este proyecto está bajo la Licencia MIT. Eres libre de usarlo, modificarlo y distribuirlo para tus propias pruebas.
