import React, { useState } from "react";
import { Row, Col, Card, Button, Form, Alert, Spinner } from "react-bootstrap";
import { toast } from "react-toastify";
import axios from "axios";
import { API_ENDPOINTS } from "../config";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const Benchmark = () => {
  const [benchmarkConfig, setBenchmarkConfig] = useState({
    data_size: 5000,
    n_workers: 4,
  });
  const [benchmarkResults, setBenchmarkResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleRunBenchmark = async () => {
    setLoading(true);
    try {
      const response = await axios.post(API_ENDPOINTS.BENCHMARK, benchmarkConfig);
      setBenchmarkResults(response.data);
      toast.success("Benchmark ejecutado exitosamente");
    } catch (error) {
      console.error("Error running benchmark:", error);
      toast.error("Error al ejecutar el benchmark");
    } finally {
      setLoading(false);
    }
  };

  const handleConfigChange = (field, value) => {
    setBenchmarkConfig((prev) => ({
      ...prev,
      [field]: parseInt(value) || 0,
    }));
  };

  const prepareChartData = (results) => {
    if (!results) return [];

    return [
      {
        name: "Secuencial",
        tiempo: results.sequential_time,
        speedup: 1,
      },
      {
        name: "Paralelo",
        tiempo: results.parallel_time,
        speedup: results.speedup,
      },
    ];
  };

  return (
    <div>
      <h1 className="text-white mb-4">Benchmark de Rendimiento</h1>

      <Row>
        <Col md={4}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Configuración del Benchmark</h5>
            </Card.Header>
            <Card.Body>
              <Form>
                <Form.Group className="mb-3">
                  <Form.Label>Tamaño del Dataset</Form.Label>
                  <Form.Control
                    type="number"
                    value={benchmarkConfig.data_size}
                    onChange={(e) =>
                      handleConfigChange("data_size", e.target.value)
                    }
                    min="1000"
                    max="20000"
                    step="1000"
                  />
                  <Form.Text className="text-muted">
                    Número de muestras para el benchmark
                  </Form.Text>
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Número de Workers</Form.Label>
                  <Form.Control
                    type="number"
                    value={benchmarkConfig.n_workers}
                    onChange={(e) =>
                      handleConfigChange("n_workers", e.target.value)
                    }
                    min="1"
                    max="8"
                  />
                  <Form.Text className="text-muted">
                    Workers para paralelización
                  </Form.Text>
                </Form.Group>

                <Button
                  variant="info"
                  onClick={handleRunBenchmark}
                  disabled={loading}
                  className="w-100"
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
                      Ejecutando benchmark...
                    </>
                  ) : (
                    "⚡ Ejecutar Benchmark"
                  )}
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>

        <Col md={8}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Resultados del Benchmark</h5>
            </Card.Header>
            <Card.Body>
              {benchmarkResults ? (
                <div>
                  <Row className="mb-4">
                    <Col md={4}>
                      <div className="metric-card">
                        <div className="metric-value">
                          {benchmarkResults.benchmark_results.speedup.toFixed(
                            2
                          )}
                          x
                        </div>
                        <div className="metric-label">Speedup</div>
                      </div>
                    </Col>
                    <Col md={4}>
                      <div className="metric-card">
                        <div className="metric-value">
                          {(
                            (benchmarkResults.benchmark_results.speedup /
                              benchmarkConfig.n_workers) *
                            100
                          ).toFixed(1)}
                          %
                        </div>
                        <div className="metric-label">Eficiencia</div>
                      </div>
                    </Col>
                    <Col md={4}>
                      <div className="metric-card">
                        <div className="metric-value">
                          {benchmarkResults.benchmark_results.parallel_time.toFixed(
                            2
                          )}
                          s
                        </div>
                        <div className="metric-label">Tiempo Paralelo</div>
                      </div>
                    </Col>
                  </Row>

                  <div className="benchmark-chart">
                    <h6>Comparación de Tiempos</h6>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart
                        data={prepareChartData(
                          benchmarkResults.benchmark_results
                        )}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar
                          dataKey="tiempo"
                          fill="#667eea"
                          name="Tiempo (segundos)"
                        />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>

                  <Row className="mt-4">
                    <Col md={6}>
                      <h6>Detalles del Benchmark:</h6>
                      <ul>
                        <li>
                          <strong>Tiempo Secuencial:</strong>{" "}
                          {benchmarkResults.benchmark_results.sequential_time.toFixed(
                            2
                          )}
                          s
                        </li>
                        <li>
                          <strong>Tiempo Paralelo:</strong>{" "}
                          {benchmarkResults.benchmark_results.parallel_time.toFixed(
                            2
                          )}
                          s
                        </li>
                        <li>
                          <strong>Speedup:</strong>{" "}
                          {benchmarkResults.benchmark_results.speedup.toFixed(
                            2
                          )}
                          x
                        </li>
                        <li>
                          <strong>Eficiencia:</strong>{" "}
                          {(
                            (benchmarkResults.benchmark_results.speedup /
                              benchmarkConfig.n_workers) *
                            100
                          ).toFixed(1)}
                          %
                        </li>
                        <li>
                          <strong>Dataset:</strong> {benchmarkResults.data_size}{" "}
                          muestras
                        </li>
                        <li>
                          <strong>Workers:</strong> {benchmarkResults.n_workers}
                        </li>
                      </ul>
                    </Col>
                    <Col md={6}>
                      <h6>Análisis de Rendimiento:</h6>
                      <Alert variant="info">
                        <strong>Speedup:</strong> Factor de mejora en velocidad
                        comparado con ejecución secuencial.
                      </Alert>
                      <Alert variant="success">
                        <strong>Eficiencia:</strong> Porcentaje de utilización
                        efectiva de los recursos paralelos.
                      </Alert>
                      {benchmarkResults.benchmark_results.speedup >
                        benchmarkConfig.n_workers * 0.8 && (
                        <Alert variant="success">
                          <strong>Excelente escalabilidad!</strong> La
                          eficiencia es superior al 80%.
                        </Alert>
                      )}
                    </Col>
                  </Row>
                </div>
              ) : (
                <div className="text-center text-muted">
                  <div className="mb-3">
                    <i className="fas fa-chart-bar fa-3x"></i>
                  </div>
                  <p>Ejecute un benchmark para ver los resultados aquí</p>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Información del Benchmark */}
      <Row className="mt-4">
        <Col>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Información del Benchmark</h5>
            </Card.Header>
            <Card.Body>
              <Row>
                <Col md={6}>
                  <h6>¿Qué mide el benchmark?</h6>
                  <ul>
                    <li>
                      <strong>Speedup:</strong> Mejora en velocidad vs ejecución
                      secuencial
                    </li>
                    <li>
                      <strong>Eficiencia:</strong> Utilización efectiva de
                      recursos paralelos
                    </li>
                    <li>
                      <strong>Tiempo de Procesamiento:</strong> Tiempo total de
                      ejecución
                    </li>
                    <li>
                      <strong>Escalabilidad:</strong> Comportamiento con
                      diferentes números de workers
                    </li>
                  </ul>
                </Col>
                <Col md={6}>
                  <h6>Metodología:</h6>
                  <ul>
                    <li>Compara ejecución secuencial vs paralela</li>
                    <li>Utiliza el mismo dataset para ambas ejecuciones</li>
                    <li>Mide tiempo total del pipeline completo</li>
                    <li>Calcula métricas de rendimiento estándar</li>
                    <li>Evalúa la eficiencia de la paralelización con Ray</li>
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

export default Benchmark;
