import tempfile
from importlib import reload
import io
import sys
import os
import src.Frontend as app

path = os.path.dirname(os.path.abspath(__file__))

# test for login
#-----------------Login---------------------------#
def test_R1T1(capsys):
    """
    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """
    #--R1T1--Login in System
    # test for login to the bank
    helper(
        capsys=capsys,
        terminal_input=[
            'login'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Welcome to bank system!!!!', '', 'There are seven transaction operations:',
            '', 'Please enter your transaction operations:', 'There are two types of mode you can login:', '',
            'Enter [atm]: ----> for ATM mode',
            'Enter [agent]: ----> for Agent or privileged (teller) mode', '', 'Which mode do you want to login:'
        ],
        expected_output_transactions=[]
    )

def test_R2T1(capsys):
    #--R2T1--Logout before Login
    # test for logout without login
    helper(
        capsys=capsys,
        terminal_input=[
            'logout'
        ],
        intput_valid_accounts=[
            '1234567','0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error prompt for login failed.', 'There are seven transaction operations:',
            '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=[]
    )

def test_R2T2(capsys):
    # --R2T2--create account before login
    # test for create account without login
    helper(
        capsys=capsys,
        terminal_input=[
            'createacct'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error prompt for login failed'
        ],
        expected_output_transactions=[]
    )

def test_R2T3(capsys):
    # --R2T3--delete account before login
    # test for delete account without login
    helper(
        capsys=capsys,
        terminal_input=[
            'deleteacct'
        ],
        intput_valid_accounts=[
            '1234567','0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error prompt for login failed'
        ],
        expected_output_transactions=[]
    )

def test_R2T4(capsys):
    # --R2T4--deposit before login
    # test for deposit without login
    helper(
        capsys=capsys,
        terminal_input=[
            'deposit'
        ],
        intput_valid_accounts=[
            '1234567','0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error! Error prompt for login failed'
        ],
        expected_output_transactions=[]
    )

def test_R2T5(capsys):
    # -- R2T5--withdraw before login
    # test for withdraw without login
    helper(
        capsys=capsys,
        terminal_input=[
            'withdraw'
        ],
        intput_valid_accounts=[
            '1234567','0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error prompt for login failed'
        ],
        expected_output_transactions=[]
    )

def test_R2T6(capsys):
    # -- R2T6--transfer before login
    # test for transfer without login
    helper(
        capsys=capsys,
        terminal_input=[
            'transfer'
        ],
        intput_valid_accounts=[
            '1234567','0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error prompt for login failed'
        ],
        expected_output_transactions=[]
    )

def test_R3T1(capsys):
    # -- R3T1--Invalid input operation
    # test for invalid input operation for login
    helper(
        capsys=capsys,
        terminal_input=[
            'what??'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter a valid transaction operation!', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=[]
    )

def test_R3T2(capsys):
    # -- R3T2--Invalid Input Mode
    # test for input invalid operation mode
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'lalala'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_output_transactions=[],
        expected_tail_of_terminal_output=[
            'Which mode do you want to login:', 'Please enter a valid mode!', 'Which mode do you want to login:'
        ]
    )

def test_R3T3(capsys):
    # -- R3T3--Valid Input Mode for atm
    # test for input valid operation mode for atm
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_output_transactions=[],
        expected_tail_of_terminal_output=[
            'There are seven transaction operations:',
            '', 'Please enter your transaction operations:'
        ]
    )

def test_R3T4(capsys):
    # -- R3T4--Valid Input Mode for agent
    # test for input valid operation mode for agent
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_output_transactions=[],
        expected_tail_of_terminal_output=[
            'There are seven transaction operations:',
            '', 'Please enter your transaction operations:'
        ]
    )

def test_R4T1(capsys):
    # --R4T1--Over Login in atm
    # test for multiple login in atm
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'login'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error prompt for multiple login.', 'There are seven transaction operations:',
            '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=[]
    )

def test_R4T2(capsys):
    # -- R4T2--Over Login in agent
    # test for multiple login in agent
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'login'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error prompt for multiple login.', 'There are seven transaction operations:',
            '', 'Please enter your transaction operations:'
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
