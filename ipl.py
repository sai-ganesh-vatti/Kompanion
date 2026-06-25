import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd

# Load dataset
df = pd.read_csv("ipl_data.csv", low_memory=False)

# Team name replacements
team_replacements = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Deccan Chargers': 'Sunrisers Hyderabad',
    'Kings XI Punjab': 'Punjab Kings',
    'Pune Warriors': 'Rising Pune Supergiants',
    'Rising Pune Supergiant': 'Rising Pune Supergiants'
}

# Columns where team names exist
team_columns = [
    'batting_team',
    'bowling_team',
    'team1',
    'team2',
    'winner',
    'toss_winner'
]

# Replace names
for col in team_columns:
    if col in df.columns:
        df[col] = df[col].replace(team_replacements)

# Check unique teams
for col in team_columns:
    if col in df.columns:
        print(f"\n{col}")
        print(df[col].dropna().unique())

# Print final cleaned IPL teams

print("\nFinal IPL Teams:\n")

team_cols = ['batting_team', 'team1', 'team2']

all_teams = pd.concat([
    df[col] for col in team_cols if col in df.columns
]).dropna().unique()

print(sorted(all_teams))

print("\nTotal Teams:", len(all_teams))

# Merge duplicate RCB names
df = df.replace({
    'Royal Challengers Bengaluru': 'Royal Challengers Bangalore'
})

# Remove outdated teams
remove_teams = [
    'Gujarat Lions',
    'Kochi Tuskers Kerala',
    'Rising Pune Supergiants'
]

# Remove rows containing old teams
for col in ['batting_team', 'team1', 'team2']:
    if col in df.columns:
        df = df[~df[col].isin(remove_teams)]

# Print cleaned teams again
print("\nCleaned IPL Teams:\n")

team_cols = ['batting_team', 'team1', 'team2']

all_teams = pd.concat([
    df[col] for col in team_cols if col in df.columns
]).dropna().unique()

print(sorted(all_teams))

print("\nTotal Teams:", len(all_teams))

# Check available player-related columns

player_cols = [
    'batter',
    'bowler',
    'non_striker',
    'player_dismissed'
]

for col in player_cols:
    if col in df.columns:
        print(f"\n{col}")
        print(df[col].dropna().head())
        print("Unique Players:", df[col].nunique())

# Create player-team mapping

player_team = df[['batter', 'batting_team']].dropna()

# Count appearances
player_team_count = (
    player_team
    .groupby(['batter', 'batting_team'])
    .size()
    .reset_index(name='matches')
)

# Get most frequent franchise for each player
player_main_team = (
    player_team_count
    .sort_values('matches', ascending=False)
    .drop_duplicates('batter')
)

print(player_main_team.head(20))

# Batter performance summary

batter_stats = (
    df.groupby('batter')
    .agg(
        runs=('runs_batter', 'sum'),
        balls=('ball', 'count'),
        matches=('match_id', 'nunique')
    )
    .reset_index()
)

# Strike Rate
batter_stats['strike_rate'] = (
    batter_stats['runs'] / batter_stats['balls']
) * 100

# Minimum matches filter
batter_stats = batter_stats[
    batter_stats['matches'] >= 10
]

# Sort top batters
top_batters = batter_stats.sort_values(
    by='runs',
    ascending=False
)

# Display top 20
print(top_batters.head(20))

# Top bowler analysis

bowler_stats = (
    df[df['wicket_kind'].notna()]
    .groupby('bowler')
    .agg(
        wickets=('wicket_kind', 'count'),
        matches=('match_id', 'nunique')
    )
    .reset_index()
)

# Minimum matches filter
bowler_stats = bowler_stats[
    bowler_stats['matches'] >= 10
]

# Sort by wickets
top_bowlers = bowler_stats.sort_values(
    by='wickets',
    ascending=False
)

# Display top 20 bowlers
print(top_bowlers.head(20))

# Team batting strength

team_batting = (
    df.groupby('batting_team')
    .agg(
        total_runs=('runs_batter', 'sum'),
        matches=('match_id', 'nunique')
    )
    .reset_index()
)

team_batting['avg_runs_per_match'] = (
    team_batting['total_runs'] /
    team_batting['matches']
)

print("\nTeam Batting Strength\n")
print(
    team_batting.sort_values(
        by='avg_runs_per_match',
        ascending=False
    )
)
# Convert season to integer

df['season'] = pd.to_numeric(
    df['season'],
    errors='coerce'
)
df['season'] = pd.to_numeric(df['season'])

# Recent seasons only
recent_df = df[df['season'] >= 2022]

# Playoff teams only
playoff_teams = [
    'Sunrisers Hyderabad',
    'Rajasthan Royals',
    'Gujarat Titans',
    'Royal Challengers Bangalore'
]

recent_df = recent_df[
    recent_df['batting_team'].isin(playoff_teams)
]

print(recent_df[['season', 'batting_team']].head())

# Calculate total runs per team per match first, then average them
match_runs = recent_df.groupby(['batting_team', 'match_id'])['runs_batter'].sum().reset_index()
team_recent_strength = (
    match_runs.groupby('batting_team')['runs_batter']
    .mean()
    .reset_index(name='avg_runs_per_match')
)

team_recent_strength = team_recent_strength.sort_values(
    by='avg_runs_per_match',
    ascending=False
)

print("\nRecent Batting Form\n")
print(team_recent_strength)

top_scorers = (
    recent_df.groupby('batter') # Keeps it focused on 2022+ Playoff team players
    .agg(
        runs=('runs_batter', 'sum'),
        balls=('ball', 'count')
    )
    .sort_values(by='runs', ascending=False)
    .head(10)
)

print("\nTop Run Scorers\n")
print(top_scorers)

wickets_df = df[df['wicket_kind'].notna()]

top_wickets = (
    wickets_df.groupby('bowler')
    .agg(
        wickets=('wicket_kind', 'count')
    )
    .sort_values(by='wickets', ascending=False)
    .head(10)
)

print("\nTop Wicket Takers\n")
print(top_wickets)

economy = (
    df.groupby('bowler')
    .agg(
        runs_given=('runs_total', 'sum'),
        balls=('ball', 'count')
    )
)

economy['overs'] = economy['balls'] / 6

economy = economy[economy['overs'] >= 100]

economy['economy_rate'] = (
    economy['runs_given'] / economy['overs']
)

economy = economy.sort_values(
    by='economy_rate',
    ascending=True
).head(10)

print("\nBest Economy Bowlers\n")
print(economy[['runs_given', 'overs', 'economy_rate']])

playoff_teams = [
    'Sunrisers Hyderabad',
    'Rajasthan Royals',
    'Gujarat Titans',
    'Royal Challengers Bangalore'
]

playoff_df = df[
    df['batting_team'].isin(playoff_teams)
]
# Retired / inactive players to remove
retired_players = [
    'AB de Villiers',
    'CH Gayle',
    'SK Raina',
    'SL Malinga',
    'Harbhajan Singh',
    'A Mishra',
    'DJ Bravo',
    'PP Chawla',
    'AD Russell'
]

# Strike Rate Race (only playoff teams)
strike_rate_df = (
    playoff_df.groupby('batter')
    .agg(
        runs=('runs_batter', 'sum'),  # <--- CHANGED TO runs_batter
        balls=('ball', 'count')
    )
)

# Remove low-run players
strike_rate_df = strike_rate_df[
    strike_rate_df['runs'] >= 500
]

# Remove retired players
strike_rate_df = strike_rate_df[
    ~strike_rate_df.index.isin(retired_players)
]

# Calculate strike rate
strike_rate_df['strike_rate'] = (
    strike_rate_df['runs'] / strike_rate_df['balls']
) * 100

# Top strike rates
strike_rate_df = strike_rate_df.sort_values(
    by='strike_rate',
    ascending=False
).head(10)

print("\nPlayoff Teams Strike Rate Leaders\n")
print(strike_rate_df)

orange_cap = (
    playoff_df.groupby('batter')
    .agg(
        runs=('runs_batter', 'sum'),
        balls=('ball', 'count')
    )
)

orange_cap['strike_rate'] = (
    orange_cap['runs'] /
    orange_cap['balls']
) * 100

orange_cap = orange_cap.sort_values(
    by='runs',
    ascending=False
).head(10)

print("\nPlayoff Teams - Orange Cap Race\n")
print(orange_cap)

wickets_df = playoff_df[
    playoff_df['wicket_kind'].notna()
]

purple_cap = (
    wickets_df.groupby('bowler')
    .agg(
        wickets=('wicket_kind', 'count')
    )
    .sort_values(by='wickets', ascending=False)
    .head(10)
)

print("\nPlayoff Teams - Purple Cap Race\n")
print(purple_cap)

strike_rate_df = (
    playoff_df.groupby('batter')
    .agg(
        runs=('runs_batter', 'sum'),
        balls=('ball', 'count')
    )
)

# minimum balls filter
# Strike Rate Race (Only Playoff Teams)

strike_rate = (
    playoff_df.groupby('batter')
    .agg(
        runs=('runs_batter', 'sum'),
        balls=('ball', 'count')
    )
)

# minimum runs filter

# Strike Rate Race (only playoff teams)
strike_rate_df = (
    playoff_df.groupby('batter')
    .agg(
        runs=('runs_batter', 'sum'),
        balls=('ball', 'count')
    )
)

# ==============================================================================
# 5. MATCH OUTCOME PREDICTION (Machine Learning)
# ==============================================================================
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

print("\n--- Starting Match Outcome Prediction Training ---\n")

# 1. Collapse the ball-by-ball data into one row per unique match
match_df = df.drop_duplicates(subset=['match_id']).copy()

# 2. Select columns that are actually known BEFORE the match happens
features = ['team1', 'team2', 'toss_winner', 'toss_decision', 'venue']
target = 'winner'

# Drop any rows missing these crucial prediction columns
predict_data = match_df[features + [target]].dropna()

# 3. Convert text data (teams, venues) into numbers so the ML model can read it
encoders = {}
for col in features + [target]:
    le = LabelEncoder()
    predict_data[col] = le.fit_transform(predict_data[col].astype(str))
    encoders[col] = le  # Saves the encoder for future use

# 4. Separate your inputs (X) from what you want to predict (y)
X = predict_data[features]
y = predict_data[target]

# 5. Split data: 80% to train the model, 20% to test its accuracy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Initialize and train the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7. Evaluate how well your model predicts the outcomes
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model Training Complete!")
print(f"Match Outcome Prediction Accuracy: {accuracy * 100:.2f}%")

# ==============================================================================
# 6. IPL 2026 GRAND FINALS OUTCOME PREDICTION
# ==============================================================================
print("\n" + "="*55)
print("         🏆 IPL 2026 GRAND FINALS SIMULATION 🏆")
print("="*55)

# 1. Define our target matchup parameters
final_match = {
    'team1': 'Royal Challengers Bangalore',
    'team2': 'Gujarat Titans',
    'toss_winner': 'Gujarat Titans',
    'toss_decision': 'field',
    'venue': 'Narendra Modi Stadium'
}

# Helper function to find closest matching encoder label to prevent crashes
def get_safe_encoded_value(col_name, value, encoder):
    known_classes = encoder.classes_
    if value in known_classes:
        return encoder.transform([value])[0]
    
    # Check for partial string matches (case insensitive)
    for cls in known_classes:
        if value.lower() in cls.lower() or cls.lower() in value.lower():
            return encoder.transform([cls])[0]
            
    # Fallback to the first class in the encoder if no matches found
    return encoder.transform([known_classes[0]])[0]

# 2. Encode matching features using our safety helper
encoded_match = {}
for col in features:
    val = final_match[col]
    encoded_match[col] = get_safe_encoded_value(col, val, encoders[col])

# Convert into DataFrame format
final_df = pd.DataFrame([encoded_match])

# 3. Predict the Winner Name
predicted_winner_code = model.predict(final_df)[0]
predicted_winner = encoders['winner'].inverse_transform([predicted_winner_code])[0]

# 4. Calculate Individual Win Probabilities
try:
    probabilities = model.predict_proba(final_df)[0]
    classes = model.classes_
    team_probs = {}
    
    for idx, prob in enumerate(probabilities):
        team_name = encoders['winner'].inverse_transform([classes[idx]])[0]
        team_probs[team_name] = prob

    t1 = final_match['team1']
    t2 = final_match['team2']
    t1_prob = team_probs.get(t1, 0.0) * 100
    t2_prob = team_probs.get(t2, 0.0) * 100
    
    # Fallback helper for partial class names
    if t1_prob == 0 and t2_prob == 0:
        for t, p in team_probs.items():
            if t1[:10].lower() in t.lower():
                t1_prob = p * 100
            elif t2[:10].lower() in t.lower():
                t2_prob = p * 100
except Exception:
    t1_prob, t2_prob = 50.0, 50.0  # Fallback if probability array structure varies

# 5. Output Clean Prediction Report
print(f"Matchup:       {final_match['team1']} vs {final_match['team2']}")
print(f"Venue:         {final_match['venue']}")
print(f"Toss Winner:   {final_match['toss_winner']} elects to {final_match['toss_decision']} first")
print("-" * 55)
print(f"🤖 Win Probabilities:")
print(f"  • {final_match['team1']}: {t1_prob:.1f}%")
print(f"  • {final_match['team2']}: {t2_prob:.1f}%")
print("-" * 55)
print(f"🔮 PREDICTED IPL CHAMPION:  🏆  {predicted_winner.upper()}  🏆")
print("="*55 + "\n")