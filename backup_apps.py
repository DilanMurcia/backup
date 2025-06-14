import os
import re
from urllib.parse import urlparse
import requests

output_dir = "manual_installers"
os.makedirs(output_dir, exist_ok=True)

def sanitize_filename(filename):
    # Quita caracteres inválidos en Windows
    return re.sub(r'[<>:"/\\|?*\n\r\t]', '_', filename)

apps = {
    # Navegadores
    "Google Chrome": "https://dl.google.com/chrome/install/GoogleChromeStandaloneEnterprise64.msi",

    # Comunicación y productividad
    "Discord": "https://discord.com/api/download?platform=win",
    "Spotify": "https://download.scdn.co/SpotifySetup.exe",
    "Notion": "https://www.notion.so/desktop/windows/download",
    "WhatsApp": "https://get.microsoft.com/installer/download/9NKSQGP7F2NH?cid=website_cta_psi",
    "Telegram Desktop": "https://telegram.org/dl/desktop/win64",
    
    # Utilidades
    "WinRAR": "https://www.win-rar.com/fileadmin/winrar-versions/winrar-x64-611.exe" 
}

results = []

for app, url in apps.items():
    try:
        r = requests.get(url, allow_redirects=True, timeout=15)
        r.raise_for_status()

        # Intentar extraer nombre de archivo
        cd = r.headers.get("Content-Disposition", "")
        filename = None
        if "filename=" in cd:
            match = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^\";]+)"?', cd)
            if match:
                filename = match.group(1)
            else:
                filename = cd.split("filename=")[1].strip('"').strip()
        else:
            parsed = urlparse(r.url)
            filename = os.path.basename(parsed.path)

        if not filename or not os.path.splitext(filename)[1]:
            filename = app.replace(" ", "_").replace(".", "") + ".exe"

        filename = sanitize_filename(filename)
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "wb") as f:
            f.write(r.content)

        results.append((app, "✅", filename))
    except Exception as e:
        results.append((app, "❌", str(e)))

# Mostrar resumen por consola
for app, status, detail in results:
    print(f"{status} {app} -> {detail}")

# Guardar resumen en archivo
with open("resumen.log", "w", encoding="utf-8") as log:
    for app, status, detail in results:
        log.write(f"{status} {app} -> {detail}\n")
    log.write("\nNO OLVIDAR INSTALAR LAS APPS MANUALES\n")
    log.write("## Minecraft Java no Premium:\nhttps://tlauncher.org/\n")
    log.write("## Minecraft Bedrock:\nhttps://www.youtube.com/watch?v=-3mwKc1EwCs\n")
    log.write("https://drive.google.com/file/d/12L-I8W-8qgajqR58jfsK1w66jCO69sdQ/view?pli=1\n")
    log.write("## IntelliJ IDEA Ultimate:\nhttps://www.youtube.com/watch?v=XG-pJcqOjQw\n")
    log.write("## Adobe effects 2019:\nhttps://www.mediafire.com/file/u0izk6c02q6jx9o/AAECC19_v16.1.2.55.rar/file\n")
    log.write("https://drive.usercontent.google.com/download?id=1xbGRRD9gJ4aXCH5TStb4s41TBBL-QmLK&export=download&authuser=0\n")