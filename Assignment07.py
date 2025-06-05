# -------------------------------------------------------------------------- #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Stefan Sandberg,6/4/2025,Implemented Person and Student classes with validation
#   Stefan Sandberg,6/4/2025,Added JSON serialization/deserialization methods
#   Stefan Sandberg,6/4/2025,Enhanced file operations with proper error handling
#   Stefan Sandberg,6/4/2025,Improved input validation and user feedback
#   Stefan Sandberg,6/4/2025,Added comprehensive documentation
#   Stefan Sandberg,6/4/2025,Removed @dataclass decorator and implemented 
#                            getters/setters
#   Stefan Sandberg,6/4/2025,Updated name validation to allow hyphens and 
#                            apostrophes
# -------------------------------------------------------------------------- #
import json
from typing import List

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str  # Hold the choice made by the user.

class Person:
    """
    A class representing a person with first and last name.
    
    This class implements:
    - Properties for first_name and last_name with validation
    - Getters and setters for both name properties
    - String representation method
    
    Properties:
        first_name (str): The person's first name (letters, hyphens, and 
                         apostrophes only)
        last_name (str): The person's last name (letters, hyphens, and 
                        apostrophes only)
    
    Methods:
        __init__(): Initializes a new Person object
        __str__(): Returns a comma-separated string of first and last name
    
    ChangeLog: (Who, When, What)
    RRoot,1/1/2030,Created Class
    Stefan Sandberg,6/4/2025,Added detailed class documentation and validation
    Stefan Sandberg,6/4/2025,Removed @dataclass decorator and implemented 
                             getters/setters
    Stefan Sandberg,6/4/2025,Updated name validation to allow hyphens and 
                             apostrophes
    """
    def __init__(self, first_name: str = "", last_name: str = ""):
        """
        Initialize a new Person object.
        
        Args:
            first_name (str): The person's first name
            last_name (str): The person's last name
        """
        self._first_name = first_name
        self._last_name = last_name
    
    @property
    def first_name(self) -> str:
        """Get the person's first name."""
        return self._first_name
    
    @first_name.setter
    def first_name(self, value: str):
        """
        Set the person's first name.
        
        Args:
            value (str): The new first name
            
        Raises:
            ValueError: If the first name contains invalid characters
        """
        # Check each character is either a letter, hyphen, or apostrophe
        if not all(c.isalpha() or c in "-'" for c in value):
            raise ValueError(
                "First name must contain only letters, hyphens, and apostrophes"
            )
        self._first_name = value
    
    @property
    def last_name(self) -> str:
        """Get the person's last name."""
        return self._last_name
    
    @last_name.setter
    def last_name(self, value: str):
        """
        Set the person's last name.
        
        Args:
            value (str): The new last name
            
        Raises:
            ValueError: If the last name contains invalid characters
        """
        # Check each character is either a letter, hyphen, or apostrophe
        if not all(c.isalpha() or c in "-'" for c in value):
            raise ValueError(
                "Last name must contain only letters, hyphens, and apostrophes"
            )
        self._last_name = value
    
    def __str__(self) -> str:
        """Return a string representation of the Person object."""
        return f"{self.first_name},{self.last_name}"

class Student(Person):
    """
    A class representing a student that inherits from Person.
    
    This class implements:
    - Inheritance from Person class
    - Additional course_name property with validation
    - Methods for JSON serialization/deserialization
    - String representation method
    
    Properties:
        course_name (str): The course the student is enrolled in (cannot be empty)
    
    Methods:
        __init__(): Initializes a new Student object
        to_dict(): Converts Student object to dictionary format
        from_dict(): Creates Student object from dictionary
        __str__(): Returns comma-separated string of all student data
    
    ChangeLog: (Who, When, What)
    RRoot,1/1/2030,Created Class
    Stefan Sandberg,6/4/2025,Added JSON serialization methods and documentation
    Stefan Sandberg,6/4/2025,Removed @dataclass decorator and implemented 
                             getters/setters
    Stefan Sandberg,6/4/2025,Replaced @classmethod with regular method for 
                             from_dict
    """
    def __init__(self, first_name: str = "", last_name: str = "", 
                 course_name: str = ""):
        """
        Initialize a new Student object.
        
        Args:
            first_name (str): The student's first name
            last_name (str): The student's last name
            course_name (str): The course the student is enrolled in
        """
        super().__init__(first_name, last_name)
        self._course_name = course_name
    
    @property
    def course_name(self) -> str:
        """Get the student's course name."""
        return self._course_name
    
    @course_name.setter
    def course_name(self, value: str):
        """
        Set the student's course name.
        
        Args:
            value (str): The new course name
            
        Raises:
            ValueError: If the course name is empty
        """
        if not value.strip():
            raise ValueError("Course name cannot be empty")
        self._course_name = value
    
    def __str__(self) -> str:
        """Return a string representation of the Student object."""
        return f"{self.first_name},{self.last_name},{self.course_name}"
    
    def to_dict(self) -> dict:
        """
        Convert the Student object to a dictionary.
        
        Returns:
            dict: A dictionary representation of the Student object
        """
        return {
            "FirstName": self.first_name,
            "LastName": self.last_name,
            "CourseName": self.course_name
        }
    
    def from_dict(self, data: dict) -> 'Student':
        """
        Create a Student object from a dictionary.
        
        Args:
            data (dict): Dictionary containing student data
            
        Returns:
            Student: A new Student object created from the dictionary data
        """
        return Student(
            first_name=data["FirstName"],
            last_name=data["LastName"],
            course_name=data["CourseName"]
        )

# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files.
    
    This class implements:
    - Reading student data from JSON files
    - Writing student data to JSON files
    - Converting between Student objects and JSON format
    - Error handling for file operations
    
    Methods:
        read_data_from_file(): Reads and converts JSON data to Student objects
        write_data_to_file(): Converts and writes Student objects to JSON file
    
    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    Stefan Sandberg,6/4/2025,Enhanced file operations with proper error handling
    Stefan Sandberg,6/4/2025,Updated to work with regular from_dict method
    """
    @staticmethod
    def read_data_from_file(file_name: str) -> List[Student]:
        """ This function reads data from a json file and loads it into a list of 
        Student objects
        
        This function:
        - Opens and reads a JSON file
        - Converts JSON data to Student objects
        - Handles file not found and other exceptions
        - Ensures proper file closure
        
        Args:
            file_name (str): Name of the JSON file to read from
            
        Returns:
            List[Student]: List of Student objects created from file data
            
        Raises:
            FileNotFoundError: If the specified file doesn't exist
            Exception: For other file reading errors
            
        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Stefan Sandberg,6/4/2025,Added comprehensive error handling and type hints
        Stefan Sandberg,6/4/2025,Updated to work with regular from_dict method
        """
        file = None
        try:
            # Get a list of dictionary rows from the data file
            file = open(file_name, "r")
            json_students = json.load(file)

            # Convert the list of dictionary rows into a list of Student objects
            student_objects = []
            for student_dict in json_students:
                student = Student()  # Create empty Student object
                student_objects.append(student.from_dict(student_dict))

        except FileNotFoundError as e:
            IO.output_error_messages(
                "Text file must exist before running this script!", e
            )
        except Exception as e:
            IO.output_error_messages(
                "There was a non-specific error when reading the file!", e
            )
        finally:
            if file is not None and not file.closed:
                file.close()
        return student_objects

    @staticmethod
    def write_data_to_file(file_name: str, student_data: List[Student]):
        """ This function writes data to a json file with data from a list of 
        Student objects
        
        This function:
        - Converts Student objects to dictionary format
        - Writes data to JSON file
        - Handles file writing exceptions
        - Ensures proper file closure
        - Displays confirmation message
        
        Args:
            file_name (str): Name of the JSON file to write to
            student_data (List[Student]): List of Student objects to write
            
        Raises:
            Exception: For file writing errors
            
        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Stefan Sandberg,6/4/2025,Implemented proper file handling and error 
                                 management
        """
        file = None
        try:
            # Convert Student objects to dictionaries
            student_dicts = [student.to_dict() for student in student_data]
            
            file = open(file_name, "w")
            json.dump(student_dicts, file)
            file.close()
            IO.output_student_and_course_names(student_data=student_data)
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message, error=e)
        finally:
            if file is not None and not file.closed:
                file.close()

# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output.
    
    This class implements:
    - Menu display and input handling
    - Student data input and validation
    - Error message display
    - Student information display
    
    Methods:
        output_error_messages(): Displays error messages to user
        output_menu(): Displays program menu
        input_menu_choice(): Gets and validates menu choice
        output_student_and_course_names(): Displays student information
        input_student_data(): Collects and validates student data
    
    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    RRoot,1.2.2030,Added menu output and input functions
    RRoot,1.3.2030,Added a function to display the data
    RRoot,1.4.2030,Added a function to display custom error messages
    Stefan Sandberg,6/4/2025,Enhanced input validation and user feedback
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays custom error messages to the user
        
        This function:
        - Displays user-friendly error message
        - Optionally displays technical error details
        - Formats error output for readability
        
        Args:
            message (str): User-friendly error message
            error (Exception, optional): Technical error details
            
        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function
        Stefan Sandberg,6/4/2025,Improved error message formatting and technical 
                                 details display
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user
        
        This function:
        - Displays formatted menu options
        - Adds spacing for better readability
        
        Args:
            menu (str): Menu text to display
            
        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Stefan Sandberg,6/4/2025,Enhanced menu formatting for better user 
                                 experience
        """
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user
        
        This function:
        - Prompts user for menu choice
        - Validates input is a valid menu option
        - Handles invalid input with error message
        
        Returns:
            str: User's validated menu choice
            
        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Stefan Sandberg,6/4/2025,Added input validation and error handling
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1","2","3","4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the 
                                                  # technical message

        return choice

    @staticmethod
    def output_student_and_course_names(student_data: List[Student]):
        """ This function displays the student and course names to the user
        
        This function:
        - Displays formatted list of student information
        - Shows each student's name and course
        - Adds visual separators for readability
        
        Args:
            student_data (List[Student]): List of Student objects to display
            
        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Stefan Sandberg,6/4/2025,Improved display formatting and added type hints
        """
        print("-" * 50)
        for student in student_data:
            print(f'Student {student.first_name} {student.last_name} is enrolled '
                  f'in {student.course_name}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: List[Student]) -> List[Student]:
        """ This function gets the student's first name and last name, with a 
        course name from the user
        
        This function:
        - Prompts for student information
        - Creates new Student object
        - Validates input data
        - Adds student to list
        - Displays confirmation message
        
        Args:
            student_data (List[Student]): Current list of Student objects
            
        Returns:
            List[Student]: Updated list with new student added
            
        Raises:
            ValueError: For invalid input data
            Exception: For other input errors
            
        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        Stefan Sandberg,6/4/2025,Implemented input validation and error handling
        """
        try:
            student_first_name = input("Enter the student's first name: ")
            student_last_name = input("Enter the student's last name: ")
            course_name = input("Please enter the name of the course: ")

            student = Student(
                first_name=student_first_name,
                last_name=student_last_name,
                course_name=course_name
            )

            student_data.append(student)
            print()
            print(f"You have registered {student.first_name} {student.last_name} "
                  f"for {student.course_name}.")
        except ValueError as e:
            IO.output_error_messages(
                message="One of the values was the correct type of data!", 
                error=e
            )
        except Exception as e:
            IO.output_error_messages(
                message="Error: There was a problem with your entered data.", 
                error=e
            )
        return student_data

# Start of main body

# When the program starts, read the file data into a list of Student objects
# Extract the data from the file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME)

# Present and Process the data
while (True):
    # Present the menu of choices
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # Using string comparison as menu_choice is a string
        students = IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_and_course_names(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(
            file_name=FILE_NAME, 
            student_data=students
        )
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, 3, or 4")

print("Program Ended") 
