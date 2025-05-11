# Verifica si winget está instalado
function Check-Winget {
    try {
        winget --version
        return $true
    } catch {
        Write-Host "winget no está instalado o no es compatible en este sistema." -ForegroundColor Red
        return $false
    }
}

# Verifica si Chocolatey está instalado
function Check-Chocolatey {
    try {
        choco --version
        return $true
    } catch {
        Write-Host "Chocolatey no está instalado." -ForegroundColor Red
        return $false
    }
}

# Verifica si el software está disponible en winget o no
function Install-With-Winget {
    param ($appId)
    if (Check-Winget) {
        winget install --id $appId --source winget --accept-source-agreements --accept-package-agreements
    } else {
        Write-Host "No se pudo encontrar winget. Intentando con Chocolatey..." -ForegroundColor Yellow
        Install-With-Chocolatey $appId
    }
}

# Intentar instalar con Chocolatey si winget no está disponible
function Install-With-Chocolatey {
    param ($appId)
    if (Check-Chocolatey) {
        choco install $appId -y
    } else {
        Write-Host "No se pudo encontrar Chocolatey. Proporcionando enlace de descarga manual." -ForegroundColor Red
        Provide-Manual-DownloadLink $appId
    }
}

# Proporcionar enlace de descarga manual si no se puede instalar con winget o chocolatey
function Provide-Manual-DownloadLink {
    param ($appId)
    # Aquí puedes agregar enlaces específicos de descarga manual según el ID de la aplicación
    switch ($appId) {
        # Navegadores
        "BraveSoftware.BraveBrowser" { Write-Host "Descarga manual de Brave: https://brave.com/download/" }
        "Mozilla.Firefox" { Write-Host "Descarga manual de Firefox: https://www.mozilla.org/firefox/download/" }
        "Google.Chrome" { Write-Host "Descarga manual de Google Chrome: https://www.google.com/chrome/" }

        # Herramientas de Desarrollo
        "Microsoft.VisualStudioCode" { Write-Host "Descarga manual de Visual Studio Code: https://code.visualstudio.com/download" }
        "JetBrains.IntelliJIDEA.Community" { Write-Host "Descarga manual de IntelliJ IDEA Community Edition: https://www.jetbrains.com/idea/download/" }
        "OpenJS.NodeJS.LTS" { Write-Host "Descarga manual de Node.js: https://nodejs.org/en/download/" }
        "Git.Git" { Write-Host "Descarga manual de Git: https://git-scm.com/downloads" }
        "coreybutler.nvm" { Write-Host "Descarga manual de NVM para Windows: https://github.com/coreybutler/nvm-windows/releases" }

        # Aplicaciones de Productividad y Comunicación
        "Spotify.Spotify" { Write-Host "Descarga manual de Spotify: https://www.spotify.com/download/" }
        "Discord.Discord" { Write-Host "Descarga manual de Discord: https://discord.com/download" }
        "Notion.Notion" { Write-Host "Descarga manual de Notion: https://www.notion.so/desktop" }
        "WhatsApp.WhatsApp" { Write-Host "Descarga manual de WhatsApp Web: https://www.whatsapp.com/download" }
        "RiotGames.LeagueOfLegends" { Write-Host "Descarga manual de League of Legends: https://signup.leagueoflegends.com/es-mx/#/" }
        "Telegram.TelegramDesktop" { Write-Host "Descarga manual de Telegram Desktop: https://desktop.telegram.org/" }

        # Herramientas de Infraestructura y Bases de Datos
        "Docker.DockerDesktop" { Write-Host "Descarga manual de Docker Desktop: https://www.docker.com/products/docker-desktop" }
        "MongoDB.Compass" { Write-Host "Descarga manual de MongoDB Compass: https://www.mongodb.com/try/download/compass" }
        "MySQL.MySQLServer" { Write-Host "Descarga manual de MySQL: https://dev.mysql.com/downloads/installer/" }
        "MySQL.MySQLWorkbench" { Write-Host "Descarga manual de MySQL Workbench: https://dev.mysql.com/downloads/workbench/" }
        "Oracle.VirtualBox" { Write-Host "Descarga manual de Oracle VirtualBox: https://www.virtualbox.org/wiki/Downloads" }

        # Herramientas para Multimedia y Diseño
        "Adobe.AfterEffects" { Write-Host "Descarga manual de Adobe After Effects 2019: https://adobe.com/downloads" }
        "OBSProject.OBSStudio" { Write-Host "Descarga manual de OBS Studio: https://obsproject.com/download" }
        "Audacity.Audacity" { Write-Host "Descarga manual de Audacity: https://www.audacityteam.org/download/" }
        "Kiritax64" { Write-Host "Descarga manual de Kiritax64: [Aquí iría la URL]" }
        "REVisionEffects.OFX" { Write-Host "Descarga manual de RE:Vision Effects OFX: [Aquí iría la URL]" }
        "HandBrake.HandBrake" { Write-Host "Descarga manual de HandBrake: https://handbrake.fr/downloads.php" }
        "Cakewalk.Cakewalk" { Write-Host "Descarga manual de Cakewalk: https://www.bandlab.com/products/cakewalk" }
        "Apple.MobileDeviceSupport" { Write-Host "Descarga manual de Apple Mobile Device Support: [Aquí iría la URL]" }
        "Apple.Bonjour" { Write-Host "Descarga manual de Bonjour: [Aquí iría la URL]" }
        
        # Herramientas de Seguridad
        "Avast.AvastFreeAntivirus" { Write-Host "Descarga manual de Avast: https://www.avast.com/es-es/index" }
        "Malwarebytes.Malwarebytes" { Write-Host "Descarga manual de Malwarebytes: https://www.malwarebytes.com/mwb-download" }

        # Utilidades y Otros
        "7zip.7zip" { Write-Host "Descarga manual de 7zip: https://www.7-zip.org/download.html" }
        "WinDirStat.WinDirStat" { Write-Host "Descarga manual de WinDirStat: https://windirstat.net/download.html" }

        # Herramientas de Java y Python
        "AdoptOpenJDK.OpenJDK.17" { Write-Host "Descarga manual de OpenJDK 17: https://adoptium.net/" }
        "Python.Python.3" { Write-Host "Descarga manual de Python 3: https://www.python.org/downloads/" }

        # Software de Música
        "MuseScore.MuseScore" { Write-Host "Descarga manual de MuseScore: https://musescore.org/es" }
        "MuseScore.MuseHub" { Write-Host "Descarga manual de MuseHub: https://musescore.org/es/musehub" }

        # Caso por defecto si no hay enlace disponible
        default { Write-Host "No hay enlace de descarga manual disponible para $appId" }
    }
}

# Lista de aplicaciones para instalar
$apps = @(
    # Navegadores
    @{name = "Brave Browser"; id = "BraveSoftware.BraveBrowser"},
    @{name = "Firefox"; id = "Mozilla.Firefox"},
    @{name = "Google Chrome"; id = "Google.Chrome"},

    # Herramientas de Desarrollo
    @{name = "Visual Studio Code"; id = "Microsoft.VisualStudioCode"},
    @{name = "IntelliJ IDEA Community Edition 2024"; id = "JetBrains.IntelliJIDEA.Community"},
    @{name = "Node.js LTS"; id = "OpenJS.NodeJS.LTS"},
    @{name = "Git"; id = "Git.Git"},
    @{name = "NVM for Windows"; id = "coreybutler.nvm"},

    # Aplicaciones de Productividad y Comunicación
    @{name = "Spotify"; id = "Spotify.Spotify"},
    @{name = "Discord"; id = "Discord.Discord"},
    @{name = "Notion"; id = "Notion.Notion"},
    @{name = "WhatsApp Web"; id = "WhatsApp.WhatsApp"},
    @{name = "League of Legends"; id = "RiotGames.LeagueOfLegends"},
    @{name = "Telegram Desktop"; id = "Telegram.TelegramDesktop"},

    # Herramientas de Infraestructura y Bases de Datos
    @{name = "Docker Desktop"; id = "Docker.DockerDesktop"},
    @{name = "MongoDB Compass"; id = "MongoDB.Compass"},
    @{name = "MySQL Community Server"; id = "MySQL.MySQLServer"},
    @{name = "MySQL Workbench"; id = "MySQL.MySQLWorkbench"},
    @{name = "Oracle VirtualBox"; id = "Oracle.VirtualBox"},

    # Herramientas para Multimedia y Diseño
    @{name = "Adobe After Effects 2019"; id = "Adobe.AfterEffects"},
    @{name = "OBS Studio"; id = "OBSProject.OBSStudio"},
    @{name = "Audacity"; id = "Audacity.Audacity"},

    # Herramientas de Seguridad
    @{name = "Avast Antivirus"; id = "Avast.AvastFreeAntivirus"},
    @{name = "Malwarebytes"; id = "Malwarebytes.Malwarebytes"},

    # Utilidades y Otros
    @{name = "7zip"; id = "7zip.7zip"},
    @{name = "WinDirStat"; id = "WinDirStat.WinDirStat"},

    # Herramientas de Java y Python
    @{name = "OpenJDK 17"; id = "AdoptOpenJDK.OpenJDK.17"},
    @{name = "Python 3"; id = "Python.Python.3"},

    # Software de Música
    @{name = "MuseScore"; id = "MuseScore.MuseScore"},
    @{name = "MuseHub"; id = "MuseScore.MuseHub"}
)

foreach ($app in $apps) {
    $answer = Read-Host "¿Quieres instalar $($app.name)? (s/n)"
    if ($answer -eq "s") {
        Write-Host "Instalando $($app.name)..." -ForegroundColor Cyan
        Install-With-Winget $app.id
    } else {
        Write-Host "Saltando $($app.name)." -ForegroundColor Yellow
    }
}

Write-Host "Proceso de instalación terminado." -ForegroundColor Green
