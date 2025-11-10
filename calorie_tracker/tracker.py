"""
---------------------------------------------------
Project: Daily Calorie Tracker CLI
Author: Ankit Kumar Mishra
Date: 08/11/2025
Course: Programming for Problem Solving using Python
----------------------------------------------------
Description:
A simple command-line calorie tracker where users can log
their meals, track total calories, compare with a daily limit,
and optionally save the session report to a text file.
----------------------------------------------------
"""

import datetime

# --------------------------
# Task 1: Setup & Introduction
# --------------------------
print("----------------------------------------------------")
print("Welcome to the Daily Calorie Tracker CLI!")
print("Track your daily calorie intake and compare it to your goal.")
print("----------------------------------------------------\n")

# --------------------------
# Task 2: Input & Data Collection
# --------------------------
meals = []
calories = []

num_meals = int(input("How many meals would you like to log today? "))

for i in range(num_meals):
    meal_name = input(f"\nEnter the name of meal #{i+1}: ")
    cal_amount = float(input(f"Enter calories for {meal_name}: "))
    meals.append(meal_name)
    calories.append(cal_amount)

# --------------------------
# Task 3: Calorie Calculations
# --------------------------
total_calories = sum(calories)
average_calories = total_calories / len(calories)

daily_limit = float(input("\nEnter your daily calorie limit: "))

# --------------------------
# Task 4: Exceed Limit Warning System
# --------------------------
if total_calories > daily_limit:
    status_message = "⚠️ You have exceeded your daily calorie limit!"
else:
    status_message = "✅ You are within your daily calorie limit. Great job!"

# --------------------------
# Task 5: Neatly Formatted Output
# --------------------------
print("\n----------------------------------------------------")
print("             DAILY CALORIE SUMMARY")
print("----------------------------------------------------")
print("Meal Name\t\tCalories")
print("----------------------------------------------------")

for meal, cal in zip(meals, calories):
    print(f"{meal:<15}\t{cal}")

print("----------------------------------------------------")
print(f"Total Calories:\t\t{total_calories}")
print(f"Average per Meal:\t{average_calories:.2f}")
print(f"Calorie Limit:\t\t{daily_limit}")
print(f"Status:\t\t\t{status_message}")
print("----------------------------------------------------")

# --------------------------
# Task 6 (Bonus): Save Session Log to File
# --------------------------
save_choice = input("\nWould you like to save this session report? (yes/no): ").lower()

if save_choice == 'yes':
    filename = "calorie_log.txt"
    with open(filename, "w") as file:
        file.write("DAILY CALORIE TRACKER REPORT\n")
        file.write("----------------------------------------------------\n")
        file.write(f"Date & Time: {datetime.datetime.now()}\n\n")
        file.write("Meal Name\tCalories\n")
        file.write("----------------------------------------------------\n")
        for meal, cal in zip(meals, calories):
            file.write(f"{meal:<15}\t{cal}\n")
        file.write("----------------------------------------------------\n")
        file.write(f"Total Calories:\t{total_calories}\n")
        file.write(f"Average per Meal:\t{average_calories:.2f}\n")
        file.write(f"Calorie Limit:\t{daily_limit}\n")
        file.write(f"Status:\t{status_message}\n")
        file.write("----------------------------------------------------\n")
    print(f"\nSession successfully saved to '{filename}' ✅")
else:
    print("\nSession not saved.")

print("\nThank you for using the Daily Calorie Tracker! 🥗")
