# Install libraries
!pip install xgboost -q

# Import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

print("✅ Libraries loaded!")

# Load CSV
df = pd.read_csv('final_table.csv')
df.columns = df.columns.str.strip()

# Show data
print("📊 Data Preview:")
print(df.head())
print(f"\n📋 Columns: {df.columns.tolist()}")
print(f"📊 Total rows: {len(df)}")

# Filter Pakistan
pakistan = df[df['country'] == 'Pakistan'].copy()
pakistan = pakistan.sort_values('year')

print("🇵🇰 Pakistan Data:")
print(pakistan[['year', 'gdp', 'population', 'internet_users']].tail(10))

# Create lag features for time series
pakistan['gdp_lag1'] = pakistan['gdp'].shift(1)
pakistan['gdp_lag2'] = pakistan['gdp'].shift(2)
pakistan['gdp_lag3'] = pakistan['gdp'].shift(3)
pakistan['pop_growth'] = pakistan['population'].pct_change()
pakistan['internet_change'] = pakistan['internet_users'].diff()

# Drop NaN rows
pakistan_clean = pakistan.dropna()

print(f"\n✅ Clean data: {len(pakistan_clean)} rows")
print(pakistan_clean[['year', 'gdp', 'gdp_lag1', 'pop_growth']].head(10))

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# Prepare data
X = pakistan[['year']].values
y = pakistan['gdp'].values

# Create polynomial features (degree=2 for curve)
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

# Train model
print("🤖 Training Polynomial Regression model...")
model = LinearRegression()
model.fit(X_poly, y)

# Predictions
y_pred = model.predict(X_poly)

# Metrics
r2 = r2_score(y, y_pred)
mae = mean_absolute_error(y, y_pred)
rmse = np.sqrt(mean_squared_error(y, y_pred))

print("\n📊 MODEL PERFORMANCE:")
print(f"   R² Score: {r2:.4f} ({r2*100:.1f}%)")
print(f"   MAE: {mae/1e9:.2f} Billion USD")
print(f"   RMSE: {rmse/1e9:.2f} Billion USD")

# Plot
plt.figure(figsize=(14, 6))
plt.scatter(pakistan['year'], y/1e9, color='#00D4FF', s=80, label='Actual GDP', zorder=5)
plt.plot(pakistan['year'], y_pred/1e9, color='#FF6B6B', linewidth=2.5, label='Predicted GDP')
plt.title('Pakistan GDP: Actual vs Predicted (Polynomial Regression)', fontsize=16, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('GDP (Billions USD)', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Forecast next 30 years
future_years = np.array(range(2024, 2054)).reshape(-1, 1)
future_poly = poly.transform(future_years)
forecast_values = model.predict(future_poly)

# Create forecast dataframe
forecast_df = pd.DataFrame({
    'year': range(2024, 2054),
    'predicted_gdp': forecast_values
})
forecast_df.set_index('year', inplace=True)

print("🔮 GDP Forecast (2024-2053):")
print(forecast_df.head(10))

# Plot
plt.figure(figsize=(16, 7))

# Historical
plt.plot(pakistan['year'], pakistan['gdp']/1e9, marker='o',
         label='Historical GDP', color='#00D4FF', linewidth=2.5, markersize=6)

# Forecast
plt.plot(forecast_df.index, forecast_df['predicted_gdp']/1e9, marker='s',
         label='Forecasted GDP', color='#FFD700', linewidth=2.5, markersize=6, linestyle='--')

# Divider
plt.axvline(x=2023, color='white', linestyle=':', alpha=0.5, linewidth=2)
plt.axvspan(2024, 2053, alpha=0.1, color='yellow')

plt.title('Pakistan GDP: Historical & Forecast (2024-2053)', fontsize=16, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('GDP (Billions USD)', fontsize=12)
plt.legend(fontsize=11, loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(f"\n📈 GDP in 2030: ${forecast_df.iloc[6]['predicted_gdp']/1e9:.2f} Billion")
print(f"📈 GDP in 2040: ${forecast_df.iloc[16]['predicted_gdp']/1e9:.2f} Billion")
print(f"📈 GDP in 2053: ${forecast_df.iloc[-1]['predicted_gdp']/1e9:.2f} Billion")

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('final_table.csv')
df.columns = df.columns.str.strip()

# Countries to forecast
countries = ['Pakistan', 'India', 'China', 'United States', 'Bangladesh']

# Store all results
all_forecasts = []
all_metrics = []

for country_name in countries:
    print(f"\n🤖 Processing: {country_name}")

    # Filter & sort
    country_data = df[df['country'] == country_name].copy()
    country_data = country_data.sort_values('year')

    # Features
    X = country_data[['year']].values
    y = country_data['gdp'].values

    # Train model
    poly = PolynomialFeatures(degree=2)
    model = LinearRegression()
    model.fit(poly.fit_transform(X), y)
    y_pred = model.predict(poly.fit_transform(X))

    # Metrics
    r2 = r2_score(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))

    print(f"   R²: {r2:.4f} | MAE: ${mae/1e9:.1f}B | RMSE: ${rmse/1e9:.1f}B")

    # Store metrics
    all_metrics.append({
        'Country': country_name,
        'R²_Score': round(r2, 4),
        'MAE_Billions': round(mae/1e9, 2),
        'RMSE_Billions': round(rmse/1e9, 2)
    })

    # Add historical data
    for i, row in country_data.iterrows():
        all_forecasts.append({
            'Country': country_name,
            'Year': row['year'],
            'GDP': row['gdp'],
            'Type': 'Historical'
        })

    # Forecast 30 years
    future_years = np.array(range(2024, 2054)).reshape(-1, 1)
    forecast_values = model.predict(poly.transform(future_years))

    for i, year in enumerate(range(2024, 2054)):
        all_forecasts.append({
            'Country': country_name,
            'Year': year,
            'GDP': forecast_values[i],
            'Type': 'Forecasted'
        })

# Save files
pd.DataFrame(all_forecasts).to_csv('all_countries_forecast.csv', index=False)
pd.DataFrame(all_metrics).to_csv('all_metrics.csv', index=False)

print("\n✅ All files saved!")
print("\n📊 Final Metrics:")
print(pd.DataFrame(all_metrics).to_string(index=False))

