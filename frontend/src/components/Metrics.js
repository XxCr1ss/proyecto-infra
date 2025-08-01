import React, { useState, useEffect } from "react";
import { Row, Col, Card, Button, Alert } from "react-bootstrap";
import { toast } from "react-toastify";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

const Metrics = () => {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(null);

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000); // Actualizar cada 5 segundos
    return () => clearInterval(interval);
  }, []);

  const fetchMetrics = async () => {
    try {
      const response = await axios.get("/metrics");
      setMetrics(response.data);
      setLastUpdate(new Date());
      setLoading(false);
    } catch (error) {
      console.error("Error fetching metrics:", error);
      setLoading(false);
      toast.error("Error al obtener las métricas");
    }
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

  const prepareResourceData = (resources) => {
    if (!resources) return [];

    return Object.entries(resources).map(([key, value]) => ({
      name: key,
      value: typeof value === "number" ? value : 0,
    }));
  };

  const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#8884D8"];

  if (loading) {
    return (
      <div className="loading-spinner">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Cargando métricas...</span>
        </div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-white mb-4">Métricas del Sistema</h1>

      {/* Métricas Principales */}
      <Row className="mb-4">
        <Col md={3}>
          <Card>
            <Card.Body className="metric-card">
              <div className="metric-value">
                {metrics?.pipeline_workers || 0}
              </div>
              <div className="metric-label">Workers Activos</div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card>
            <Card.Body className="metric-card">
              <div className="metric-value">
                {metrics?.ray_metrics?.nodes || 0}
              </div>
              <div className="metric-label">Nodos Ray</div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card>
            <Card.Body className="metric-card">
              <div className="metric-value">
                {metrics?.training_status?.status === "training"
                  ? "🔄"
                  : metrics?.training_status?.status === "completed"
                  ? "✅"
                  : "⏸️"}
              </div>
              <div className="metric-label">Estado Entrenamiento</div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card>
            <Card.Body className="metric-card">
              <div className="metric-value">
                {lastUpdate ? lastUpdate.toLocaleTimeString() : "--:--"}
              </div>
              <div className="metric-label">Última Actualización</div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Estado del Sistema */}
      <Row className="mb-4">
        <Col md={6}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Estado del Sistema</h5>
            </Card.Header>
            <Card.Body>
              {metrics?.training_status ? (
                <div>
                  <Alert
                    variant={getStatusColor(metrics.training_status.status)}
                  >
                    <strong>Estado del Entrenamiento:</strong>{" "}
                    {metrics.training_status.status}
                  </Alert>

                  {metrics.training_status.message && (
                    <p>
                      <strong>Mensaje:</strong>{" "}
                      {metrics.training_status.message}
                    </p>
                  )}

                  {metrics.training_status.progress > 0 && (
                    <div className="mb-3">
                      <strong>Progreso:</strong>{" "}
                      {metrics.training_status.progress}%
                    </div>
                  )}

                  {metrics.training_status.results && (
                    <div className="training-status status-completed">
                      <h6>Resultados del Último Entrenamiento:</h6>
                      <ul>
                        <li>
                          <strong>R² del Ensemble:</strong>{" "}
                          {metrics.training_status.results.ensemble_r2?.toFixed(
                            4
                          )}
                        </li>
                        <li>
                          <strong>MSE del Ensemble:</strong>{" "}
                          {metrics.training_status.results.ensemble_mse?.toFixed(
                            4
                          )}
                        </li>
                        <li>
                          <strong>Modelos Entrenados:</strong>{" "}
                          {metrics.training_status.results.models_trained}
                        </li>
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <Alert variant="secondary">
                  No hay información de entrenamiento disponible
                </Alert>
              )}
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Recursos del Cluster Ray</h5>
            </Card.Header>
            <Card.Body>
              {metrics?.ray_metrics ? (
                <div>
                  <h6>Recursos del Cluster:</h6>
                  <ul>
                    <li>
                      <strong>Nodos:</strong> {metrics.ray_metrics.nodes}
                    </li>
                    <li>
                      <strong>CPU Total:</strong>{" "}
                      {metrics.ray_metrics.cluster_resources?.CPU || "N/A"}
                    </li>
                    <li>
                      <strong>Memoria Total:</strong>{" "}
                      {metrics.ray_metrics.cluster_resources?.memory || "N/A"}
                    </li>
                    <li>
                      <strong>GPU Total:</strong>{" "}
                      {metrics.ray_metrics.cluster_resources?.GPU || "N/A"}
                    </li>
                  </ul>

                  <h6>Recursos Disponibles:</h6>
                  <ul>
                    <li>
                      <strong>CPU Disponible:</strong>{" "}
                      {metrics.ray_metrics.available_resources?.CPU || "N/A"}
                    </li>
                    <li>
                      <strong>Memoria Disponible:</strong>{" "}
                      {metrics.ray_metrics.available_resources?.memory || "N/A"}
                    </li>
                    <li>
                      <strong>GPU Disponible:</strong>{" "}
                      {metrics.ray_metrics.available_resources?.GPU || "N/A"}
                    </li>
                  </ul>
                </div>
              ) : (
                <Alert variant="warning">
                  No se pudieron obtener las métricas de Ray
                </Alert>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Gráficos de Recursos */}
      {metrics?.ray_metrics && (
        <Row className="mb-4">
          <Col md={6}>
            <Card>
              <Card.Header>
                <h5 className="mb-0">Distribución de Recursos del Cluster</h5>
              </Card.Header>
              <Card.Body>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={prepareResourceData(
                        metrics.ray_metrics.cluster_resources
                      )}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) =>
                        `${name}: ${(percent * 100).toFixed(0)}%`
                      }
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {prepareResourceData(
                        metrics.ray_metrics.cluster_resources
                      ).map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={COLORS[index % COLORS.length]}
                        />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </Card.Body>
            </Card>
          </Col>

          <Col md={6}>
            <Card>
              <Card.Header>
                <h5 className="mb-0">Recursos Disponibles vs Utilizados</h5>
              </Card.Header>
              <Card.Body>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart
                    data={[
                      {
                        name: "Cluster",
                        utilizados:
                          metrics.ray_metrics.cluster_resources?.CPU || 0,
                        disponibles:
                          metrics.ray_metrics.available_resources?.CPU || 0,
                      },
                    ]}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="utilizados"
                      stroke="#8884d8"
                      name="Utilizados"
                    />
                    <Line
                      type="monotone"
                      dataKey="disponibles"
                      stroke="#82ca9d"
                      name="Disponibles"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}

      {/* Información del Sistema */}
      <Row>
        <Col>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Información del Sistema</h5>
            </Card.Header>
            <Card.Body>
              <Row>
                <Col md={6}>
                  <h6>Métricas Monitoreadas:</h6>
                  <ul>
                    <li>
                      <strong>Estado del Pipeline:</strong> Verificación de
                      workers activos
                    </li>
                    <li>
                      <strong>Cluster Ray:</strong> Recursos y nodos disponibles
                    </li>
                    <li>
                      <strong>Entrenamiento:</strong> Progreso y resultados
                    </li>
                    <li>
                      <strong>Rendimiento:</strong> Tiempos de respuesta y
                      throughput
                    </li>
                  </ul>
                </Col>
                <Col md={6}>
                  <h6>Acciones Disponibles:</h6>
                  <ul>
                    <li>
                      <strong>Actualización Automática:</strong> Cada 5 segundos
                    </li>
                    <li>
                      <strong>Monitoreo en Tiempo Real:</strong> Estado del
                      sistema
                    </li>
                    <li>
                      <strong>Alertas:</strong> Notificaciones de cambios de
                      estado
                    </li>
                    <li>
                      <strong>Histórico:</strong> Seguimiento de métricas
                    </li>
                  </ul>
                </Col>
              </Row>

              <div className="text-center mt-3">
                <Button
                  variant="outline-primary"
                  onClick={fetchMetrics}
                  className="me-2"
                >
                  🔄 Actualizar Métricas
                </Button>
                <small className="text-muted">
                  Última actualización:{" "}
                  {lastUpdate ? lastUpdate.toLocaleString() : "Nunca"}
                </small>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Metrics;
