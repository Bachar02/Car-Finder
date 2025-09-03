from fastapi import FastAPI, Request
from services.gemini_service import get_gemini_response
from services.sql_service import read_sql_query

app = FastAPI()

@app.post("/query")
async def query(request: Request):
    data = await request.json()
    question = data.get("question", "")

    sql = get_gemini_response(question)
    rows, cols = read_sql_query(sql)

    return {
        "sql": sql,
        "columns": cols,
        "rows": rows
    }

@app.get("/")
def health_check():
    return {"status": "Backend running 🚀"}


# backend/backend.py - Add these functions

def initialize_alerts_table():
    """Initialize alerts table"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS car_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                brand TEXT,
                max_price INTEGER,
                max_mileage INTEGER,
                min_year INTEGER,
                fuel_type TEXT,
                transmission TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')

        conn.commit()
        conn.close()
        print("✅ Alerts table initialized successfully")

    except Exception as e:
        print(f"❌ Alerts table initialization failed: {e}")

# Add this to your existing initialize_database function
def initialize_database():
    # ... your existing code ...
    initialize_alerts_table()  # Add this line

# Add these new API endpoints
@app.post("/api/alerts")
async def create_alert(request: Request):
    """Create a new car alert"""
    data = await request.json()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO car_alerts (user_id, brand, max_price, max_mileage, min_year, fuel_type, transmission)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('user_id', 'default_user'),
            data.get('brand'),
            data.get('max_price'),
            data.get('max_mileage'),
            data.get('min_year'),
            data.get('fuel_type'),
            data.get('transmission')
        ))

        conn.commit()
        alert_id = cursor.lastrowid
        conn.close()

        return {"message": "Alert created successfully", "alert_id": alert_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create alert: {str(e)}")

@app.get("/api/alerts/{user_id}")
def get_user_alerts(user_id: str):
    """Get alerts for a specific user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM car_alerts WHERE user_id = ? AND is_active = TRUE ORDER BY created_at DESC", (user_id,))

        alerts = []
        columns = [description[0] for description in cursor.description]

        for row in cursor.fetchall():
            alert = dict(zip(columns, row))
            alerts.append(alert)

        conn.close()
        return {"alerts": alerts}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get alerts: {str(e)}")

@app.get("/api/check-alerts")
def check_alerts():
    """Check if any cars match existing alerts (for cron job)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get all active alerts
        cursor.execute("SELECT * FROM car_alerts WHERE is_active = TRUE")
        alerts = cursor.fetchall()

        matches = []
        for alert in alerts:
            alert_id, user_id, brand, max_price, max_mileage, min_year, fuel_type, transmission, created_at, is_active = alert

            # Build query based on alert criteria
            query = "SELECT * FROM cars WHERE 1=1"
            params = []

            if brand:
                query += " AND LOWER(brand) LIKE ?"
                params.append(f"%{brand.lower()}%")

            if max_price:
                query += " AND price <= ?"
                params.append(max_price)

            if max_mileage:
                query += " AND mileage <= ?"
                params.append(max_mileage)

            if min_year:
                query += " AND year >= ?"
                params.append(min_year)

            if fuel_type:
                query += " AND LOWER(fuel) LIKE ?"
                params.append(f"%{fuel_type.lower()}%")

            if transmission:
                query += " AND LOWER(transmission) LIKE ?"
                params.append(f"%{transmission.lower()}%")

            cursor.execute(query, params)
            matching_cars = cursor.fetchall()

            if matching_cars:
                matches.append({
                    "alert_id": alert_id,
                    "user_id": user_id,
                    "matching_cars": len(matching_cars),
                    "criteria": {
                        "brand": brand,
                        "max_price": max_price,
                        "max_mileage": max_mileage,
                        "min_year": min_year,
                        "fuel_type": fuel_type,
                        "transmission": transmission
                    }
                })

        conn.close()
        return {"matches": matches}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check alerts: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
