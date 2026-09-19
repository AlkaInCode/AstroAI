import { useEffect, useState } from "react";
import { api } from "../api/client";
import LoadingState from "../components/LoadingState";
import ErrorState from "../components/ErrorState";

const PROVIDERS = [
  { value: "anthropic", label: "Anthropic (Claude)", placeholderModel: "claude-sonnet-5" },
  { value: "openai", label: "OpenAI (GPT)", placeholderModel: "gpt-4o-mini" },
  { value: "google", label: "Google (Gemini)", placeholderModel: "gemini-2.0-flash" },
  { value: "deepseek", label: "DeepSeek", placeholderModel: "deepseek-chat" },
];

export default function Settings() {
  const [current, setCurrent] = useState(null);
  const [provider, setProvider] = useState("anthropic");
  const [apiKey, setApiKey] = useState("");
  const [model, setModel] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    api
      .getLLMSettings()
      .then((data) => {
        setCurrent(data);
        if (data.provider) setProvider(data.provider);
        if (data.model) setModel(data.model);
      })
      .catch((err) => setError(err.message || "Could not load your settings."));
  }, []);

  async function handleSave(e) {
    e.preventDefault();
    setError("");
    setSuccess("");
    setIsSubmitting(true);
    try {
      const updated = await api.updateLLMSettings({ provider, api_key: apiKey, model: model || null });
      setCurrent(updated);
      setApiKey("");
      setSuccess("Saved. Your key will be used for all future chat messages.");
    } catch (err) {
      setError(err.message || "Could not save your API key.");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleClear() {
    if (!window.confirm("Remove your saved API key? Chat will fall back to the app's shared key, if any.")) return;
    setError("");
    setSuccess("");
    try {
      const updated = await api.clearLLMSettings();
      setCurrent(updated);
      setApiKey("");
      setSuccess("Your key has been removed.");
    } catch (err) {
      setError(err.message || "Could not remove your API key.");
    }
  }

  if (!current) return <LoadingState label="Loading settings..." />;

  const selectedProvider = PROVIDERS.find((p) => p.value === provider);

  return (
    <div className="mx-auto max-w-xl px-6 py-10">
      <h1 className="text-2xl font-bold text-brand-slate">AI Settings</h1>
      <p className="mt-1 text-sm text-brand-slate/60">
        Bring your own LLM key so chat responses use your own account instead of a shared server key.
      </p>

      <div className="mt-6 rounded-3xl bg-white/80 p-6 shadow-lg">
        {current.has_api_key ? (
          <div className="mb-5 flex items-center justify-between rounded-xl bg-brand-lavender/30 px-4 py-3 text-sm">
            <span className="text-brand-slate">
              Currently using <strong>{current.provider}</strong>
              {current.model ? ` (${current.model})` : ""}
            </span>
            <button onClick={handleClear} className="text-xs font-semibold text-brand-slate/60 hover:text-brand-slate">
              Remove
            </button>
          </div>
        ) : (
          <div className="mb-5 rounded-xl bg-brand-blue/20 px-4 py-3 text-sm text-brand-slate/70">
            No personal key set — chat uses the app's shared key, if the operator configured one.
          </div>
        )}

        <form onSubmit={handleSave} className="space-y-4">
          <label className="block text-sm font-medium text-brand-slate/80">
            Provider
            <select
              value={provider}
              onChange={(e) => {
                setProvider(e.target.value);
                setModel(""); // a model name from the previous provider would be meaningless here
              }}
              className="mt-1 w-full rounded-xl border border-brand-blue/60 bg-white px-4 py-2.5 text-brand-slate outline-none focus:border-brand-blue-deep focus:ring-2 focus:ring-brand-blue/50"
            >
              {PROVIDERS.map((p) => (
                <option key={p.value} value={p.value}>
                  {p.label}
                </option>
              ))}
            </select>
          </label>

          <label className="block text-sm font-medium text-brand-slate/80">
            API key
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder={current.has_api_key ? "Enter a new key to replace the saved one" : "Paste your API key"}
              required
              autoComplete="off"
              className="mt-1 w-full rounded-xl border border-brand-blue/60 bg-white px-4 py-2.5 text-brand-slate outline-none transition focus:border-brand-blue-deep focus:ring-2 focus:ring-brand-blue/50"
            />
          </label>

          <label className="block text-sm font-medium text-brand-slate/80">
            Model <span className="font-normal text-brand-slate/40">(optional)</span>
            <input
              type="text"
              value={model}
              onChange={(e) => setModel(e.target.value)}
              placeholder={selectedProvider?.placeholderModel}
              className="mt-1 w-full rounded-xl border border-brand-blue/60 bg-white px-4 py-2.5 text-brand-slate outline-none transition focus:border-brand-blue-deep focus:ring-2 focus:ring-brand-blue/50"
            />
          </label>

          <ErrorState message={error} />
          {success && <p className="text-sm text-green-700">{success}</p>}

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-full bg-brand-blue-deep px-6 py-3 font-semibold text-white shadow-md transition hover:shadow-lg disabled:opacity-60"
          >
            {isSubmitting ? "Saving..." : "Save Key"}
          </button>
        </form>

        <p className="mt-4 text-xs text-brand-slate/40">
          Your key is encrypted at rest and only ever used server-side to call your chosen provider on your behalf —
          it's never sent back to this page after saving.
        </p>
      </div>
    </div>
  );
}
