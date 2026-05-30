#!/usr/bin/env python3
import os
import re
from urllib.parse import urlparse

import requests

output_dir = "manual_installers"
os.makedirs(output_dir, exist_ok=True)
output_log = "resumen_cachyos.log"

apps = {
    # Navegadores
    "Brave Browser": "https://laptop-updates.brave.com/latest/linux-x64",
    "Firefox": "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=es-ES",
    "Visual Studio Code": "https://update.code.visualstudio.com/latest/linux-x64/stable",

    # Desarrollo
    "IntelliJ IDEA Community": "https://download.jetbrains.com/idea/ideaIC-2025.1.1.tar.gz",
    "Node.js LTS": "https://nodejs.org/dist/v24.0.1/node-v24.0.1-linux-x64.tar.xz",
    "Git": "https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.44.1.tar.gz",

    # Comunicación
    "Discord": "https://discord.com/api/download?platform=linux&format=tar.gz",
    "Telegram Desktop": "https://telegram.org/dl/desktop/linux",

    # Multimedia
    "OBS Studio": "https://github.com/obsproject/obs-studio/releases/download/30.1.1/obs-studio-30.1.1.tar.xz",
    "VLC Media Player": "https://get.videolan.org/vlc/3.0.18/linux/vlc-3.0.18.tar.xz",
    "HandBrake": "https://github.com/HandBrake/HandBrake/releases/download/1.9.2/HandBrake-1.9.2-source.tar.bz2",
    "GIMP": "https://download.gimp.org/pub/gimp/v2.10/gimp-2.10.34.tar.bz2",

    # Infraestructura y bases de datos
    "Docker Engine": "https://download.docker.com/linux/static/stable/x86_64/docker-24.0.6.tgz",
    "MongoDB Community": "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2004-6.0.7.tgz",
    "MySQL Community": "https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-8.0.41-linux-glibc2.12-x86_64.tar.xz",
    "VirtualBox": "https://download.virtualbox.org/virtualbox/7.0.18/VirtualBox-7.0.18.tar.bz2",

    # Utilidades
    "7zip": "https://sourceforge.net/projects/p7zip/files/p7zip/16.02/p7zip_16.02_src_all.tar.bz2",
    "Wine": "https://dl.winehq.org/wine/source/8.0/wine-8.0.tar.xz",

    # Juegos y entretenimiento
    "Steam": "https://cdn.cloudflare.steamstatic.com/client/installer/steam.deb",
    "Lutris": "https://github.com/lutris/lutris/releases/download/v1.7.3/lutris-1.7.3.tar.gz",

    # Lenguajes y runtimes
    "Python 3": "https://www.python.org/ftp/python/3.12.3/Python-3.12.3.tgz",
    "OpenJDK 21": "https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.3+9/OpenJDK21U-jdk_x64_linux_hotspot_21.0.3_9.tar.gz",
}

results = []


def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*\n\r\t]', "_", filename)


def get_filename_from_response(response, fallback_url):
    # Extrae el nombre de archivo de Content-Disposition si el servidor lo proporciona.
    # También maneja encabezados con filename* y UTF-8 encoded filenames.
    cd = response.headers.get("Content-Disposition", "")
    if "filename=" in cd:
        match = re.search(r"filename\*?=(?:UTF-8'')?\"?([^\";]+)\"?", cd)
        if match:
            return match.group(1)
        return cd.split("filename=")[1].strip('"').strip()

    parsed = urlparse(response.url)
    name = os.path.basename(parsed.path)
    if name:
        return name

    parsed_fallback = urlparse(fallback_url)
    return os.path.basename(parsed_fallback.path) or None


def download_app(app, url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=30)
        response.raise_for_status()

        filename = get_filename_from_response(response, url)
        if not filename or not os.path.splitext(filename)[1]:
            filename = sanitize_filename(app.replace(" ", "_") + ".tar.gz")

        filename = sanitize_filename(filename)
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "wb") as f:
            f.write(response.content)

        return True, filename
    except Exception as exc:
        return False, str(exc)


def main():
    print("Descargando instaladores directos para CachyOS...")
    for app, url in apps.items():
        print(f"-> {app}")
        success, detail = download_app(app, url)
        status = "✅" if success else "❌"
        results.append((app, status, detail))

    print("\nResumen de descargas:")
    for app, status, detail in results:
        print(f"{status} {app} -> {detail}")

    with open(output_log, "w", encoding="utf-8") as log:
        for app, status, detail in results:
            log.write(f"{status} {app} -> {detail}\n")
        log.write("\nDirectorio de descargas: {}\n".format(os.path.abspath(output_dir)))


if __name__ == "__main__":
    main()
