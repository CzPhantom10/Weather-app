import streamlit as st
import requests 
from g4f.client import Client 
from datetime import datetime
import matplotlib.pyplot as plt

def get_weather_data(city, weather_api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": weather_api_key,
        "units": "metric"  # This will give temperature in Celsius directly
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None

def generate_weather_description(data):
    client = Client()
    try:
        temperature = data['main']['temp']  # Already in Celsius due to units=metric
        description = data['weather'][0]['description']
        prompt = f"The current weather in your city is {description} with a temperature of {temperature:.1f}°C. Explain this in a simple way for a general audience."
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Updated model
            messages=[{"role": "user", "content": prompt}],
            web_search=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Unable to generate weather description: {str(e)}"
    
def get_weekly_forecast(weather_api_key, lat, lon):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": weather_api_key,
        "units": "metric"  # This will give temperature in Celsius directly
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching forecast data: {str(e)}")
        return None

def display_weekly_forecast(data):
    try:
        st.write("_______________________________________________________________________________________________")
        st.write("## Weekly Weather Forecast")
        displayed_dates = set()
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("", "Day")
        with c2:
            st.metric("", "Description")
        with c3:
            st.metric("", "Min Temp ❄️")
        with c4:
            st.metric("", "Max Temp ☀️")
        
        dates = []
        min_temps = []
        max_temps = []
        
        for day in data['list']:
            date = datetime.fromtimestamp(day['dt']).strftime('%A, %B %d')
            if date not in displayed_dates:
                displayed_dates.add(date)
                # Get all temperatures for this date
                temps = [d['main']['temp'] for d in data['list'] 
                        if datetime.fromtimestamp(d['dt']).strftime('%A, %B %d') == date]
                min_temp = min(temps)
                max_temp = max(temps)
                description = day['weather'][0]['description']
                
                with c1:
                    st.write(f"{date}")
                with c2:
                    st.write(f"{description.capitalize()}")
                with c3:
                    st.write(f"{min_temp:.1f}°C")
                with c4:
                    st.write(f"{max_temp:.1f}°C")
                
                dates.append(date)
                min_temps.append(min_temp)
                max_temps.append(max_temp)
        
        st.write("")
        st.subheader("Graphical Representation of Weekly Temperature Forecast 📉")
        st.write("")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(dates, min_temps, label='Min Temperature ❄️', marker='o', linewidth=2)
        ax.plot(dates, max_temps, label='Max Temperature ☀️', marker='o', linewidth=2)
        ax.set_xlabel('Date')
        ax.set_ylabel('Temperature (°C)')
        ax.set_title('Weekly Temperature Forecast')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error displaying weekly forecast: {str(e)}")

def main():
    st.sidebar.image("logo.jpeg", width=120)
    st.sidebar.title("Weather Prediction Model using LLM")
    city = st.sidebar.text_input("Enter city name", "London")
    weather_api_key = "bec5708354c95bcef3babdbc5950a280"
    submit = st.sidebar.button("Get Weather")
    
    if submit:
        if not city.strip():
            st.error("Please enter a valid city name.")
            return
            
        st.title(f"Weather updates for {city}:")
        
        with st.spinner("Fetching weather data..."):
            weather_data = get_weather_data(city, weather_api_key)
            
            if weather_data is None:
                return
                
            # Check if the API returned a successful response
            if weather_data.get('cod') == 200:
                if 'main' in weather_data:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Temperature 🌡️", f"{weather_data['main']['temp']:.2f}°C")
                        st.metric("Humidity 💧", f"{weather_data['main']['humidity']}%")
                    with col2:
                        st.metric("Pressure", f"{weather_data['main']['pressure']} hPa")
                        if 'wind' in weather_data:
                            st.metric("Wind Speed 🍃", f"{weather_data['wind']['speed']} m/s")
                        else:
                            st.metric("Wind Speed 🍃", "N/A")
                    
                    lat = weather_data['coord']['lat']
                    lon = weather_data['coord']['lon']
                    
                    # Generate weather description using updated g4f model
                    weather_description = generate_weather_description(weather_data)
                    st.write("### Weather Description")
                    st.write(weather_description)
                    
                    # Get weekly forecast
                    forecast_data = get_weekly_forecast(weather_api_key, lat, lon)
                    if forecast_data and forecast_data.get('cod') == '200':
                        display_weekly_forecast(forecast_data)
                    else:
                        st.error("Error fetching weekly forecast data!")      
                else:
                    st.error("Invalid weather data received.")
            elif weather_data.get('cod') == 404:
                st.error(f"City '{city}' not found. Please check the spelling and try again.")
            elif weather_data.get('cod') == 401:
                st.error("Invalid API key. Please check your OpenWeatherMap API key.")
            else:
                st.error(f"Error: {weather_data.get('message', 'Unknown error occurred')}")

if __name__ == "__main__":
    main()