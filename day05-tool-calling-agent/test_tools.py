from tool_registry import ToolRegistry

registry = ToolRegistry()

print("=" * 50)
print("Available Tools")
print("=" * 50)

print(
    registry.get_available_tools()
)

print()

print("=" * 50)
print("Weather")
print("=" * 50)

print(
    registry.execute(
        "get_weather",
        city="Mumbai"
    )
)

print()

print("=" * 50)
print("Currency")
print("=" * 50)

print(
    registry.execute(
        "convert_currency",
        amount=500,
        from_currency="USD",
        to_currency="INR"
    )
)

print()

print("=" * 50)
print("Tool Metadata")
print("=" * 50)

for tool in registry.describe_tools():
    print(tool)