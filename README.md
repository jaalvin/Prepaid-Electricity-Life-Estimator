# Prepaid Electricity Life Estimator

A Python-based smart prepaid electricity life estimator and usage forecaster.
It combines **numerical methods** like interpolation, root-finding, integration, and optimization to estimate prepaid electricity lifespan, forecast usage, and recommend optimal reduction strategies for efficient power management.

---

## Project Overview

Prepaid electricity meters are widely used, but users often struggle to predict how long their balance will last. This project provides:

* Forecast of electricity usage based on recent consumption history.
* Estimation of how many days remain before balance depletion.
* Optimal percentage reduction in appliance usage to extend balance life.
* Graphical visualization of consumption trends.

---

## Problem Statement

Given daily usage data and the current prepaid balance, the system estimates:

* Average daily consumption in kWh.
* Forecasted usage for upcoming days.
* Number of days until credit depletion.
* Optimal reduction percentage to extend usage time.

---

## Numerical Methods Applied

* **Newton's Divided Difference Interpolation**

  * Forecasts future electricity usage based on past data.
  * Builds a polynomial approximation for Days 6–10.

* **Bisection Method (Root-Finding)**

  * Estimates the day prepaid balance runs out by solving:
    `TotalCost(x) - Balance = 0`.

* **Golden Section Search (Optimization)**

  * Determines optimal percentage reduction in electricity usage.

* **Trapezoidal Rule (Approximate Integration)**

  * Estimates cumulative consumption cost over forecasted days.

---

## Algorithm Design

**Inputs:**

* Past usage data (kWh per day).
* Current prepaid balance.
* Unit cost per kWh.
* Appliance power ratings and usage hours.

**Steps:**

1. Estimate average daily consumption.
2. Forecast usage for the next 5 days.
3. Compute cumulative costs until balance depletion.
4. Apply bisection method to estimate balance exhaustion day.
5. Use golden section search to find optimal usage reduction.
6. Plot results for visualization.

---

## Sample Simulation

**Input:**

* Past 5-day usage: `[5.5, 6.1, 5.8, 6.4, 5.9] kWh`
* Unit cost: `GHS 1.60/kWh`
* Prepaid balance: `GHS 50.00`

**Output:**

* Estimated Daily kWh: `5.92`
* Estimated Cost/Day: `GHS 9.47`
* Forecasted Usage (Days 6–10): `[6.2, 5.5, 4.1, 1.8, 0.0]`
* Estimated Days Until Exhaustion: `~5.3 days`
* Optimal Appliance Reduction: `~48.6%`

---

## Graphical Representation

The program generates plots that show:

* Historical daily usage.
* Forecasted values (Days 6–10).
* Current usage threshold for comparison.

---

## Tools & Libraries

* **Language:** Python 3.13
* **Libraries:**

  * `math`
  * `matplotlib`

---

## Implementation

```python
# Core logic snippet
daily_kwh = compute_daily_kwh(APPLIANCES)
forecasted_usage = [newton_interpolation(x_used, y_used, d) for d in range(6, 11)]
estimated_days = estimate_days_remaining(BALANCE_GHS, cumulative_cost)
optimal_reduction = golden_section_search(reduction_to_life, 0.0, 0.5)
```

Run the script to get:

* Daily consumption estimate
* Days left until balance depletion
* Suggested appliance reduction percentage
* Forecast plots

