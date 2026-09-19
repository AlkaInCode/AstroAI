// A curated shortlist covering the most common birth-place regions for Phase 1.
// A real geocoding+timezone API (e.g. the same provider chosen for production
// geocoding) should replace manual selection once wired up.
export const COMMON_TIMEZONES = [
  "Pacific/Midway",
  "Pacific/Honolulu",
  "America/Anchorage",
  "America/Los_Angeles",
  "America/Denver",
  "America/Chicago",
  "America/New_York",
  "America/Sao_Paulo",
  "Atlantic/Azores",
  "UTC",
  "Europe/London",
  "Europe/Paris",
  "Europe/Berlin",
  "Europe/Moscow",
  "Africa/Cairo",
  "Africa/Johannesburg",
  "Asia/Dubai",
  "Asia/Karachi",
  "Asia/Kolkata",
  "Asia/Dhaka",
  "Asia/Bangkok",
  "Asia/Shanghai",
  "Asia/Tokyo",
  "Australia/Sydney",
  "Pacific/Auckland",
];

/** Rough guess only -- a real timezone API should confirm this from lat/long + date. */
export function guessTimezone(longitude) {
  const hourOffset = Math.round((longitude / 15) * 2) / 2;
  const known = {
    0: "UTC",
    1: "Europe/Paris",
    2: "Africa/Cairo",
    3: "Europe/Moscow",
    4: "Asia/Dubai",
    5: "Asia/Karachi",
    5.5: "Asia/Kolkata",
    6: "Asia/Dhaka",
    7: "Asia/Bangkok",
    8: "Asia/Shanghai",
    9: "Asia/Tokyo",
    10: "Australia/Sydney",
    "-5": "America/New_York",
    "-6": "America/Chicago",
    "-7": "America/Denver",
    "-8": "America/Los_Angeles",
  };
  return known[hourOffset] || "UTC";
}
