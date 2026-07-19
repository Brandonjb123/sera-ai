// ============================================================
// SERA AI — Embeddable Chat Widget (Shadow DOM)
// ============================================================
(function () {
  // Hindari inisialisasi ganda
  if (window.SeraWidgetLoaded) return;
  window.SeraWidgetLoaded = true;

  // Buat container utama (host)
  const host = document.createElement("div");
  host.id = "sera-widget-host";
  document.body.appendChild(host);

  // Attach Shadow DOM
  const shadow = host.attachShadow({ mode: "open" });

  // ============================================================
  // CSS WIDGET (terisolasi di dalam Shadow DOM)
  // ============================================================
  const styles = `
    :host {
      all: initial;
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    .widget-container {
      position: fixed;
      bottom: 20px;
      right: 20px;
      z-index: 9999;
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Tombol chat bubble */
    .chat-button {
      width: 56px;
      height: 56px;
      border-radius: 50%;
      background: #0ea5e9;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      color: white;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      transition: transform 0.2s, background 0.2s;
      margin-left: auto;
    }
    .chat-button:hover {
      background: #0284c7;
      transform: scale(1.05);
    }

    /* Jendela chat */
    .chat-window {
      display: none;
      width: 360px;
      height: 480px;
      background: #ffffff;
      border-radius: 16px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.12);
      margin-bottom: 12px;
      flex-direction: column;
      overflow: hidden;
    }
    .chat-window.open {
      display: flex;
    }

    /* Header */
    .chat-header {
      background: #0ea5e9;
      color: white;
      padding: 16px 20px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .chat-header .logo {
      width: 32px;
      height: 32px;
      background: rgba(255,255,255,0.2);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
    }
    .chat-header .title {
      font-weight: 600;
      font-size: 16px;
    }
    .chat-header .close-btn {
      margin-left: auto;
      background: none;
      border: none;
      color: white;
      cursor: pointer;
      font-size: 20px;
      padding: 4px 8px;
      border-radius: 6px;
      transition: background 0.2s;
    }
    .chat-header .close-btn:hover {
      background: rgba(255,255,255,0.2);
    }

    /* Area pesan */
    .chat-messages {
      flex: 1;
      padding: 16px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 12px;
      background: #f8fafc;
    }
    .message {
      max-width: 80%;
      padding: 10px 14px;
      border-radius: 16px;
      font-size: 14px;
      line-height: 1.4;
      word-wrap: break-word;
    }
    .message.user {
      align-self: flex-end;
      background: #0ea5e9;
      color: white;
      border-bottom-right-radius: 4px;
    }
    .message.assistant {
      align-self: flex-start;
      background: #ffffff;
      color: #0f172a;
      border-bottom-left-radius: 4px;
      box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }

    /* Input area */
    .chat-input-area {
      border-top: 1px solid #e2e8f0;
      padding: 12px 16px;
      display: flex;
      gap: 8px;
      background: #ffffff;
    }
    .chat-input-area input {
      flex: 1;
      padding: 10px 14px;
      border: 1px solid #e2e8f0;
      border-radius: 20px;
      font-size: 14px;
      outline: none;
      background: #f8fafc;
      font-family: inherit;
    }
    .chat-input-area input:focus {
      border-color: #0ea5e9;
    }
    .chat-input-area button {
      background: #0ea5e9;
      color: white;
      border: none;
      border-radius: 20px;
      padding: 10px 16px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      font-family: inherit;
    }
    .chat-input-area button:hover {
      background: #0284c7;
    }

    /* Placeholder saat kosong */
    .placeholder {
      text-align: center;
      color: #94a3b8;
      margin-top: 40px;
      font-size: 14px;
    }
  `;

  // ============================================================
  // HTML WIDGET
  // ============================================================
  const html = `
    <div class="widget-container">
      <div class="chat-window" id="sera-chat-window">
        <div class="chat-header">
          <div class="logo">💬</div>
          <div class="title">Sera AI</div>
          <button class="close-btn" id="sera-close-btn">✕</button>
        </div>
        <div class="chat-messages" id="sera-messages">
          <div class="placeholder">👋 Hello! Ask me anything.</div>
        </div>
        <div class="chat-input-area">
          <input type="text" id="sera-input" placeholder="Type a message...">
          <button id="sera-send-btn">Send</button>
        </div>
      </div>
      <button class="chat-button" id="sera-toggle-btn">💬</button>
    </div>
  `;

  // Render ke Shadow DOM
  shadow.innerHTML = `<style>${styles}</style>${html}`;

  // ============================================================
  // INTERAKSI BUKA/TUTUP
  // ============================================================
  const toggleBtn = shadow.getElementById("sera-toggle-btn");
  const closeBtn = shadow.getElementById("sera-close-btn");
  const chatWindow = shadow.getElementById("sera-chat-window");

  toggleBtn.addEventListener("click", () => {
    const isOpen = chatWindow.classList.contains("open");
    if (isOpen) {
      chatWindow.classList.remove("open");
      toggleBtn.textContent = "💬";
    } else {
      chatWindow.classList.add("open");
      toggleBtn.textContent = "✕";
    }
  });

  closeBtn.addEventListener("click", () => {
    chatWindow.classList.remove("open");
    toggleBtn.textContent = "💬";
  });

  // ============================================================
  // KONEKSI KE BACKEND
  // ============================================================
  const API_BASE = "https://sera-ai-production-ad38.up.railway.app";

  const messagesContainer = shadow.getElementById("sera-messages");
  const inputField = shadow.getElementById("sera-input");
  const sendBtn = shadow.getElementById("sera-send-btn");

  function appendMessage(role, text) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${role}`;
    msgDiv.textContent = text;
    messagesContainer.appendChild(msgDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  async function sendMessage() {
    const message = inputField.value.trim();
    if (!message) return;

    // Tampilkan pesan user
    appendMessage("user", message);
    inputField.value = "";

    // Placeholder loading
    const loadingDiv = document.createElement("div");
    loadingDiv.className = "message assistant";
    loadingDiv.textContent = "Typing...";
    loadingDiv.style.opacity = "0.6";
    const loadingId = Date.now();
    loadingDiv.setAttribute("data-loading", loadingId);
    messagesContainer.appendChild(loadingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      const data = await res.json();

      // Hapus placeholder loading
      const loader = shadow.querySelector(`[data-loading="${loadingId}"]`);
      if (loader) loader.remove();

      // Tampilkan respons AI
      appendMessage("assistant", data.response || "Sorry, something went wrong.");
    } catch (err) {
      const loader = shadow.querySelector(`[data-loading="${loadingId}"]`);
      if (loader) loader.remove();
      appendMessage("assistant", "Sorry, there was an error connecting to the server.");
    }
  }

  // Hapus placeholder saat pertama kali kirim pesan
  let firstMessage = true;
  const originalSend = sendMessage;
  window.sendMessage = async function() {
    if (firstMessage) {
      const placeholder = shadow.querySelector(".placeholder");
      if (placeholder) placeholder.remove();
      firstMessage = false;
    }
    await originalSend();
  };

  // Event listener untuk tombol kirim
  sendBtn.addEventListener("click", () => window.sendMessage());

  // Event listener untuk Enter key
  inputField.addEventListener("keypress", (e) => {
    if (e.key === "Enter") window.sendMessage();
  });

  console.log("✅ Sera AI Widget loaded successfully (Shadow DOM)");
})();