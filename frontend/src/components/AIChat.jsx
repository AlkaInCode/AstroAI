import { useEffect, useRef, useState } from "react";
import { api } from "../api/client";
import ChatMessage from "./ChatMessage";
import ErrorState from "./ErrorState";

const SUGGESTIONS = [
  "What is my Moon sign?",
  "Tell me about my career.",
  "What does my 7th house mean?",
  "What about my love life?",
];

export default function AIChat({ profileId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState("");
  const bottomRef = useRef(null);

  useEffect(() => {
    api
      .getChatHistory(profileId)
      .then((history) => setMessages(history.map((m) => ({ role: m.role, message: m.message }))))
      .catch(() => {});
  }, [profileId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend(text) {
    const question = text ?? input;
    if (!question.trim() || isSending) return;

    setError("");
    setInput("");
    setMessages((prev) => [...prev, { role: "user", message: question }]);
    setIsSending(true);

    try {
      const response = await api.sendChatMessage(profileId, question, sessionId);
      setSessionId(response.session_id);
      setMessages((prev) => [...prev, { role: "assistant", message: response.reply }]);
    } catch (err) {
      setError(err.message || "Something went wrong reaching the AI. Please try again.");
    } finally {
      setIsSending(false);
    }
  }

  return (
    <div className="flex h-[32rem] flex-col rounded-3xl bg-brand-lavender/30 p-4 shadow-sm">
      <h3 className="px-2 pb-3 font-semibold text-brand-slate">💬 Ask about your chart</h3>

      <div className="flex-1 space-y-3 overflow-y-auto px-2">
        {messages.length === 0 && (
          <div className="flex flex-wrap gap-2 pt-2">
            {SUGGESTIONS.map((s) => (
              <button
                key={s}
                onClick={() => handleSend(s)}
                className="rounded-full bg-white/80 px-3 py-1.5 text-xs text-brand-slate/70 shadow-sm hover:bg-white"
              >
                {s}
              </button>
            ))}
          </div>
        )}
        {messages.map((m, i) => (
          <ChatMessage key={i} role={m.role} message={m.message} />
        ))}
        {isSending && <ChatMessage role="assistant" message="Thinking..." />}
        <div ref={bottomRef} />
      </div>

      <ErrorState message={error} />

      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="mt-3 flex gap-2"
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask anything about your chart..."
          className="flex-1 rounded-full border border-brand-blue/50 bg-white px-4 py-2.5 text-sm text-brand-slate outline-none focus:border-brand-blue-deep focus:ring-2 focus:ring-brand-blue/50"
        />
        <button
          type="submit"
          disabled={isSending}
          className="rounded-full bg-brand-blue-deep px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:shadow-md disabled:opacity-60"
        >
          Send
        </button>
      </form>
    </div>
  );
}
