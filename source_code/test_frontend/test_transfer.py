import tempfile
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

    # ------------------------Transfer-------------------------------------#
    # --R1T1--Invalid from transfer account number in atm mode start with 0-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'transfer', '0123456'
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
    # --R1T2--Invalid from transfer account number in atm mode not in 7 digits-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'transfer', '12345'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter a valid account number! (Only 7 digits)', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R1T3_1(capsys):
    '''
    # --R1T3--Invalid from transfer account number not in valid accounts list file-----Failed
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'transfer', '8888888'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Transfer account not existed', 'Enter your account number:'
        ],
        expected_output_transactions=['']
    )
    '''

def test_R1T3(capsys):
    # --R1T3--Invalid from transfer account number in atm mode mixed with characters-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'transfer', '12345b@'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter a valid digit number!', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R1T4(capsys):
    # --R1T4--Invalid from transfer account number in atm mode not in valid accounts list file-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'transfer', '8888888'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter your account number:Account not exist! Enter a exist account to transfer!', 'Transfer from ------>',
            'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R2T1(capsys):
    # --R2T1--Invalid to transfer account number in atm mode start with 0-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'transfer', '1234567', '0123456'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Account number first digit cannot be zero!', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R2T2(capsys):
    # --R2T2--Invalid to transfer account number in atm mode not in 7 digits-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'transfer', '1234567', '12345'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter a valid account number! (Only 7 digits)', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R2T3(capsys):

    '''
    # --R2T3--Invalid to transfer account number not in valid accounts list file-----Failed
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'transfer', '1234567', '8888888'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Transfer account not existed', 'Enter your account number:'
        ],
        expected_output_transactions=['']
    )
    '''

def test_R2T3(capsys):
    # --R2T3--Invalid to transfer account number in atm mode mixed with characters-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'transfer', '1234567', '12345a@'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter a valid digit number!', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R2T4(capsys):
    # --R2T4--Invalid to transfer account number in atm mode not in valid accounts list file-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'transfer', '1234567', '8888888'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter your account number:Account not exist! Enter a exist account to transfer!', 'Transfer to -------->',
            'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R3T1(capsys):
    # --R3T1--Invalid from transfer account number in agent mode start with 0-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'transfer', '0123456'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Account number first digit cannot be zero!', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R3T2(capsys):
    # --R3T2--Invalid from transfer account number in agent mode not in 7 digits-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'transfer',  '12345'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter a valid account number! (Only 7 digits)', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R3T3(capsys):
    # --R3T3--Invalid from transfer account number in agent mode mixed with characters-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'transfer', '12345a@'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter a valid digit number!', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R3T4(capsys):
    # --R3T4--Invalid from transfer account number in agent mode not in valid accounts list file-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'transfer', '8888888'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter your account number:Account not exist! Enter a exist account to transfer!', 'Transfer from ------>', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R4T1(capsys):
    # --R4T1--Invalid to transfer account number in agent mode start with 0-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'transfer', '1234567', '0123456'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Account number first digit cannot be zero!', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R4T2(capsys):
    # --R4T2--Invalid to transfer account number in agent mode not in 7 digits-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'transfer', '1234567', '12345'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter a valid account number! (Only 7 digits)', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R4T3(capsys):
    # --R4T3--Invalid to transfer account number in agent mode mixed with characters-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'transfer', '1234567', '12345a@'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter a valid digit number!', 'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R4T4(capsys):
    # --R4T4--Invalid to transfer account number in agent mode not in valid accounts list file-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'transfer', '1234567', '8888888'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter your account number:Account not exist! Enter a exist account to transfer!', 'Transfer to -------->',
            'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R5T1(capsys):
    # --R5T1--ATM transfer over daily amount----Failed
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'transfer', '1234567', '7654321', '450000000'
        ],
        intput_valid_accounts=[
            '1234567', '7654321', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter your amount:Over ATM transfer daily limit, enter a valid amount!', 'Enter your amount:'
        ],
        expected_output_transactions=[]
    )

def test_R5T2(capsys):
    # --R5T2--ATM transfer within daily amount----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'transfer', '1234567', '7654321', '200', 'logout'
        ],
        intput_valid_accounts=[
            '1234567', '7654321'
        ],
        expected_tail_of_terminal_output=[
            'Transfer successfully! Go back to main menu!', '', 'There are seven transaction operations:',
            "['login', 'logout', 'createacct', 'deleteacct', 'deposit', 'withdraw', 'transfer']", '',
            'Please enter your transaction operations:', 'Log out successfully!', '',
            'There are seven transaction operations:', "['login', 'logout', 'createacct', 'deleteacct', 'deposit', 'withdraw', 'transfer']",
            '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=['XFR 1234567 20000 7654321 ***', 'EOS 0000000 000 0000000 ***']
    )

def test_R5T3(capsys):
    # --R5T3--Multiple transfer over ATM daily amount limit-----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'transfer', '1234567', '7654321', '10000', 'logout', 'login', 'atm', 'transfer', '1234567', '7654321', '200'
        ],
        intput_valid_accounts=[
            '1234567', '7654321'
        ],
        expected_tail_of_terminal_output=[
            'Error! Over atm daily transfer limit!'
        ],
        expected_output_transactions=['XFR 1234567 1000000 7654321 ***', 'EOS 0000000 000 0000000 ***']
    )

def test_R6T1(capsys):
    # --R6T1--Agent transfer over daily amount----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'transfer', '1234567', '7654321', '99999999999'
        ],
        intput_valid_accounts=[
            '1234567', '7654321'
        ],
        expected_tail_of_terminal_output=[
            'Enter your amount:Over agent transfer daily limit, enter a valid amount!', 'Enter your amount:'
        ],
        expected_output_transactions=[]
    )

def test_R6T2(capsys):
    # --R6T2--Agent transfer within daily amount----Pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'transfer', '1234567', '7654321', '999', 'logout'
        ],
        intput_valid_accounts=[
            '1234567', '7654321'
        ],
        expected_tail_of_terminal_output=[
            'Transfer successfully! Go back to main menu!', '', 'There are seven transaction operations:', "['login', 'logout', 'createacct', 'deleteacct', 'deposit', 'withdraw', 'transfer']", '', 'Please enter your transaction operations:',
            'Log out successfully!', '', 'There are seven transaction operations:', "['login', 'logout', 'createacct', 'deleteacct', 'deposit', 'withdraw', 'transfer']",
            '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=['XFR 1234567 99900 7654321 ***', 'EOS 0000000 000 0000000 ***']
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

