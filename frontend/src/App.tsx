import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import SavedArticlesPage from './pages/SavedArticlesPage';
import './index.css';

const App: React.FC = () => {
  return (
    <Router>
      <nav className="navbar">
        <ul>
          <li>
            <Link to="/">Inicio</Link>
          </li>
          <li>
            <Link to="/saved-articles">Mis artículos guardados</Link>
          </li>
        </ul>
      </nav>
      <div className="container">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/saved-articles" element={<SavedArticlesPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;