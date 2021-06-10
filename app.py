# -*- coding: utf-8 -*-
"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans.

Example:
    $ python app.py
"""
import sys
import fire
import questionary
from pathlib import Path

# This will import save and load functionality for csv files.  
from qualifier.utils.fileio import load_csv, save_csv  

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value

def load_bank_data():
    """Ask for the file path to the latest banking data and load the CSV file.

    Returns:
        The bank data from the data rate sheet CSV file.
    """

    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask() # ./data/daily_rate_sheet.csv
    csvpath = Path(csvpath)
    if not csvpath.exists():
        sys.exit(f"Oops! Can't find this path: {csvpath}")

    return load_csv(csvpath)


def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
        Returns the applicant's financial information.
    """

    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask()

    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value


def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")
    
    return bank_data_filtered


def save_qualifying_loans(qualifying_loans):
    """Saves the qualifying loans to a CSV file.

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
    """
    # @TODO: Complete the usability dialog for savings the CSV Files.
    # YOUR CODE HERE!
    # Step 1: This will check if there are any qualifying loans for the user, 
    # if not then it will prompt the user and automatically exit the program.
    if len(qualifying_loans) == 0: 
        sys.exit("You don't have any qualifying loans. Unable to save results.\nGood bye!") 
        # but if there are no qualified loans then the program will exit and will not save any file.


    # Step 2: Prompt the user whether or not they would like to save their qualifying loans.
    user_answer = questionary.confirm("Would you like to save your qualifying loans to a csv file?").ask() 
    if user_answer == True: #If the user answers Yes, then this will prompt the user to 

        # Step 3: Ask the user the output file path
        
        file_name_from_user = questionary.text("Enter a file name: ").ask()
        # This was created to hard code the header.
        header = "Lender,Max Loan Amount,Max LTV,Max DTI,Min Credit Score,Interest Rate"
        # The split method converts string to a list of strings given the ',' as a separator/ delimiter.
        header = header.split(",") # ["Lender", "Max Loan Amount", ..., "Interest Rate"]  
        # This determines if the user define an output path, and 
        # if not empty then it will save it and user can name the file.
        if file_name_from_user != "":  
            csvpath = Path("./data/output/" + file_name_from_user + ".csv") # This will prompt the user where their file is located.
            print("Your file is located at: " + str(Path(__file__).parent.absolute()) + "/" + str(csvpath)) # __file__ refers to “this” file which is app.py, 
            # while .parent refers to the folder where “this” file is located, 
            # and .absolute would give the absolute path. 
            # In this case, it now refers to the .parent and we are chaining these with the dot “.” Operator
            save_csv(csvpath, qualifying_loans, header)  

def run():
    """The main function for running the script."""

    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )
    # Save qualifying loans
    save_qualifying_loans(qualifying_loans)


if __name__ == "__main__":
    fire.Fire(run)