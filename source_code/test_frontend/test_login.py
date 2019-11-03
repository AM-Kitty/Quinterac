from importlib import reload
import io
import sys
import frontend.Frontend as app


# path = os.path.dirname(os.path.abspath(__file__))


def test_R1T1(capsys):
    """
    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """
    #-----------------Login-----------------------------#

    #---------------- R1T1------------------------------#
    # test for login to the bank
    # Test all terminal output to ensure we have keywords as we want
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
            "['login', 'logout', 'create account', 'delete account', 'deposit', 'withdraw', 'transfer']",
            '', 'Please enter your transaction operations:', 'There are two types of mode you can login:', '',
            'Enter [atm]: ----> for ATM mode',
            'Enter [agent]: ----> for Agent or privileged (teller) mode', '', 'Which mode do you want to login:'
        ],
        expected_output_transactions=[]
    )

def test_R2T1(capsys):
    #---------------- R2T1------------------------------#
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
            "['login', 'logout', 'create account', 'delete account', 'deposit', 'withdraw', 'transfer']",
            '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=[]
    )

def test_R2T2(capsys):
    # ---------------- R2T2------------------------------#
    # test for create account without login
    helper(
        capsys=capsys,
        terminal_input=[
            'create account'
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
    # ---------------- R2T3------------------------------#
    # test for delete account without login
    helper(
        capsys=capsys,
        terminal_input=[
            'delete account'
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
    # ---------------- R2T4------------------------------#
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
    # ---------------- R2T5------------------------------#
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
    # ---------------- R2T6------------------------------#
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
    # ---------------- R3T1------------------------------#
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
    # ---------------- R3T2------------------------------#
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
    # ---------------- R3T3------------------------------#
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
            'There are seven transaction operations:', "['login', 'logout', 'create account', 'delete account', 'deposit', 'withdraw', 'transfer']",
            '', 'Please enter your transaction operations:'
        ]
    )

def test_R3T4(capsys):
    # ---------------- R3T4------------------------------#
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
            "['login', 'logout', 'create account', 'delete account', 'deposit', 'withdraw', 'transfer']",
            '', 'Please enter your transaction operations:'
        ]
    )

def test_R4T1(capsys):
    # ---------------- R4T1------------------------------#
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
            "['login', 'logout', 'create account', 'delete account', 'deposit', 'withdraw', 'transfer']",
            '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=[]
    )

def test_R4T2(capsys):
    # ---------------- R4T2------------------------------#
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
            "['login', 'logout', 'create account', 'delete account', 'deposit', 'withdraw', 'transfer']",
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
