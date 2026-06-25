import tiktoken

encoding  = tiktoken.get_encoding("cl100k_base")

samples = {
    "Plain English": """
Retrieval Augmented Generation combines vector search with large language models.
""",

    "Python Function": """
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total
""",

    "JSON Object": """
{
  "name": "Siddhesh",
  "role": "Backend Engineer",
  "language": "Java",
  "database": "PostgreSQL",
  "experience": 3
}
""",

    "SQL Query": """
SELECT e.id,
       e.name,
       d.department_name
FROM employees e
JOIN departments d
  ON e.department_id = d.id
WHERE e.salary > 100000;
""",

    "Hindi Paragraph": """
मेरा नाम सिद्धेश है। मैं एक सॉफ्टवेयर इंजीनियर हूँ और एआई इंजीनियरिंग सीख रहा हूँ।
"""
}

print("-"*90)

print(
    f"{'Type':<20}"
    f"{'Characters':<15}"
    f"{'Tokens':<15}"
    f"{'Chars/Token':<15}" 
)
print("-" * 90)

for text_type, text in samples.items():
    chars = len(text)

    tokens = len(encoding.encode(text))
    ratio = chars / tokens

    print(
        f"{text_type:<20}"
        f"{chars:<15}"
        f"{tokens:<15}"
        f"{ratio:<15.2f}"
    )

print("-"*90)