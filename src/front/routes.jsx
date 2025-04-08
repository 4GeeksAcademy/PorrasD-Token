import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import  {Home}  from "./pages/Home.jsx";
import {Login}  from "./pages/Login.jsx";
import  {Signup}  from "./pages/SignUp.jsx";
import  {Private}  from "./pages/Private.jsx";

function App() {
  return (
    <Router>
      <Routes>
          <Route index element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/private" element={<Private />} />
      </Routes>
    </Router>
  );
}

export default App;
