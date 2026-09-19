import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import BirthDetailsForm from "../components/BirthDetailsForm";
import { AuthCard } from "../components/FormPrimitives";

export default function CreateProfile() {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(payload) {
    setError("");
    setIsSubmitting(true);
    try {
      const profile = await api.createProfile(payload);
      await Promise.all([api.generateChart(profile.id), api.generateNumerology(profile.id)]);
      navigate(`/dashboard/${profile.id}`);
    } catch (err) {
      setError(err.message || "Could not generate your Kundli. Please check your details and try again.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AuthCard title="Tell us about your birth" subtitle="This creates your permanent, personal Kundli.">
      <BirthDetailsForm onSubmit={handleSubmit} isSubmitting={isSubmitting} error={error} />
    </AuthCard>
  );
}
