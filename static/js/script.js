
const form = document.querySelector("#weather-form");
const cityInput = document.querySelector("#city-input");
const searchButton = document.querySelector("#search-button");
const searchHint = document.querySelector("#search-hint");
const backToTop = document.querySelector("#back-to-top");


// Update HTML elements with weather data
function setText(id, value) {
  const element = document.getElementById(id);

  if (element && value !== undefined && value !== null) {
    element.textContent = value;
  }
}


// Display weather data on the dashboard
function updateWeather(data) {
  setText("temperature", Math.round(data.temperature));
  setText("condition", data.condition || "Current Conditions");

  setText(
    "location",
    [data.city, data.country].filter(Boolean).join(", ")
  );

  setText("feels-like", `${Math.round(data.feels_like)}°C`);
  setText("humidity", `${data.humidity}%`);
  setText("wind-speed", `${data.wind_speed} km/h`);
  setText("wind-direction", data.wind_direction || "—");
  setText("pressure", `${data.pressure} hPa`);

  setText(
    "weather-message",
    data.message || "Weather conditions updated."
  );

  // Display the time when the data was fetched
  setText(
    "updated-at",
    new Intl.DateTimeFormat(undefined, {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    }).format(new Date())
  );
}


// Show loading state while fetching weather
function setLoading(isLoading) {
  searchButton.disabled = isLoading;

  const buttonText = searchButton.querySelector(
    "span:not(.button-arrow)"
  );

  if (buttonText) {
    buttonText.textContent = isLoading
      ? "Loading..."
      : "Get Weather";
  }
}


// Fetch weather data from Flask backend
async function getWeather(city) {
  const response = await fetch(
    `/api/weather?city=${encodeURIComponent(city)}`,
    {
      method: "GET",
      headers: {
        "Accept": "application/json"
      }
    }
  );

  const data = await response.json();

  // Handle backend errors
  if (!response.ok) {
    throw new Error(
      data.error || "Could not find weather for this city."
    );
  }

  return data;
}


// Handle city search form
form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const city = cityInput.value.trim();

  // Check if city input is empty
  if (!city) {
    searchHint.textContent = "Please enter a city name first.";
    cityInput.focus();
    return;
  }

  setLoading(true);

  searchHint.textContent =
    `Getting the latest weather for ${city}...`;

  try {
    // Request weather from Flask backend
    const weatherData = await getWeather(city);

    // Update dashboard
    updateWeather(weatherData);

    searchHint.textContent =
      `Weather updated for ${weatherData.city || city}.`;

  } catch (error) {
    searchHint.textContent =
      error.message || "Unable to fetch weather. Please try again.";

  } finally {
    // Restore search button
    setLoading(false);
  }
});


// Back to top button
if (backToTop) {
  backToTop.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  });
}
