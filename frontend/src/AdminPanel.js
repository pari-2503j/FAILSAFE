import React, { useState } from "react";
import API from "./api";

function AdminPanel({ token }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const createTeacher = async () => {
    try {
      const response = await API.post(
        "/admin/create-teacher",
        { username, password },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setMessage(response.data.message);
      setUsername("");
      setPassword("");
    } catch (err) {
      setMessage(err.response?.data?.detail || "Failed to create teacher");
    }
  };

  return (
    <div className="admin-panel">
      <h2>Admin Panel — Create Teacher Account</h2>
      <input
        type="text"
        placeholder="New teacher username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="New teacher password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={createTeacher}>Create Teacher</button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default AdminPanel;