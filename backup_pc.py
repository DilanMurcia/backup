import os
from urllib.parse import urlparse
import requests

# Carpeta destino
output_dir = "manual_installers"
os.makedirs(output_dir, exist_ok=True)

# URLs actualizadas y confiables
apps = {
    "Brave Browser": "https://laptop-updates.brave.com/latest/winx64",
    "Firefox": "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=es-ES",
    "Google Chrome": "https://dl.google.com/chrome/install/GoogleChromeStandaloneEnterprise64.msi",
    "Visual Studio Code": "https://update.code.visualstudio.com/latest/win32-x64-user/stable",
    "Notion": "https://www.notion.com/desktop/windows/download?from=marketing&pathname=%2Fes%2Fdesktop&tid=ed06fb8881a7472daf5e96df593df77c",
    "Node.js LTS": "https://nodejs.org/dist/v24.0.1/node-v24.0.1-x64.msi",
    "Git": "https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.exe",
    "NVM for Windows": "https://github.com/coreybutler/nvm-windows/releases/download/1.1.12/nvm-setup.exe",
    "Discord": "https://discord.com/api/download?platform=win",
    "Telegram Desktop": "https://telegram.org/dl/desktop/win64",
    "Docker Desktop": "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe",
    "MySQL Workbench": "https://dev.mysql.com/get/Downloads/MySQLGUITools/mysql-workbench-community-8.0.36-winx64.msi",
    "OBS Studio": "https://cdn-fastly.obsproject.com/downloads/OBS-Studio-30.1.1-Full-Installer-x64.exe",
    "7zip": "https://www.7-zip.org/a/7z2301-x64.exe",
    "Python 3": "https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe",
    "OpenJDK 21": "https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.3+9/OpenJDK21U-jdk_x64_windows_hotspot_21.0.3_9.msi"
}

# Descargar los instaladores
results = []
for app, url in apps.items():
    try:
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path)
        if not filename or "?" in filename:
            filename = app.replace(" ", "_").replace(".", "") + ".exe"
        filepath = os.path.join(output_dir, filename)

        print(f"⬇️  Descargando {app} desde {url}...")

        r = requests.get(url, allow_redirects=True, timeout=60)
        r.raise_for_status()

        with open(filepath, "wb") as f:
            f.write(r.content)

        print(f"✅ {app} descargado correctamente como {filename}")
        results.append((app, "Éxito", filename))
    except Exception as e:
        print(f"❌ Error al descargar {app}: {str(e)}")
        results.append((app, "Fallo", str(e)))

# Mostrar resumen final
print("\n===== RESUMEN DE DESCARGAS =====")
successes = [r for r in results if r[1] == "Éxito"]
failures = [r for r in results if r[1] == "Fallo"]

print(f"✔️  Completadas: {len(successes)}")
for app, _, filename in successes:
    print(f"  - {app}: {filename}")

print(f"\n❌ Fallidas: {len(failures)}")
for app, _, error in failures:
    print(f"  - {app}: {error}")

# Guardar resumen en archivo
with open("resumen.log", "w", encoding="utf-8") as f:
    f.write("===== RESUMEN DE DESCARGAS =====\n")
    f.write(f"✔️  Completadas: {len(successes)}\n")
    for app, _, filename in successes:
        f.write(f"  - {app}: {filename}\n")
    f.write(f"\n❌ Fallidas: {len(failures)}\n")
    for app, _, error in failures:
        f.write(f"  - {app}: {error}\n")

print("\n📄 Resumen guardado en resumen.log")
