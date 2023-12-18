# ...

# Inicia Docker Desktop
Write-Host "Iniciando Docker Desktop..."
#Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe" -Wait
Write-Host "Docker Desktop iniciado correctamente."

# Espera un tiempo para que Docker Desktop se inicie completamente
$tiempoEsperaDesktop = 10
Start-Sleep -Seconds $tiempoEsperaDesktop
Write-Host "Progreso: 33%"

# Construye la imagen de Docker
Write-Host "Construyendo la imagen de Docker..."
docker build -t my_airflow .
Write-Host "Imagen de Docker construida correctamente."

# Espera un tiempo para que construya la imagen de Docker
$tiempoEsperaImagen = 10
Start-Sleep -Seconds $tiempoEsperaImagen
Write-Host "Progreso: 66%"

# Inicia Docker Compose en modo daemon (-d)
Write-Host "Iniciando Docker Compose..."
docker-compose up -d
Write-Host "Docker Compose iniciado correctamente."

# Progreso completo
Write-Host "Progreso: 100%"
