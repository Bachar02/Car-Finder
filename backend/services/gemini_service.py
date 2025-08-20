import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = [
    """
    You are an assistant that generates SQL queries from user requests.
    You must ONLY return valid SQL queries.
    Do not add explanations. Do not use extra text.

    Database schema:
    Table name: cars
    Columns:
    - id (integer)
    - name (text)
    - brand (text)
    - model (text)
    - year (integer)
    - price (integer, euros)
    - mileage (integer, kilometers)
    - transmission (text: 'manual' or 'automatic')
    - fuel (text: 'diesel', 'petrol', 'electric', etc.)
    - power (integer, horsepower)
    - date_posted (date)

    Rules:
    1. Always use SELECT statements only. Never modify the database.
    2. Use `LIKE` with wildcards for text searches (example: `LOWER(brand) LIKE '%mercedes%'`).
    3. Always add `LIMIT 20` if the user doesn’t specify a limit.
    4. When asking for cheapest or most expensive, sort by `price`.
    5. When asking for newest or latest, sort by `date_posted DESC`.
    6. When asking for oldest, sort by `date_posted ASC`.
    7. When filtering by year, price, or mileage, use correct numeric comparisons.
    8. Output must be only the SQL query, no explanations.
    9. The sql code should not have ''' un beginning or end and sql word in output.

    Examples:

    User: "Give me the 3 cheapest Peugeot cars"
    SQL:
    SELECT * FROM cars
    WHERE LOWER(brand) LIKE '%peugeot%'
    ORDER BY price ASC
    LIMIT 3;

    User: "Show me Mercedes cars under 7000 euros"
    SQL:
    SELECT * FROM cars
    WHERE LOWER(brand) LIKE '%mercedes%' AND price < 7000
    ORDER BY date_posted DESC
    LIMIT 20;

    User: "Latest 5 automatic cars"
    SQL:
    SELECT * FROM cars
    WHERE LOWER(transmission) LIKE '%automatic%'
    ORDER BY date_posted DESC
    LIMIT 5;
    """
]

def get_gemini_response(question: str) -> str:
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content([prompt[0], question])
    return response.text.strip()
