from yahoo_oauth import OAuth2
import json

oauth = OAuth2(None, None, from_file="oauth_creds.json")

if not oauth.token_is_valid():
    oauth.refresh_access_token()

league_key = "469.l.5422"
team_key = "469.l.5422.t.9"

# Get roster first
url = f"https://fantasysports.yahooapis.com/fantasy/v2/team/{team_key}/roster/players?format=json"
response = oauth.session.get(url)
data = response.json()
roster = data["fantasy_content"]["team"][1]["roster"]["0"]["players"]

# Collect pitcher keys
pitcher_keys = []
pitcher_names = {}

for key in roster:
    if key == "count":
        continue
    p = roster[key]["player"][0]
    name = p[2]["name"]["full"]
    pos_type = "???"
    player_key = "???"
    for item in p:
        if isinstance(item, dict):
            if "position_type" in item:
                pos_type = item["position_type"]
            if "player_key" in item:
                player_key = item["player_key"]
    if pos_type == "P":
        pitcher_keys.append(player_key)
        pitcher_names[player_key] = name

# Now get stats for each pitcher
pitch_stats = {"50": "IP", "28": "W", "32": "SV", "37": "ER", "42": "K", "48": "HLD", "83": "QS"}

print("Team SueShar - Pitcher Stats (2026 Season):")
print("-" * 70)
print(f"  {'Name':<22} {'IP':<7} {'W':<4} {'SV':<4} {'ER':<5} {'K':<5} {'HLD':<5} {'QS'}")
print("-" * 70)

for pk in pitcher_keys:
    url = f"https://fantasysports.yahooapis.com/fantasy/v2/player/{pk}/stats?format=json"
    response = oauth.session.get(url)
    data = response.json()
    stats_list = data["fantasy_content"]["player"][1]["player_stats"]["stats"]
    stats = {}
    for s in stats_list:
        sid = str(s["stat"]["stat_id"])
        if sid in pitch_stats:
            stats[sid] = s["stat"]["value"]
    name = pitcher_names[pk]
    print(f"  {name:<22} {stats.get('50',''):<7} {stats.get('28',''):<4} {stats.get('32',''):<4} {stats.get('37',''):<5} {stats.get('42',''):<5} {stats.get('48',''):<5} {stats.get('83','')}")