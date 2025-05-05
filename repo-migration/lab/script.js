document.addEventListener('DOMContentLoaded', function() {
    const cityInput = document.getElementById('city-input');
    const searchBtn = document.getElementById('search-btn');
    const cityName = document.getElementById('city-name');
    const temperature = document.getElementById('temperature');
    const weatherDescription = document.getElementById('weather-description');
    const humidity = document.getElementById('humidity');
    const windSpeed = document.getElementById('wind-speed');
    
    // Mock weather data (in a real app, this would come from an API)
    const mockWeatherData = {
        'new york': { temp: 20, description: 'cloudy', humidity: 65, wind: 5.5 },
        'london': { temp: 15, description: 'rainy', humidity: 80, wind: 4.2 },
        'tokyo': { temp: 25, description: 'sunny', humidity: 50, wind: 3.1 },
        'paris': { temp: 18, description: 'partly cloudy', humidity: 60, wind: 4.8 },
        'sydney': { temp: 28, description: 'clear sky', humidity: 45, wind: 6.2 }
    };
    
    searchBtn.addEventListener('click', function() {
        const city = cityInput.value.trim().toLowerCase();
        if (city) {
            getWeatherData(city);
        }
    });
    
    // Temperature conversion function - to be uncommented in Part 2
    /*
    function convertTemperature(celsius) {
        // Convert Celsius to Fahrenheit
        const fahrenheit = (celsius * 9/5) + 32;
        
        // Update the temperature display
        temperature.textContent = celsius;
        
        // Add Fahrenheit in parentheses
        const fahrenheitDisplay = document.createElement('span');
        fahrenheitDisplay.textContent = ` (${fahrenheit.toFixed(1)}°F)`;
        fahrenheitDisplay.style.fontSize = '0.7em';
        fahrenheitDisplay.style.color = '#666';
        
        // Clear any existing conversion before adding new one
        temperature.innerHTML = celsius;
        temperature.appendChild(fahrenheitDisplay);
    }
    */
    
    function getWeatherData(city) {
        // In a real app, this would be an API call
        setTimeout(() => {
            if (mockWeatherData[city]) {
                displayWeather(city, mockWeatherData[city]);
            } else {
                alert('City not found. Try New York, London, Tokyo, Paris, or Sydney.');
            }
        }, 500);
    }
    
    function displayWeather(city, data) {
        cityName.textContent = city.charAt(0).toUpperCase() + city.slice(1);
        temperature.textContent = data.temp;
        weatherDescription.textContent = data.description;
        humidity.textContent = data.humidity + '%';
        windSpeed.textContent = data.wind + ' m/s';
        
        // The convertTemperature function would be called here in Part 2
        // convertTemperature(data.temp);
    }
});
