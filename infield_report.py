import requests
import pandas as pd
from datetime import datetime, timedelta

# ─────────────────────────────────────────
# DATE RANGE — CURRENT WEEK
# ─────────────────────────────────────────
start_date = "2026-05-04"
end_date = "2026-05-10"

print(f"\nInfield Analysis - Week of May 4 to May 10, 2026")
print("=" * 60)

# ─────────────────────────────────────────
# PULL MLB SCHEDULE FOR THE WEEK
# ─────────────────────────────────────────
url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={start_date}&endDate={end_date}"
response = requests.get(url)
data = response.json()

print(f"API Status: {response.status_code}")
print(f"Total dates returned: {len(data.get('dates', []))}")

# Show first date to confirm structure
if data.get('dates'):
    first_date = data['dates'][0]
    print(f"\nFirst date: {first_date['date']}")
    print(f"Games that day: {first_date['totalGames']}")

    # ─────────────────────────────────────────
# BUILD GAME SCHEDULE — TEAMS + DATES
# ─────────────────────────────────────────
games = []

for date_entry in data['dates']:
    game_date = date_entry['date']
    for game in date_entry['games']:
        away_team = game['teams']['away']['team']['name']
        home_team = game['teams']['home']['team']['name']
        away_id = game['teams']['away']['team']['id']
        home_id = game['teams']['home']['team']['id']
        games.append({
            'date': game_date,
            'away_team': away_team,
            'away_id': away_id,
            'home_team': home_team,
            'home_id': home_id
        })

df_games = pd.DataFrame(games)
print(f"\nTotal games this week: {len(df_games)}")
print(f"\nGames by date:")
print(df_games.groupby('date').size())

# ─────────────────────────────────────────
# COUNT GAMES PER TEAM THIS WEEK
# ─────────────────────────────────────────
team_games = {}

for _, row in df_games.iterrows():
    # Count for away team
    if row['away_team'] not in team_games:
        team_games[row['away_team']] = {'team_id': row['away_id'], 'games': 0}
    team_games[row['away_team']]['games'] += 1

    # Count for home team
    if row['home_team'] not in team_games:
        team_games[row['home_team']] = {'team_id': row['home_id'], 'games': 0}
    team_games[row['home_team']]['games'] += 1

df_teams = pd.DataFrame([
    {'team': team, 'team_id': info['team_id'], 'games_this_week': info['games']}
    for team, info in team_games.items()
])

df_teams = df_teams.sort_values('games_this_week', ascending=False)
print("\nGames per team this week:")
print(df_teams.to_string(index=False))

# ─────────────────────────────────────────
# PULL INFIELDER STATS — CURRENT SEASON
# ─────────────────────────────────────────
print("\nPulling infielder stats...")

stats_url = "https://statsapi.mlb.com/api/v1/stats?stats=season&season=2026&group=hitting&gameType=R&playerPool=All&limit=500"
stats_response = requests.get(stats_url)
stats_data = stats_response.json()

print(f"API Status: {stats_response.status_code}")
print(f"Players returned: {len(stats_data.get('stats', [{}])[0].get('splits', []))}")

# Peek at first player to see structure
if stats_data.get('stats'):
    first_player = stats_data['stats'][0]['splits'][0]
    print(f"\nFirst player sample:")
    print(f"  Name: {first_player['player']['fullName']}")
    print(f"  Team: {first_player['team']['name']}")
    print(f"  Position: {first_player.get('position', {}).get('abbreviation', 'N/A')}")
    print(f"  Stats keys: {list(first_player['stat'].keys())[:10]}")

# ─────────────────────────────────────────
# PULL LAST 14 DAYS STATS
# ─────────────────────────────────────────
print("\nPulling last 14 days stats...")

end_14 = "2026-05-03"
start_14 = "2026-04-20"

stats_14_url = f"https://statsapi.mlb.com/api/v1/stats?stats=byDateRange&startDate={start_14}&endDate={end_14}&season=2026&group=hitting&gameType=R&playerPool=All&limit=500"

try:
    stats_14_response = requests.get(stats_14_url, timeout=30)
    stats_14_data = stats_14_response.json()
    print(f"API Status: {stats_14_response.status_code}")
    print(f"Players returned: {len(stats_14_data.get('stats', [{}])[0].get('splits', []))}")
except requests.exceptions.Timeout:
    print("Request timed out — trying again...")
    stats_14_response = requests.get(stats_14_url, timeout=60)
    stats_14_data = stats_14_response.json()
    print(f"API Status: {stats_14_response.status_code}")

# ─────────────────────────────────────────
# BUILD 14-DAY OBP LOOKUP
# ─────────────────────────────────────────
recent_stats = {}

for split in stats_14_data['stats'][0]['splits']:
    player_id = split['player']['id']
    stat = split['stat']
    
    at_bats = int(stat.get('atBats', 0))
    hits = int(stat.get('hits', 0))
    walks = int(stat.get('baseOnBalls', 0))
    hbp = int(stat.get('hitByPitch', 0))
    sac_flies = int(stat.get('sacFlies', 0))
    plate_appearances = at_bats + walks + hbp + sac_flies
    
    if plate_appearances >= 20:
        obp_14 = round((hits + walks + hbp) / plate_appearances, 3)
        recent_stats[player_id] = obp_14

print(f"Players with 20+ PA in last 14 days: {len(recent_stats)}")    

# ─────────────────────────────────────────
# BUILD INFIELDER DATAFRAME
# ─────────────────────────────────────────
infield_positions = ['1B', '2B', '3B', 'SS', 'C']
players = []

for split in stats_data['stats'][0]['splits']:
    position = split.get('position', {}).get('abbreviation', '')
    if position not in infield_positions:
        continue
    
    stat = split['stat']
    player_name = split['player']['fullName']
    player_id = split['player']['id']
    team_name = split['team']['name']
    
    # Only include players with meaningful sample size
    games_played = int(stat.get('gamesPlayed', 0))
    if games_played < 15:
        continue
    
    at_bats = int(stat.get('atBats', 0))
    hits = int(stat.get('hits', 0))
    hr = int(stat.get('homeRuns', 0))
    walks = int(stat.get('baseOnBalls', 0))
    hbp = int(stat.get('hitByPitch', 0))
    sac_flies = int(stat.get('sacFlies', 0))
    plate_appearances = at_bats + walks + hbp + sac_flies

    # Calculate OBP
    obp = round((hits + walks + hbp) / plate_appearances, 3) if plate_appearances > 0 else 0

    # Calculate HR Rate (HR per plate appearance)
    hr_rate = round(hr / plate_appearances, 3) if plate_appearances > 0 else 0

    players.append({
        'name': player_name,
        'team': team_name,
        'position': position,
        'games_played': games_played,
        'player_id': player_id,
        'hr': hr,
        'obp': obp,
        'hr_rate': hr_rate,
        'plate_appearances': plate_appearances
    })

df_players = pd.DataFrame(players)
print(f"\nInfielders with 15+ games: {len(df_players)}")
print(f"\nBy position:")
print(df_players.groupby('position').size())

# ─────────────────────────────────────────
# MERGE PLAYERS WITH TEAM SCHEDULE
# ─────────────────────────────────────────
df_merged = df_players.merge(
    df_teams[['team', 'games_this_week']],
    on='team',
    how='left'
)

# Fill any teams not found with 6 games (default)
df_merged['games_this_week'] = df_merged['games_this_week'].fillna(6)

# ─────────────────────────────────────────
# CALCULATE WEEKLY SCORE
# ─────────────────────────────────────────
# Apply position-specific rest day discount
def expected_starts(row):
    if row['position'] == 'C':
        return row['games_this_week'] * 0.60  # catchers play ~60% of games
    else:
        return row['games_this_week'] - 1     # everyone else gets 1 rest day

df_merged['expected_starts'] = df_merged.apply(expected_starts, axis=1)

# Weekly score = OBP (50%) + HR Rate (30%) + Schedule Factor (20%)
# Schedule factor = expected starts / 7 (max possible)
df_merged['schedule_factor'] = df_merged['expected_starts'] / 7

# Blend season OBP (40%) with 14-day OBP (60%)
df_merged['obp_blended'] = df_merged.apply(
    lambda row: round(
        (row['obp'] * 0.40) + (recent_stats.get(row['player_id'], row['obp']) * 0.60), 3
    ), axis=1
)

df_merged['weekly_score'] = round(
    (df_merged['obp_blended'] * 0.50) +
    (df_merged['hr_rate'] * 0.30) +
    (df_merged['schedule_factor'] * 0.20), 4
)

# Sort by weekly score
df_merged = df_merged.sort_values('weekly_score', ascending=False)

print("\nTop 10 Infielders This Week:")
print(f"{'Name':<25} {'Pos':<5} {'Team':<25} {'OBP':<6} {'HR':<4} {'Games':<7} {'Score'}")
print("-" * 85)
for _, row in df_merged.head(10).iterrows():
    print(f"  {row['name']:<23} {row['position']:<5} {row['team']:<25} {row['obp']:<6} {row['hr']:<4} {int(row['games_this_week']):<7} {row['weekly_score']}")

# ─────────────────────────────────────────
# TOP 5 BY POSITION
# ─────────────────────────────────────────
print("\n" + "=" * 60)
print("TOP 5 BY POSITION — Week of May 4-10, 2026")
print("=" * 60)

for pos in ['C', '1B', '2B', '3B', 'SS']:
    pos_df = df_merged[df_merged['position'] == pos].head(5)
    print(f"\n--- {pos} ---")
    print(f"  {'Name':<25} {'Team':<25} {'OBP':<6} {'HR':<4} {'Games':<7} {'Score'}")
    print(f"  {'-'*70}")
    for _, row in pos_df.iterrows():
        print(f"  {row['name']:<25} {row['team']:<25} {row['obp']:<6} {row['hr']:<4} {int(row['games_this_week']):<7} {row['weekly_score']}")

# ─────────────────────────────────────────
# SAVE TO CSV
# ─────────────────────────────────────────
output_file = "C:/Users/daveg/OneDrive/Desktop/infield_rankings_may4_10.csv"
df_merged[['name', 'position', 'team', 'obp', 'hr', 'hr_rate',
           'games_this_week', 'expected_starts', 'weekly_score']].to_csv(output_file, index=False)
print(f"\nReport saved to Desktop: infield_rankings_may4_10.csv")

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ─────────────────────────────────────────
# VISUALIZATION — TOP 5 BY POSITION
# ─────────────────────────────────────────
positions = ['C', '1B', '2B', '3B', 'SS']
colors = {
    'C': '#2E75B6',
    '1B': '#E74C3C', 
    '2B': '#27AE60',
    '3B': '#F39C12',
    'SS': '#8E44AD'
}

fig, axes = plt.subplots(1, 5, figsize=(20, 8))
fig.suptitle(
    'Top 5 Infielders by Position — Week of May 4-10, 2026\nBlended OBP (40% Season / 60% Last 14 Days) + Schedule + HR Rate',
    fontsize=13, fontweight='bold', y=1.02
)

for ax, pos in zip(axes, positions):
    pos_df = df_merged[df_merged['position'] == pos].head(5).copy()
    pos_df = pos_df.sort_values('weekly_score', ascending=True)  # ascending for horizontal bar

    bars = ax.barh(
        pos_df['name'],
        pos_df['weekly_score'],
        color=colors[pos],
        alpha=0.85,
        edgecolor='white',
        linewidth=0.5
    )

    # Add score labels on bars
    for bar, score in zip(bars, pos_df['weekly_score']):
        ax.text(
            bar.get_width() - 0.002,
            bar.get_y() + bar.get_height() / 2,
            f'{score:.3f}',
            va='center', ha='right',
            fontsize=8, color='white', fontweight='bold'
        )

    # Add games this week as annotation
    for i, (_, row) in enumerate(pos_df.iterrows()):
        ax.text(
            0.001,
            i,
            f"{int(row['games_this_week'])}G",
            va='center', ha='left',
            fontsize=7, color='white', alpha=0.9
        )

    ax.set_title(f'--- {pos} ---', fontweight='bold', color=colors[pos], fontsize=12)
    ax.set_xlabel('Weekly Score', fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='y', labelsize=8)
    ax.set_xlim(0, df_merged['weekly_score'].max() + 0.02)

plt.tight_layout()
plt.savefig(
    'C:/Users/daveg/OneDrive/Desktop/infield_rankings_may4_10.png',
    dpi=150, bbox_inches='tight', facecolor='white'
)
print("\nChart saved to Desktop: infield_rankings_may4_10.png")
plt.show()