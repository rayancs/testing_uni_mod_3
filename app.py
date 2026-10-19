
import csv
import os

# constants
FILE_NAME = "employees.csv"

# calculate monthly pay
def pay_maths(rate, hpw):
    return rate * hpw * 52 / 12


print("Welcome to the Employee Management System")
def main_screen_opts() -> str:
    return (
        "\n1)View All Employees\n"
        "2)Add A New Employee\n"
        "3)Remove Employee\n"
        "4)Update Employee Record\n"
        "5)Calculate Monthly Pay\n"
        "6)Exit"
    )


import csv
import os

FILE_NAME = "employees.csv"


def write_data(
    id, hourly_rate, fname, age, role, hours_worked,
    filename=FILE_NAME
):
    try:
        file_exists = os.path.exists(filename)

        with open(filename, "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists or os.path.getsize(filename) == 0:
                writer.writerow([
                    "id", "rate", "name", "age", "role", "hpw"
                ])
            writer.writerow([
                id, hourly_rate, fname, age, role, hours_worked
            ])
        return True
    except (OSError, csv.Error):
        return False

def read_data():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def view_employees():
    employees = read_data()

    if not employees:
        print("No employee records found.")
        return
    for employee in employees:
        print(
            f"\nID: {employee['id']}"
            f"\nName: {employee['name']}"
            f"\nAge: {employee['age']}"
            f"\nRole: {employee['role']}"
            f"\nHourly Rate: £{employee['rate']}"
            f"\nHours Per Week: {employee['hpw']}"
        )
        
def add_employee():
    try:
        employee_id = input("Enter employee id: ").strip()
        name = input("Enter employee name: ").strip()
        age = int(input("Enter employee age: "))
        role = input("Enter employee role: ").strip()
        hourly_rate = float(input("Enter hourly rate (£): "))
        hours_worked = float(input("Enter hours worked per week: "))
        if not employee_id or not name or not role:
            print("id, name and role cannot be empty.")
            return
        if age <= 0:
            print("Age must be greater than zero.")
            return
        if hourly_rate < 0:
            print("Hourly rate cannot be negative.")
            return
        if not 0 <= hours_worked <= 168:
            print("Hours per week must be between 0 and 168.")
            return
        employees = read_data()
        if any(e["id"] == employee_id for e in employees):
            print("An employee with this id already exists.")
            return
        write_data(
            employee_id, hourly_rate, name,
            age, role, hours_worked,filename=str(FILE_NAME)
        )
        print("Employee added successfully.")
    except ValueError:
        print("Invalid input. Please enter valid numeric values.")

def remove_employee():
    employee_id = input("Enter employee id to remove: ").strip()
    employees = read_data()
    updated_employees = [
        e for e in employees if e["id"] != employee_id
    ]
    if len(updated_employees) == len(employees):
        print("Employee not found.")
        return

    save_all_employees(updated_employees)
    print("Employee removed successfully.")


def save_all_employees(employees):
    with open(FILE_NAME, "w", newline="") as file:
        fieldnames = [
            "id", "rate", "name", "age",
            "role", "hpw"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(employees)

def update_employee():
    employee_id = input("Enter employee id to update: ").strip()
    employees = read_data()

    for employee in employees:
        if employee["id"] == employee_id:
            try:
                print("Leave a field blank to keep its current value.")
                new_rate = input(
                    f"Hourly rate (£) [{employee['Hourly Rate']}]: "
                ).strip()

                new_hours = input(
                    f"Hours per week [{employee['Hours Per Week']}]: "
                ).strip()
                if new_rate:
                    rate = float(new_rate)
                    if rate < 0:
                        print("Hourly rate cannot be negative.")
                        return
                    employee["Hourly Rate"] = str(rate)
                if new_hours:
                    hours = float(new_hours)
                    if not 0 <= hours <= 168:
                        print("Hours must be between 0 and 168.")
                        return
                    employee["Hours Per Week"] = str(hours)

                save_all_employees(employees)
                print("Employee record updated successfully.")
                return

            except ValueError:
                print("Please enter valid numeric values.")

    print("Employee not found.")


def calculate_monthly_pay():
    employee_id = input("Enter employee id: ").strip()
    employees = read_data()

    for employee in employees:
        if employee["id"] == employee_id:
            rate = float(employee["rate"])
            hpw = float(employee["hpw"])
            res = pay_maths(rate,hpw)
            print(f"Employee: {employee['name']}")
            print(f"Estimated monthly gross pay: £{res:.2f}")
            return
    print("Employee not found.")

def main():
    while True:
        print(main_screen_opts())
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_employees()
        elif choice == "2":
            add_employee()
        elif choice == "3":
            remove_employee()
        elif choice == "4":
            update_employee()
        elif choice == "5":
            calculate_monthly_pay()
        elif choice == "6":
            print("Exiting Employee Management System.")
            break
        else:
            print("Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()
