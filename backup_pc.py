import os
from urllib.parse import urlparse
import requests

output_dir = "manual_installers"
os.makedirs(output_dir, exist_ok=True)

apps = {
    "Brave Browser": "https://laptop-updates.brave.com/latest/winx64",
    "Firefox": "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=es-ES",
    "Google Chrome": "https://dl.google.com/chrome/install/GoogleChromeStandaloneEnterprise64.msi",
    "Visual Studio Code": "https://update.code.visualstudio.com/latest/win32-x64-user/stable",
    "Notion": "https://www.notion.so/desktop/windows/download?from=marketing&pathname=/es/desktop",
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

results = []

for app, url in apps.items():
    try:
        r = requests.get(url, allow_redirects=True)
        r.raise_for_status()

        # Detectar nombre del archivo desde headers o URL
        cd = r.headers.get("Content-Disposition", "")
        if "filename=" in cd:
            filename = cd.split("filename=")[1].strip('"').strip()
        else:
            parsed = urlparse(r.url)  # usar r.url por si hubo redirección
            filename = os.path.basename(parsed.path)

        # Si no tiene extensión válida, usar nombre base del app
        if not filename or not os.path.splitext(filename)[1]:
            filename = app.replace(" ", "_").replace(".", "") + ".exe"

        filepath = os.path.join(output_dir, filename)
        with open(filepath, "wb") as f:
            f.write(r.content)

        results.append((app, "✅", filename))
    except Exception as e:
        results.append((app, "❌", str(e)))

# Mostrar los resultados
for app, status, detail in results:
    print(f"{status} {app} -> {detail}")
