import React, { useState, useEffect } from "react";
import { Row, Col, Card, Button, Form, Alert, Spinner } from "react-bootstrap";
import { toast } from "react-toastify";
import axios from "axios";

const Prediction = () => {
  const [features, setFeatures] = useState([0, 0, 0, 0]);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [sampleData, setSampleData] = useState(null);

  useEffect(() => {
    loadSampleData();
  }, []);

  const loadSampleData = async () => {
    try {
      const response = await axios.get("/sample-data?n_samples=1");
      setSampleData(response.data);
      if (response.data.features.length > 0) {
        setFeatures(response.data.features[0]);
      }
    } catch (error) {
      console.error("Error loading sample data:", error);
      toast.error("Error al cargar datos de ejemplo");
    }
  };

  const handleFeatureChange = (index, value) => {
    const newFeatures = [...features];
    newFeatures[index] = parseFloat(value) || 0;
    setFeatures(newFeatures);
  };

  const handlePredict = async () => {
    setLoading(true);
    try {
      const response = await axios.post("/predict", {
        features: [features],
      });

      setPrediction(response.data);
      toast.success("Predicción realizada exitosamente");
    } catch (error) {
      console.error("Error making prediction:", error);
      toast.error("Error al realizar la predicción");
    } finally {
      setLoading(false);
    }
  };

  const handleUseSampleData = () => {
    if (sampleData && sampleData.features.length > 0) {
      setFeatures(sampleData.features[0]);
      toast.info("Datos de ejemplo cargados");
    }
  };

  const featureNames = ["Feature 1", "Feature 2", "Feature 3", "Feature 4"];

  return (
    <div>
      <h1 className="text-white mb-4">Realizar Predicciones</h1>

      <Row>
        <Col md={6}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Entrada de Features</h5>
            </Card.Header>
            <Card.Body>
              <Form>
                {features.map((feature, index) => (
                  <div key={index} className="feature-input">
                    <Form.Label>{featureNames[index]}</Form.Label>
                    <Form.Control
                      type="number"
                      step="0.01"
                      value={feature}
                      onChange={(e) =>
                        handleFeatureChange(index, e.target.value)
                      }
                      placeholder={`Ingrese ${featureNames[
                        index
                      ].toLowerCase()}`}
                    />
                  </div>
                ))}

                <div className="d-grid gap-2 mt-3">
                  <Button
                    variant="primary"
                    onClick={handlePredict}
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <Spinner
                          as="span"
                          animation="border"
                          size="sm"
                          role="status"
                          aria-hidden="true"
                          className="me-2"
                        />
                        Realizando predicción...
                      </>
                    ) : (
                      "🎯 Realizar Predicción"
                    )}
                  </Button>

                  <Button
                    variant="outline-secondary"
                    onClick={handleUseSampleData}
                    disabled={!sampleData}
                  >
                    📊 Usar Datos de Ejemplo
                  </Button>
                </div>
              </Form>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Resultado de la Predicción</h5>
            </Card.Header>
            <Card.Body>
              {prediction ? (
                <div className="prediction-result">
                  <h4>Predicción Realizada</h4>
                  <div className="mb-3">
                    <strong>Valor Predicho:</strong>
                    <div className="h3 text-white mb-2">
                      {prediction.predictions[0].toFixed(4)}
                    </div>
                  </div>

                  <div className="mb-3">
                    <strong>Tiempo de Predicción:</strong>
                    <div className="text-white">
                      {(prediction.prediction_time * 1000).toFixed(2)} ms
                    </div>
                  </div>

                  <div>
                    <strong>Features Utilizadas:</strong>
                    <ul className="text-white mt-2">
                      {features.map((feature, index) => (
                        <li key={index}>
                          {featureNames[index]}: {feature.toFixed(4)}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              ) : (
                <div className="text-center text-muted">
                  <div className="mb-3">
                    <i className="fas fa-chart-line fa-3x"></i>
                  </div>
                  <p>Realice una predicción para ver los resultados aquí</p>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Información Adicional */}
      <Row className="mt-4">
        <Col>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Información del Modelo</h5>
            </Card.Header>
            <Card.Body>
              <Row>
                <Col md={6}>
                  <h6>Características del Modelo:</h6>
                  <ul>
                    <li>
                      <strong>Tipo:</strong> Ensemble de Random Forest
                    </li>
                    <li>
                      <strong>Algoritmo:</strong> Random Forest Regressor
                    </li>
                    <li>
                      <strong>Features:</strong> 4 variables numéricas
                    </li>
                    <li>
                      <strong>Paralelización:</strong> Ray Framework
                    </li>
                  </ul>
                </Col>
                <Col md={6}>
                  <h6>Instrucciones:</h6>
                  <ul>
                    <li>Ingrese valores numéricos para cada feature</li>
                    <li>
                      Use el botón "Usar Datos de Ejemplo" para cargar valores
                      de prueba
                    </li>
                    <li>
                      El modelo realizará la predicción usando paralelización
                      con Ray
                    </li>
                    <li>
                      Los resultados incluyen el valor predicho y el tiempo de
                      procesamiento
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

export default Prediction;
