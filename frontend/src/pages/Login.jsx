import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import ErrorState from "../components/ErrorState";
import { AuthCard, Field, SubmitButton } from "../components/FormPrimitives";

export default function Login() {
  const { login } = useAuth();
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
      await login(email, password);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message || "Invalid email or password.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AuthCard title="Welcome back" subtitle="Log in to see your Kundli.">
      <form onSubmit={handleSubmit} className="space-y-4">
        <Field label="Email" type="email" value={email} onChange={setEmail} required />
        <Field label="Password" type="password" value={password} onChange={setPassword} required />
        <ErrorState message={error} />
        <SubmitButton isSubmitting={isSubmitting} label="Log in" />
      </form>
      <p className="mt-4 text-center text-sm text-brand-slate/60">
        New here?{" "}
        <Link to="/signup" className="font-semibold text-brand-blue-deep">
          Create an account
        </Link>
      </p>
    </AuthCard>
  );
}
