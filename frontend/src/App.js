import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const App = () => {
  const [assignments, setAssignments] = useState([]);
  const [priorityAssignments, setPriorityAssignments] = useState([]);

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) {
      alert("Please select a file.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post("http://localhost:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log("File uploaded successfully:", response.data);
      processSyllabus(response.data.outputFile);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  const processSyllabus = (filePath) => {
    const mockAssignments = [
      { className: "Math 101", dueDate: "2024-12-10", assignmentName: "Homework 3" },
      { className: "History 202", dueDate: "2024-12-15", assignmentName: "Essay on WWII" },
    ];

    const mockPriorityAssignments = [
      { className: "Physics 301", dueDate: "2024-12-05", type: "Lab", assignmentName: "Lab Report 7" },
    ];

    setAssignments(mockAssignments);
    setPriorityAssignments(mockPriorityAssignments);
  };

  return (
    <div>
      <nav className="navbar">
        <h1>Syllabus Tracker</h1>
      </nav>

      <header className="hero">
        <h2>Stay Organized, Stay Ahead</h2>
        <p>Upload your syllabus and let us handle the rest.</p>
      </header>

      <div className="upload-bar">
        <input type="file" accept=".pdf, .docx" onChange={handleFileChange} />
      </div>

      <section className="upcoming-assignments">
        <h2>📅 Upcoming Assignments</h2>
        <div className="card-container">
          {assignments.map((assignment, index) => (
            <div className="card" key={index}>
              <h3>{assignment.className}</h3>
              <p><strong>Due:</strong> {assignment.dueDate}</p>
              <p><strong>Assignment:</strong> {assignment.assignmentName}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="priority-section">
        <h2>❗Priority Assignments</h2>
        <div className="priority-list">
          {priorityAssignments.map((assignment, index) => (
            <div className="priority-item" key={index}>
              <h3>{assignment.className}</h3>
              <p><strong>Due:</strong> {assignment.dueDate}</p>
              <p><strong>Type:</strong> {assignment.type}</p>
              <p><strong>Assignment:</strong> {assignment.assignmentName}</p>
              <label>
                Completed:
                <input type="checkbox" />
              </label>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default App;
