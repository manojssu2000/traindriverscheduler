# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 09:58:13 2025

@author: Manoj
"""

import pandas as pd
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD

# Load driver availability CSV
df_availability = pd.read_csv("driver_availability.csv")

# Extract driver IDs
drivers = df_availability["Driver"].tolist()

# Extract available days as a dictionary {Driver: {Day: 0/1}}
availability = df_availability.set_index("Driver").iloc[:, 1:].to_dict(orient="index")

# Define shift structure
shifts = ["Shift 1", "Shift 2", "Shift 3", "Shift 4", "Shift 5"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Required number of drivers per shift
drivers_per_shift = 97

# Shift length (7 hours)
shift_hours = 7

# Maximum weekly hours per driver (35 hours / 5 shifts max)
max_weekly_hours = 35
max_shifts_per_week = max_weekly_hours // shift_hours  # Max 5 shifts per week

# Define the LP problem
model = LpProblem("Shift_Scheduling", LpMinimize)

# Decision Variables (Binary: 1 = Assigned, 0 = Not Assigned)
x = {
    (d, day, shift): LpVariable(f"x_{d}_{day}_{shift}", cat="Binary")
    for d in drivers
    for day in days
    for shift in shifts
}

# **Constraint 1: Each shift must have at least `drivers_per_shift` drivers**
for day in days:
    for shift in shifts:
        model += (
            lpSum(x[d, day, shift] for d in drivers) >= drivers_per_shift,
            f"Shift_Coverage_{day}_{shift}",
        )

# **Constraint 2: Each driver can only work one shift per day**
for d in drivers:
    for day in days:
        model += (
            lpSum(x[d, day, shift] for shift in shifts) <= 1,
            f"One_Shift_Per_Day_{d}_{day}",
        )

# **Constraint 3: Assign only if driver is available**
for d in drivers:
    for day in days:
        for shift in shifts:
            if availability[d][day] == 0:
                model += x[d, day, shift] == 0

# **Constraint 4: Maximum weekly hours per driver (35 hours / 5 shifts max)**
for d in drivers:
    model += (
        lpSum(x[d, day, shift] * shift_hours for day in days for shift in shifts) <= max_weekly_hours,
        f"Max_Weekly_Hours_{d}",
    )

# **Objective Function: Distribute shifts fairly**
model += lpSum(x[d, day, shift] for d in drivers for day in days for shift in shifts)

# Solve the model
model.solve(PULP_CBC_CMD(msg=0))

# Create an empty dictionary to store shift assignments
output_data = {d: {day: {shift: "?" for shift in shifts} for day in days} for d in drivers}

# Populate the output dictionary with assigned shifts (1 = Assigned, ? = Not Assigned)
for d in drivers:
    for day in days:
        for shift in shifts:
            if x[d, day, shift].varValue == 1:
                output_data[d][day][shift] = "1"  # Assigned shift
            else:
                output_data[d][day][shift] = "0"

# Convert dictionary to DataFrame for structured output
columns = ["Driver"] + [f"{day} {shift}" for day in days for shift in shifts]
formatted_data = []

for d in drivers:
    row = [d] + [output_data[d][day][shift] for day in days for shift in shifts]
    formatted_data.append(row)

df_schedule = pd.DataFrame(formatted_data, columns=columns)

# Save to CSV
df_schedule.to_csv("shift_allocation.csv", index=False)
print("✅ Shift allocation saved to shift_allocation.csv!")
