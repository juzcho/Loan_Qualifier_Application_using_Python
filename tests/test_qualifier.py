# Import pathlib

from pathlib import Path

#Import fileio
from qualifier.utils import fileio

# Import Calculators
from qualifier.utils import calculators

# Import Filters
from qualifier.filters import credit_score
from qualifier.filters import debt_to_income
from qualifier.filters import loan_to_value
from qualifier.filters import max_loan_size
import app # located in the same location as tests folder.


# This test will check whether or not a file has been created. 
# This is will not check the data inside the file.
def test_save_csv():
    # @TODO: Your code here!
    # Use Path from pathlib to output the test csv to ./data/output/qualifying_loans.csv
    fileio.save_csv(Path('../data/output/qualifying_loans.csv'), [[]]) # Based on calling the save_csv function, it needs a path as well as a data of lists of list, hence an empty list of list was added for testing purposes.
    assert Path('../data/output/qualifying_loans.csv').exists()

def test_calculate_monthly_debt_ratio():
    assert calculators.calculate_monthly_debt_ratio(1500, 4000) == 0.375

def test_calculate_loan_to_value_ratio():
    assert calculators.calculate_loan_to_value_ratio(210000, 250000) == 0.84

def test_filters():
    bank_data = fileio.load_csv(Path('../data/daily_rate_sheet.csv'))
    current_credit_score = 750
    debt = 1500
    income = 4000
    loan = 210000
    home_value = 250000

    monthly_debt_ratio = 0.375

    loan_to_value_ratio = 0.84

    # test_csv
    # @TODO: Test the new save_csv code!
    # YOUR CODE HERE!
    
    # arrange - prepare the data
    test_bank_data = [["Bank of Big - Premier Option",300000, 0.85, 0.47, 740, 3.6]]

    # This just asserts using the credit_score variable. It acts (execute the function) & asserts - checks if actual == expected.
    assert credit_score.filter_credit_score(current_credit_score, test_bank_data) == [["Bank of Big - Premier Option",300000, 0.85, 0.47, 740, 3.6]]


# To cover all scenarios for the filters, equality operators was used (greater than or less than or equal to) depending on what filter it will result. We also used 'Bank of Big' as a sample bank in the asserts to test different parameters.

    # We start with testing the filter_credit_score() function, wherein we have to be sure that the user's credit score is greater than or equal to what the bank's minimum, thus it should pass.

    # Test filter_credit_score() function

    # If credit score < bank's minimum allowed, then it should not add the bank to the list.
    assert credit_score.filter_credit_score(730, test_bank_data) == []

    # If credit score == bank's minimum allowed, then it should add the bank to the list.
    assert credit_score.filter_credit_score(740, test_bank_data) == [["Bank of Big - Premier Option",300000, 0.85, 0.47, 740, 3.6]]

    # If credit score > bank's minimum allowed, then it should add the bank to the list.
    assert credit_score.filter_credit_score(760, test_bank_data) == [["Bank of Big - Premier Option",300000, 0.85, 0.47, 740, 3.6]]

     # Second, we are testing the filter_debt_to_income() function, wherein we have to be sure that the user's debt to income ratio (DTI ratio) is less than or equal to what the bank's minimum, thus it should pass.

    # Test filter_debt_to_income() function

    # If DTI ratio < bank's minimum allowed, then it should add the bank to the list.
    assert debt_to_income.filter_debt_to_income(0.30, test_bank_data) == [["Bank of Big - Premier Option",300000, 0.85, 0.47, 740, 3.6]]

    # If DTI ratio = bank's minimum allowed, then it should add the bank to the list.
    assert debt_to_income.filter_debt_to_income(0.47, test_bank_data) == [["Bank of Big - Premier Option",300000, 0.85, 0.47, 740, 3.6]]

    # If DTI ratio > bank's minimum allowed, then it should not add the bank to the list.
    assert debt_to_income.filter_debt_to_income(0.50, test_bank_data) == []

    # Third, we are testing the filter_loan_to_value() function, wherein we have to be sure that the user's loan to value ratio (LTV ratio) is less than or equal to what the bank's minimum, thus it should pass.

    # test filter_loan_to_value() function

    # If LTV ratio < bank's minimum allowed, then it should add the bank to the list.
    assert loan_to_value.filter_loan_to_value(0.81, test_bank_data) == [["Bank of Big - Premier Option",300000, 0.85, 0.47, 740, 3.6]]

    # If LTV ratio = bank's minimum allowed, then it should add the bank to the list.
    assert loan_to_value.filter_loan_to_value(0.85, test_bank_data) == [["Bank of Big - Premier Option",300000, 0.85, 0.47, 740, 3.6]]

    # If LTV ratio > bank's minimum allowed, then it should not add the bank to the list.
    assert loan_to_value.filter_loan_to_value(0.90, test_bank_data) == []

    # Fourth, we are testing the filter_max_loan_size() function, wherein we have to be sure that the user's loan is less than or equal to what the bank's minimum, thus it should pass.

    # test filter_max_loan_size() function

    # If loan < bank's minimum allowed, then it should add the bank to the list.
    assert max_loan_size.filter_max_loan_size(200000, test_bank_data) == [["Bank of Big - Premier Option",300000, 0.85, 0.47, 740, 3.6]]

    # If loan = bank's minimum allowed, then it should add the bank to the list.
    assert max_loan_size.filter_max_loan_size(300000, test_bank_data) == [["Bank of Big - Premier Option",300000, 0.85, 0.47, 740, 3.6]]

    # If loan > bank's minimum allowed, then it should not add the bank to the list.
    assert max_loan_size.filter_max_loan_size(400000, test_bank_data) == []
    
    
######################  EXTRA TEST  ############################

    # We are putting things together by testing the qualfying_loans() function. #

    # This variable was used to get the filtered data without the need to get data from the saved csv loans since the qualifying loans in this case already has that filtered list of banks once our inputs are called.

    qualifying_loans = app.find_qualifying_loans(bank_data, current_credit_score, debt, income, loan, home_value) 
    
    # The expected_bank_data is a list expected filtered bank results based on the given user input. The user input was passed through the qualifying loans.
    
    expected_bank_data = [["Bank of Big - Premier Option", "300000", "0.85", "0.47", "740", "3.6"],["Bank of Fintech - Premier Option","300000", "0.9", "0.47", "740", "3.15"], ["Prosper MBS - Premier Option", "400000", "0.85", "0.42", "750", "3.45"], ["Bank of Big - Starter Plus", "300000", "0.85", "0.39", "700", "4.35"], ["FHA Fredie Mac - Starter Plus", "300000", "0.85", "0.45", "550", "4.35"], ["iBank - Starter Plus", "300000", "0.9", "0.4", "620", "3.9"]]
    
    # Check if actual data results is an exact match with expected data.
    for i in range(len(qualifying_loans)): 
        # assert if bank names are the same.
        assert qualifying_loans[i][0] == expected_bank_data[i][0]

    # Asserts the following in the actual results:
    # customer credit score >= bank credit score minimum allowed
    # customer debt ratio <= bank's maximum allowed
    # customer loan to value ratio  <= bank's maximum allowed 
    # customer loan <= bank's maximum allowed 
    for i in range(len(qualifying_loans)):
        assert current_credit_score >= int(qualifying_loans[i][4])
        assert monthly_debt_ratio <= float(qualifying_loans[i][3])
        assert loan_to_value_ratio <= float(qualifying_loans[i][2])
        assert loan <= int(qualifying_loans[i][1])
