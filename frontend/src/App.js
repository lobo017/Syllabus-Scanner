import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import Notes from "./Notes";
import axios from "axios";

const App = () => {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");
  const [upcomingAssignments, setUpcomingAssignments] = useState([]);
  const [priorityAssignments, setPriorityAssignments] = useState([]);
  const [error, setError] = useState("");

  const extractAssignments = async (parsedFilePath) => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/generate-report`, {
        params: { file: parsedFilePath }
      });
      const { important_dates, upcoming_assignments } = response.data;
      
      setUpcomingAssignments(upcoming_assignments || []);
      setPriorityAssignments(important_dates || []);
      setError("");
    } catch (error) {
      console.error('Failed to extract assignments', error);
      setError('Could not extract assignments. Please check your syllabus format.');
      setUpcomingAssignments([]);
      setPriorityAssignments([]);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append('file', file);

      try {
        // Reset previous states
        setUploadedFile(null);
        setUploadMessage("");
        setError("");
        setUpcomingAssignments([]);
        setPriorityAssignments([]);

        const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        setUploadedFile(file);
        // setUploadMessage(response.data.message);
        
        // Extract assignments from the parsed file
        if (response.data.parsed_path) {
          extractAssignments(response.data.parsed_path);
        }
      } catch (error) {
        console.error('File upload failed', error);
        setError('File upload failed. Please try again.');
        setUploadMessage('');
      }
    }
  };

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
                  <input 
                    type="file" 
                    accept=".txt,.docx,.pdf" 
                    onChange={handleFileUpload} 
                  />
                  {uploadMessage}
                  {error}
                </section>

                <section className="upcoming-assignments">
                  <h2>📅 Upcoming Assignments</h2>
                  <div className="card-container">
                    {upcomingAssignments.length > 0 ? (
                      upcomingAssignments.map((assignment, index) => (
                        <div key={index} className="card">
                          <h3>{assignment.name}</h3>
                          <p>Due: {assignment.due_date}</p>
                          <p><strong>{assignment.details}</strong></p>
                        </div>
                      ))
                    ) : (
                      <div className="card">
                        <h3>Nothing yet.</h3>
                        <p><strong>Great job!</strong> You're up to date on all your work.</p>
                      </div>
                    )}
                  </div>
                </section>

                <section className="priority-section">
                  <h2>🔥 Priority Assignments</h2>
                  <div className="priority-list">
                    {priorityAssignments.length > 0 ? (
                      priorityAssignments.map((assignment, index) => (
                        <div key={index} className="priority-item">
                          <p>{assignment.event}</p>
                          <label>Due: {assignment.date}</label>
                        </div>
                      ))
                    ) : (
                      <div className="priority-item">
                        <p>Nothing yet!</p>
                      </div>
                    )}
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