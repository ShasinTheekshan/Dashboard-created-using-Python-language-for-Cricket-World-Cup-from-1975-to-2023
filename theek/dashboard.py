import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash

# Load the cricket dataset
try:
    df = pd.read_csv("processed_cricket_data.csv")
except FileNotFoundError:
    print("Error: 'processed_cricket_data.csv' not found. Please ensure the file path is correct.")
    exit()

# Check if the necessary columns exist
required_columns = ['team_1', 'team_1_runs', 'team_2', 'team_2_runs', 
                    'match_category', 'world_cup_year', 'winning_team', 
                    'best_batter_1', 'best_batter_1_runs', 'venue']
if not all(col in df.columns for col in required_columns):
    print("Error: The dataset does not contain the required columns. Please check your data preparation.")
    exit()

# Initialize the Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Cricket World Cup Dashboard", style={'textAlign': 'center'}),
    dcc.Tabs([
        # Tab 1: Team Performance
        dcc.Tab(label='Team Performance', children=[
            dcc.Graph(
                id='team-performance',
                figure=px.bar(df, x='team_1', y='team_1_runs', color='team_1',
                              title="Runs Scored by Teams",
                              labels={'team_1': "Team", 'team_1_runs': "Total Runs"})
            )
        ]),

        # Tab 2: Match Outcomes
        dcc.Tab(label='Match Outcomes', children=[
            dcc.Graph(
                id='match-outcomes',
                figure=px.pie(df, names='match_category', title="Match Outcomes Distribution")
            )
        ]),

        # Tab 3: Yearly Trends
        dcc.Tab(label='Yearly Trends', children=[
            dcc.Graph(
                id='yearly-trends',
                figure=px.line(df, x='world_cup_year', y='team_1_runs', color='team_1',
                               title="Runs Scored Over the Years",
                               labels={'world_cup_year': "Year", 'team_1_runs': "Runs Scored"})
            )
        ]),

        # Tab 4: Winning Teams
        dcc.Tab(label='Winning Teams', children=[
            dcc.Graph(
                id='winning-teams',
                figure=px.bar(df, x='winning_team', title="Matches Won by Teams",
                              labels={'winning_team': "Winning Team"}, color='winning_team')
            )
        ]),

        # Tab 5: Top Batters
        dcc.Tab(label='Top Batters', children=[
            dcc.Graph(
                id='top-batters',
                figure=px.bar(df.dropna(subset=['best_batter_1', 'best_batter_1_runs']),
                              x='best_batter_1', y='best_batter_1_runs', color='best_batter_1',
                              title="Top Batters and Their Runs",
                              labels={'best_batter_1': "Batter", 'best_batter_1_runs': "Runs"})
            )
        ]),

        # Tab 6: Venue Performance
        dcc.Tab(label='Venue Performance', children=[
            dcc.Graph(
                id='venue-performance',
                figure=px.bar(df, x='venue', color='winning_team',
                              title="Winning Teams by Venue",
                              labels={'venue': "Venue", 'winning_team': "Winning Team"})
            )
        ]),

        # Tab 7: Team Runs Comparison
        dcc.Tab(label='Team Runs Comparison', children=[
            dcc.Graph(
                id='team-runs-comparison',
                figure=px.scatter(df, x='team_1_runs', y='team_2_runs', color='team_1',
                                  title="Team Runs Comparison",
                                  labels={'team_1_runs': "Team 1 Runs", 'team_2_runs': "Team 2 Runs"})
            )
        ]),
    ])
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
