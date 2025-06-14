# 🧰 Descargador Automático de Instaladores para Windows

Este script en Python automatiza la descarga de instaladores de software esencial para Windows, agrupando herramientas de desarrollo, multimedia, utilidades del sistema, drivers y más. Ideal para formateos, entornos limpios o configuraciones recurrentes.

---

## 📦 ¿Qué hace el script?

- Descarga múltiples instaladores desde URLs oficiales.
- Guarda los archivos en una carpeta llamada `manual_installers`.
- Registra un **log de estado** con éxito o fallos (`resumen.log`).
- Evita caracteres inválidos en nombres de archivos (compatibilidad con Windows).
- Incluye un recordatorio para instalar manualmente algunas apps especiales.

---

## 🛠️ Requisitos

- Python 3.8 o superior.
- Librería:
  - `requests`

Instalación:

```bash
pip install requests
```
