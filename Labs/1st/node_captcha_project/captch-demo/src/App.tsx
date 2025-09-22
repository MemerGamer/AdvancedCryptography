import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import { Turnstile } from "@marsidev/react-turnstile";

function App() {
  const [name, setName] = useState("");
  const [token, setToken] = useState("");

  const handleSumit = async (e: React.FormEvent) => {
    if (!token) {
      alert("Please complete the CAPTCHA");
      return;
    }

    e.preventDefault();
    const result = fetch("http://localhost:3000/hello", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, token }),
    });

    const data = (await result).json();
    console.log(data);
  };

  return (
    <>
      <div>
        <a
          href="https://vite.dev
"
          target="_blank"
        >
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a
          href="https://react.dev
"
          target="_blank"
        >
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <form onSubmit={handleSumit}>
          <input
            type="text"
            name="name"
            placeholder="Enter your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <Turnstile
            siteKey={import.meta.env.VITE_CLOUDFLARE_TURNSTILE_PUBLIC}
            onSuccess={(token) => setToken(token)}
            onExpire={() => setToken("")}
            onError={(error) => {
              setToken("");
              alert("Turnstile error: " + error);
            }}
          />
          <button type="submit">Submit</button>
        </form>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  );
}

export default App;
