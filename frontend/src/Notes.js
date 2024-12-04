import React, { useState } from "react";
import "./Notes.css";

const Notes = () => {
  const [notes, setNotes] = useState([]);
  const [noteText, setNoteText] = useState("");
  const [noteTag, setNoteTag] = useState("");

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

  return (
    <div className="notes-page">
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
          <div className="note-group" key={tag}>
            <h3 className={`tag-${tag}`}>{tag}</h3>
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
  );
};

export default Notes;
