#!/usr/bin/env python3
"""
Script de verificación de configuración de puertos
Verifica que todos los archivos del proyecto tengan la configuración correcta de puertos
"""

import os
import re
import sys

def check_file_for_port(file_path, expected_port="8001", old_port="8000"):
    """Verifica si un archivo tiene la configuración correcta de puertos"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar específicamente referencias al puerto 8000 (incorrecto)
        old_port_pattern = r':8000|8000:|\"8000\"|\'8000\''
        matches = re.findall(old_port_pattern, content)
        
        issues = []
        if matches:
            issues.append(f"Puerto {old_port} encontrado - debe ser {expected_port}")
        
        return issues
    except Exception as e:
        return [f"Error leyendo archivo: {e}"]


def main():
    """Función principal de verificación"""
    print("🔍 Verificando configuración de puertos...")
    print("=" * 50)
    
    # Archivos críticos a verificar
    critical_files = [
        "microservices/api/main.py",
        "api_simple.py",
        "docker-compose.yml",
        "docker-compose.simple.yml",
        "frontend/package.json",
        "frontend/src/config.js",
        "Dockerfile.api",
        "test_system.py",
        "deployment/README.md",
        "deployment/deploy.sh",
        "docs/INFORME_TECNICO.md"
    ]
    
    all_issues = []
    
    for file_path in critical_files:
        if os.path.exists(file_path):
            issues = check_file_for_port(file_path)
            if issues:
                print(f"❌ {file_path}:")
                for issue in issues:
                    print(f"   - {issue}")
                all_issues.extend(issues)
            else:
                print(f"✅ {file_path}")
        else:
            print(f"⚠️  {file_path} (no encontrado)")
    
    print("\n" + "=" * 50)
    
    if all_issues:
        print(f"❌ Se encontraron {len(all_issues)} problemas de configuración")
        return 1
    else:
        print("✅ Todos los archivos tienen la configuración correcta de puertos")
        print("\n📋 Resumen de configuración:")
        print("   - Backend API: Puerto 8001")
        print("   - Frontend: Puerto 3000")
        print("   - Ray Redis: Puerto 6379")
        print("   - Ray Dashboard: Puerto 8265")
        return 0


if __name__ == "__main__":
    sys.exit(main()) 