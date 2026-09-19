export default function LoadingState({ label = "Loading..." }) {
  return (
    <div className="flex items-center justify-center gap-3 py-10 text-brand-slate/70">
      <span className="h-3 w-3 animate-bounce rounded-full bg-brand-blue-deep [animation-delay:-0.3s]" />
      <span className="h-3 w-3 animate-bounce rounded-full bg-brand-pink [animation-delay:-0.15s]" />
      <span className="h-3 w-3 animate-bounce rounded-full bg-brand-lavender" />
      <span className="ml-2 text-sm">{label}</span>
    </div>
  );
}
