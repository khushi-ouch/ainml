import json
import os
import numpy as np
from sklearn.linear_model import LinearRegression

DATA_FILE = "data.json"

# Load data
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as file:
        return json.load(file)

# Save data
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Menu
def menu():
    print("\n====== Attendance Tracker (AI Enabled) ======")
    print("1. Add Subject")
    print("2. View Attendance")
    print("3. Get Basic Prediction")
    print("4. AI Prediction (ML)")
    print("5. Exit")

# Add subject
def add_subject(data):
    subject = input("Enter subject name: ")

    try:
        total = int(input("Total classes: "))
        attended = int(input("Attended classes: "))

        if total <= 0:
            print("Total must be greater than 0!")
            return

        if attended > total:
            print("Attended cannot be greater than total!")
            return

        data[subject] = {
            "total": total,
            "attended": attended
        }

        print(f"{subject} added successfully!")

    except:
        print("Invalid input! Enter numbers only.")

# View attendance
def view_attendance(data):
    if not data:
        print("No subjects found!")
        return

    print("\n====== Attendance Summary ======")

    for subject, details in data.items():
        total = details["total"]
        attended = details["attended"]

        percentage = (attended / total) * 100 if total > 0 else 0

        status = "✅ Safe" if percentage >= 75 else "⚠ Low"

        print(f"\nSubject: {subject}")
        print(f"Total: {total}, Attended: {attended}")
        print(f"Attendance: {percentage:.2f}% ({status})")

def prediction(data):
    if not data:
        print("No subjects available!")
        return

    subject = input("Enter subject name: ")

    if subject not in data:
        print("Subject not found!")
        return

    total = data[subject]["total"]
    attended = data[subject]["attended"]

    if total == 0:
        print("No classes conducted yet!")
        return

    percentage = (attended / total) * 100
    print(f"\nCurrent Attendance: {percentage:.2f}%")

    # CASE 1: Already safe → calculate bunk
    if percentage >= 75:
        bunk = 0
        while True:
            if (attended / (total + bunk)) >= 0.75:
                bunk += 1
            else:
                break
        print(f"✅ You can bunk {bunk - 1} classes safely.")

    # CASE 2: Below 75 → calculate needed classes
    else:
        needed = 0
        while True:
            if ((attended + needed) / (total + needed)) >= 0.75:
                break
            needed += 1

        print(f"⚠ You must attend {needed} more classes to reach 75%.")
# AI / ML Prediction
def ml_prediction(data):
    if not data:
        print("No data available!")
        return

    subject = input("Enter subject name: ")

    if subject not in data:
        print("Subject not found!")
        return

    total = data[subject]["total"]
    attended = data[subject]["attended"]

    if total == 0:
        print("No classes conducted yet!")
        return

    # Create dataset (1 = attended, 0 = missed)
    X = np.array(range(1, total + 1)).reshape(-1, 1)
    y = np.array([1]*attended + [0]*(total - attended))

    model = LinearRegression()
    model.fit(X, y)

    try:
        future_classes = int(input("Enter number of upcoming classes: "))
    except:
        print("Invalid input!")
        return

    future_X = np.array(range(total + 1, total + future_classes + 1)).reshape(-1, 1)
    predictions = model.predict(future_X)

    predicted_attendance = sum(predictions > 0.5)
    final_attendance = (attended + predicted_attendance) / (total + future_classes) * 100

    print(f"\nPredicted Attendance: {final_attendance:.2f}%")

    # Risk classification
    if final_attendance >= 75:
        print("✅ Safe")
    elif final_attendance >= 65:
        print("⚠ At Risk")
    else:
        print("🚨 Critical")

# Main program
def main():
    data = load_data()

    while True:
        menu()
        choice = input("Enter choice: ")

        if choice == "1":
            add_subject(data)
        elif choice == "2":
            view_attendance(data)
        elif choice == "3":
            prediction(data)
        elif choice == "4":
            ml_prediction(data)
        elif choice == "5":
            save_data(data)
            print("Data saved. Exiting...")
            break
        else:
            print("Invalid choice!")

# Run program
main()
