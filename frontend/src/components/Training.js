import React, { useState, useEffect } from "react";
import {
  Row,
  Col,
  Card,
  Button,
  Form,
  ProgressBar,
  Alert,
} from "react-bootstrap";
import { toast } from "react-toastify";
import axios from "axios";
import { API_ENDPOINTS } from "../config";

const Training = () => {
  const [trainingConfig, setTrainingConfig] = useState({
    data_size: 10000,
    n_workers: 4,
  });
  const [trainingStatus, setTrainingStatus] = useState(null);
  const [isTraining, setIsTraining] = useState(false);

  useEffect(() => {
    fetchTrainingStatus();
    const interval = setInterval(fetchTrainingStatus, 2000); // Actualizar cada 2 segundos
    return () => clearInterval(interval);
  }, []);

  const fetchTrainingStatus = async () => {
    try {
      const response = await axios.get(API_ENDPOINTS.TRAINING_STATUS);
      setTrainingStatus(response.data);
      setIsTraining(response.data.status === "training");
    } catch (error) {
      console.error("Error fetching training status:", error);
    }
  };

  const handleStartTraining = async () => {
    setIsTraining(true);
    try {
      await axios.post(API_ENDPOINTS.TRAIN, trainingConfig);
      toast.success("Entrenamiento iniciado exitosamente");
    } catch (error) {
      console.error("Error starting training:", error);
      toast.error("Error al iniciar el entrenamiento");
      setIsTraining(false);
    }
  };

  const handleConfigChange = (field, value) => {
    setTrainingConfig((prev) => ({
      ...prev,
      [field]: parseInt(value) || 0,
    }));
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "training":
        return "info";
      case "completed":
        return "success";
      case "error":
        return "danger";
      default:
        return "secondary";
    }
  };

  return (
    <div>
      <h1 className="text-white mb-4">Entrenamiento de Modelos</h1>

      <Row>
        <Col md={6}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Configuración de Entrenamiento</h5>
            </Card.Header>
            <Card.Body>
              <Form>
                <Form.Group className="mb-3">
                  <Form.Label>Tamaño del Dataset</Form.Label>
                  <Form.Control
                    type="number"
                    value={trainingConfig.data_size}
                    onChange={(e) =>
                      handleConfigChange("data_size", e.target.value)
                    }
                    min="1000"
                    max="100000"
                    step="1000"
                  />
                  <Form.Text className="text-muted">
                    Número de muestras para entrenar el modelo (1000 - 100000)
                  </Form.Text>
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Número de Workers</Form.Label>
                  <Form.Control
                    type="number"
                    value={trainingConfig.n_workers}
                    onChange={(e) =>
                      handleConfigChange("n_workers", e.target.value)
                    }
                    min="1"
                    max="8"
                  />
                  <Form.Text className="text-muted">
                    Número de workers para paralelización (1 - 8)
                  </Form.Text>
                </Form.Group>

                <Button
                  variant="success"
                  onClick={handleStartTraining}
                  disabled={isTraining}
                  className="w-100"
                >
                  🏋️ Iniciar Entrenamiento
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Estado del Entrenamiento</h5>
            </Card.Header>
            <Card.Body>
              {trainingStatus ? (
                <div>
                  <Alert variant={getStatusColor(trainingStatus.status)}>
                    <strong>Estado:</strong> {trainingStatus.status}
                  </Alert>

                  {trainingStatus.message && (
                    <p>
                      <strong>Mensaje:</strong> {trainingStatus.message}
                    </p>
                  )}

                  {trainingStatus.progress > 0 && (
                    <div className="training-progress">
                      <ProgressBar
                        now={trainingStatus.progress}
                        label={`${trainingStatus.progress}%`}
                      />
                    </div>
                  )}

                  {trainingStatus.results && (
                    <div className="training-status status-completed">
                      <h6>Resultados del Entrenamiento:</h6>
                      <ul>
                        <li>
                          <strong>R² del Ensemble:</strong>{" "}
                          {trainingStatus.results.ensemble_r2?.toFixed(4)}
                        </li>
                        <li>
                          <strong>MSE del Ensemble:</strong>{" "}
                          {trainingStatus.results.ensemble_mse?.toFixed(4)}
                        </li>
                        <li>
                          <strong>Modelos Entrenados:</strong>{" "}
                          {trainingStatus.results.models_trained}
                        </li>
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center text-muted">
                  <p>No hay entrenamiento activo</p>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Información del Proceso */}
      <Row className="mt-4">
        <Col>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Proceso de Entrenamiento</h5>
            </Card.Header>
            <Card.Body>
              <Row>
                <Col md={6}>
                  <h6>Fases del Entrenamiento:</h6>
                  <ol>
                    <li>
                      <strong>Generación de Datos:</strong> Creación del dataset
                      sintético
                    </li>
                    <li>
                      <strong>Procesamiento Paralelo:</strong> Limpieza y
                      feature engineering con Ray
                    </li>
                    <li>
                      <strong>Entrenamiento Paralelo:</strong> Múltiples modelos
                      Random Forest
                    </li>
                    <li>
                      <strong>Evaluación del Ensemble:</strong> Combinación de
                      predicciones
                    </li>
                  </ol>
                </Col>
                <Col md={6}>
                  <h6>Características Técnicas:</h6>
                  <ul>
                    <li>
                      <strong>Algoritmo:</strong> Random Forest Regressor
                    </li>
                    <li>
                      <strong>Paralelización:</strong> Ray Framework
                    </li>
                    <li>
                      <strong>Ensemble:</strong> Promedio de predicciones
                    </li>
                    <li>
                      <strong>Métricas:</strong> R² y MSE
                    </li>
                    <li>
                      <strong>Validación:</strong> Train/Test split 80/20
                    </li>
                  </ul>
                </Col>
              </Row>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Training;
