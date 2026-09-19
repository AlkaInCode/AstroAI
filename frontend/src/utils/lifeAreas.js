// Simple, deterministic Phase-1 interpretation built ONLY from the customer's
// actual calculated chart facts (never generic horoscope filler). This is a
// template-based first pass; Phase 3 ("Better Personal Analysis" in the PRD)
// replaces/extends this with stronger RAG-grounded LLM reasoning.

const SIGN_TRAITS = {
  Aries: "bold, direct and quick to act",
  Taurus: "steady, patient and grounded",
  Gemini: "curious, adaptable and communicative",
  Cancer: "sensitive, nurturing and intuitive",
  Leo: "confident, warm and expressive",
  Virgo: "detail-oriented, practical and thoughtful",
  Libra: "diplomatic, balanced and relationship-focused",
  Scorpio: "intense, resilient and perceptive",
  Sagittarius: "optimistic, adventurous and philosophical",
  Capricorn: "disciplined, ambitious and responsible",
  Aquarius: "independent, original and idealistic",
  Pisces: "imaginative, compassionate and dreamy",
};

function findPlanetsInHouse(planets, house) {
  return planets.filter((p) => p.house === house).map((p) => p.name);
}

function joinNames(names) {
  if (names.length === 0) return null;
  if (names.length === 1) return names[0];
  return `${names.slice(0, -1).join(", ")} and ${names[names.length - 1]}`;
}

export function buildLifeAreas(chart) {
  const { lagna, rashi, planets } = chart;
  const careerPlanets = joinNames(findPlanetsInHouse(planets, 10));
  const lovePlanets = joinNames(findPlanetsInHouse(planets, 7));
  const moneyPlanets = joinNames(findPlanetsInHouse(planets, 2));
  const generalPlanets = joinNames(findPlanetsInHouse(planets, 1));

  return [
    {
      title: "Personality",
      icon: "🌟",
      text: `With ${lagna} rising and a ${rashi} Moon, your natural temperament leans ${SIGN_TRAITS[lagna] ?? lagna} with a ${SIGN_TRAITS[rashi] ?? rashi} emotional undercurrent.`,
    },
    {
      title: "Career",
      icon: "💼",
      text: careerPlanets
        ? `${careerPlanets} in your 10th house shapes how you show up professionally and what recognition looks like for you.`
        : `Your 10th house of career has no major placements in this chart — career themes are better read through your Lagna and its ruling planet.`,
    },
    {
      title: "Love & Relationships",
      icon: "💗",
      text: lovePlanets
        ? `${lovePlanets} in your 7th house influences how you approach partnership and commitment.`
        : `Your 7th house of partnership has no major placements here — relationship patterns are better read through your Moon and Venus.`,
    },
    {
      title: "Money",
      icon: "💰",
      text: moneyPlanets
        ? `${moneyPlanets} in your 2nd house colors your relationship with personal finances and accumulated resources.`
        : `Your 2nd house of wealth has no major placements here — money patterns are better read through your 11th house of gains.`,
    },
    {
      title: "General Life Themes",
      icon: "🧭",
      text: generalPlanets
        ? `${generalPlanets} placed directly in your 1st house strongly colors how you present yourself to the world.`
        : `Your chart's overall tone is set by your ${lagna} Lagna — that's the lens worth exploring first with the AI chat below.`,
    },
  ];
}
