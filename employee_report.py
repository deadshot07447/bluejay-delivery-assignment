import sys
import pandas as pd

# Define functions
def emp_with_consecutive_days(no_of_days, df):
    print("Calculating...")
    count=0
    prev_pos = None
    consecutive_x_days_attendance_set = set()
    prev_shift_end_date = None

    for index, row in df.iterrows():
        if prev_pos is None or prev_pos != row['Position ID'] or (row['Time'].date() - prev_shift_end_date.date()).days > 1:
            count = 1
            prev_pos = row['Position ID']
            prev_shift_end_date = row['Time Out']
            continue

        count += (row['Time'].date() - prev_shift_end_date.date()).days
        count += (row['Time Out'].date() - row['Time'].date()).days

        prev_shift_end_date = row['Time Out']

        if count >= 7:
            consecutive_x_days_attendance_set.add(row['Position ID'])
            count = 0
            prev_pos = None

    print('\n*********** Output ***********')
    print(consecutive_x_days_attendance_set)
    print('**********************')



def emp_with_shift_diff(hours_max, hours_min, df):
    print("Calculating...")
    count=0
    prev_pos = None
    consecutive_x_days_attendance_set = set()
    prev_shift_end_date = None
    lt_x_hours_and_gt_y_hours_set = set()

    for index, row in df.iterrows():

        if prev_pos is None or prev_pos != row['Position ID']:
            count = 1
            prev_pos = row['Position ID']
            prev_shift_end_date = row['Time Out']
            continue

        time_diff = (row['Time'] - prev_shift_end_date)
        if time_diff <= pd.Timedelta(hours=hours_max) and time_diff >= pd.Timedelta(hours=hours_min):
            lt_x_hours_and_gt_y_hours_set.add(row['Position ID'])

    print('\n*********** Output ***********')
    print(lt_x_hours_and_gt_y_hours_set)
    print('**********************')

def emp_with_gt_x_hours_of_shift(x, df):
    print("Calculating...")
    count=0
    prev_pos = None
    employee_worked_more_than_x_hrs_in_a_shift_set = set()
    prev_shift_end_date = None

    for index, row in df.iterrows():

        if (row['Time Out'] - row['Time']) > pd.Timedelta(hours=14):
            employee_worked_more_than_x_hrs_in_a_shift_set.add(row['Position ID'])

    print('\n*********** Output ***********')
    print(employee_worked_more_than_x_hrs_in_a_shift_set)
    print('**********************')

if len(sys.argv) != 2:
    print("Usage: python employee_report.py [excel/csv file path]")
    sys.exit(1)

filepath = sys.argv[1]
print(filepath)

df = pd.read_excel(filepath)

print("Reading the input file...")
print('File loaded.')
print('Now cleansing the bad data...')
df['Time'] = pd.to_datetime(df['Time'])
df['Time Out'] = pd.to_datetime(df['Time Out'])
# Data cleansing
df = df.dropna(subset=['Time', 'Position ID', 'Time Out'])
grouped = df.groupby(['Position ID'])
sorted_df = grouped.apply(lambda x: x.sort_values(by='Time'))

# Get the argument from the command line
user_input = sys.argv[1]

while True:
    try:
        print('----------- Select Task ------------')
        print("Enter the operation number you want to perform:")
        print("1. Get a list of employee worked for 'X' consecutive days")

        print("2. Get a list of employee who has less than 'X' hours and greater than 'Y' hours between shifts.")

        print("3. Get a list of employee worked for more than 'X' hours in a shift")

        print("4 Exit")
        user_input = input()

        # Use conditional statements to call functions
        if user_input == "1":
            days = input("Enter the minimum number of consecutive days: ")
            if (days.isnumeric() == False or int(days) < 0):
                print("Please enter a valid number of days.")
                continue
            emp_with_consecutive_days(int(days), df)
        elif user_input == "2":
            hours_max = input("Enter the max hours of gap between shifts: ")
            if (hours_max.isnumeric() == False or int(hours_max) < 0):
                print("Please enter a valid number of hours.")
                continue
            hours_min = input("Enter the min hours of gap between shifts: ")
            if (hours_min.isnumeric() == False or int(hours_min) < 0):
                print("Please enter a valid number of hours.")
                continue
            emp_with_shift_diff(int(hours_max), int(hours_min), df)
        elif user_input == "3":
            hours = input("Enter the minimum number of shift hours: ")
            if (hours.isnumeric() == False or int(hours) < 0):
                print("Please enter a valid number of hours.")
                continue
            emp_with_gt_x_hours_of_shift(hours, df)
        elif user_input == "4":
            print("Exiting the program...")
            sys.exit(0)
        else:
            print("Invalid input. Please enter 1, 2, 3 or 4.")
        print('----------- Finished Task. ------------\n\n')
    except ValueError:
        print("error")

#Requirements - pandas,openpyxl
#python employee_report.py <filepath>