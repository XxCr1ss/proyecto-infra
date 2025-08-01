#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento del sistema ML con Ray
"""

import sys
import os
import time
import requests
import json

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ray_pipeline():
    """Prueba el pipeline de Ray"""
    print("🧪 Probando pipeline de Ray...")
    
    try:
        from ray_parallelization.ml_pipeline import MLPipeline
        
        # Crear pipeline
        pipeline = MLPipeline(n_workers=2)
        
        # Ejecutar pipeline
        start_time = time.time()
        results = pipeline.run_pipeline()
        end_time = time.time()
        
        print(f"✅ Pipeline ejecutado en {end_time - start_time:.2f} segundos")
        print(f"   - Datos procesados: {results['data_processing']['processed_rows']}")
        print(f"   - Modelos entrenados: {results['model_training']['models_trained']}")
        print(f"   - R² del ensemble: {results['ensemble_performance']['ensemble_r2']:.4f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en pipeline de Ray: {e}")
        return False

def test_api_endpoints():
    """Prueba los endpoints de la API"""
    print("\n🧪 Probando endpoints de la API...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Health check
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check funcionando")
        else:
            print(f"❌ Health check falló: {response.status_code}")
            return False
        
        # Metrics
        response = requests.get(f"{base_url}/metrics", timeout=5)
        if response.status_code == 200:
            print("✅ Metrics endpoint funcionando")
        else:
            print(f"❌ Metrics endpoint falló: {response.status_code}")
            return False
        
        # Sample data
        response = requests.get(f"{base_url}/sample-data?n_samples=10", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sample data endpoint funcionando ({data['n_samples']} muestras)")
        else:
            print(f"❌ Sample data endpoint falló: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar a la API. ¿Está ejecutándose?")
        return False
    except Exception as e:
        print(f"❌ Error probando API: {e}")
        return False

def test_prediction():
    """Prueba la funcionalidad de predicción"""
    print("\n🧪 Probando predicciones...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Obtener datos de ejemplo
        response = requests.get(f"{base_url}/sample-data?n_samples=5", timeout=5)
        if response.status_code != 200:
            print("❌ No se pudieron obtener datos de ejemplo")
            return False
        
        sample_data = response.json()
        
        # Realizar predicción
        prediction_request = {
            "features": sample_data["features"]
        }
        
        response = requests.post(f"{base_url}/predict", 
                               json=prediction_request, 
                               timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Predicción exitosa ({len(result['predictions'])} predicciones)")
            print(f"   - Tiempo de predicción: {result['prediction_time']:.4f}s")
            return True
        else:
            print(f"❌ Predicción falló: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en predicción: {e}")
        return False

def test_benchmark():
    """Prueba la funcionalidad de benchmark"""
    print("\n🧪 Probando benchmark...")
    
    base_url = "http://localhost:8000"
    
    try:
        benchmark_request = {
            "data_size": 1000,
            "n_workers": 2
        }
        
        response = requests.post(f"{base_url}/benchmark", 
                               json=benchmark_request, 
                               timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            benchmark = result["benchmark_results"]
            print(f"✅ Benchmark exitoso")
            print(f"   - Speedup: {benchmark['speedup']:.2f}x")
            print(f"   - Eficiencia: {(benchmark['speedup'] / 2 * 100):.1f}%")
            return True
        else:
            print(f"❌ Benchmark falló: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en benchmark: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas del sistema ML con Ray")
    print("=" * 50)
    
    tests = [
        ("Pipeline de Ray", test_ray_pipeline),
        ("Endpoints de API", test_api_endpoints),
        ("Predicciones", test_prediction),
        ("Benchmark", test_benchmark)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error inesperado en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen de resultados
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El sistema está funcionando correctamente.")
        return 0
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los logs para más detalles.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 