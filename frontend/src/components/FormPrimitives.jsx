export function AuthCard({ title, subtitle, children }) {
  return (
    <div className="mx-auto flex max-w-md flex-col items-center px-6 py-16">
      <div className="w-full rounded-3xl bg-white/80 p-8 shadow-lg">
        <h1 className="text-2xl font-bold text-brand-slate">{title}</h1>
        <p className="mt-1 text-sm text-brand-slate/60">{subtitle}</p>
        <div className="mt-6">{children}</div>
      </div>
    </div>
  );
}

export function Field({ label, value, onChange, type = "text", required = false, minLength }) {
  return (
    <label className="block text-sm font-medium text-brand-slate/80">
      {label}
      <input
        type={type}
        required={required}
        minLength={minLength}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="mt-1 w-full rounded-xl border border-brand-blue/60 bg-white px-4 py-2.5 text-brand-slate outline-none transition focus:border-brand-blue-deep focus:ring-2 focus:ring-brand-blue/50"
      />
    </label>
  );
}

export function SubmitButton({ isSubmitting, label }) {
  return (
    <button
      type="submit"
      disabled={isSubmitting}
      className="w-full rounded-full bg-brand-blue-deep px-6 py-3 font-semibold text-white shadow-md transition hover:shadow-lg disabled:opacity-60"
    >
      {isSubmitting ? "Please wait..." : label}
    </button>
  );
}
