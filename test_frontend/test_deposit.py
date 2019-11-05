import tempfile
from importlib import reload
import os
import io
import sys
import src.Frontend as app

path = os.path.dirname(os.path.abspath(__file__))

# test for deposit
# ------------------------Deposit----------------------------------#
def test_R1T1(capsys):
    # --R1T1--deposit with invalid number (beginning with 0) in atm mode
    # Cannot deposit if the account number is invalid with error -pass
    """
    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """

    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'deposit', '0123456'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Account number first digit cannot be zero!', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R1T2(capsys):
    # --R1T2--deposit with invalid number (less than 7) in atm mode
    # Cannot deposit if the account number is invalid with error -pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'deposit', '123456'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter a valid account number! (Only 7 digits)', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R1T3(capsys):
    # --R1T3--deposit with invalid number (larger than 7) in atm mode
    # Cannot deposit if the account number is invalid with error  -pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'deposit', '12345678'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter a valid account number! (Only 7 digits)', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R1T4(capsys):
    # --R1T4--deposit with invalid number (having letters and symbols other than number) in atm mode
    # Cannot deposit if the account number is invalid with error  -pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'deposit', '1234sa7'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter a valid digit number!', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R1T5(capsys):
    # --R1T5--deposit with invalid number (beginning with 0) in agent mode
    # Cannot deposit if the account number is invalid with error  -pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'deposit', '0123456'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Account number first digit cannot be zero!', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R1T6(capsys):
    # --R1T6--deposit with invalid number (less than 7) in agent mode
    # Cannot deposit if the account number is invalid with error  -pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'deposit', '123456'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter a valid account number! (Only 7 digits)', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R1T7(capsys):
    # --R1T7--deposit with invalid number (larger than 7) in agent mode
    # Cannot deposit if the account number is invalid with error  -pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'deposit', '12345678'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter a valid account number! (Only 7 digits)', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R1T8(capsys):
    # --R1T4--deposit with invalid number (having letters and symbols other than number) in agent mode
    # Cannot deposit if the account number is invalid with error  -pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'deposit', '1234sa7'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter a valid digit number!', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R2T1(capsys):
    # --R2T1--ATM deposit above per time limit
    # Cannot deposit if the deposit amount over per time limit($2,000) in ATM mode  -pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'deposit', '1234567', '3000'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Over deposit limit, enter a valid amount!', 'Enter your amount:'
        ],
        expected_output_transactions=[]
    )

def test_R2T2(capsys):
    # --R2T2--ATM deposit within per time limit
    # Deposit within $2,000 per time in ATM successfully  -pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'deposit', '1234567', '1000', 'logout'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Deposit successfully! Go back to main menu!', '', 'There are seven transaction operations:', '',
            'Please enter your transaction operations:', 'Log out successfully!', '',
            'There are seven transaction operations:', '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=['DEP 1234567 100000 0000000 ***', 'EOS 0000000 000 0000000 ***']
    )

def test_R3T1(capsys):
    # --R3T1--ATM deposit above daily limit
    # Cannot deposit if the daily deposit amount exceeds $5,000 for ATM  -pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'deposit', '1234567', '2000', 'deposit', '1234567', '2000',
            'logout', 'login', 'atm', 'deposit', '1234567', '2000'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error! Over daily deposit limit!'
        ],
        expected_output_transactions=['DEP 1234567 200000 0000000 ***', 'DEP 1234567 200000 0000000 ***', 'EOS 0000000 000 0000000 ***']
    )

def test_R3T2(capsys):
    # --R3T2--ATM deposit within limit
    # Deposit within $5,000 daily successfully - pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'deposit', '1234567', '2000', 'deposit', '1234567', '2000',
            'logout'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Deposit successfully! Go back to main menu!', '', 'There are seven transaction operations:', '',
            'Please enter your transaction operations:', 'Log out successfully!', '',
            'There are seven transaction operations:', '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=['DEP 1234567 200000 0000000 ***', 'DEP 1234567 200000 0000000 ***', 'EOS 0000000 000 0000000 ***']
    )

def test_R3T3(capsys):
    # --R3T3--Deposit with invalid amount(with letter or symbol) in atm mode
    # error prompt deposit with invalid amount -- Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'deposit', '1234567', '99f9'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter a valid amount!', 'Enter your amount:'
        ],
        expected_output_transactions=[]
    )

def test_R4T1(capsys):
    # --R4T1--Agent deposit exceeds
    # Cannot deposit if the depoists amount
    # exceeds $999,999.99 in agent mode with error - pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'deposit', '1234567', '100000000'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Over deposit limit, enter a valid amount!', 'Enter your amount:'
        ],
        expected_output_transactions=['DEP 1234567 200000 0000000 ***', 'DEP 1234567 200000 0000000 ***', 'EOS 0000000 000 0000000 ***']
    )

def test_R4T2(capsys):
    # --R4T2--Deposit in agent mode
    # Deposit in agent mode successfully
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'deposit', '1234567', '999999.99', 'logout'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Deposit successfully! Go back to main menu!', '', 'There are seven transaction operations:', '',
            'Please enter your transaction operations:', 'Log out successfully!', '',
            'There are seven transaction operations:', '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=['DEP 1234567 99999999 0000000 ***', 'EOS 0000000 000 0000000 ***']
    )

def test_R4T3(capsys):
    # --R4T4--Deposit with invalid amount(with letter or symbol) in agent mode
    # error prompt deposit with invalid amount
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'deposit', '1234567', '99f9'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter a valid amount!', 'Enter your amount:'
        ],
        expected_output_transactions=[]
    )

def test_R5T1(capsys):
    # --R5T1--Deposit on a deleted or Non-existent account in agent mode
    # error prompt for non existent account -- Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'deposit', '1234565'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
             'Account not exist! Enter a exist account to deposit!', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R5T2(capsys):
    # --R5T2--Deposit on a deleted or Non-existent account in atm mode
    # error prompt for non existent account --Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'deposit', '1234565'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
             'Account not exist! Enter a exist account to deposit!', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def helper(
        capsys,
        terminal_input,
        expected_tail_of_terminal_output,
        intput_valid_accounts,
        expected_output_transactions
):
    """Helper function for testing

        Arguments:
            capsys -- object created by pytest to capture stdout and stderr
            terminal_input -- list of string for terminal input
            expected_tail_of_terminal_output list of expected string at the tail of terminal
            intput_valid_accounts -- list of valid accounts in the valid_account_list_file
            expected_output_transactions -- list of expected output transactions
    """

    # cleanup package
    reload(app)

    # create a temporary file in the system to store output transactions
    temp_fd, temp_file = tempfile.mkstemp()
    transaction_summary_file = temp_file

    # create a temporary file in the system to store the valid accounts:
    temp_fd2, temp_file2 = tempfile.mkstemp()
    valid_account_list_file = temp_file2
    with open(valid_account_list_file, 'w') as wf:
        wf.write('\n'.join(intput_valid_accounts))

    # prepare program parameters
    sys.argv = [
        'Frontend.py',
        valid_account_list_file,
        transaction_summary_file]

    # set terminal input
    sys.stdin = io.StringIO(
        '\n'.join(terminal_input))

    # run the program
    app.main()

    # capture terminal output / errors
    # assuming that in this case we don't use stderr
    out, err = capsys.readouterr()

    # split terminal output in lines
    out_lines = out.splitlines()

    # print out the testing information for debugging
    # the following print content will only display if a
    # test case failed:
    print('std.in:', terminal_input)
    print('valid accounts:', intput_valid_accounts)
    print('terminal output:', out_lines)
    print('terminal output (expected tail):', expected_tail_of_terminal_output)

    # compare terminal outputs at the end.`
    for i in range(1, len(expected_tail_of_terminal_output) + 1):
        index = i * -1
        assert expected_tail_of_terminal_output[index] == out_lines[index]

    # compare transactions:
    with open(transaction_summary_file, 'r') as of:
        content = of.read().splitlines()

        # print out the testing information for debugging
        # the following print content will only display if a
        # test case failed:
        print('output transactions:', content)
        print('output transactions (expected):', expected_output_transactions)

        for ind in range(len(content)):
            assert content[ind] == expected_output_transactions[ind]

    # clean up
    os.close(temp_fd)
    os.remove(temp_file)

