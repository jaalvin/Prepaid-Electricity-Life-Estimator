import math
from typing import List, Tuple
import matplotlib.pyplot as plt

# Sample Input Data
BALANCE_GHS = 50.0             # Prepaid credit in Ghana Cedis
COST_PER_KWH = 1.6             # GHS/kWh pricing

# List of appliances with (name, power in Watts, hours used daily)
APPLIANCES = [
    ("Fan", 70, 8),
    ("Fridge", 200, 24),
    ("Bulb", 10, 6),
    ("TV", 100, 5),
]
# Historical usage for interpolation forecast (Day, kWh used)
HISTORICAL_DAYS = [1, 2, 3, 4, 5]
HISTORICAL_USAGE = [5.8, 6.0, 6.1, 6.3, 6.4]

# Use last 3 days for Newton interpolation to improve extrapolation
x_used = HISTORICAL_DAYS[-3:]
y_used = HISTORICAL_USAGE[-3:]

# Numerical Method 1: Trapezoidal Integration
def compute_daily_kwh(appliances: List[Tuple[str, float, float]]) -> float:
    #Estimate total daily kWh used using a simple sum (∑Power × Time / 1000).
    total_kwh = sum((power * hours) / 1000 for _, power, hours in appliances)
    return total_kwh

# Numerical Method 2: Newton's Divided Difference Interpolation
def newton_divided_diff(x, y):
    """
    Build divided difference table for Newton's interpolation.
    Returns list of coefficients for interpolation polynomial.
    """
    n = len(x)
    coef = list(y)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (x[i] - x[i - j])
    return coef

def newton_interpolation(x_data, y_data, target_x):
    #Evaluate the Newton interpolating polynomial at a target x value.
    coef = newton_divided_diff(x_data, y_data)
    n = len(coef)
    result = coef[-1]
    for i in range(n - 2, -1, -1):
        result = result * (target_x - x_data[i]) + coef[i]
    return max(0, round(result, 2))

# Numerical Method 3: Root Finding (Bisection Method)
def estimate_days_remaining(balance_ghs, daily_cost_func, max_days=30):
    #Estimate when balance runs out by solving: balance - daily_cost(days) = 0
    def f(t):
        return balance_ghs - daily_cost_func(t)

    a, b = 0, max_days
    tol = 0.01
    while b - a > tol:
        mid = (a + b) / 2
        if f(mid) * f(a) < 0:
            b = mid
        else:
            a = mid
    return (a + b) / 2

# Numerical Method 4: Golden Section Search (Optimization)
def golden_section_search(f, a, b, tol=1e-2):
    #Find minimum of unimodal function f in [a, b]
    gr = (math.sqrt(5) + 1) / 2
    c = b - (b - a) / gr
    d = a + (b - a) / gr
    while abs(c - d) > tol:
        if f(c) < f(d):
            b = d
        else:
            a = c
        c = b - (b - a) / gr
        d = a + (b - a) / gr
    return (b + a) / 2

# Core Logic
daily_kwh = compute_daily_kwh(APPLIANCES)
daily_cost = daily_kwh * COST_PER_KWH

# Interpolated forecast for next 5 days
forecasted_usage = [newton_interpolation(x_used, y_used, d) for d in range(6, 11)]

# Define cost function over t days
def cumulative_cost(t):
    return daily_cost * t  # Could integrate over forecast for more realism

# Estimate how many days the balance lasts using root-finding
estimated_days = estimate_days_remaining(BALANCE_GHS, cumulative_cost)

# Optimize reduction in appliance usage to extend days
def reduction_to_life(r):
    reduced_daily = daily_kwh * (1 - r)
    return -BALANCE_GHS / (reduced_daily * COST_PER_KWH)
optimal_reduction = golden_section_search(reduction_to_life, 0.0, 0.5)

# Output
print("Estimated Daily kWh:", round(daily_kwh, 2))
print("Estimated Cost/Day (GHS):", round(daily_cost, 2))
print("Forecasted Usage (kWh) for Days 6-10:", forecasted_usage)
print("Estimated Days Until Balance Exhaustion:", round(estimated_days, 1))
print("Optimal Appliance Reduction (for extended life):", round(optimal_reduction * 100, 1), "%")

# Plotting Forecast
plt.plot(HISTORICAL_DAYS, HISTORICAL_USAGE, 'bo-', label="Historical")
plt.plot(list(range(6, 11)), forecasted_usage, 'ro--', label="Forecast")
plt.axhline(y=daily_kwh, color='green', linestyle='--', label="Current Usage Level")
plt.xlabel("Day")
plt.ylabel("kWh")
plt.title("Electricity Usage Forecast (Newton Interpolation)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()