import { Link } from "react-router-dom";

export default function Landing() {
  return (
    <div className="mx-auto max-w-5xl px-6 py-16">
      <div className="grid items-center gap-10 md:grid-cols-2">
        <div>
          <span className="inline-block rounded-full bg-brand-lavender px-4 py-1 text-xs font-semibold uppercase tracking-wide text-brand-slate/70">
            AI-Powered Vedic Astrology
          </span>
          <h1 className="mt-4 text-4xl font-bold leading-tight text-brand-slate md:text-5xl">
            Your birth chart, <span className="text-brand-blue-deep">explained by AI</span>
          </h1>
          <p className="mt-4 text-lg text-brand-slate/70">
            Enter your birth details once. Get your Kundli calculated for real, saved forever, and
            explained by a personal AI assistant that actually knows your chart.
          </p>
          <div className="mt-8 flex gap-4">
            <Link
              to="/signup"
              className="rounded-full bg-brand-blue-deep px-6 py-3 font-semibold text-white shadow-md transition hover:shadow-lg"
            >
              Create my Kundli
            </Link>
            <Link
              to="/login"
              className="rounded-full bg-white px-6 py-3 font-semibold text-brand-slate shadow-sm transition hover:shadow-md"
            >
              I already have an account
            </Link>
          </div>
        </div>
        <div className="flex justify-center">
          <div className="grid h-64 w-64 place-items-center rounded-[2rem] bg-gradient-to-br from-brand-blue via-brand-lavender to-brand-pink text-6xl shadow-xl md:h-80 md:w-80">
            🔮
          </div>
        </div>
      </div>

      <div className="mt-20 grid gap-6 md:grid-cols-3">
        <FeatureCard icon="🪐" title="Real calculations" text="Every planet, house and degree comes from a real astrology engine — never guessed." />
        <FeatureCard icon="💬" title="Ask anything" text="Chat naturally about your own chart: your Moon sign, your 7th house, your career, and more." />
        <FeatureCard icon="🔒" title="Saved forever" text="Your profile and chart are stored permanently — log back in anytime, nothing to re-enter." />
      </div>
    </div>
  );
}

function FeatureCard({ icon, title, text }) {
  return (
    <div className="rounded-3xl bg-white/70 p-6 shadow-sm">
      <div className="text-3xl">{icon}</div>
      <h3 className="mt-3 font-semibold text-brand-slate">{title}</h3>
      <p className="mt-1 text-sm text-brand-slate/70">{text}</p>
    </div>
  );
}
