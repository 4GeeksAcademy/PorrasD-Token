import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export const Private = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/login");  // Redirigir a login si no hay token
      return;
    }

    const fetchUserData = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/private`, {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${token}`,
          },
        });

        const data = await response.json();

        if (response.ok) {
          setUser(data);  // Mostrar datos del usuario
        } else {
          navigate("/login");  // Si la respuesta no es OK, redirigir a login
        }
      } catch (error) {
        navigate("/login");  // Si hay un error, redirigir a login
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [navigate]);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="container">
      <h2>Página Privada</h2>
      <p>Bienvenido, {user ? user.name : "Cargando..."}</p>
    </div>
  );
};
