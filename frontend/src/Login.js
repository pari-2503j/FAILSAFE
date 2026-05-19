import React, { useState } from "react";
import API from "./api";
import "./Login.css";

function Login({onLogin}) {

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const login = async () => {

    const formData = new FormData();

    formData.append("username", username);
    formData.append("password", password);

    try {

      const response = await API.post("/login",formData);
      onLogin(response.data.access_token,username);  //<-- pass token up to app

    } catch (err) {

      alert(err.response?.data?.detail ||"Invalid Credentials");

    }
  };

  return (

    <div className="login-container">

      <h2>Faculty Login</h2>

      <input
        type="text"
        placeholder="Username"
        onChange={(e) => setUsername(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={login}>Login</button>
    </div>
  );
}

export default Login;