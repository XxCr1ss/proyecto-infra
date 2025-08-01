import React, { useState, useEffect } from "react";
import { Row, Col, Card, Button, Alert } from "react-bootstrap";
import { toast } from "react-toastify";
import axios from "axios";

const Dashboard = () => {
  const [healthStatus, setHealthStatus] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSystemStatus();
    const interval = setInterval(fetchSystemStatus, 10000); // Actualizar cada 10 segundos
    return () => clearInterval(interval);
  }, []);

  const fetchSystemStatus = async () => {
    try {
      const [healthResponse, metricsResponse] = await Promise.all([
        axios.get("/health"),
        axios.get("/metrics"),
      ]);

      setHealthStatus(healthResponse.data);
      setMetrics(metricsResponse.data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching system status:", error);
      setLoading(false);
      toast.error("Error al obtener el estado del sistema");
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "healthy":
        return "success";
      case "warning":
        return "warning";
      case "error":
        return "danger";
      default:
        return "secondary";
    }
  };

  if (loading) {
    return (
      <div className="loading-spinner">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Cargando...</span>
        </div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-white mb-4">Dashboard del Sistema ML</h1>

      {/* Estado del Sistema */}
      <Row className="mb-4">
        <Col md={6}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Estado del Sistema</h5>
            </Card.Header>
            <Card.Body>
              {healthStatus ? (
                <div>
                  <Alert variant={getStatusColor(healthStatus.status)}>
                    <strong>Estado:</strong> {healthStatus.status}
                  </Alert>
                  <p>
                    <strong>Ray Status:</strong>{" "}
                    {healthStatus.ray_status ? "✅ Activo" : "❌ Inactivo"}
                  </p>
                  <p>
                    <strong>Pipeline:</strong>{" "}
                    {healthStatus.pipeline_ready
                      ? "✅ Listo"
                      : "❌ No inicializado"}
                  </p>
                  <p>
                    <strong>Última actualización:</strong>{" "}
                    {new Date(healthStatus.timestamp * 1000).toLocaleString()}
                  </p>
                </div>
              ) : (
                <Alert variant="danger">
                  No se pudo obtener el estado del sistema
                </Alert>
              )}
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Métricas del Sistema</h5>
            </Card.Header>
            <Card.Body>
              {metrics ? (
                <div>
                  <div className="metric-card">
                    <div className="metric-value">
                      {metrics.pipeline_workers}
                    </div>
                    <div className="metric-label">Workers Activos</div>
                  </div>
                  <div className="metric-card">
                    <div className="metric-value">
                      {metrics.ray_metrics?.nodes || 0}
                    </div>
                    <div className="metric-label">Nodos Ray</div>
                  </div>
                  <Button
                    variant="outline-primary"
                    onClick={fetchSystemStatus}
                    className="w-100"
                  >
                    Actualizar Métricas
                  </Button>
                </div>
              ) : (
                <Alert variant="warning">
                  No se pudieron obtener las métricas
                </Alert>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Acciones Rápidas */}
      <Row className="mb-4">
        <Col>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Acciones Rápidas</h5>
            </Card.Header>
            <Card.Body>
              <Row>
                <Col md={3}>
                  <Button
                    variant="primary"
                    className="w-100 mb-2"
                    href="/prediction"
                  >
                    🎯 Realizar Predicción
                  </Button>
                </Col>
                <Col md={3}>
                  <Button
                    variant="success"
                    className="w-100 mb-2"
                    href="/training"
                  >
                    🏋️ Entrenar Modelo
                  </Button>
                </Col>
                <Col md={3}>
                  <Button
                    variant="info"
                    className="w-100 mb-2"
                    href="/benchmark"
                  >
                    ⚡ Ejecutar Benchmark
                  </Button>
                </Col>
                <Col md={3}>
                  <Button
                    variant="secondary"
                    className="w-100 mb-2"
                    href="/metrics"
                  >
                    📊 Ver Métricas Detalladas
                  </Button>
                </Col>
              </Row>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Información del Proyecto */}
      <Row>
        <Col>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Información del Proyecto</h5>
            </Card.Header>
            <Card.Body>
              <Row>
                <Col md={6}>
                  <h6>Características del Sistema:</h6>
                  <ul>
                    <li>✅ Paralelización con Ray Framework</li>
                    <li>✅ Arquitectura de Microservicios</li>
                    <li>✅ APIs REST con FastAPI</li>
                    <li>✅ Frontend React Interactivo</li>
                    <li>✅ Containerización con Docker</li>
                    <li>✅ Despliegue en AWS EC2</li>
                  </ul>
                </Col>
                <Col md={6}>
                  <h6>Tecnologías Utilizadas:</h6>
                  <ul>
                    <li>
                      <strong>Backend:</strong> Python, Ray, FastAPI
                    </li>
                    <li>
                      <strong>Frontend:</strong> React, Bootstrap
                    </li>
                    <li>
                      <strong>ML:</strong> Scikit-learn, Pandas, NumPy
                    </li>
                    <li>
                      <strong>Infraestructura:</strong> Docker, AWS EC2
                    </li>
                    <li>
                      <strong>Monitoreo:</strong> Prometheus, Métricas
                      personalizadas
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

export default Dashboard;
