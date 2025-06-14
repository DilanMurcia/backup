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

    #Utilidades
    "winrar": "https://www.rarlab.com/rar/winrar-x64-602.exe",
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
 