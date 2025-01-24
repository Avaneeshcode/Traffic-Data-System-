#Author: Kesavan Avaneesh
#Date: 21/11/2024
#Student ID: IIT - 20240830 | UOW - 21197457

import csv

# Task A: Input Validation

def is_leap_year(year):
    """
    Determines if a year is a leap year within the range 2000-2024.
    A year is a leap year if it is divisible by 4.
    """
    return year % 4 == 0

def validate_date_input(date, min_value, maxi_value):
    """
    Validates date input for a specific range and ensures it is an integer.
    Prompts the user until a valid value is entered.
    Input validation will be asked in the main program
    
    Parameters:
    date (str): Prompt message displayed to the user.
    min_value (int): Minimum valid value for the input.
    maxi_value (int): Maximum valid value for the input.

    Returns:
    int: A validated integer input from the user.
    """
    
    while True:
        user_input = input(date)
        if not user_input.isdigit(): #https://www.w3schools.com/python/ref_string_isdigit.asp (this will check whether the input is digit or not)
            print("Positive Integer required")
        else:
            value = int(user_input) # Change the input to the integer
            if value < min_value or value > maxi_value: # To check the range
                print(f"Out of range - values must be in the range {min_value} and {maxi_value}.")
            else:
                return value
            
def validate_day_month_year():
    """
    Validates day, month, and year inputs with leap year consideration.
    Returns valid day, month, and year values.
    """
    day = validate_date_input("Please enter the day of the survey in the format DD: ", 1, 31)
    month = validate_date_input("Please enter the month of the survey in the format MM: ", 1, 12)
    year = validate_date_input("Please enter the year of the survey in the format YYYY: ", 2000, 2024)

    if month == 2: # For February
        if is_leap_year(year):
            max_days = 29
        else:
            max_days = 28
        if day > max_days:
            print(f"Invalid day for February in the year {year}. Maximum is {max_days}.")
            return validate_day_month_year()  # Recursively ask again
    elif month in {4, 6, 9, 11} and day > 30: # For months with only 30 days
        print(f"Invalid day for the month {month}. Maximum is 30.")
        return validate_day_month_year()  # Recursively ask again
    return day, month, year

def validate_continue_input():
    """
    Prompts the user to confirm if they want to continue processing another dataset.
    Ensures only valid inputs ("Y" or "N") are accepted.
    
    Returns:
    str: "Y" for yes or "N" for no.
    """
    while True:
        user_input = input("Do you want to select another data file for a different date? Y/N : ").upper() # Take the input in upper case
        if user_input in {"Y", "N"}:  # Check for valid input
            return user_input
        else:
            print("Invalid input. Please enter Y/N.")  # Shows error for invalid input

# Task B: Processed Outcomes

def process_csv_data(file_name):
    """
    Processes traffic data from a CSV file to compute various metrics, such as:
    Total number of vehicles, trucks, electric vehicles, and two-wheeled vehicles.
    Buses traveling north at a specific junction.
    Vehicles that didn't turn and those exceeding the speed limit.
    Junction-specific vehicle counts and hourly traffic patterns.
    Hours with rain and busiest traffic hour.
    
    Parameters:
    file_name (str): Name of the CSV file to process.

    Returns:
    list: Computed metrics or None if the file is not found.
    """
    
    try: #https://docs.python.org/3/library/csv.html#csv.DictReader
        with open(file_name, 'r') as file:
            csv_reader = csv.DictReader(file) # Read the CSV data into dictionaries
            data = list(csv_reader) # convert it into list

        # Check if the file is empty or not formatted properly
        if not data:
            print(f"Error: The file '{file_name}' is empty or not formatted properly.")
            return None

        # Variables that are assigned
        total_vehicles = 0
        total_trucks = 0
        electric_vechiles = 0
        two_wheeled_vehicles = 0
        buses_north = 0
        no_turn = 0
        total_bicycles = 0
        over_speed = 0
        elm_junction = 0
        hanley_junction = 0
        scooter_count = 0
        rain_hours = set() # Creating an empty set to store because set doesn't allow duplicates
        hourly_counts = {} # Dictionary to store the hourly traffic count
        
        # Process the records
        for row in data:
            total_vehicles += 1
            vehicle_type = row["VehicleType"].strip().lower()
            
            # Total number of Trucks and its percentage
            if vehicle_type == "truck":
                total_trucks += 1
                # Equation to find the truck percentage
                truck_percentage = round ((total_trucks / total_vehicles) * 100) if total_vehicles > 0 else 0
                
            # Total number of Electric vehicles
            if row["elctricHybrid"].strip().lower() == "true":
                electric_vechiles += 1
                
            # Total number of Two wheeled vehicles
            if vehicle_type in ["bicycle", "motorcycle", "scooter"]:
                two_wheeled_vehicles += 1
                
            # Buses goes in north at Elm avenue
            if row["JunctionName"].strip() == "Elm Avenue/Rabbit Road" and row["travel_Direction_out"].strip().lower() == "n" and vehicle_type == "buss":
                buses_north += 1
                
            # Vehicles that didn't turn
            if row["travel_Direction_in"].strip().lower() == row["travel_Direction_out"].strip().lower():
                no_turn += 1
            
            # Total number of bicycle and find average
            if vehicle_type == "bicycle":
                total_bicycles += 1
                # Equation to find the average bicycle per hour
                average_bicycles_per_hour = round(total_bicycles / 24) if total_bicycles > 0 else 0
                
            # Over speeded vehicles
            if int(row["VehicleSpeed"]) > int(row["JunctionSpeedLimit"]):
                over_speed += 1
                
            # Vehicles per junction
            if row["JunctionName"].strip() == "Elm Avenue/Rabbit Road":
                elm_junction += 1
                if vehicle_type == "scooter":
                    scooter_count += 1
                    # Equation to find the scooter percentage
                    scooter_percentage = round((scooter_count / elm_junction) * 100) if elm_junction > 0 else 0
            elif row["JunctionName"].strip() == "Hanley Highway/Westway":
                hanley_junction += 1
            
            
            # Vehicle counts per hour for Hanley Highway/Westway
            if row["JunctionName"].strip() == "Hanley Highway/Westway":
                hour = row["timeOfDay"].split(":")[0]  # Extract only the hour from time
                hourly_counts[hour] = hourly_counts.get(hour, 0) + 1  # Increment count for this hour

            # Find the busiest hour specifically for Hanley Highway/Westway
            busiest_hour = max(hourly_counts.values(), default=0)
            busiest_hour_times = [f"Between {hour}:00 and {int(hour) + 1}:00" for hour, count in hourly_counts.items() if count == busiest_hour]
            
            # Record hours with rain
            hour = row["timeOfDay"].split(":")[0]  # Extract hour
            if "rain" in row["Weather_Conditions"].strip().lower(): # search for the word rain in the row
                rain_hours.add(hour)
        
        
        # Results are stored as list
        return [ total_vehicles, total_trucks, electric_vechiles, two_wheeled_vehicles, buses_north, no_turn, over_speed,
                 elm_junction, hanley_junction, truck_percentage, average_bicycles_per_hour, scooter_percentage, 
                 busiest_hour, ",".join(busiest_hour_times),len(rain_hours) ]
    
    
    # Output when the there is no such file is found    
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return None 

def display_outcomes(outcomes, file_name):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    print(f"\n***************************")
    print(f"Data file selected is {file_name}")
    print(f"***************************")
    print(f"The total number of vehicles recorded for this date is {outcomes[0]}")
    print(f"The total number of trucks recorded for this date is {outcomes[1]}")
    print(f"The total number of electric vehicles for this date is {outcomes[2]}")
    print(f"The total number of two-wheeled vehicles for this date is {outcomes[3]}")
    print(f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes[4]}")
    print(f"The total number of Vehicles through both junctions not turning left or right is {outcomes[5]}")
    print(f"The percentage of total vehicles recorded that are trucks for this date is {outcomes[9]}%")
    print(f"the average number of Bikes per hour for this date is {outcomes[10]}")
    print(f"The total number of Vehicles recorded as over the speed limit for this date is {outcomes[6]}")
    print(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes[7]}")
    print(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes[8]}")
    print(f"{outcomes[11]}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.")
    print(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes[12]}")
    print(f"The most vehicles through Hanley Highway/Westway were recorded between {outcomes[13]}")
    print(f"The number of hours of rain for this date is {outcomes[14]}")


# Task C: Save Results to Text File

def save_results_to_file(outcomes, fileName="results.txt", csv_file=None):
    """
    Saves the processed outcomes to a text file (results.txt) and appends if the program loops.
    """
    with open(fileName, "a") as file: # Updating the reults everytime in the results.txt
        file.write(f" \n")
        file.write(f"Data file selected is {csv_file}")
        file.write(f"\nThe total number of vehicles recorded for this date is {outcomes[0]}")
        file.write(f"\nThe total number of trucks recorded for this date is {outcomes[1]}")
        file.write(f"\nThe total number of electric vehicles for this date is {outcomes[2]}")
        file.write(f"\nThe total number of two-wheeled vehicles for this date is {outcomes[3]}")
        file.write(f"\nThe total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes[4]}")
        file.write(f"\nThe total number of Vehicles through both junctions not turning left or right {outcomes[5]}")
        file.write(f"\nThe percentage of total vehicles recorded that are trucks for this rate is{outcomes[9]}%")
        file.write(f"\nThe average number of bikes per hour for this date is {outcomes[10]}")
        file.write(f"\nThe total number of Vehicles recorded as over the speed limit for this date is {outcomes[6]}")
        file.write(f"\nThe total number of Vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes[7]}")
        file.write(f"\nThe total number of Vehicles recorded throug Hanley Highway/Westway is {outcomes[8]}")
        file.write(f"\n{outcomes[11]}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters")
        file.write(f"\nThe highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes[12]}")
        file.write(f"\nThe most vehicles through Hanley Highway/Westway were recorded between {outcomes[13]}")
        file.write(f"\nThe number of hours of rain for this date is {outcomes[14]}\n")
        file.write(f" \n")
        file.write("***********************************")
        file.write(f" \n")


def process_csv_data_with_histogram(file_name):
    """
    Extended version of process_csv_data to include hourly traffic counts for histogram.
    Returns hourly counts for Elm Avenue and Hanley Highway.
    This is done using dictionary rather than list to acess the certain hour easily

    """
    hourly_counts_elm = {} # Dictionary to store data
    hourly_counts_hanley = {}

    outcomes = process_csv_data(file_name)  # Reuse the existing logic
    if outcomes:
        # Extract hourly traffic counts
        with open(file_name, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                hour = row["timeOfDay"].split(":")[0]  # Extract hour using split
                junction = row["JunctionName"].strip()
                if junction == "Elm Avenue/Rabbit Road":
                    hourly_counts_elm[hour] = hourly_counts_elm.get(hour, 0) + 1
                elif junction == "Hanley Highway/Westway":
                    hourly_counts_hanley[hour] = hourly_counts_hanley.get(hour, 0) + 1

    return outcomes, hourly_counts_elm, hourly_counts_hanley


# Task D
import tkinter as tk

class HistogramApp:
    """
    Creates a histogram to visualize hourly traffic data for both junctions.
    """
    def __init__(self, hourly_counts_elm, hourly_counts_hanley, date):
        """ 
        Initializes the app with traffic data and the date for the title.
        """
        self.hourly_counts_elm = hourly_counts_elm
        self.hourly_counts_hanley = hourly_counts_hanley
        self.date = date
        self.root = tk.Tk()
        self.canvas = None  # Will hold the canvas for drawing

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        self.root.title(f"Histogram")
        self.root.geometry("1300x600")
        self.canvas = tk.Canvas(self.root, width=1300, height=600, bg="white")
        self.canvas.pack()

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        bar_width = 20
        gap = 30
        max_height = 400
        x_start = 50
        y_start = 500

        # Find the maximum hourly traffic count for scaling
        max_count = max(max(self.hourly_counts_elm.values(), default=0),
                        max(self.hourly_counts_hanley.values(), default=0))

        # Axis labels
        self.canvas.create_text(700, 550, text="Hours 00:00 to 24:00", font=("Arial", 12))

        for i in range(24):
            hour = f"{i:02d}"

            # Elm Avenue bar
            elm_count = self.hourly_counts_elm.get(hour, 0)
            elm_height = (elm_count / max_count) * max_height if max_count > 0 else 0
            self.canvas.create_rectangle(
                x_start + (bar_width + gap) * i, y_start - elm_height,
                x_start + bar_width + (bar_width + gap) * i, y_start,
                fill="#96f997", outline="black"
            )

            # Display Elm Avenue value
            self.canvas.create_text(
            x_start + (bar_width + gap) * i + bar_width / 2, y_start - elm_height - 10,
            text=str(elm_count), font=("Arial", 8), fill="#96f997"
            )

            # Hanley Highway bar
            hanley_count = self.hourly_counts_hanley.get(hour, 0)
            hanley_height = (hanley_count / max_count) * max_height if max_count > 0 else 0
            self.canvas.create_rectangle(
                x_start + (bar_width + gap) * i + bar_width, y_start - hanley_height,
                x_start + 2 * bar_width + (bar_width + gap) * i, y_start,
                fill="#f89796", outline="black"
            )

            # Display Hanley Highway value
            self.canvas.create_text(
            x_start + (bar_width + gap) * i + bar_width + bar_width / 2, y_start - hanley_height - 10,
            text=str(hanley_count), font=("Arial", 8), fill="#f89796"
            )

            # Hour label
            self.canvas.create_text(
                x_start + (bar_width + gap) * i + bar_width, y_start + 15,
                text=f"{hour}", font=("Arial", 8)
            )

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        self.canvas.create_text(242, 30, text=f"Histogram of Vehicle Frequency per Hour ({self.date})", font=("Arial", 12))
        self.canvas.create_rectangle(50, 50, 70, 70, fill="#96f997", outline="black")
        self.canvas.create_text(90, 60, text="Elm Avenue/Rabbit Road", anchor="w", font=("Arial", 10))
        self.canvas.create_rectangle(50, 80, 70, 100, fill="#f89796", outline="black")
        self.canvas.create_text(90, 90, text="Hanley HighwayWestway", anchor="w", font=("Arial", 10))

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.root.mainloop()

# Task E
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.outcomes = None  # Stores processed outcomes (e.g., averages or summaries).
        self.hourly_counts_elm = {}  # Holds hourly traffic data for "Elm Avenue/Rabbit Road".
        self.hourly_counts_hanley = {}  # Holds hourly traffic data for "Hanley Highway/Westway".
        self.csv_file = None  # Stores the name of the currently loaded CSV file.

    def load_csv_file(self, file_name, day, month, year):
        """
        Loads a CSV file, processes its data, and handles result display and visualization.
        """
        try:
            # Process the file and extract necessary data
            self.outcomes, self.hourly_counts_elm, self.hourly_counts_hanley = process_csv_data_with_histogram(file_name)
            
            if self.outcomes:  # Check if processing was successful
                # Display outcomes
                display_outcomes(self.outcomes, file_name)
                
                # Save results to a file
                save_results_to_file(self.outcomes, fileName="results.txt", csv_file=file_name)
                
                # Show histogram
                histogram_app = HistogramApp(
                    self.hourly_counts_elm, self.hourly_counts_hanley, f"{day:02d}/{month:02d}/{year}"
                )
                histogram_app.run()
                return True  # Indicate success
            else:
                print(f"Error: Failed to process data from file '{file_name}'.")
                return False  # Indicate failure
        except Exception as e:
            print(f"An error occurred while processing file '{file_name}': {e}")
            return False

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.outcomes = None
        self.hourly_counts_elm.clear()
        self.hourly_counts_hanley.clear()
        self.csv_file = None  # Reset the file name

    def handle_user_interaction(self):
        """
        Handles user interaction for input validation and processing.
        """
        # Input validation for date
        day, month, year = validate_day_month_year()
        self.csv_file = f"traffic_data{day:02d}{month:02d}{year}.csv"  # Construct file name

        # Load and process the file
        if not self.load_csv_file(self.csv_file, day, month, year):
            print(f"Error: Failed to process file '{self.csv_file}'. Please check if the file exists and is correctly formatted.")

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        print("Welcome to the Traffic Data Analysis Program!")
        while True:
            self.clear_previous_data()  # Clear previous data
            self.handle_user_interaction()  # Handle current dataset

            # Prompt to continue or exit
            continue_choice = validate_continue_input()
            if continue_choice == "N":
                print("\nEnd of run. Goodbye!")
                break


if __name__ == "__main__":
    processor = MultiCSVProcessor()
    processor.process_files()

