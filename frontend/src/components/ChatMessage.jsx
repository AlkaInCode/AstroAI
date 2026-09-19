export default function ChatMessage({ role, message }) {
  const isUser = role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${
          isUser ? "bg-brand-blue-deep text-white" : "bg-white/80 text-brand-slate shadow-sm"
        }`}
      >
        {message}
      </div>
    </div>
  );
}
