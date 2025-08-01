"""
API principal para microservicios de ML
Este módulo implementa las APIs REST para el sistema de Machine Learning
utilizando FastAPI y Ray Serve.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import ray
import numpy as np
import pandas as pd
import time
import logging
from typing import List, Dict, Optional
import json
import os

# Importar módulos del proyecto
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from ray_parallelization.ml_pipeline import MLPipeline, ModelTrainer

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Ray usando el script de inicialización
from ray_parallelization.init_ray import init_ray_cluster, get_ray_status

if not init_ray_cluster():
    logger.error("No se pudo inicializar Ray")
    raise RuntimeError("Ray no pudo inicializarse")

# Crear aplicación FastAPI
app = FastAPI(
    title="ML Microservices API",
    description="API para servicios de Machine Learning con Ray y paralelización",
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
pipeline = None
training_status = {"status": "idle", "progress": 0, "message": ""}

@app.on_event("startup")
async def startup_event():
    """Inicializar el pipeline al arrancar el servicio"""
    global pipeline
    logger.info("Inicializando ML Pipeline...")
    pipeline = MLPipeline(n_workers=4)
    logger.info("ML Pipeline inicializado correctamente")

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "ML Microservices API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Verificar estado del servicio"""
    ray_status = get_ray_status()
    
    return {
        "status": "healthy",
        "ray_status": ray_status,
        "pipeline_ready": pipeline is not None,
        "timestamp": time.time()
    }

@app.get("/metrics")
async def get_metrics():
    """Obtener métricas del servicio"""
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline no inicializado")
    
    # Obtener métricas de Ray usando el script de inicialización
    ray_metrics = get_ray_status()
    
    return {
        "ray_metrics": ray_metrics,
        "training_status": training_status,
        "pipeline_workers": pipeline.n_workers if pipeline else 0
    }

@app.post("/predict")
async def predict(request: PredictionRequest):
    """Realizar predicciones con el modelo entrenado"""
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline no inicializado")
    
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
            "n_samples": len(predictions)
        }
        
    except Exception as e:
        logger.error(f"Error en predicción: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en predicción: {str(e)}")

@app.post("/train")
async def train_model(request: TrainingRequest, background_tasks: BackgroundTasks):
    """Entrenar modelo en segundo plano"""
    global training_status
    
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline no inicializado")
    
    # Verificar si ya hay un entrenamiento en curso
    if training_status["status"] == "training":
        raise HTTPException(status_code=409, detail="Ya hay un entrenamiento en curso")
    
    # Iniciar entrenamiento en segundo plano
    background_tasks.add_task(train_model_background, request.data_size, request.n_workers)
    
    return {
        "message": "Entrenamiento iniciado en segundo plano",
        "job_id": f"train_{int(time.time())}"
    }

async def train_model_background(data_size: int, n_workers: int):
    """Función de entrenamiento en segundo plano"""
    global training_status, pipeline
    
    try:
        training_status = {"status": "training", "progress": 0, "message": "Generando datos..."}
        
        # Generar datos
        data = pipeline.generate_sample_data(data_size)
        training_status["progress"] = 25
        training_status["message"] = "Procesando datos..."
        
        # Procesar datos
        processed_data = pipeline.parallel_data_processing(data)
        training_status["progress"] = 50
        training_status["message"] = "Entrenando modelos..."
        
        # Preparar features
        feature_cols = [col for col in processed_data.columns if col.startswith('feature')]
        X = processed_data[feature_cols].values
        y = processed_data['target'].values
        
        # Entrenar modelos
        training_results = pipeline.parallel_model_training(X, y)
        training_status["progress"] = 75
        training_status["message"] = "Evaluando ensemble..."
        
        # Evaluar ensemble
        ensemble_pred = pipeline.ensemble_predict(X)
        from sklearn.metrics import mean_squared_error, r2_score
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
                "processed_rows": len(processed_data),
                "features_used": feature_cols
            },
            "model_training": {
                "models_trained": len(training_results),
                "best_r2": max(result['r2'] for result in training_results),
                "avg_r2": np.mean([result['r2'] for result in training_results]),
                "training_results": training_results
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
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline no inicializado")
    
    try:
        from ray_parallelization.ml_pipeline import benchmark_sequential_vs_parallel
        
        # Generar datos para benchmark
        data = pipeline.generate_sample_data(request.data_size)
        
        # Ejecutar benchmark
        benchmark_results = benchmark_sequential_vs_parallel()
        
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
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline no inicializado")
    
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
    uvicorn.run(app, host="0.0.0.0", port=8000) 