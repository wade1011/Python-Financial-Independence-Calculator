"""

Financial Independence Console Application

Parses files output by the Financial Independence console application, displays
a maximum, minimum and average value for each simulations result set.

Version: 1.0
Author: Wade Casey
Date: 02/06/2018

"""



import os
import random



# =========================================================================== #
#                            Validation Functions                             #
# =========================================================================== #

def validate_positive_integer(user_input):
    """Check if value passed is a valid, positive integer.

    Args:
        user_input: input passed by the user.
    Returns:
        value passed as a positive integer, or the string 'invalid_input'
    Raises:
        ValueError: if value passed is not an integer.

    """
    try:
        user_input = int(user_input)
        if user_input < 0:
            print("\nPlease enter a non-negative integer.")
            return "invalid_input"
        else:
            return user_input
    except ValueError:
        print("\nInvalid input, please enter an integer.")
        return "invalid_input"


def validate_integer(user_input):
    """Check if value passed is a valid integer.

    Args:
        user_input: input passed by the user.
    Returns:
        value passed as an integer, or the string 'invalid_input'
    Raises:
        ValueError: if value passed is not an integer.

    """    
    try:
        return int(user_input)
    except ValueError:
        print("\nInvalid input, please enter an integer.")
        return "invalid_input"


def validate_float(user_input):
    """Check if value passed is a float.

    Args:
        user_input: input passed by the user.
    Returns:
        value passed as a float, or the string 'invalid_input'
    Raises:
        ValueError: if value passed is not a float.

    """        
    try:
        return float(user_input)
    except:
        print("\nPlease enter a real number.")
        return "invalid_input"



# =========================================================================== #
#                             Input Functions                                 #
# =========================================================================== #

def get_annual_spend():
    """Request yearly spend, validate input, recursive until input is valid.
    """
    print("\nHow much did you spend last year to support your current lifestyle?")
    annual_spend = validate_positive_integer(input("(Must be positive integer): "))
    if annual_spend == "invalid_input":
        return get_annual_spend()
    else:
        return annual_spend


def get_inflation_rate():
    """Request inflation rate, validate input, recursive until input is valid.
    """    
    print("\nPlease enter the base inflation rate:")
    inflation_rate = validate_float(input("(e.g. 2% should be entered as 0.02): "))
    if inflation_rate == "invalid_input":
        return get_inflation_rate()
    else:
        return inflation_rate


def get_savings_balance():
    """Request savings balance, validate input, recursive until input is valid.
    """     
    print("\nHow much do you currently have saved for investment?")
    savings_balance = validate_integer(input("(Must be an integer): "))
    if savings_balance == "invalid_input":
        return get_savings_balance()
    else:
        return savings_balance


def get_interest_rate():
    """Request annual interest rate, validate input, recursive until input is valid.
    """      
    print("\nPlease enter the base annual interest rate:")
    interest_rate = validate_float(input("(e.g. 4% should be entered as 0.04): "))
    if interest_rate == "invalid_input":
        return get_interest_rate()
    else:
        return interest_rate


def get_num_years():
    """Request number of year to test, validate input, recursive until input is valid.
    """     
    print("\nHow many years do you want to test?")
    num_years = validate_positive_integer(input("(Must be positive integer, less than 10,000): "))
    if num_years != "invalid_input" and num_years > 9999:
        print("\nPlease enter a value less than 10,000.")
        return get_num_years()
    if num_years == "invalid_input":
        return get_num_years()
    else:
        if num_years > 0:
            return num_years
        else:
            print("\nPlease enter a positive integer.")
            return get_num_years()


def get_inflation_change():
    """Request maximum change for inflation in a given year, validate input,
    recursive until input is valid."""     
    print("\nPlease enter the expected maximum change for inflation in a given year:")
    inflation_change = validate_float(input("(e.g. 0.25% should be entered as 0.0025): "))
    if inflation_change == "invalid_input":
        return get_inflation_change()
    else:
        return inflation_change


def get_interest_change():
    """Request expected maximum change for interest in a given year, validate
    input, recursive until input is valid."""     
    print("\nPlease enter the expected maximum change for interest in a given year:")
    interest_change = validate_float(input("(e.g. 1% should be entered as 0.01): "))
    if interest_change == "invalid_input":
        return get_interest_change()
    else:
        return interest_change


def get_simulations_to_run():
    """Request number of simulations to run, validate input, recursive until input is valid."""       
    print("\nHow many simulations should be run?")
    simulations_to_run = validate_positive_integer(input("(Must be positive integer, less than 10,000): "))
    if simulations_to_run != "invalid_input" and simulations_to_run > 9999:
        print("\nPlease enter a value less than 10,000.")
        return get_simulations_to_run()
    if simulations_to_run == "invalid_input":
        return get_simulations_to_run()
    else:
        if simulations_to_run > 0:
            return simulations_to_run
        else:
            print("\nPlease enter a positive integer.")
            return get_simulations_to_run()



# =========================================================================== #
#                                Functions                                    #
# =========================================================================== #

def run_again():
    """ 
    Prompt to input 'Q' to Quit, or 'R' to Restart the application.
    """
    decision = str(input("--------------------------\nWhat would you like to do?\n'Quit' or 'Restart'?\n "))
    if decision.upper() == "QUIT" or decision.upper() == "Q":
        print("--------------------------\nfi.py has closed.\n--------------------------")
        quit()
    elif decision.upper() == "RESTART" or decision.upper() == "R":
        print("--------------------------\nfi.py has restarted.\n--------------------------")
        begin()
    else:
        print("--------------------------\n\n", decision, "is not a valid option.\n")
        run_again()


def run_simulation(annual_spend, inflation_rate, savings_balance,
            interest_rate, num_years, inflation_change, interest_change):
    """ 
    Calculates savings_balance value after yearly expenses, taking into account 
    interest and inflation rates. Interest and inflation values undergo randomization each iteration.

    Args:
        annual_spend,
        inflation_rate,
        savings_balance,
        interest_rate,
        num_years,
        inflation_change,
        interest_change:
        Validated values input by the user.
    Returns: 
        An array of floats, representing the users saving balance after spending, interest and inflation.
    Explanation:
    Loop for int(num_years):
        annual_spend is adjusted by inflation_rate. 
        Adjusted annual_spend is subtracted from savings_balance.
        interest_rate is applied to remaining savings_balance.
        Final savings_balance is appended to ???San array.
    End loop.
    return array.
    """
    results = []
    for i in range(0, num_years):
        annual_spend = annual_spend + (annual_spend * inflation_rate)
        savings_balance = savings_balance - annual_spend
        savings_balance = savings_balance + (savings_balance * interest_rate)

        inflation_rate = modify_rate(inflation_rate, inflation_change)
        interest_rate = modify_rate(interest_rate, interest_change)

        results.append(savings_balance)

    return results


def modify_rate(rate, change):
    """
    Calculate a random value within change of the given rate

    Args:
        rate: the initial rate to change from
        change: the maximum amount to add or subtract from the rate
    Returns:
        random value within change of the given rate
    Explanation:
        random.random() calculates a random value between 0 and 1.
        Thus random.random() * 2 gives a value between 0 and 2,
        so 1 - random.random() * 2 gives a value between -1 and 1.
        Multiplying by change gives a value between -change and change,
        which is then added to the rate.
    """
    return rate + change * (0.75 - random.random() * 2.5)


def begin():
    """
    Will cause the application to prompt user for input, validate, store
    and process the input. 

    Processed data is written to file 'output.txt' which will be created and stored
    in the same directory as 'fi.py'.
    """

    # Confirm the file 'output.txt' can be opened or created, and written to.
    try:
        with open('output.txt', '+w') as f:
            f.write("")
    # Instruct user how to resolve the error then close the application.            
    except IOError:
        input("\nError accessing output.txt from:\n" + os.getcwd() +
        "\nCheck you have permissions to read and write to files in this " +
        "directory then try again.\n\nPress and 'Enter' or 'Return' to quit the application.")
        quit()

    # Get values from the user to so the calculations can be run.
    annual_spend = get_annual_spend()
    inflation_rate = get_inflation_rate()
    inflation_change = get_inflation_change()
    savings_balance = get_savings_balance()
    interest_rate = get_interest_rate()
    interest_change = get_interest_change()
    num_years = get_num_years()
    simulations_to_run = get_simulations_to_run()

    # Used to determin the percentage of simulations which end with a positive number.
    successful_count = 0
    # Loop for the number of simulations the user requested.
    for i in range(0, simulations_to_run):
        # 'run_simulation' returns an array of savings balances remaining after
        # expenses for each year have been calculated and deducted.
        result = run_simulation(annual_spend, inflation_rate, savings_balance,
                interest_rate, num_years, inflation_change, interest_change)

        # Open the file 'output.txt' in append mode.
        # For each value in results array, format to two decimal places and
        # append if to the file. If the last result was positive, append
        # 'successful', else append 'unsuccessful'.
        with open('output.txt', 'a') as f:
            for val in result:
                f.write(format(val, '.2f') + " ")
            if float(result[len(result)-1]) < 0:
                f.write("unsuccessful")
            else:
                f.write("successful")
                successful_count  += 1
            f.write("\n")

    # Calculate the percent of successful results, and write to the console.
    percent = (successful_count/simulations_to_run)*100
    print("\n----------------------------------------------")
    print("Simulation was successful in " + str(successful_count) + "/" +
        str(simulations_to_run) + " runs " + "(" + format(percent, '.2f') + "%)")
    print("----------------------------------------------")
    print("See 'output.txt' located in directory:\n" + os.getcwd() +  ". for more detailed results.")
    # Once processing has finished, prompt user to 'Quit' or 'Restart' the application.
    run_again()



# Entry point for application
begin()