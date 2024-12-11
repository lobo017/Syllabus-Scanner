import React, { useState } from "react";
import "./App.css";
import "./Notes.css";
import axios from "axios";
import Chatbot from "./components/Chatbot";

const App = () => {
  const [notes, setNotes] = useState([]);
  const [noteText, setNoteText] = useState("");
  const [noteTag, setNoteTag] = useState("");
  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");
  const [upcomingAssignments, setUpcomingAssignments] = useState([]);
  const [priorityAssignments, setPriorityAssignments] = useState([]);
  const [error, setError] = useState("");

  const generateColor = (tag) => {
    const colors = [
      "#3a7ca5",
      "#2f6690",
      "#16425b",
      "#81c3d7",
      "#ceb992",
      "#14bef0",
      "#b1e5f2",
      "#73c2fb",
    ];
    const hash = [...tag].reduce((acc, char) => acc + char.charCodeAt(0), 0);
    return colors[hash % colors.length];
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (noteText && noteTag) {
      setNotes([...notes, { text: noteText, tag: noteTag }]);
      setNoteText("");
      setNoteTag("");
    } else {
      alert("Please fill out both fields.");
    }
  };

  const groupedNotes = notes.reduce((acc, note) => {
    if (!acc[note.tag]) {
      acc[note.tag] = [];
    }
    acc[note.tag].push(note);
    return acc;
  }, {});

  const extractAssignments = async (parsedFilePath) => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/generate-report`, {
        params: { file: parsedFilePath },
      });
      const { important_dates, upcoming_assignments } = response.data;
      setUpcomingAssignments(upcoming_assignments || []);
      setPriorityAssignments(important_dates || []);
      setError("");
    } catch (error) {
      console.error("Failed to extract assignments", error);
      setError("Could not extract assignments. Please check your syllabus format.");
      setUpcomingAssignments([]);
      setPriorityAssignments([]);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append("file", file);
      try {
        setUploadedFile(null);
        setUploadMessage("");
        setError("");
        setUpcomingAssignments([]);
        setPriorityAssignments([]);
        const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        setUploadedFile(file);
        if (response.data.parsed_path) {
          extractAssignments(response.data.parsed_path);
        }
      } catch (error) {
        console.error("File upload failed", error);
        setError("File upload failed. Please try again.");
        setUploadMessage("");
      }
    }
  };

  return (
    <div>
      <header className="hero">
        <h2>Stay Organized, Stay Ahead</h2>
        <p>Upload your syllabus and let us handle the rest.</p>
      </header>

      <section className="upload-bar">
        <input
          type="file"
          accept=".txt,.docx,.pdf"
          onChange={handleFileUpload}
        />
        {uploadMessage}
        {error}
      </section>

      <div>
        <h2>Notes</h2>
        <form onSubmit={handleSubmit} className="note-form">
          <input
            type="text"
            value={noteTag}
            onChange={(e) => setNoteTag(e.target.value)}
            placeholder="Tag this note"
            required
          />
          <textarea
            value={noteText}
            onChange={(e) => setNoteText(e.target.value)}
            placeholder="Write your note here..."
            required
          />
          <button type="submit">Add Note</button>
        </form>

        <div className="notes-container">
          {Object.keys(groupedNotes).map((tag) => (
            <div
              className="note-group"
              key={tag}
              style={{ backgroundColor: generateColor(tag) }}
            >
              <h3>{tag}</h3>
              <div className="notes-list">
                {groupedNotes[tag].map((note, index) => (
                  <div className="note-card" key={index}>
                    <p>{note.text}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Chatbot stays throughout the site */}
      <Chatbot />
    </div>
  );
};

export default App;
