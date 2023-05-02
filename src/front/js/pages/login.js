import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";

const initialvalue = {
  email: "",
  password: "",
};

export const Login = () => {
  const { store, actions } = useContext(Context);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const hanledClick = async () => {
    const opts = {
      method: "POST",
      headers: {
        "Content-Type": "aplication/json",
      },
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    };

    fetch(
      "https://3001-4geeksacade-reactflaskh-7ls1dddc4fh.ws-us96b.gitpod.io/api/login",
      opts
    )
      .then((response) => {
        if (response.status === 200) return response.json();
        else alert("hay algun error");
      })
      .then()
      .catch((error) => {
        console.error("hay un error", error);
      });
  };
  return (
    <div className="text-center mt-5">
      <h1>Hola Mundo </h1>
      <input
        placeholder="email"
        value={email}
        onChange={(event) => setEmail(event.target.value)}
      />
      <input
        placeholder="password"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
      />
      <button onClick={() => hanledClick()}>Registrate</button>
    </div>
  );
};
