import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import ErrorState from "../components/ErrorState";
import { AuthCard, Field, SubmitButton } from "../components/FormPrimitives";

export default function Signup() {
  const { signup } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setIsSubmitting(true);
    try {
      await signup(email, password);
      navigate("/create-profile");
    } catch (err) {
      setError(err.message || "Could not create your account.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AuthCard title="Create your account" subtitle="Let's get your Kundli started.">
      <form onSubmit={handleSubmit} className="space-y-4">
        <Field label="Email" type="email" value={email} onChange={setEmail} required />
        <Field label="Password" type="password" value={password} onChange={setPassword} required minLength={8} />
        <ErrorState message={error} />
        <SubmitButton isSubmitting={isSubmitting} label="Sign up" />
      </form>
      <p className="mt-4 text-center text-sm text-brand-slate/60">
        Already have an account?{" "}
        <Link to="/login" className="font-semibold text-brand-blue-deep">
          Log in
        </Link>
      </p>
    </AuthCard>
  );
}
