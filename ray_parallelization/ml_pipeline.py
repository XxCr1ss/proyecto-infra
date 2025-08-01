"""
ML Pipeline con paralelización usando Ray
Este módulo implementa un pipeline de Machine Learning que utiliza Ray
para paralelizar el procesamiento de datos y entrenamiento de modelos.
"""

import ray
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import time
import logging
from typing import Dict, List, Tuple

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Ray (se inicializará desde el servicio principal)
# ray.init(ignore_reinit_error=True)

@ray.remote
class DataProcessor:
    """Clase remota para procesamiento de datos en paralelo"""
    
    def __init__(self, chunk_id: int):
        self.chunk_id = chunk_id
        self.processed_data = None
    
    def process_chunk(self, data_chunk: pd.DataFrame) -> pd.DataFrame:
        """Procesa un chunk de datos en paralelo"""
        logger.info(f"Procesando chunk {self.chunk_id} con {len(data_chunk)} filas")
        
        # Simular procesamiento costoso
        time.sleep(0.1)
        
        # Limpieza de datos
        processed = data_chunk.copy()
        processed = processed.dropna()
        
        # Feature engineering
        if 'feature1' in processed.columns:
            processed['feature1_squared'] = processed['feature1'] ** 2
        if 'feature2' in processed.columns:
            processed['feature2_log'] = np.log1p(processed['feature2'])
        
        self.processed_data = processed
        return processed
    
    def get_processing_stats(self) -> Dict:
        """Retorna estadísticas del procesamiento"""
        if self.processed_data is not None:
            return {
                'chunk_id': self.chunk_id,
                'rows_processed': len(self.processed_data),
                'columns': list(self.processed_data.columns)
            }
        return {'chunk_id': self.chunk_id, 'status': 'not_processed'}

@ray.remote
class ModelTrainer:
    """Clase remota para entrenamiento de modelos en paralelo"""
    
    def __init__(self, model_id: int):
        self.model_id = model_id
        self.model = None
        self.metrics = {}
    
    def train_model(self, X_train: np.ndarray, y_train: np.ndarray, 
                   X_val: np.ndarray, y_val: np.ndarray) -> Dict:
        """Entrena un modelo en paralelo"""
        logger.info(f"Entrenando modelo {self.model_id}")
        
        start_time = time.time()
        
        # Crear y entrenar modelo
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42 + self.model_id
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluar modelo
        y_pred = self.model.predict(X_val)
        mse = mean_squared_error(y_val, y_pred)
        r2 = r2_score(y_val, y_pred)
        
        training_time = time.time() - start_time
        
        self.metrics = {
            'model_id': self.model_id,
            'mse': mse,
            'r2': r2,
            'training_time': training_time
        }
        
        logger.info(f"Modelo {self.model_id} entrenado - R²: {r2:.4f}, MSE: {mse:.4f}")
        
        return self.metrics
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Realiza predicciones con el modelo entrenado"""
        if self.model is None:
            raise ValueError("Modelo no entrenado")
        return self.model.predict(X)
    
    def get_model_info(self) -> Dict:
        """Retorna información del modelo"""
        return {
            'model_id': self.model_id,
            'model_type': 'RandomForestRegressor',
            'metrics': self.metrics
        }

class MLPipeline:
    """Pipeline principal de Machine Learning con Ray"""
    
    def __init__(self, n_workers: int = 4):
        self.n_workers = n_workers
        self.data_processors = []
        self.model_trainers = []
        self.processed_data = None
        self.trained_models = []
        
    def generate_sample_data(self, n_samples: int = 10000) -> pd.DataFrame:
        """Genera datos de ejemplo para demostración"""
        np.random.seed(42)
        
        data = pd.DataFrame({
            'feature1': np.random.normal(0, 1, n_samples),
            'feature2': np.random.exponential(1, n_samples),
            'feature3': np.random.uniform(-1, 1, n_samples),
            'feature4': np.random.choice([0, 1], n_samples, p=[0.7, 0.3])
        })
        
        # Crear target variable
        data['target'] = (
            2 * data['feature1'] + 
            1.5 * data['feature2'] + 
            0.5 * data['feature3'] + 
            data['feature4'] + 
            np.random.normal(0, 0.1, n_samples)
        )
        
        return data
    
    def parallel_data_processing(self, data: pd.DataFrame) -> pd.DataFrame:
        """Procesa datos en paralelo usando Ray"""
        logger.info("Iniciando procesamiento paralelo de datos")
        
        # Dividir datos en chunks
        chunk_size = len(data) // self.n_workers
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        
        # Crear procesadores remotos
        self.data_processors = [
            DataProcessor.remote(chunk_id=i) 
            for i in range(len(chunks))
        ]
        
        # Procesar chunks en paralelo
        start_time = time.time()
        futures = [
            processor.process_chunk.remote(chunk)
            for processor, chunk in zip(self.data_processors, chunks)
        ]
        
        # Obtener resultados
        processed_chunks = ray.get(futures)
        processing_time = time.time() - start_time
        
        # Combinar resultados
        self.processed_data = pd.concat(processed_chunks, ignore_index=True)
        
        logger.info(f"Procesamiento completado en {processing_time:.2f}s")
        logger.info(f"Datos procesados: {len(self.processed_data)} filas")
        
        return self.processed_data
    
    def parallel_model_training(self, X: np.ndarray, y: np.ndarray) -> List[Dict]:
        """Entrena múltiples modelos en paralelo"""
        logger.info("Iniciando entrenamiento paralelo de modelos")
        
        # Dividir datos en train/validation
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Crear entrenadores remotos
        self.model_trainers = [
            ModelTrainer.remote(model_id=i)
            for i in range(self.n_workers)
        ]
        
        # Entrenar modelos en paralelo
        start_time = time.time()
        futures = [
            trainer.train_model.remote(X_train, y_train, X_val, y_val)
            for trainer in self.model_trainers
        ]
        
        # Obtener resultados
        training_results = ray.get(futures)
        training_time = time.time() - start_time
        
        self.trained_models = training_results
        
        logger.info(f"Entrenamiento completado en {training_time:.2f}s")
        logger.info(f"Modelos entrenados: {len(training_results)}")
        
        return training_results
    
    def ensemble_predict(self, X: np.ndarray) -> np.ndarray:
        """Realiza predicciones usando un ensemble de modelos"""
        if not self.model_trainers:
            raise ValueError("No hay modelos entrenados")
        
        # Obtener predicciones de todos los modelos
        futures = [
            trainer.predict.remote(X)
            for trainer in self.model_trainers
        ]
        
        predictions = ray.get(futures)
        
        # Promedio de predicciones (ensemble simple)
        ensemble_prediction = np.mean(predictions, axis=0)
        
        return ensemble_prediction
    
    def run_pipeline(self, data: pd.DataFrame = None) -> Dict:
        """Ejecuta el pipeline completo"""
        logger.info("Iniciando pipeline de ML con Ray")
        
        # Generar datos si no se proporcionan
        if data is None:
            data = self.generate_sample_data()
        
        # Paso 1: Procesamiento paralelo de datos
        processed_data = self.parallel_data_processing(data)
        
        # Preparar features y target
        feature_cols = [col for col in processed_data.columns if col.startswith('feature')]
        X = processed_data[feature_cols].values
        y = processed_data['target'].values
        
        # Paso 2: Entrenamiento paralelo de modelos
        training_results = self.parallel_model_training(X, y)
        
        # Paso 3: Evaluación del ensemble
        ensemble_pred = self.ensemble_predict(X)
        ensemble_mse = mean_squared_error(y, ensemble_pred)
        ensemble_r2 = r2_score(y, ensemble_pred)
        
        # Resultados finales
        results = {
            'data_processing': {
                'original_rows': len(data),
                'processed_rows': len(processed_data),
                'features_used': feature_cols
            },
            'model_training': {
                'models_trained': len(training_results),
                'best_r2': max(result['r2'] for result in training_results),
                'avg_r2': np.mean([result['r2'] for result in training_results]),
                'training_results': training_results
            },
            'ensemble_performance': {
                'ensemble_mse': ensemble_mse,
                'ensemble_r2': ensemble_r2
            }
        }
        
        logger.info("Pipeline completado exitosamente")
        logger.info(f"R² del ensemble: {ensemble_r2:.4f}")
        
        return results

def benchmark_sequential_vs_parallel():
    """Compara rendimiento secuencial vs paralelo"""
    logger.info("Iniciando benchmark secuencial vs paralelo")
    
    # Datos de prueba
    data = MLPipeline().generate_sample_data(5000)
    
    # Benchmark secuencial
    start_time = time.time()
    pipeline_seq = MLPipeline(n_workers=1)
    results_seq = pipeline_seq.run_pipeline(data)
    sequential_time = time.time() - start_time
    
    # Benchmark paralelo
    start_time = time.time()
    pipeline_par = MLPipeline(n_workers=4)
    results_par = pipeline_par.run_pipeline(data)
    parallel_time = time.time() - start_time
    
    # Resultados del benchmark
    speedup = sequential_time / parallel_time
    
    benchmark_results = {
        'sequential_time': sequential_time,
        'parallel_time': parallel_time,
        'speedup': speedup,
        'efficiency': speedup / 4,  # Asumiendo 4 workers
        'sequential_results': results_seq,
        'parallel_results': results_par
    }
    
    logger.info(f"Benchmark completado:")
    logger.info(f"Tiempo secuencial: {sequential_time:.2f}s")
    logger.info(f"Tiempo paralelo: {parallel_time:.2f}s")
    logger.info(f"Speedup: {speedup:.2f}x")
    logger.info(f"Eficiencia: {benchmark_results['efficiency']:.2f}")
    
    return benchmark_results

if __name__ == "__main__":
    # Ejecutar pipeline de ejemplo
    pipeline = MLPipeline(n_workers=4)
    results = pipeline.run_pipeline()
    
    # Ejecutar benchmark
    benchmark_results = benchmark_sequential_vs_parallel()
    
    # Guardar resultados
    import json
    with open('pipeline_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    with open('benchmark_results.json', 'w') as f:
        json.dump(benchmark_results, f, indent=2, default=str)
    
    print("Pipeline ejecutado exitosamente. Resultados guardados en pipeline_results.json")
    print("Benchmark completado. Resultados guardados en benchmark_results.json") 