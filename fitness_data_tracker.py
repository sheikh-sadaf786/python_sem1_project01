"""
PS 70 - Fitness Data Tracker
----------------------------
Records daily fitness data (steps and calories burned), checks whether the
daily step goal is achieved, calculates BMI and shows a weekly summary with a
Matplotlib bar chart of the daily steps.

Rules
  * daily goal = 10000 steps (reaching exactly 10000 counts as achieved)
  * BMI = weight (kg) / height (m) squared
        below 18.5 Underweight | 18.5 to 24.9 Normal
        25 to 29.9 Overweight  | 30 and above Obese
  * records are kept in Python lists (steps, calories); days are numbered
    Day 1, Day 2, ...

Run from the console:
    python fitness_data_tracker.py
"""

import math

try:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
except ImportError:  # the rest of the program still works without it
    plt = None

DAILY_GOAL = 10000


# --------------------------------------------------------------------------
# Input validation
# --------------------------------------------------------------------------
def parse_steps(text):
    """Return steps as an int, or None if not a non-negative whole number."""
    text = text.strip()
    if text.isascii() and text.isdigit():
        return int(text)
    return None


def parse_number(text, allow_zero):
    """Return a finite float, or None if the text is not a valid number.

    allow_zero=True  -> accepts 0 and above   (calories)
    allow_zero=False -> accepts above 0 only  (weight, height)
    """
    try:
        value = float(text)
    except ValueError:
        return None
    if not math.isfinite(value):  # rejects 'nan' and 'inf'
        return None
    if value < 0 or (value == 0 and not allow_zero):
        return None
    return value


def format_number(value):
    """Show 1200.0 as '1200' but keep real decimals such as 1200.5."""
    return f"{value:.2f}".rstrip("0").rstrip(".")


# --------------------------------------------------------------------------
# Calculations
# --------------------------------------------------------------------------
def goal_percentage(steps):
    """Percentage of the daily step goal that was completed."""
    return steps / DAILY_GOAL * 100


def average_steps(steps_list):
    """Average steps per day."""
    return sum(steps_list) / len(steps_list)


def total_calories(calories_list):
    """Total calories burned."""
    return sum(calories_list)


def best_day(steps_list):
    """Return (day_number, steps) of the day with the most steps."""
    best_steps = max(steps_list)
    return steps_list.index(best_steps) + 1, best_steps  # first one on a tie


def goal_days(steps_list):
    """Number of days on which the step goal was achieved."""
    return sum(1 for steps in steps_list if steps >= DAILY_GOAL)


def calculate_bmi(weight_kg, height_m):
    """BMI = weight (kg) / height (m) squared, rounded to 2 decimals."""
    return round(weight_kg / (height_m ** 2), 2)


def bmi_category(bmi):
    """Return the BMI category name."""
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


# --------------------------------------------------------------------------
# Menu actions
# --------------------------------------------------------------------------
def add_record(steps_list, calories_list):
    """Ask for one day's steps and calories, validate and store them."""
    steps_text = input("Steps: ")
    calories_text = input("Calories: ")

    steps = parse_steps(steps_text)
    calories = parse_number(calories_text, allow_zero=True)

    errors = []
    if steps is None:
        errors.append("Invalid steps. Enter a non-negative whole number.")
    if calories is None:
        errors.append("Invalid calories. Enter a non-negative number.")
    if errors:
        print(*errors, sep="\n")
        print("Record not saved.")
        return

    steps_list.append(steps)
    calories_list.append(calories)

    day = len(steps_list)
    achieved = "Yes" if steps >= DAILY_GOAL else "No"
    print(
        f"Record saved for Day {day}. Goal achieved: {achieved} "
        f"({goal_percentage(steps):.2f}% of goal)"
    )


def show_summary(steps_list, calories_list):
    """Print the weekly summary."""
    if not steps_list:
        print("No records yet. Add a record first.")
        return

    day, steps = best_day(steps_list)
    print(
        f"Average steps: {average_steps(steps_list):.2f} | "
        f"Total calories: {format_number(total_calories(calories_list))} | "
        f"Best day: Day {day} ({steps} steps) | "
        f"Goal days: {goal_days(steps_list)}/{len(steps_list)}"
    )


def show_bmi():
    """Ask for weight and height, validate and print BMI with its category."""
    weight_text = input("Weight (kg): ")
    height_text = input("Height (m): ")

    weight = parse_number(weight_text, allow_zero=False)
    height = parse_number(height_text, allow_zero=False)

    errors = []
    if weight is None:
        errors.append("Invalid weight. Enter a positive number.")
    if height is None:
        errors.append("Invalid height. Enter a positive number.")
    if errors:
        print(*errors, sep="\n")
        print("BMI not calculated.")
        return

    bmi = calculate_bmi(weight, height)
    print(f"BMI: {bmi:.2f} | Category: {bmi_category(bmi)}")


def build_chart(steps_list):
    """Create the 'Daily Steps' bar chart (with the 10000-step goal line)."""
    days = [f"Day {i}" for i in range(1, len(steps_list) + 1)]
    colors = ["seagreen" if s >= DAILY_GOAL else "steelblue" for s in steps_list]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(days, steps_list, color=colors)
    ax.bar_label(bars, padding=3)
    ax.axhline(DAILY_GOAL, color="crimson", linestyle="--", linewidth=1.5)

    ax.set_title("Daily Steps")
    ax.set_xlabel("Day")
    ax.set_ylabel("Steps")
    ax.set_ylim(0, max(max(steps_list), DAILY_GOAL) * 1.15)
    ax.legend(
        handles=[
            Patch(facecolor="seagreen", label="Goal achieved"),
            Patch(facecolor="steelblue", label="Below goal"),
            Line2D([0], [0], color="crimson", linestyle="--",
                   label=f"Goal ({DAILY_GOAL} steps)"),
        ],
        loc="upper right",
    )
    fig.tight_layout()
    return fig


def show_chart(steps_list):
    """Display the bar chart of the daily steps."""
    if not steps_list:
        print("No records yet. Add a record first.")
        return
    if plt is None:
        print("Matplotlib is not installed. Install it with: pip install matplotlib")
        return

    build_chart(steps_list)
    print("Bar chart 'Daily Steps' displayed")
    plt.show()


# --------------------------------------------------------------------------
# Main program
# --------------------------------------------------------------------------
def print_menu():
    print()
    print("===== Fitness Data Tracker =====")
    print("1. Add record")
    print("2. Summary")
    print("3. BMI")
    print("4. Chart")
    print("5. Exit")


def main():
    steps_list = []      # steps for Day 1, Day 2, ...
    calories_list = []   # calories burned for Day 1, Day 2, ...

    try:
        while True:
            print_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                add_record(steps_list, calories_list)
            elif choice == "2":
                show_summary(steps_list, calories_list)
            elif choice == "3":
                show_bmi()
            elif choice == "4":
                show_chart(steps_list)
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Choose 1 to 5.")
    except (EOFError, KeyboardInterrupt):  # input ended or Ctrl+C
        print()


if __name__ == "__main__":
    main()
