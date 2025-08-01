import ray
from ray import serve
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import time
import logging
from ray.serve.exceptions import RayServeException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class IrisData(BaseModel):
    data: list

@serve.deployment
@serve.ingress(app)
class ApiServer:
    def __init__(self, model_handle):
        self.model_handle = model_handle

    @app.post("/")
    async def predict(self, iris_data: IrisData):
        data = np.array(iris_data.data)
        prediction_ref = await self.model_handle.predict.remote(data)
        prediction = await prediction_ref
        return {"prediction": prediction.tolist()}

if __name__ == "__main__":
    ray.init(address='ray://ray-head:10001', namespace="serve")

    model_handle = None
    max_retries = 20
    retry_delay_seconds = 5

    logger.info("Connecting to Ray and waiting for 'PredictionServer' deployment...")

    for attempt in range(max_retries):
        try:
            model_handle = serve.get_deployment_handle("PredictionServer")
            logger.info("'PredictionServer' handle acquired successfully.")
            break
        except RayServeException:
            logger.warning(f"PredictionServer not ready yet. Retrying in {retry_delay_seconds} seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(retry_delay_seconds)

    if model_handle is None:
        logger.error("Failed to get 'PredictionServer' handle after multiple retries. Exiting.")
        exit(1)

    api_server = ApiServer.bind(model_handle)
    serve.run(api_server, name='api_server', route_prefix='/predict', host='0.0.0.0', port=8000)