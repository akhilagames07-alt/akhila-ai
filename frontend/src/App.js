import { useState } from "react";
import "./App.css";

function App() {
  const [template, setTemplate] = useState("chat");
  const [prompt, setPrompt] = useState("");
  const [output, setOutput] = useState("");
  const [history, setHistory] = useState([]);

  const generate = async () => {
    if (!prompt) return;

    const res = await fetch("http://127.0.0.1:8000/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ template, prompt })
    });

    const data = await res.json();
    setOutput(data.output);

    setHistory([
      {
        template,
        prompt,
        output: data.output
      },
      ...history
    ]);
  };

  const clearAll = () => {
    setPrompt("");
    setOutput("");
    setHistory([]);
  };

  return (
    <div className="app">
      <h1>🤖 Akhila AI</h1>

      <select value={template} onChange={(e) => setTemplate(e.target.value)}>
        <option value="chat">💬 Chat</option>
        <option value="email">✉️ Email</option>
        <option value="blog">✍️ Blog</option>
        <option value="ad">📢 Ad</option>
        <option value="youtube_thumbnail">🎬 YouTube Thumbnail</option>
      </select>

      <textarea
        placeholder="Enter your idea..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />

      <div className="buttons">
        <button onClick={generate}>🚀 Generate</button>
        <button onClick={clearAll}>🧹 Clear</button>
      </div>

      {output && (
        <>
          <h3>✨ Output</h3>
          <pre>{output}</pre>
        </>
      )}

      <h3>📜 History</h3>
      {history.length === 0 && <p>No history yet</p>}
      {history.map((item, i) => (
        <div key={i} className="history-item">
          <b>{item.template}</b>
          <p><b>Prompt:</b> {item.prompt}</p>
          <p><b>Output:</b> {item.output}</p>
        </div>
      ))}
    </div>
  );
}

export default App;
