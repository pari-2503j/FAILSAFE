import React,{useState} from "react";
import Login from "./Login";
import Predict from "./Predict";
import Dashboard from "./Dashboard";
import AdminPanel from "./AdminPanel";
import "./App.css";

function App() {

  const [token,setToken] = useState(localStorage.getItem("token"));
  const [username, setUsername] = useState(
    localStorage.getItem("username")
  );

  const handleLogin = (newToken,loggedInUser) => {
    localStorage.setItem("token",newToken);
    localStorage.setItem("username",loggedInUser);
    setToken(newToken);
    setUsername(loggedInUser);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    setToken(null);
    setUsername(null);
  };

  return (
    <div className="app">

      <h1 className="title">FAILSAFE</h1>

      {!token ? (
        <Login onLogin={handleLogin} />
      ) : (
        <>
          <div className="top-bar">

            <p>
              Logged in as:
              <b> {username}</b>
            </p>

            <button onClick={handleLogout}>
              Logout
            </button>

          </div>

          {/* SHOW ADMIN PANEL ONLY FOR ADMIN */}

          {username === "admin" && (
            <AdminPanel token={token} />
          )}

          <Dashboard />
          <Predict />
        </>
      )}

    </div>
  );
}

export default App;