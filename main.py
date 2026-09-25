from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests, os
from datetime import datetime

app = FastAPI(title="PR-PRONOS API PROPRE")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

FOOT_KEY = os.getenv("API_FOOTBALL_KEY", "6d6779cb3070f936bdcba790fadb8e0e")
ODDS_KEY = os.getenv("ODDS_API_KEY", "5a7dbf0d8caf78c99aed5b")

@app.get("/")
def home():
    return {"message": "PR-PRONOS PROPRE V1 ✅", "bookmakers": "1xBet, Bet365 inclus"}

@app.get("/v1/matchs")
def matchs():
    today = datetime.now().strftime("%Y-%m-%d")
    r = requests.get(f"https://v3.football.api-sports.io/fixtures?date={today}", headers={"x-apisports-key": FOOT_KEY}, timeout=20)
    data = r.json().get("response", [])[:20]
    matchs = [{"domicile": f["teams"]["home"]["name"], "exterieur": f["teams"]["away"]["name"], "ligue": f["league"]["name"]} for f in data]
    return {"date": today, "total": len(matchs), "matchs": matchs}

@app.get("/v1/bookmakers")
def bookmakers():
    url = f"https://api.the-odds-api.com/v4/sports/soccer_epl/odds/?apiKey={ODDS_KEY}&regions=eu&markets=h2h"
    r = requests.get(url, timeout=20)
    return {"cotes": r.json()[:5], "credits": r.headers.get("x-requests-remaining")}
