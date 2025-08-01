"""
Script de inicialización para Ray
Maneja la conexión al cluster de Ray de manera robusta
"""

import ray
import logging
import time
import os

logger = logging.getLogger(__name__)

def init_ray_cluster():
    """Inicializa Ray con configuración de cluster"""
    
    # Configuración del cluster
    ray_head_host = os.getenv('RAY_HEAD_SERVICE_HOST', 'ray-head')
    ray_head_port = os.getenv('RAY_HEAD_SERVICE_PORT', '6379')
    
    # Intentar conectar al cluster
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Intentando conectar al cluster de Ray (intento {attempt + 1}/{max_retries})")
            
            ray.init(
                address=f"ray://{ray_head_host}:10001",
                ignore_reinit_error=True,
                runtime_env={"working_dir": "/app"},
                logging_level=logging.INFO
            )
            
            logger.info("✅ Ray conectado exitosamente al cluster")
            return True
            
        except Exception as e:
            logger.warning(f"❌ Intento {attempt + 1} falló: {e}")
            
            if attempt < max_retries - 1:
                logger.info(f"Esperando {retry_delay} segundos antes del siguiente intento...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Backoff exponencial
            else:
                logger.warning("No se pudo conectar al cluster de Ray, usando modo local")
                try:
                    ray.init(ignore_reinit_error=True)
                    logger.info("✅ Ray inicializado en modo local")
                    return True
                except Exception as local_error:
                    logger.error(f"❌ Error inicializando Ray en modo local: {local_error}")
                    return False
    
    return False

def get_ray_status():
    """Obtiene el estado actual de Ray"""
    try:
        if ray.is_initialized():
            cluster_resources = ray.cluster_resources()
            available_resources = ray.available_resources()
            nodes = ray.nodes()
            
            return {
                "initialized": True,
                "cluster_resources": cluster_resources,
                "available_resources": available_resources,
                "nodes_count": len(nodes),
                "nodes": nodes
            }
        else:
            return {"initialized": False}
    except Exception as e:
        logger.error(f"Error obteniendo estado de Ray: {e}")
        return {"initialized": False, "error": str(e)}

if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Inicializar Ray
    success = init_ray_cluster()
    
    if success:
        # Mostrar estado
        status = get_ray_status()
        print(f"Estado de Ray: {status}")
    else:
        print("❌ No se pudo inicializar Ray") 