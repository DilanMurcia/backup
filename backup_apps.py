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
    # Controladores de la placa base A520M-HDV de Rita
    #Para gestionar el procesador y la placa base.
    "AMD chipset driver ver:4.7.13.2243":"https://download.asrock.com/Drivers/CPU/Chipset(v4.7.13.2243).zip",
    #Para el sonido analógico.
    "Realtek high definition audio driver": "https://download.asrock.com/Drivers/All/Audio/Realtek_Audio(v6.0.9384.1_WHQL_RTK).zip",
    #Para el internet por cable.
    "Realtek Lan driver":"https://download.asrock.com/Drivers/All/LAN/Realtek_LAN(v10.060.0615.2022).zip",
    #Para tus gráficos integrados Vega.
    "AMD Graphics Driver (ver:22.20.2.220623)":"https://download.asrock.com/Drivers/VGA/AMD_VGA(v22.20.2.220623).zip",
    #Soporte por si tienes un disco duro NVMe.
    "AMD NVMe_DID":"https://download.asrock.com/Drivers/AMD/SATA/AM4_SATA_Floppy_DID(v9.3.0.296).zip",
    #Extras recomendados para la placa base.
    "ASRock Motherboard Utility ver:3.0.504":"https://download.asrock.com/Utility/MotherboardUtility/MotherboardUtility(v3.0.504).zip",
    "Restart to UEFI ver:1.0.15":"https://download.asrock.com/Utility/Others/RestartToUEFI(v1.0.15).zip",
    "APP Shop ver:2.0.0.6":"https://download.asrock.com/Utility/Others/APPShop(v2.0.0.6).zip"
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

    log.write("No olvides instalar el instalador automatico de graficos de AMD:\nhttps://www.amd.com/en/support/download/drivers.html")