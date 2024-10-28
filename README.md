# Weather Prediction Model using LLM 🌦️

A web application built using Streamlit that provides current weather updates and a weekly weather forecast for any city. This app leverages the OpenWeatherMap API for real-time data and utilizes an LLM model to generate easy-to-understand descriptions of the weather. The weekly forecast includes a graphical representation of daily minimum and maximum temperatures.

## Features 📋
- **Current Weather Data**: Displays current temperature, humidity, pressure, and wind speed for the specified city.
- **Weather Description**: Uses an LLM model to generate a user-friendly description of the current weather.
- **Weekly Forecast**: Provides a detailed daily forecast for the next week, including min and max temperatures.
- **Graphical Representation**: Visualizes the weekly temperature forecast in a line graph.

## Demo 🎬
![Demo Screenshot](Weather-app-ss.pdf)

## Installation 🚀

1. **Clone the repository**:
    ```bash
    git clone https://github.com/CzPhantom10/Weather-App.git
    cd weather-prediction-llm
    ```

2. **Install the required libraries**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up API keys**:
    Replace the placeholder `weather_api_key` in `main()` function with your OpenWeatherMap API key.

## Usage 🖥️

1. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

2. **Enter a city** in the sidebar and click "Get Weather" to retrieve current weather updates and weekly forecast.

### Main Components

- **get_weather_data(city, weather_api_key)**: Fetches current weather data from OpenWeatherMap API.
- **generate_weather_description(data)**: Uses an LLM to generate a description of the current weather.
- **get_weekly_forecast(weather_api_key, lat, lon)**: Retrieves a 7-day weather forecast based on city coordinates.
- **display_weekly_forecast(data)**: Displays daily min and max temperatures, along with a graph, for the weekly forecast.

### Dependencies

- **Streamlit** for the web interface
- **Requests** for handling API calls
- **Matplotlib** for graphing weekly forecast data
- **LLM Client** for generating user-friendly weather descriptions

## License 📝
This project is licensed under the MIT License.

## Acknowledgements 🙌
- **OpenWeatherMap API** for providing weather data
- **Streamlit** for making it easy to build and deploy web applications

Feel free to contribute and open issues if you have suggestions or find any bugs. Enjoy forecasting! 🌤️
