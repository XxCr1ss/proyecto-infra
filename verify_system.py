#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de verificación del sistema

Este script verifica que todos los componentes del sistema estén funcionando correctamente.
Comprueba la conectividad con la API, el frontend y el cluster Ray (si está disponible).
"""

import os
import sys
import time
import json
import subprocess
import platform
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Colores para la salida en terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Desactivar colores en Windows si no se soporta
if platform.system() == 'Windows' and not os.environ.get('ANSICON'):
    Colors.HEADER = ''
    Colors.OKBLUE = ''
    Colors.OKGREEN = ''
    Colors.WARNING = ''
    Colors.FAIL = ''
    Colors.ENDC = ''
    Colors.BOLD = ''
    Colors.UNDERLINE = ''

# Configuración
API_URL = "http://localhost:8001"
FRONTEND_URL = "http://localhost:3000"
RAY_DASHBOARD_URL = "http://localhost:8265"

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {text} ==={Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKBLUE}ℹ {text}{Colors.ENDC}")

def check_url(url, description, timeout=5):
    print(f"Verificando {description} ({url})...")
    try:
        req = Request(url)
        response = urlopen(req, timeout=timeout)
        print_success(f"{description} está disponible. Código de estado: {response.status}")
        return True
    except HTTPError as e:
        print_warning(f"{description} respondió con error HTTP: {e.code}")
        return False
    except URLError as e:
        print_error(f"No se pudo conectar a {description}: {e.reason}")
        return False
    except Exception as e:
        print_error(f"Error al verificar {description}: {str(e)}")
        return False

def check_api_health():
    url = f"{API_URL}/health"
    try:
        req = Request(url)
        response = urlopen(req, timeout=5)
        data = json.loads(response.read().decode('utf-8'))
        if data.get('status') == 'ok':
            print_success("API health check pasó correctamente")
            return True
        else:
            print_warning(f"API health check respondió con estado inesperado: {data}")
            return False
    except Exception as e:
        print_error(f"Error al verificar API health: {str(e)}")
        return False

def check_api_docs():
    return check_url(f"{API_URL}/docs", "Documentación de la API")

def check_docker_status():
    print("Verificando estado de Docker...")
    try:
        result = subprocess.run(['docker', 'ps'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              text=True,
                              check=False)
        if result.returncode == 0:
            print_success("Docker está en ejecución")
            return True
        else:
            print_error(f"Docker no está en ejecución o no está instalado: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"Error al verificar Docker: {str(e)}")
        return False

def check_docker_compose_status():
    print("Verificando contenedores de Docker Compose...")
    try:
        result = subprocess.run(['docker-compose', 'ps'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              text=True,
                              check=False)
        if result.returncode == 0:
            if "Up" in result.stdout:
                print_success("Contenedores de Docker Compose están en ejecución")
                return True
            else:
                print_warning("Docker Compose está disponible pero los contenedores no están en ejecución")
                return False
        else:
            print_error(f"Error con Docker Compose: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"Error al verificar Docker Compose: {str(e)}")
        return False

def check_ray_status():
    # Primero intentamos con el dashboard
    dashboard_available = check_url(RAY_DASHBOARD_URL, "Dashboard de Ray")
    
    # Luego verificamos con ray CLI si está disponible
    print("Verificando estado de Ray con CLI...")
    try:
        result = subprocess.run(['ray', 'status'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              text=True,
                              check=False)
        if result.returncode == 0 and "ALIVE" in result.stdout:
            print_success("Cluster Ray está activo según CLI")
            return True
        else:
            if dashboard_available:
                print_warning("Ray CLI no disponible pero el dashboard responde")
                return True
            else:
                print_error("Cluster Ray no está activo o no está accesible")
                return False
    except Exception as e:
        if dashboard_available:
            print_warning(f"Ray CLI no disponible pero el dashboard responde: {str(e)}")
            return True
        else:
            print_error(f"Error al verificar Ray: {str(e)}")
            return False

def check_ports():
    print_header("Verificando puertos")
    ports = [
        (8001, "API Backend"),
        (3000, "Frontend"),
        (6379, "Ray Redis"),
        (8265, "Ray Dashboard"),
        (10001, "Ray Client")
    ]
    
    for port, service in ports:
        try:
            # Verificamos si el puerto está en uso
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex(('localhost', port))
            s.close()
            
            if result == 0:
                print_success(f"Puerto {port} ({service}) está en uso")
            else:
                print_warning(f"Puerto {port} ({service}) no está en uso")
        except Exception as e:
            print_error(f"Error al verificar puerto {port}: {str(e)}")

def main():
    print_header("Verificación del Sistema")
    
    # Verificar componentes principales
    api_available = check_url(API_URL, "API Backend")
    frontend_available = check_url(FRONTEND_URL, "Frontend")
    
    if api_available:
        check_api_health()
        check_api_docs()
    
    # Verificar Docker y Ray solo si la API no está disponible o si se especifica
    if not api_available or '--full' in sys.argv:
        check_docker_status()
        check_docker_compose_status()
        check_ray_status()
    
    # Verificar puertos
    check_ports()
    
    # Resumen
    print_header("Resumen")
    if api_available and frontend_available:
        print_success("El sistema está funcionando correctamente")
        print_info("API: " + API_URL)
        print_info("Frontend: " + FRONTEND_URL)
        print_info("Documentación API: " + API_URL + "/docs")
    elif api_available:
        print_warning("API disponible pero el frontend no responde")
        print_info("Verifica que el frontend esté en ejecución")
    elif frontend_available:
        print_warning("Frontend disponible pero la API no responde")
        print_info("Verifica que la API esté en ejecución")
    else:
        print_error("Ni la API ni el frontend están respondiendo")
        print_info("Verifica que los servicios estén en ejecución")
        print_info("Para modo simplificado: python api_simple.py y npm start en frontend/")
        print_info("Para modo completo: docker-compose up --build")

if __name__ == "__main__":
    main()