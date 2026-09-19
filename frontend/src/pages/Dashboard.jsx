import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../api/client";
import LoadingState from "../components/LoadingState";
import ErrorState from "../components/ErrorState";
import KundliChart from "../components/KundliChart";
import PlanetTable from "../components/PlanetTable";
import LifeAreaCards from "../components/LifeAreaCards";
import DashaTimeline from "../components/DashaTimeline";
import YogaCard from "../components/YogaCard";
import AIChat from "../components/AIChat";

export default function Dashboard() {
  const { profileId } = useParams();
  const [profile, setProfile] = useState(null);
  const [chart, setChart] = useState(null);
  const [dasha, setDasha] = useState(null);
  const [yogas, setYogas] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setIsLoading(true);
    setError("");

    Promise.all([api.getProfile(profileId), api.getChart(profileId), api.getDasha(profileId), api.getYogas(profileId)])
      .then(([profileData, chartData, dashaData, yogasData]) => {
        if (cancelled) return;
        setProfile(profileData);
        setChart({ ...chartData, planets: chartData.planetary_data.planets });
        setDasha(dashaData);
        setYogas(yogasData.yogas);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message || "Could not load this Kundli.");
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [profileId]);

  if (isLoading) return <LoadingState label="Reading the stars..." />;
  if (error) {
    return (
      <div className="mx-auto max-w-2xl px-6 py-16">
        <ErrorState message={error} />
        <Link to="/create-profile" className="mt-4 inline-block text-sm font-semibold text-brand-blue-deep">
          Create a new Kundli
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-5xl px-6 py-10">
      <div className="rounded-3xl bg-white/70 p-6 shadow-sm">
        <h1 className="text-2xl font-bold text-brand-slate">{profile.full_name}'s Kundli</h1>
        <p className="mt-1 text-sm text-brand-slate/60">
          Born {profile.dob} at {profile.birth_time} · {profile.city}
          {profile.state ? `, ${profile.state}` : ""}, {profile.country}
        </p>
        <div className="mt-3 flex gap-4 text-sm">
          <span className="rounded-full bg-brand-blue/40 px-3 py-1 font-medium text-brand-slate">
            Lagna: {chart.lagna}
          </span>
          <span className="rounded-full bg-brand-pink/50 px-3 py-1 font-medium text-brand-slate">
            Rashi: {chart.rashi}
          </span>
        </div>
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-2">
        <div className="rounded-3xl bg-white/70 p-6 shadow-sm">
          <h2 className="mb-4 font-semibold text-brand-slate">Lagna Chart</h2>
          <KundliChart chart={chart} />
        </div>
        <div className="rounded-3xl bg-white/70 p-6 shadow-sm">
          <h2 className="mb-4 font-semibold text-brand-slate">Planetary Placements</h2>
          <PlanetTable planets={chart.planets} />
        </div>
      </div>

      <div className="mt-6">
        <h2 className="mb-4 px-1 font-semibold text-brand-slate">Your Chart, In Plain Words</h2>
        <LifeAreaCards areas={chart.life_areas} />
      </div>

      <div className="mt-6">
        <DashaTimeline dasha={dasha} />
      </div>

      <div className="mt-6">
        <h2 className="mb-4 px-1 font-semibold text-brand-slate">Yogas</h2>
        {yogas.length > 0 ? (
          <div className="grid gap-4 sm:grid-cols-2">
            {yogas.map((yoga) => (
              <YogaCard key={yoga.name + yoga.planets.join("")} yoga={yoga} />
            ))}
          </div>
        ) : (
          <div className="rounded-2xl bg-white/70 p-5 text-sm text-brand-slate/60 shadow-sm">
            No classical Yogas from our current detection set were found in this chart.
          </div>
        )}
      </div>

      <div className="mt-6">
        <AIChat profileId={profile.id} />
      </div>
    </div>
  );
}
