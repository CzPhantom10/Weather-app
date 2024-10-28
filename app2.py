import streamlit as st
import requests 
from g4f.client import Client 
from datetime import datetime
import matplotlib.pyplot as plt
def get_weather_data(city, weather_api_key):
    base_url="https://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + weather_api_key + "&q=" + city
    response = requests.get(complete_url)
    return response.json()
def generate_weather_description(data):
    client = Client()
    try:
        temperature = data['main']['temp'] - 273.15
        description= data['weather'][0]['description']
        prompt = f"The current weather in your city is {description} with a temperature of {temperature:.1f}C. Explain this in a simple way for a general audience."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)
    
def get_weekly_forecast(weather_api_key, lat, lon):
    base_url= "https://api.openweathermap.org/data/2.5/"
    complete_url = f"{base_url}forecast?lat={lat}&lon={lon}&appid={weather_api_key}"
    response = requests.get(complete_url)
    return response.json()

def display_weekly_forecast(data):
    try:
        st.write("_______________________________________________________________________________________________")
        st.write("## Weekly Weather Forecast")
        displayed_dates = set()
        c1,c2,c3,c4 =st.columns(4)
        with c1:
            st.metric("","Day")
        with c2:
            st.metric("","Desc")
        with c3:
            st.metric("","Min Temp ❄️")
        with c4:
            st.metric("","Max Temp ☀️")
        dates = []
        min_temps = []
        max_temps = []
        for day in data['list']:
            date = datetime.fromtimestamp(day['dt']).strftime('%A, %B %d')
            if date not in displayed_dates:
                displayed_dates.add(date)
                temps = [d['main']['temp'] - 273.15 for d in data['list'] if datetime.fromtimestamp(d['dt']).strftime('%A, %B %d') == date]
                min_temp = min(temps)
                max_temp = max(temps)
                description= day['weather'][0]['description']
                with c1:
                    st.write(f"{date}")
                with c2:
                    st.write(f"{description.capitalize()}")
                with c3:
                    st.write(f"{min_temp:.1f}C")
                with c4:
                    st.write(f"{max_temp:.1f}C")
                dates.append(date)
                min_temps.append(min_temp)
                max_temps.append(max_temp)
        st.write("")
        st.subheader("Graphical Representation of Weekly Temperature Forecast 📉")
        st.write("")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(dates, min_temps, label='Min Temperature ❄️', marker='o')
        ax.plot(dates, max_temps, label='Max Temperature ☀️', marker='o')
        ax.set_xlabel('Date')
        ax.set_ylabel('Temperature (C)')
        ax.set_title('Weekly Temperature Forecast')
        ax.legend(loc='upper left')
        ax.grid(True)
        plt.xticks(rotation=45) 
        st.pyplot(fig)

    except Exception as e:
        st.error("Error is displaying weekly forecast : " + str(e))

def main():
    st.sidebar.image("logo.jpeg",width=120)
    st.sidebar.title("Weather Prediction Model using LLM")
    city = st.sidebar.text_input("Enter city name","London")
    weather_api_key="c536542ac20e1b32f809cb981f9c46b4"
    submit = st.sidebar.button("Get Weather")
    if submit:
        st.title("Weather updates for " + city + " is:")
        with st.spinner("Fetching weather data.."):
            weather_data = get_weather_data(city, weather_api_key)
            print(weather_data)
            if 'cod' in weather_data and weather_data['cod'] != 404:
                if 'main' in weather_data:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Temperature 🌡️",f"{weather_data['main']['temp']-273.15:.2f}C")
                        st.metric("Humidity 💧",f"{weather_data['main']['humidity']}%")
                    with col2:
                        st.metric("Pressure", f"{weather_data['main']['pressure']} hPa")
                        st.metric("wind Speed 🍃",f"{weather_data['wind']['speed']} m/s")
                    lat = weather_data['coord']['lat']
                    lon = weather_data['coord']['lon']
                    weather_description = generate_weather_description(weather_data)
                    st.write(weather_description)
                    forecast_data = get_weekly_forecast(weather_api_key, lat, lon)
                    print(forecast_data)
                    if 'cod' in forecast_data and forecast_data['cod'] != "404":
                        display_weekly_forecast(forecast_data)
                    else:
                        st.error("Error fetching weekly forecast data!")      
                else:
                    st.error("City not found or invalid data.")
            else:
                st.error("City not found.")

if __name__ == "__main__":
    main()