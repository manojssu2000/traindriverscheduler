# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 12:04:11 2025

@author: Manoj
"""

import numpy as np
import matplotlib.pyplot as plt
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD

# Define Problem
model = LpProblem("Shift_Scheduling", LpMinimize)

# Decision Variables (Binary)
drivers = [f"D{i}" for i in range(1, 1501)]  # Sample 10 drivers
shifts = ["Shift 1", "Shift 2", "Shift 3", "Shift 4", "Shift 5"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

x = {
    (d, day, shift): LpVariable(f"x_{d}_{day}_{shift}", cat="Binary")
    for d in drivers
    for day in days
    for shift in shifts
}

# Constraint: Each shift should have at least 97 drivers (example)
for day in days:
    for shift in shifts:
        model += lpSum(x[d, day, shift] for d in drivers) >= 97, f"Shift_Coverage_{day}_{shift}"

# Constraint: Each driver works at most one shift per day
for d in drivers:
    for day in days:
        model += lpSum(x[d, day, shift] for shift in shifts) <= 1, f"One_Shift_Per_Day_{d}_{day}"

# Solve Model
model.solve(PULP_CBC_CMD(msg=0))

# Extract Solution
solutions = [(d, day, shift) for d in drivers for day in days for shift in shifts if x[d, day, shift].varValue == 1]

# Convert to Plot Data
day_shift_map = {day: i for i, day in enumerate(days)}
shift_map = {shift: i for i, shift in enumerate(shifts)}
plot_data = [(day_shift_map[day], shift_map[shift]) for _, day, shift in solutions]

# Plot Integer Solutions
fig, ax = plt.subplots(figsize=(8, 6))
x_vals, y_vals = zip(*plot_data)
ax.scatter(x_vals, y_vals, color="blue", label="Integer Solutions")

# Constraint Line (Example Linear Bound)
x_line = np.linspace(0, 6, 100)
y_line = 6 - x_line  # Example constraint equation
ax.plot(x_line, y_line, 'r--', label="Linear Programming Boundary")

# Highlight Optimal Integer Solution
opt_x, opt_y = min(plot_data)
ax.scatter(opt_x, opt_y, color="red", s=100, edgecolors="black", label="Optimal Integer Solution")

# Labels and Titles
ax.set_xticks(range(len(days)))
ax.set_xticklabels(days, rotation=45)
ax.set_yticks(range(len(shifts)))
ax.set_yticklabels(shifts)
ax.set_xlabel("Days of the Week")
ax.set_ylabel("Shifts")
ax.set_title("Optimal Shift Allocation")
ax.legend()

# Show Plot
plt.grid(True)
plt.show()
