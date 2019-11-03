from importlib import reload
import os
import io
import sys
import frontend.Frontend as app


# path = os.path.dirname(os.path.abspath(__file__))


def test_r2(capsys):
    """
    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """

    # ------------------------Deposit-------------------------------------#
    # --R1T1--deposit with invalid number (beginning with 0) in atm mode
    # Cannot deposit if the account number is invalid with error-pass
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

    # --R1T2--deposit with invalid number (less than 7) in atm mode
    # Cannot deposit if the account number is invalid with error-pass
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

    # --R1T3--deposit with invalid number (larger than 7) in atm mode
    # Cannot deposit if the account number is invalid with error-pass
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

    # --R1T4--deposit with invalid number (having letters and symbols other than number) in atm mode
    # Cannot deposit if the account number is invalid with error-pass
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

    # --R1T5--deposit with invalid number (beginning with 0) in agent mode
    # Cannot deposit if the account number is invalid with error-pass
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

    # --R1T6--deposit with invalid number (less than 7) in agent mode
    # Cannot deposit if the account number is invalid with error-pass
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

    # --R1T7--deposit with invalid number (larger than 7) in agent mode
    # Cannot deposit if the account number is invalid with error-pass
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

    # --R1T4--deposit with invalid number (having letters and symbols other than number) in agent mode
    # Cannot deposit if the account number is invalid with error-pass
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

    # --R2T1--ATM deposit above limit
    # Cannot deposit if the amount limit per deposit in ATM exceeds with error-pass
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

    # --R2T2--ATM deposit within limit
    # Deposit within $2,000 per time in ATM, successful-pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'deposit', '1234567', '1000', 'logout'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter your transaction operations:'
        ],
        expected_output_transactions=['DEP 1234567 100000 0000000 ***', 'EOS 0000000 000 0000000 ***']
        #expected_output_transactions=['DEP 1234567 100000 0000000 ***', 'EOS 0000000 000 0000000 ***']
    )


    # --R3T1--ATM deposit above daily limit
    # Cannot deposit if the daily deposit amount exceeds $5,000 for ATM with error-pass
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
            'Enter your amount:Error! Over daily deposit limit!'
        ],
        expected_output_transactions=['DEP 1234567 200000 0000000 ***', 'DEP 1234567 200000 0000000 ***', 'EOS 0000000 000 0000000 ***']
    )

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
            'Please enter your transaction operations:'
        ],
        expected_output_transactions=['DEP 1234567 200000 0000000 ***', 'DEP 1234567 200000 0000000 ***', 'EOS 0000000 000 0000000 ***']
    )

    # --R3 T3--Deposit with invalid amount(with letter or symbol) in atm mode
    # error prompt deposit with invalid amount
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'deposit', '1234567', '99f9'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter your amount:Enter a valid amount!', 'Enter your amount:'
        ],
        expected_output_transactions=[]
    )

    # --R4 T1--Agent deposit exceeds
    # Cannot deposit if the withdrawals amount
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
            'Enter your amount:'
        ],
        expected_output_transactions=['DEP 1234567 200000 0000000 ***', 'DEP 1234567 200000 0000000 ***', 'EOS 0000000 000 0000000 ***']
    )

    # --R4 T2--Deposit in agent mode
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
            'Please enter your transaction operations:'
        ],
        expected_output_transactions=['DEP 1234567 99999999 0000000 ***', 'EOS 0000000 000 0000000 ***']
    )

    # --R4 T3--Deposit in agent mode
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
            'Please enter your transaction operations:'
        ],
        expected_output_transactions=['DEP 1234567 99999999 0000000 ***', 'EOS 0000000 000 0000000 ***']
    )

    # --R4 T4--Deposit with invalid amount(with letter or symbol) in agent mode
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
            'Enter your amount:Enter a valid amount!', 'Enter your amount:'
        ],
        expected_output_transactions=[]
    )

    # --R5 T1--Deposit on a deleted or Non-existent account in agent mode
    # error prompt for non existent account
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

    # --R5 T2--Deposit on a deleted or Non-existent account in atm mode
    # error prompt for non existent account
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
    transaction_summary_file = "TransactionSummaryFile.txt"
    open(transaction_summary_file, 'w').close()

    # create a temporary file in the system to store the valid accounts:
    valid_account_list_file = "frontend/ValidAccountListFile.txt"

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

    # run the Frontend.py
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

