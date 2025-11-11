"""
---------------------------------------------------
Project: Daily Calorie Tracker
Author: Ankit Kumar Mishra
Date: 08/11/2025
Course: Programming for Problem Solving using Python
----------------------------------------------------
Description:
This program helps the user to record daily meals and calories,
check if they are within the daily limit, and save the report.
----------------------------------------------------
"""

import datetime

# -----------------------------
# Introduction
# -----------------------------
print("----------------------------------------------------")
print(" Welcome to the Daily Calorie Tracker! ")
print("----------------------------------------------------")
print("You can record your meals and see your total calories.\n")

# -----------------------------
# Taking input
# -----------------------------
meals = []
calories = []

num = int(input("How many meals did you have today? "))

for i in range(num):
    meal = input(f"\nEnter meal name #{i+1}: ")
    cal = float(input(f"Enter calories for {meal}: "))
    meals.append(meal)
    calories.append(cal)

# -----------------------------
# Calculations
# -----------------------------
total = sum(calories)
avg = total / len(calories)
limit = float(input("\nEnter your daily calorie limit: "))

if total > limit:
    status = "⚠ You have exceeded your daily calorie limit!"
else:
    status = "✅ You are within your daily calorie limit. Great job!"

# -----------------------------
# Display result
# -----------------------------
print("\n----------------------------------------------------")
print("            DAILY CALORIE REPORT")
print("----------------------------------------------------")
print("Meal Name\tCalories")
print("----------------------------------------------------")

for meal, cal in zip(meals, calories):
    print(f"{meal:<15}\t{cal}")

print("----------------------------------------------------")
print(f"Total Calories:\t{total}")
print(f"Average per Meal:\t{avg:.2f}")
print(f"Calorie Limit:\t{limit}")
print(f"Status:\t{status}")
print("----------------------------------------------------")

# -----------------------------
# Save the report (optional)
# -----------------------------
save = input("\nDo you want to save this report? (yes/no): ").lower()

if save == "yes":
    filename = "calorie_log.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write("DAILY CALORIE TRACKER REPORT\n")
        file.write("----------------------------------------------------\n")
        file.write(f"Date & Time: {datetime.datetime.now()}\n\n")
        file.write("Meal Name\tCalories\n")
        for meal, cal in zip(meals, calories):
            file.write(f"{meal:<15}\t{cal}\n")
        file.write("----------------------------------------------------\n")
        file.write(f"Total Calories:\t{total}\n")
        file.write(f"Average per Meal:\t{avg:.2f}\n")
        file.write(f"Calorie Limit:\t{limit}\n")
        file.write(f"Status:\t{status}\n")
        file.write("----------------------------------------------------\n")
    print(f"\nReport saved successfully to '{filename}' ✅")
else:
    print("\nReport not saved.")

print("\nThank you for using the Calorie Tracker! 🥗")
