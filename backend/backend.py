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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)