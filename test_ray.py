#!/usr/bin/env python3
"""
Script de prueba para verificar que Ray funciona correctamente
"""

import sys
import os
import time

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ray_basic():
    """Prueba básica de Ray"""
    print("🧪 Probando inicialización básica de Ray...")
    
    try:
        import ray
        from ray_parallelization.init_ray import init_ray_cluster, get_ray_status
        
        # Inicializar Ray
        if init_ray_cluster():
            print("✅ Ray inicializado correctamente")
            
            # Obtener estado
            status = get_ray_status()
            print(f"📊 Estado de Ray: {status}")
            
            return True
        else:
            print("❌ No se pudo inicializar Ray")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba básica: {e}")
        return False

def test_ray_pipeline():
    """Prueba del pipeline de ML con Ray"""
    print("\n🧪 Probando pipeline de ML con Ray...")
    
    try:
        from ray_parallelization.ml_pipeline import MLPipeline
        
        # Crear pipeline
        pipeline = MLPipeline(n_workers=2)
        print("✅ Pipeline creado correctamente")
        
        # Generar datos de prueba
        data = pipeline.generate_sample_data(1000)
        print(f"✅ Datos generados: {len(data)} filas")
        
        # Procesar datos
        processed_data = pipeline.parallel_data_processing(data)
        print(f"✅ Datos procesados: {len(processed_data)} filas")
        
        # Preparar features
        feature_cols = [col for col in processed_data.columns if col.startswith('feature')]
        X = processed_data[feature_cols].values
        y = processed_data['target'].values
        
        # Entrenar modelos
        training_results = pipeline.parallel_model_training(X, y)
        print(f"✅ Modelos entrenados: {len(training_results)}")
        
        # Realizar predicción
        predictions = pipeline.ensemble_predict(X[:10])
        print(f"✅ Predicciones realizadas: {len(predictions)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en pipeline: {e}")
        return False

def test_ray_remote_functions():
    """Prueba de funciones remotas de Ray"""
    print("\n🧪 Probando funciones remotas de Ray...")
    
    try:
        import ray
        
        @ray.remote
        def add(a, b):
            return a + b
        
        @ray.remote
        def multiply(a, b):
            return a * b
        
        # Ejecutar funciones remotas
        future1 = add.remote(3, 4)
        future2 = multiply.remote(5, 6)
        
        # Obtener resultados
        result1 = ray.get(future1)
        result2 = ray.get(future2)
        
        print(f"✅ Función remota add: 3 + 4 = {result1}")
        print(f"✅ Función remota multiply: 5 * 6 = {result2}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en funciones remotas: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas de Ray...")
    print("=" * 50)
    
    tests = [
        ("Inicialización básica", test_ray_basic),
        ("Pipeline de ML", test_ray_pipeline),
        ("Funciones remotas", test_ray_remote_functions)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Ejecutando: {test_name}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Error inesperado en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen de resultados
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        print(f"{status} - {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! Ray está funcionando correctamente.")
        return 0
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 