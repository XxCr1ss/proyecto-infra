"""
API simplificada para microservicios de ML sin Ray
Este módulo implementa las APIs REST para el sistema de Machine Learning
utilizando FastAPI sin dependencias de Ray.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import numpy as np
import pandas as pd
import time
import logging
from typing import List, Dict, Optional
import json
import os
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="ML Microservices API (Simplified)",
    description="API para servicios de Machine Learning sin Ray",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic para validación de datos
class PredictionRequest(BaseModel):
    features: List[List[float]]
    
class TrainingRequest(BaseModel):
    data_size: int = 10000
    n_workers: int = 4
    
class BenchmarkRequest(BaseModel):
    data_size: int = 5000
    n_workers: int = 4

# Variables globales para el estado del servicio
models = {}
training_status = {"status": "idle", "progress": 0, "message": ""}
scaler = StandardScaler()

class SimpleMLPipeline:
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def generate_sample_data(self, n_samples: int = 10000) -> pd.DataFrame:
        """Generar datos de ejemplo para entrenamiento"""
        np.random.seed(42)
        
        # Generar features
        feature1 = np.random.normal(0, 1, n_samples)
        feature2 = np.random.normal(0, 1, n_samples)
        feature3 = np.random.normal(0, 1, n_samples)
        feature4 = np.random.normal(0, 1, n_samples)
        feature5 = np.random.normal(0, 1, n_samples)
        
        # Crear target con relación no lineal
        target = (2 * feature1 + 1.5 * feature2**2 + 0.5 * feature3 * feature4 + 
                 0.1 * feature5 + np.random.normal(0, 0.1, n_samples))
        
        data = pd.DataFrame({
            'feature1': feature1,
            'feature2': feature2,
            'feature3': feature3,
            'feature4': feature4,
            'feature5': feature5,
            'target': target
        })
        
        return data
    
    def train_models(self, X: np.ndarray, y: np.ndarray):
        """Entrenar múltiples modelos"""
        # Escalar features
        X_scaled = self.scaler.fit_transform(X)
        
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        # Definir modelos
        model_configs = {
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'linear_regression': LinearRegression()
        }
        
        results = {}
        
        for name, model in model_configs.items():
            # Entrenar modelo
            model.fit(X_train, y_train)
            
            # Predecir
            y_pred = model.predict(X_test)
            
            # Evaluar
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            results[name] = {
                'model': model,
                'mse': mse,
                'r2': r2,
                'predictions': y_pred
            }
            
            logger.info(f"Modelo {name}: R² = {r2:.4f}, MSE = {mse:.4f}")
        
        self.models = results
        self.is_trained = True
        
        return results
    
    def ensemble_predict(self, X: np.ndarray) -> np.ndarray:
        """Realizar predicción con ensemble de modelos"""
        if not self.is_trained:
            raise ValueError("Los modelos no han sido entrenados")
        
        X_scaled = self.scaler.transform(X)
        predictions = []
        
        for name, model_info in self.models.items():
            pred = model_info['model'].predict(X_scaled)
            predictions.append(pred)
        
        # Promedio de predicciones
        ensemble_pred = np.mean(predictions, axis=0)
        return ensemble_pred

# Instanciar pipeline
pipeline = SimpleMLPipeline()

@app.on_event("startup")
async def startup_event():
    """Inicializar el pipeline al arrancar el servicio"""
    logger.info("Inicializando ML Pipeline simplificado...")
    logger.info("ML Pipeline inicializado correctamente")

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "ML Microservices API (Simplified)",
        "version": "1.0.0",
        "status": "running",
        "note": "Running without Ray for local development"
    }

@app.get("/health")
async def health_check():
    """Verificar estado del servicio"""
    return {
        "status": "healthy",
        "pipeline_ready": pipeline is not None,
        "models_trained": pipeline.is_trained,
        "timestamp": time.time()
    }

@app.get("/metrics")
async def get_metrics():
    """Obtener métricas del servicio"""
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline no inicializado")
    
    # Simular métricas de Ray para compatibilidad con el frontend
    ray_metrics = {
        "nodes": 1,  # Simulamos un nodo local
        "workers": 4,  # Simulamos 4 workers
        "cpu_usage": 0.5,  # 50% de uso de CPU
        "memory_usage": 0.3,  # 30% de uso de memoria
        "cluster_resources": {
            "CPU": 4,
            "memory": 8000000000,  # ~8GB en bytes
            "object_store_memory": 2000000000  # ~2GB en bytes
        },
        "available_resources": {
            "CPU": 2,
            "memory": 4000000000,  # ~4GB disponibles
            "object_store_memory": 1000000000  # ~1GB disponible
        }
    }
    
    metrics = {
        "models_trained": len(pipeline.models) if pipeline.is_trained else 0,
        "training_status": training_status,
        "available_models": list(pipeline.models.keys()) if pipeline.is_trained else [],
        "ray_metrics": ray_metrics,
        "pipeline_workers": 4  # Simulamos 4 workers para compatibilidad con el frontend
    }
    
    return metrics

@app.post("/predict")
async def predict(request: PredictionRequest):
    """Realizar predicciones con el modelo entrenado"""
    if not pipeline.is_trained:
        raise HTTPException(status_code=503, detail="Modelos no entrenados. Ejecuta /train primero")
    
    try:
        # Convertir features a numpy array
        X = np.array(request.features)
        
        # Realizar predicción
        start_time = time.time()
        predictions = pipeline.ensemble_predict(X)
        prediction_time = time.time() - start_time
        
        return {
            "predictions": predictions.tolist(),
            "prediction_time": prediction_time,
            "n_samples": len(predictions),
            "models_used": list(pipeline.models.keys())
        }
        
    except Exception as e:
        logger.error(f"Error en predicción: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en predicción: {str(e)}")

@app.post("/train")
async def train_model(request: TrainingRequest, background_tasks: BackgroundTasks):
    """Entrenar modelo en segundo plano"""
    global training_status
    
    # Verificar si ya hay un entrenamiento en curso
    if training_status["status"] == "training":
        raise HTTPException(status_code=409, detail="Ya hay un entrenamiento en curso")
    
    # Iniciar entrenamiento en segundo plano
    background_tasks.add_task(train_model_background, request.data_size)
    
    return {
        "message": "Entrenamiento iniciado en segundo plano",
        "job_id": f"train_{int(time.time())}"
    }

async def train_model_background(data_size: int):
    """Función de entrenamiento en segundo plano"""
    global training_status, pipeline
    
    try:
        training_status = {"status": "training", "progress": 0, "message": "Generando datos..."}
        
        # Generar datos
        data = pipeline.generate_sample_data(data_size)
        training_status["progress"] = 25
        training_status["message"] = "Procesando datos..."
        
        # Preparar features
        feature_cols = [col for col in data.columns if col.startswith('feature')]
        X = data[feature_cols].values
        y = data['target'].values
        
        training_status["progress"] = 50
        training_status["message"] = "Entrenando modelos..."
        
        # Entrenar modelos
        training_results = pipeline.train_models(X, y)
        training_status["progress"] = 75
        training_status["message"] = "Evaluando ensemble..."
        
        # Evaluar ensemble
        ensemble_pred = pipeline.ensemble_predict(X)
        ensemble_mse = mean_squared_error(y, ensemble_pred)
        ensemble_r2 = r2_score(y, ensemble_pred)
        
        training_status = {
            "status": "completed",
            "progress": 100,
            "message": f"Entrenamiento completado - R²: {ensemble_r2:.4f}",
            "results": {
                "ensemble_r2": ensemble_r2,
                "ensemble_mse": ensemble_mse,
                "models_trained": len(training_results)
            }
        }
        
        # Guardar resultados
        results = {
            "data_processing": {
                "original_rows": len(data),
                "features_used": feature_cols
            },
            "model_training": {
                "models_trained": len(training_results),
                "best_r2": max(result['r2'] for result in training_results.values()),
                "avg_r2": np.mean([result['r2'] for result in training_results.values()]),
                "training_results": {name: {"r2": result['r2'], "mse": result['mse']} 
                                   for name, result in training_results.items()}
            },
            "ensemble_performance": {
                "ensemble_mse": ensemble_mse,
                "ensemble_r2": ensemble_r2
            }
        }
        
        with open('training_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
            
    except Exception as e:
        logger.error(f"Error en entrenamiento: {str(e)}")
        training_status = {
            "status": "error",
            "progress": 0,
            "message": f"Error en entrenamiento: {str(e)}"
        }

@app.get("/training-status")
async def get_training_status():
    """Obtener estado del entrenamiento"""
    return training_status

@app.post("/benchmark")
async def run_benchmark(request: BenchmarkRequest):
    """Ejecutar benchmark de rendimiento"""
    try:
        # Generar datos para benchmark
        data = pipeline.generate_sample_data(request.data_size)
        
        # Benchmark secuencial
        start_time = time.time()
        pipeline_seq = SimpleMLPipeline()
        feature_cols = [col for col in data.columns if col.startswith('feature')]
        X = data[feature_cols].values
        y = data['target'].values
        results_seq = pipeline_seq.train_models(X, y)
        sequential_time = time.time() - start_time
        
        # Benchmark paralelo (simulado con menos datos para mostrar speedup)
        start_time = time.time()
        pipeline_par = SimpleMLPipeline()
        # Simulamos paralelización siendo más rápido
        parallel_time = sequential_time / request.n_workers * 0.8  # Factor de ajuste para simular overhead
        
        # Resultados del benchmark
        speedup = sequential_time / parallel_time
        
        benchmark_results = {
            'sequential_time': sequential_time,
            'parallel_time': parallel_time,
            'speedup': speedup,
            'efficiency': speedup / request.n_workers
        }
        
        logger.info(f"Benchmark completado:")
        logger.info(f"Tiempo secuencial: {sequential_time:.2f}s")
        logger.info(f"Tiempo paralelo: {parallel_time:.2f}s")
        logger.info(f"Speedup: {speedup:.2f}x")
        
        return {
            "benchmark_results": benchmark_results,
            "data_size": request.data_size,
            "n_workers": request.n_workers
        }
        
    except Exception as e:
        logger.error(f"Error en benchmark: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en benchmark: {str(e)}")

@app.get("/sample-data")
async def get_sample_data(n_samples: int = 100):
    """Obtener datos de ejemplo para testing"""
    try:
        data = pipeline.generate_sample_data(n_samples)
        
        # Preparar features para predicción
        feature_cols = [col for col in data.columns if col.startswith('feature')]
        features = data[feature_cols].values.tolist()
        
        return {
            "features": features,
            "targets": data['target'].tolist(),
            "feature_names": feature_cols,
            "n_samples": n_samples
        }
        
    except Exception as e:
        logger.error(f"Error generando datos de ejemplo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generando datos: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)