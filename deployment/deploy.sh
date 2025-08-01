#!/bin/bash

# Script de despliegue automático para AWS EC2
# Uso: ./deploy.sh [start|stop|restart|status|logs]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Verificar que Docker esté instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        error "Docker no está instalado. Instalando..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
        success "Docker instalado correctamente"
    else
        log "Docker ya está instalado"
    fi
}

# Verificar que Docker Compose esté instalado
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose no está instalado. Instalando..."
        sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
        success "Docker Compose instalado correctamente"
    else
        log "Docker Compose ya está instalado"
    fi
}

# Verificar archivos necesarios
check_files() {
    if [ ! -f "docker-compose.yml" ]; then
        error "docker-compose.yml no encontrado"
        exit 1
    fi
    
    if [ ! -f "requirements.txt" ]; then
        error "requirements.txt no encontrado"
        exit 1
    fi
    
    if [ ! -d "microservices" ]; then
        error "Directorio microservices no encontrado"
        exit 1
    fi
    
    if [ ! -d "ray_parallelization" ]; then
        error "Directorio ray_parallelization no encontrado"
        exit 1
    fi
    
    if [ ! -d "frontend" ]; then
        error "Directorio frontend no encontrado"
        exit 1
    fi
    
    success "Todos los archivos necesarios están presentes"
}

# Crear archivo .env si no existe
create_env() {
    if [ ! -f ".env" ]; then
        log "Creando archivo .env..."
        cat > .env << EOF
RAY_DISABLE_IMPORT_WARNING=1
PYTHONPATH=/app
REACT_APP_API_URL=http://localhost:8001
EOF
        success "Archivo .env creado"
    else
        log "Archivo .env ya existe"
    fi
}

# Función para iniciar servicios
start_services() {
    log "Iniciando servicios..."
    
    # Construir imágenes si es necesario
    log "Construyendo imágenes Docker..."
    docker-compose build --no-cache
    
    # Iniciar servicios
    log "Iniciando servicios con Docker Compose..."
    docker-compose up -d
    
    # Esperar a que los servicios estén listos
    log "Esperando a que los servicios estén listos..."
    sleep 30
    
    # Verificar estado
    check_health
}

# Función para detener servicios
stop_services() {
    log "Deteniendo servicios..."
    docker-compose down
    success "Servicios detenidos"
}

# Función para reiniciar servicios
restart_services() {
    log "Reiniciando servicios..."
    docker-compose down
    docker-compose up -d
    sleep 30
    check_health
}

# Función para verificar estado
check_health() {
    log "Verificando estado de los servicios..."
    
    # Verificar API
    if curl -f http://localhost:8001/health &> /dev/null; then
        success "API está funcionando"
    else
        error "API no está respondiendo"
    fi
    
    # Verificar Frontend
    if curl -f http://localhost:3000 &> /dev/null; then
        success "Frontend está funcionando"
    else
        error "Frontend no está respondiendo"
    fi
    
    # Verificar Ray Dashboard
    if curl -f http://localhost:8265 &> /dev/null; then
        success "Ray Dashboard está funcionando"
    else
        error "Ray Dashboard no está respondiendo"
    fi
    
    # Mostrar estado de contenedores
    log "Estado de contenedores:"
    docker-compose ps
}

# Función para mostrar logs
show_logs() {
    log "Mostrando logs de todos los servicios..."
    docker-compose logs -f
}

# Función para mostrar logs de un servicio específico
show_service_logs() {
    local service=$1
    if [ -z "$service" ]; then
        error "Debe especificar un servicio (api, frontend, ray-head, ray-worker-1, ray-worker-2)"
        exit 1
    fi
    
    log "Mostrando logs del servicio: $service"
    docker-compose logs -f "$service"
}

# Función para escalar workers
scale_workers() {
    local count=$1
    if [ -z "$count" ]; then
        count=2
    fi
    
    log "Escalando workers a $count instancias..."
    docker-compose up -d --scale ray-worker-1=$count --scale ray-worker-2=$count
    success "Workers escalados a $count instancias"
}

# Función para backup
backup_data() {
    local backup_dir="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    log "Creando backup en $backup_dir..."
    
    # Backup de logs
    docker-compose logs > "$backup_dir/docker-logs.txt"
    
    # Backup de configuraciones
    cp docker-compose.yml "$backup_dir/"
    cp .env "$backup_dir/" 2>/dev/null || true
    
    # Backup de datos (si existen)
    if [ -d "data" ]; then
        tar -czf "$backup_dir/data.tar.gz" data/
    fi
    
    success "Backup creado en $backup_dir"
}

# Función para mostrar información del sistema
show_system_info() {
    log "Información del sistema:"
    echo "=== Docker Info ==="
    docker info | head -20
    
    echo -e "\n=== Docker Compose Services ==="
    docker-compose ps
    
    echo -e "\n=== System Resources ==="
    echo "CPU: $(nproc) cores"
    echo "Memory: $(free -h | awk '/^Mem:/{print $2}')"
    echo "Disk: $(df -h / | awk 'NR==2{print $4}') available"
    
    echo -e "\n=== Network Ports ==="
    netstat -tlnp | grep -E ':(3000|8001|6379|8265)'
}

# Función principal
main() {
    local action=$1
    local service=$2
    
    case $action in
        "start")
            check_docker
            check_docker_compose
            check_files
            create_env
            start_services
            ;;
        "stop")
            stop_services
            ;;
        "restart")
            restart_services
            ;;
        "status")
            check_health
            ;;
        "logs")
            show_logs
            ;;
        "service-logs")
            show_service_logs "$service"
            ;;
        "scale")
            scale_workers "$service"
            ;;
        "backup")
            backup_data
            ;;
        "info")
            show_system_info
            ;;
        "update")
            log "Actualizando aplicación..."
            git pull origin main
            restart_services
            ;;
        *)
            echo "Uso: $0 {start|stop|restart|status|logs|service-logs|scale|backup|info|update}"
            echo ""
            echo "Comandos disponibles:"
            echo "  start         - Iniciar todos los servicios"
            echo "  stop          - Detener todos los servicios"
            echo "  restart       - Reiniciar todos los servicios"
            echo "  status        - Verificar estado de los servicios"
            echo "  logs          - Mostrar logs de todos los servicios"
            echo "  service-logs  - Mostrar logs de un servicio específico"
            echo "  scale <num>   - Escalar workers a N instancias"
            echo "  backup        - Crear backup de datos y configuraciones"
            echo "  info          - Mostrar información del sistema"
            echo "  update        - Actualizar aplicación desde Git"
            echo ""
            echo "Ejemplos:"
            echo "  $0 start"
            echo "  $0 service-logs api"
            echo "  $0 scale 4"
            exit 1
            ;;
    esac
}

# Ejecutar función principal
main "$@" 