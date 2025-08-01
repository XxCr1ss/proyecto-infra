import React from "react";
import { Navbar, Nav, Container } from "react-bootstrap";
import { Link, useLocation } from "react-router-dom";

const Navigation = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <Navbar bg="light" expand="lg" className="navbar">
      <Container>
        <Navbar.Brand as={Link} to="/" className="fw-bold">
          🤖 ML System - Ray & Microservices
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            <Nav.Link
              as={Link}
              to="/"
              className={isActive("/") ? "active fw-bold" : ""}
            >
              Dashboard
            </Nav.Link>
            <Nav.Link
              as={Link}
              to="/prediction"
              className={isActive("/prediction") ? "active fw-bold" : ""}
            >
              Predicciones
            </Nav.Link>
            <Nav.Link
              as={Link}
              to="/training"
              className={isActive("/training") ? "active fw-bold" : ""}
            >
              Entrenamiento
            </Nav.Link>
            <Nav.Link
              as={Link}
              to="/benchmark"
              className={isActive("/benchmark") ? "active fw-bold" : ""}
            >
              Benchmark
            </Nav.Link>
            <Nav.Link
              as={Link}
              to="/metrics"
              className={isActive("/metrics") ? "active fw-bold" : ""}
            >
              Métricas
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Navigation;
