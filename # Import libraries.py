# Import libraries
import pandas as pd

# Load the dataset (ensure this file is in your working directory)
df = pd.read_csv("owid-covid-data.csv")

# Explore structure
print(df.columns)
df.head()


# Check missing values
df.isnull().sum()


# Select countries of interest
countries = ["Kenya", "United States", "India"]
df = df[df['location'].isin(countries)]

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Drop rows with missing total_cases or total_deaths
df = df.dropna(subset=['total_cases', 'total_deaths'])

# Fill or interpolate missing values
df.fillna(method='ffill', inplace=True)


import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set(style="whitegrid")

# Plot total cases over time
plt.figure(figsize=(12, 6))
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['total_cases'], label=country)
plt.title("Total COVID-19 Cases Over Time")
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.legend()
plt.show()


# Plot total deaths over time
plt.figure(figsize=(12, 6))
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['total_deaths'], label=country)
plt.title("Total COVID-19 Deaths Over Time")
plt.xlabel("Date")
plt.ylabel("Total Deaths")
plt.legend()
plt.show()


# Compare daily new cases
plt.figure(figsize=(12, 6))
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['new_cases'], label=country)
plt.title("Daily New Cases Comparison")
plt.xlabel("Date")
plt.ylabel("New Cases")
plt.legend()
plt.show()


# Calculate and plot death rate
df['death_rate'] = df['total_deaths'] / df['total_cases']

plt.figure(figsize=(12, 6))
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['death_rate'], label=country)
plt.title("COVID-19 Death Rate Over Time")
plt.xlabel("Date")
plt.ylabel("Death Rate")
plt.legend()
plt.show()


# Plot total vaccinations over time
plt.figure(figsize=(12, 6))
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['total_vaccinations'], label=country)
plt.title("Total Vaccinations Over Time")
plt.xlabel("Date")
plt.ylabel("Total Vaccinations")
plt.legend()
plt.show()


# % Vaccinated (people_vaccinated_per_hundred)
plt.figure(figsize=(12, 6))
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['people_vaccinated_per_hundred'], label=country)
plt.title("People Vaccinated per Hundred")
plt.xlabel("Date")
plt.ylabel("% of Population")
plt.legend()
plt.show()


import plotly.express as px

# Get the latest date
latest_date = df['date'].max()

# Prepare data
latest_data = df[df['date'] == latest_date]
latest_data = latest_data[['iso_code', 'location', 'total_cases']]

# Drop rows without iso_code
latest_data = latest_data.dropna(subset=['iso_code'])

# Choropleth
fig = px.choropleth(latest_data,
                    locations='iso_code',
                    color='total_cases',
                    hover_name='location',
                    title=f'COVID-19 Total Cases by Country as of {latest_date.date()}',
                    color_continuous_scale='Reds')
fig.show()
