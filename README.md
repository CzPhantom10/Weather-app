
# SkyCast 

A modern weather web app built with Flask (backend API) and a beautiful HTML/CSS/JS frontend. Get real-time weather, a 5-day forecast, and temperature trends for any city, with a stylish landing page and dynamic weather icons.


## Features 
- **Landing Page**: Modern, responsive landing page with app branding and feature highlights.
- **Current Weather**: See temperature, humidity, pressure, wind speed, and weather icon for your city.
- **5-Day Forecast**: View a daily forecast with icons and temperatures.
- **Temperature Trend Chart**: Interactive line chart (ApexCharts) for high/low temps.
- **Dynamic Weather Icons**: Icons change based on weather conditions.
- **Responsive UI**: Works great on desktop and mobile.

## Installation 

1. **Clone the repository**:
    ```bash
    git clone https://github.com/CzPhantom10/Weather-App.git
    cd Weather-App
    ```

2. **Install the required libraries**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your API key**:
    - Get a free API key from [OpenWeatherMap](https://openweathermap.org/appid)
    - Add it to your `.env` file:
      ```
      WEATHER_API_KEY=your_actual_api_key_here
      ```


## Usage 

1. Start the Flask app:
    ```bash
    python app.py
    ```

2. Open your browser and go to [http://localhost:5000](http://localhost:5000)
    - The landing page is at `/`
    - The weather dashboard is at `/app`


### Main Components
- **Flask** backend: Handles API requests and serves HTML templates
- **HTML/CSS/JS**: Modern, responsive frontend (see `templates/` and `static/`)
- **ApexCharts**: For interactive temperature trend chart
- **OpenWeatherMap API**: For real-time weather and forecast data


## License 
This project is licensed under the MIT License.

## Acknowledgements 
- **OpenWeatherMap API** for providing weather data
- **ApexCharts** for charting

Feel free to contribute and open issues if you have suggestions or find any bugs. Enjoy forecasting! 
