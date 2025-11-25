# -----------------------------------------------------------
# GradeBook Analyzer
# Author: Ankit Kumar Mishra
# Date: 08-nov-2025
# -----------------------------------------------------------

import csv
import statistics

def calculate_average(marks_dict):
    return sum(marks_dict.values()) / len(marks_dict)

def calculate_median(marks_dict):
    return statistics.median(marks_dict.values())

def find_max_score(marks_dict):
    return max(marks_dict.values())

def find_min_score(marks_dict):
    return min(marks_dict.values())

def assign_grades(marks_dict):
    grades = {}
    for name, mark in marks_dict.items():
        if mark >= 90:
            grades[name] = "A"
        elif mark >= 80:
            grades[name] = "B"
        elif mark >= 70:
            grades[name] = "C"
        elif mark >= 60:
            grades[name] = "D"
        else:
            grades[name] = "F"
    return grades

def load_csv(filename):
    marks = {}
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        next(reader)  # skip header if present
        for row in reader:
            if len(row) >= 2:
                marks[row[0]] = float(row[1])
    return marks

def manual_input():
    marks = {}
    n = int(input("Enter number of students: "))
    for _ in range(n):
        name = input("Enter student name: ")
        score = float(input(f"Enter marks for {name}: "))
        marks[name] = score
    return marks

def display_table(marks, grades):
    print("\nName\t\tMarks\tGrade")
    print("-" * 30)
    for name in marks:
        print(f"{name:<10}\t{marks[name]:<6}\t{grades[name]}")
    print("-" * 30)

def main():
    print("=== GradeBook Analyzer ===")
    while True:
        print("\n1. Manual Input")
        print("2. Load from CSV")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            marks = manual_input()
        elif choice == '2':
            filename = input("Enter CSV filename (with .csv): ")
            marks = load_csv(filename)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
            continue

        # Stats
        print("\n--- Statistics ---")
        print(f"Average: {calculate_average(marks):.2f}")
        print(f"Median: {calculate_median(marks):.2f}")
        print(f"Highest: {find_max_score(marks)}")
        print(f"Lowest: {find_min_score(marks)}")

        # Grades
        grades = assign_grades(marks)

        # Grade distribution
        distribution = {g: list(grades.values()).count(g) for g in set(grades.values())}
        print("\n--- Grade Distribution ---")
        for grade, count in distribution.items():
            print(f"{grade}: {count}")

        # Pass/fail
        passed = [name for name, mark in marks.items() if mark >= 40]
        failed = [name for name, mark in marks.items() if mark < 40]
        print(f"\nPassed ({len(passed)}): {', '.join(passed)}")
        print(f"Failed ({len(failed)}): {', '.join(failed)}")

        # Results table
        display_table(marks, grades)

        again = input("\nRun again? (y/n): ")
        if again.lower() != 'y':
            break

if __name__ == "__main__":
    main()