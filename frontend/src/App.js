import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import Notes from "./Notes";

const App = () => {
  return (
    <Router>
      <div>
        <nav className="navbar">
          <h1>Syllabus Tracker</h1>
          <div className="nav-links">
            <a href="/">Home</a>
            <a href="/notes">Notes</a>
          </div>
        </nav>

        <header className="hero">
          <h2>Stay Organized, Stay Ahead</h2>
          <p>Upload your syllabus and let us handle the rest.</p>
        </header>

        <Routes>
          <Route
            path="/"
            element={
              <div>
                <section className="upload-bar">
                  <input type="file" accept=".txt" />
                </section>

                <section className="upcoming-assignments">
                  <h2>📅 Upcoming Assignments</h2>
                  <div className="card-container">
                    <div className="card">
                      <h3>Nothing yet.</h3>
                      <p><strong>Great job!</strong> You're up to date on all your work.</p>
                    </div>
                  </div>
                </section>

                <section className="priority-section">
                  <h2>🔥 Priority Assignments</h2>
                  <div className="priority-list">
                    <div className="priority-item">
                      <p> Nothing yet! </p>
                      <label>
                      </label>
                    </div>
                  </div>
                </section>
              </div>
            }
          />
          <Route path="/notes" element={<Notes />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
