from tools import get_weather
from tools import convert_currency

print("=" * 50)
print("Weather Tool")
print("=" * 50)

print(
    get_weather("Mumbai")
)

print()

print("=" * 50)
print("Currency Tool")
print("=" * 50)

print(
    convert_currency(
        500,
        "USD",
        "INR"
    )
)