#Unit testing 

#test case 1 
# test insertion of a value , with a true value and a false value 

import csv
import pytest
import app
from app import write_data , pay_maths 
from unittest.mock import patch

# Fixture: reusable employee test data
@pytest.fixture
def employee_data():
    return {
        "id": "E001",
        "hourly_rate": 12.50,
        "name": "Rayan",
        "age": 22,
        "role": "Driver",
        "hours_worked": 30
    }


def test_success_write(tmp_path, employee_data):
    file_path = tmp_path / "employees.csv"

    result = write_data(
        employee_data["id"],
        employee_data["hourly_rate"],
        employee_data["name"],
        employee_data["age"],
        employee_data["role"],
        employee_data["hours_worked"],
        filename=str(file_path)
    )

    # Assert: check the success flag
    assert result is True

    # Read the CSV file and check its contents
    with open(file_path, "r", newline="") as file:
        rows = list(csv.reader(file))

    # Check the header
    assert rows[0] == [
        "id", "rate", "name", "age", "role", "hpw"
    ]

    # Check the saved employee record
    assert rows[1] == [
        employee_data["id"],
        "12.5",
        employee_data["name"],
        str(employee_data["age"]),
        employee_data["role"],
        str(employee_data["hours_worked"])
    ]


def test_fail_write(tmp_path, employee_data):
    # Arrange: use a directory that does not exist
    file_path = tmp_path / "missing" / "employees.csv"

    # Act: attempt to save the employee
    result = write_data(
        employee_data["id"],
        employee_data["hourly_rate"],
        employee_data["name"],
        employee_data["age"],
        employee_data["role"],
        employee_data["hours_worked"],
        filename=str(file_path)
    )
# this should fail 
    assert result is False



@pytest.fixture
def pay_data():
    return [
        (12.50, 40, 2166.6666666666665),
        (15.00, 20, 1300.00),
        (12.50, 0, 0.00),
        (0.00, 40, 0.00)
    ]



def test_calculate_monthly_pay(pay_data):
    for hourly_rate, hours_per_week, expected in pay_data:
        result = pay_maths(hourly_rate, hours_per_week)
        assert result == pytest.approx(expected)


# branch test 

def test_exit_branch():
    with patch("builtins.input", side_effect=["6"]), \
         patch("builtins.print") as mock_print:

        app.main()

        mock_print.assert_any_call(
            "Exiting Employee Management System."
        )
        

def test_view_branch():
    with patch("builtins.input", side_effect=["1", "6"]), \
         patch.object(app, "view_employees") as mock_view, \
         patch("builtins.print"):

        app.main()

        mock_view.assert_called_once()