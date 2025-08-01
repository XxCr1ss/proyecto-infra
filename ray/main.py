import ray
from ray import serve
from sklearn.datasets import load_iris
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import time

@ray.remote(num_returns=4)
def preprocess_data(data):
    print("Preprocesando datos...")
    X, y = data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print("Preprocesamiento de datos completo.")
    return X_train, X_test, y_train, y_test

@ray.remote
def train_model(X_train, y_train):
    print("Entrenando modelo...")
    model = GradientBoostingClassifier()
    model.fit(X_train, y_train)
    print("Entrenamiento del modelo completo.")
    return model

@ray.remote
def evaluate_model(model, X_test, y_test):
    print("Evaluando modelo...")
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Evaluación del modelo completa. Precisión: {accuracy:.2f}")
    return accuracy

@serve.deployment
class PredictionServer:
    def __init__(self, model):
        self._model = model

    def predict(self, data):
        return self._model.predict(data).tolist()

def main():
    # It's a better practice to use a specific namespace
    ray.init(address='ray://ray-head:10001', namespace="serve")

    print("--- Starting ML Pipeline ---")
    iris = load_iris()
    data_ref = ray.put((iris.data, iris.target))

    # The pipeline can be simplified by chaining the tasks
    preprocessed_data_ref = preprocess_data.remote(data_ref)
    
    # Getting refs to pass to the next tasks
    X_train_ref, X_test_ref, y_train_ref, y_test_ref = preprocessed_data_ref

    model_ref = train_model.remote(X_train_ref, y_train_ref)
    accuracy_ref = evaluate_model.remote(model_ref, X_test_ref, y_test_ref)

    # Wait for the pipeline to finish
    final_accuracy = ray.get(accuracy_ref)
    print("--- ML Pipeline Finished ---")
    print(f"Final Model Accuracy: {final_accuracy:.2f}")

    print("--- Deploying Model for Serving ---")
    model = ray.get(model_ref)
    
    # This will block and keep the service alive
    # The host is set to 0.0.0.0 to be accessible from other containers
    serve.run(PredictionServer.bind(model), http_options={"host": "0.0.0.0"})

if __name__ == "__main__":
    main()