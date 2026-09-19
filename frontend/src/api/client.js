const BASE_URL = "/api";

function getToken() {
  return localStorage.getItem("astroai_token");
}

async function request(path, { method = "GET", body, auth = true } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (auth) {
    const token = getToken();
    if (token) headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    let detail = response.statusText;
    try {
      const errorBody = await response.json();
      detail = errorBody.detail ? JSON.stringify(errorBody.detail) : detail;
    } catch {
      // response had no JSON body
    }
    throw new Error(detail);
  }

  if (response.status === 204) return null;
  return response.json();
}

export const api = {
  signup: (email, password) => request("/auth/signup", { method: "POST", body: { email, password }, auth: false }),
  login: (email, password) => request("/auth/login", { method: "POST", body: { email, password }, auth: false }),

  listProfiles: () => request("/profiles"),
  createProfile: (payload) => request("/profiles", { method: "POST", body: payload }),
  getProfile: (profileId) => request(`/profiles/${profileId}`),

  generateChart: (profileId) => request(`/profiles/${profileId}/chart`, { method: "POST" }),
  getChart: (profileId) => request(`/profiles/${profileId}/chart`),
  getDasha: (profileId) => request(`/profiles/${profileId}/dasha`),
  getYogas: (profileId) => request(`/profiles/${profileId}/yogas`),
  listVargas: (profileId) => request(`/profiles/${profileId}/vargas`),
  getVarga: (profileId, vargaKey) => request(`/profiles/${profileId}/vargas/${vargaKey}`),
  getTransits: (profileId, asOf) =>
    request(`/profiles/${profileId}/transits${asOf ? `?as_of=${asOf}` : ""}`),

  sendChatMessage: (birthProfileId, message, sessionId) =>
    request("/chat", { method: "POST", body: { birth_profile_id: birthProfileId, message, session_id: sessionId } }),
  getChatHistory: (profileId) => request(`/chat/${profileId}/history`),
};

export function saveToken(token) {
  localStorage.setItem("astroai_token", token);
}

export function clearToken() {
  localStorage.removeItem("astroai_token");
}

export { getToken };
