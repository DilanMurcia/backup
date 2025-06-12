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
    "Brave Browser": "https://laptop-updates.brave.com/latest/winx64",
    "Firefox": "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=es-ES",
    "Google Chrome": "https://dl.google.com/chrome/install/GoogleChromeStandaloneEnterprise64.msi",

    # Desarrollo
    "Visual Studio Code": "https://update.code.visualstudio.com/latest/win32-x64-user/stable",
    "IntelliJ IDEA Community": "https://download.jetbrains.com/idea/ideaIU-2025.1.1.1.exe",
    "Node.js LTS": "https://nodejs.org/dist/v24.0.1/node-v24.0.1-x64.msi",
    "Git": "https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.exe",
    "NVM for Windows": "https://github.com/coreybutler/nvm-windows/releases/download/1.1.12/nvm-setup.exe",

    # Comunicación y productividad
    "Discord": "https://discord.com/api/download?platform=win",
    "Spotify": "https://download.scdn.co/SpotifySetup.exe",
    "Notion": "https://www.notion.so/desktop/windows/download",
    "WhatsApp": "https://get.microsoft.com/installer/download/9NKSQGP7F2NH?cid=website_cta_psi",
    "Telegram Desktop": "https://telegram.org/dl/desktop/win64",

    # Multimedia
    "OBS Studio": "https://cdn-fastly.obsproject.com/downloads/OBS-Studio-30.1.1-Full-Installer-x64.exe",
    "VLC Media Player": "https://download.videolan.org/pub/videolan/vlc/3.0.18/win64/vlc-3.0.18-win64.exe",
    "HandBrake": "https://github.com/HandBrake/HandBrake/releases/download/1.9.2/HandBrake-1.9.2-x86_64-Win_GUI.exe",
    "GIMP": "https://download.gimp.org/mirror/pub/gimp/v2.10/windows/gimp-2.10.34-setup.exe",

    # Infraestructura y bases de datos
    "Docker Desktop": "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe",
    "MongoDB Server": "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-8.0.10-signed.msi",
    "MongoDB Compass": "https://downloads.mongodb.com/compass/mongodb-compass-1.46.2-win32-x64.exe",
    "MySQL Community": "https://downloads.mysql.com/archives/get/p/25/file/mysql-installer-community-8.0.41.0.msi",
    "VirtualBox": "https://download.virtualbox.org/virtualbox/7.0.18/VirtualBox-7.0.18-162988-Win.exe",

    # Seguridad
    "Avast Antivirus": "https://files.avast.com/iavs9x/avast_free_antivirus_setup_online.exe",

    # Utilidades
    "7zip": "https://www.7-zip.org/a/7z2301-x64.exe",
    "WinDirStat": "https://github.com/windirstat/windirstat/releases/download/release/v2.2.2/WinDirStat-x64.msi",
   
   #Administrar Sistema Windows
    "Process Explorer": "https://live.sysinternals.com/procexp.exe",
    "Autoruns":"https://download.sysinternals.com/files/Autoruns.zip",
    "TCPView":"https://download.sysinternals.com/files/TCPView.zip",
    "Process Monitor":"https://download.sysinternals.com/files/ProcessMonitor.zip",
    "AccessChk":"https://download.sysinternals.com/files/AccessChk.zip",
    "RAMMap":"https://download.sysinternals.com/files/RAMMap.zip",
    
    #Analizar Hardware
    "CrystalDiskInfo":"https://cfhcable.dl.sourceforge.net/project/crystaldiskinfo/9.6.3/CrystalDiskInfo9_6_3.exe?viasf=1",
    "OCCT":"https://www.ocbase.com/download/edition:Personal/os:Windows",
    "Speccy":"https://speccy-system-information.uptodown.com/windows/descargar",
    
    #Instalar Drivers AMD CPU/GPU
    "Eliminar Drivers":"https://www.guru3d.com/getdownload/2c1b2414f56a6594ffef91236a87c0e976d52e0519bd313846bab016c2f20c7c4d6ce7dfe19a0bc843da8d448bbb670058b0c9ee9a26f5cf49bc39c97da070e6eb314629af3da2d24ab0413917f73b946419b5af447da45cefb517a0840ad3003abff4f9d5fe7828bbbb910ee270b704333a0283584211b2623dc4ca585fe82d4774d04b4af4b257b930215e13b2364fde129ef8d1f274e01f97997bd9cd142bafb48198bca595eb3c0ca399",
    "Drivers Windows":"https://drivers.amd.com/drivers/installer/25.10/whql/amd-software-adrenalin-edition-25.6.1-minimalsetup-250602_web.exe",
    
    # Lenguajes
    "Python 3": "https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe",
    "OpenJDK 21": "https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.3+9/OpenJDK21U-jdk_x64_windows_hotspot_21.0.3_9.msi",

    # Producción musical
    "Audacity": "https://muse-cdn.com/Audacity_Installer_via_MuseHub.exe",

    #Juegos
    "League of Legends": "https://lol.secure.dyn.riotcdn.net/channels/public/x/installer/current/live.la1.exe"
}

results = []

for app, url in apps.items():
    try:
        r = requests.get(url, allow_redirects=True)
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