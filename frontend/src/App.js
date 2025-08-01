import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Container } from "react-bootstrap";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "bootstrap/dist/css/bootstrap.min.css";

import Navigation from "./components/Navigation";
import Dashboard from "./components/Dashboard";
import Prediction from "./components/Prediction";
import Training from "./components/Training";
import Benchmark from "./components/Benchmark";
import Metrics from "./components/Metrics";

import "./App.css";

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <Container fluid className="mt-4">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/prediction" element={<Prediction />} />
            <Route path="/training" element={<Training />} />
            <Route path="/benchmark" element={<Benchmark />} />
            <Route path="/metrics" element={<Metrics />} />
          </Routes>
        </Container>
        <ToastContainer position="bottom-right" />
      </div>
    </Router>
  );
}

export default App;
