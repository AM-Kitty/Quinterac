from importlib import reload
import os
import io
import sys
import frontend.Frontend as app

path = os.path.dirname(os.path.abspath(__file__))

def test_R1T1(capsys):
    """
    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """

    # ------------------------Withdraw-------------------------------------#
    # --R1T1--Invalid withdraw account number in atm mode start with 0-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'withdraw', '0123456'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Account number first digit cannot be zero!', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R1T2(capsys):
    # --R1T2--Invalid withdraw account number in atm mode less than 7 digits-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'withdraw', '12345'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Please enter a valid account number! (Only 7 digits)', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R1T3(capsys):
    # --R1T3--Invalid withdraw account number in atm mode more than 7 digits-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'withdraw', '1234567890'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Please enter a valid account number! (Only 7 digits)', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R1T4(capsys):
    # --R1T4--Invalid withdraw account number in atm mode mixed with characters-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'withdraw', '12345ba'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
             'Please enter a valid digit number!', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R1T5(capsys):
    # --R1T5--Invalid withdraw account number in atm mode not in valid accounts list file-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'withdraw', '8888888'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Account not exist! Enter a existed account to withdraw!',
            'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R1T6(capsys):
    # --R1T6--Valid withdraw account number in ATM----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'withdraw', '1234567'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Enter your amount:'
        ],
        expected_output_transactions=[]
    )

def test_R2T1(capsys):
    # --R2T1--Invalid withdraw account number in agent mode start with 0-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'withdraw', '0123456'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Account number first digit cannot be zero!', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R2T3(capsys):
    # --R2T3--Invalid withdraw account number in agent mode less than 7 digits-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'withdraw', '12345'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Please enter a valid account number! (Only 7 digits)', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R2T4(capsys):
    # --R2T4--Invalid withdraw account number in agent mode more than 7 digits-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'withdraw', '1234567890'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Please enter a valid account number! (Only 7 digits)', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R2T5(capsys):
    # --R2T5--Invalid withdraw account number in agent mode mixed with characters-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'withdraw', '12345ba'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Please enter a valid digit number!', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R2T6(capsys):
    # --R2T6--Invalid withdraw account number in agent mode not in valid accounts list file-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'withdraw', '8888888'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Account not exist! Enter a existed account to withdraw!',
            'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R2T7(capsys):
    # --R2T7--Valid withdraw account number in agent----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'withdraw', '1234567'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Enter your amount:'
        ],
        expected_output_transactions=[]
    )

def test_R3T1(capsys):
    # --R3T1--ATM withdraw over per time limit----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'withdraw', '1234567', '450000000'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Over ATM withdraw per time limit, enter a valid amount!', 'Enter your amount:'
        ],
        expected_output_transactions=[]
    )

def test_R3T2(capsys):
    # --R3T2--input invalid ATM withdraw money mixed with characters----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'withdraw', '1234567', '200aa@'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Enter your amount:Enter a valid amount!', 'Enter your amount:'
        ],
        expected_output_transactions=[]
    )

def test_R3T3(capsys):
    # --R3T3--ATM withdraw within per time limit----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'withdraw', '1234567', '100' , 'logout'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Withdraw successfully! Go back to main menu!', '',
            'There are seven transaction operations:', "['login', 'logout', 'createacct', 'deleteacct', 'deposit', 'withdraw', 'transfer']",
            '', 'Please enter your transaction operations:', 'Log out successfully!', '',
            'There are seven transaction operations:',
            "['login', 'logout', 'createacct', 'deleteacct', 'deposit', 'withdraw', 'transfer']",
            '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=['WDR 1234567 10000 0000000 ***', 'EOS 0000000 000 0000000 ***']
    )

def test_R3T4(capsys):
    # --R3T4--ATM withdraw over daily limit----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'withdraw', '1234567', '1000', 'withdraw', '1234567', '1000', 'withdraw', '1234567', '1000', 'withdraw', '1234567', '1000', 'withdraw', '1234567', '1000', 'logout', 'login', 'atm', 'withdraw', '1234567', '1000',
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Enter your amount:Error! Over daily withdraw limit!'
        ],
        expected_output_transactions=['WDR 1234567 100000 0000000 ***', 'WDR 1234567 100000 0000000 ***', 'WDR 1234567 100000 0000000 ***', 'WDR 1234567 100000 0000000 ***', 'WDR 1234567 100000 0000000 ***', 'EOS 0000000 000 0000000 ***']
    )

def test_R4T1(capsys):
    # --R4T1--agent withdraw over limit----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'withdraw', '1234567', '450000000'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Over withdraw limit, enter a valid amount!', 'Enter your amount:'
        ],
        expected_output_transactions=[]
    )

def test_R4T2(capsys):
    # --R4T2--input invalid ATM withdraw money mixed with characters----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'withdraw', '1234567', '200aa@'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Enter your amount:Enter a valid amount!', 'Enter your amount:'
        ],
        expected_output_transactions=[]
    )

def test_R4T3(capsys):
    # --R4T3--agent withdraw within limit----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'withdraw', '1234567', '500', 'logout'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Withdraw successfully! Go back to main menu!', '',
            'There are seven transaction operations:',
            "['login', 'logout', 'createacct', 'deleteacct', 'deposit', 'withdraw', 'transfer']",
            '', 'Please enter your transaction operations:', 'Log out successfully!', '',
            'There are seven transaction operations:', "['login', 'logout', 'createacct', 'deleteacct', 'deposit', 'withdraw', 'transfer']",
            '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=['WDR 1234567 50000 0000000 ***', 'EOS 0000000 000 0000000 ***']
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

