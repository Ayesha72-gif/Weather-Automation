
# Weather Automation

A simple weather application built with Python and Flask that fetches current weather information for different cities using the Open-Meteo API.

## Features

- Search weather by city name
- Fetch current weather data
- Display temperature and feels-like temperature
- Show humidity and atmospheric pressure
- Display wind speed and direction
- Handle invalid city names and API errors

## Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- Open-Meteo API
- Requests

## Project Structure

```text
weather-automation/
│
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── tests/
├── reports/
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Ayesha72-gif/Weather-Automation.git
```

### 2. Navigate to the project folder

```bash
cd Weather-Automation
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## API

Weather data is provided by [Open-Meteo](https://open-meteo.com/).

No API key is required for this project.

## Author

Ayesha Saddiqua
