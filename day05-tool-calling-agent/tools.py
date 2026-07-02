"""
tools.py

Mock tools that simulate external APIs.

In a real-world AI system these would call:
- Weather APIs
- Currency Exchange APIs
- Internal Microservices
- Databases
"""

from datetime import datetime

def get_weather(city:str) -> dict:
    """
    Mock weather service.

    Args:
        city: City Name

    Returns:
        Dictionary containing weather information.
    """
    fake_weather = {
        "mumbai": {
            "temperature": 31,
            "condition": "Partly Cloudy",
            "humidity": 72
        },
        "pune": {
            "temperature": 28,
            "condition": "Sunny",
            "humidity": 45
        },
        "bangalore": {
            "temperature": 24,
            "condition": "Light Rain",
            "humidity": 80
        },
        "delhi": {
            "temperature": 38,
            "condition": "Hot",
            "humidity": 22
        }
    }

    city_key = city.lower()
    if city_key not in fake_weather:
        return {
            "success": False,
            "error": f"Weather data for {city} not found."
        }
    
    return {
        "success" : True,
        "city" : city.title(),
        "timestamp": datetime.now().isoformat(),
        "weather": fake_weather[city_key]
    }



def convert_currency(
        amount:float,
        from_currency:str,
        to_currency:str
) -> dict:
    """
    Mock currency conversion.

    Args:
        amount
        from_currency
        to_currency
    
    Returns:
        Conversion result.
    """

    rates = {
        ("USD", "INR"): 83.10,
        ("INR", "USD"): 0.012,
        ("EUR", "INR"): 90.30,
        ("INR", "EUR"): 0.011,
        ("USD", "EUR"): 0.92,
        ("EUR", "USD"): 1.08
    }

    key = (
        from_currency.upper(),
        to_currency.upper()
    )

    if key not in rates:
        return {
            "success": False,
            "error": f"Conversion from {from_currency} to {to_currency} not supported."
        }
    rate = rates[key]
    converted = round(
        amount*rate, 2
    )

    return {
        "success": True,
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "amount": amount,
        "exchange_rate": rate,
        "converted_amount": converted
    }