import tempfile
from importlib import reload
import io
import sys
import os
import src.Frontend as app

path = os.path.dirname(os.path.abspath(__file__))

# test for logout
#-----------------------logout-----------------------------#
def test_R1T1(capsys):
    """
    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """

    # --R1T1--logout in atm mode
    # test for logout after login in atm
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'logout'
        ],
        intput_valid_accounts=[
            '1234567','0000000'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***'],
        expected_tail_of_terminal_output=[
            'Log out successfully!', '', 'There are seven transaction operations:',
             '',
            'Please enter your transaction operations:'
        ]
    )

def test_R1T2(capsys):
    # --R1T2--logout in agent mode
    # test for logout after login in agent
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'logout'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***'],
        expected_tail_of_terminal_output=[
            'Log out successfully!', '', 'There are seven transaction operations:',
             '',
            'Please enter your transaction operations:'
        ]
    )

def test_R1T3(capsys):
    # --R1T3--login after logout in atm
    # test for login after logout in atm
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'logout', 'login'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter your transaction operations:', 'There are two types of mode you can login:', '',
            'Enter [atm]: ----> for ATM mode', 'Enter [agent]: ----> for Agent or privileged (teller) mode', '',
            'Which mode do you want to login:'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***']
    )

def test_R1T4(capsys):
    # --R1T4--login after logout in agent
    # test for login after logout in agent
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'logout', 'login'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter your transaction operations:', 'There are two types of mode you can login:', '',
            'Enter [atm]: ----> for ATM mode', 'Enter [agent]: ----> for Agent or privileged (teller) mode', '',
            'Which mode do you want to login:'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***']
    )

def test_R2T1(capsys):
    # -- R2T1--withdraw after logout
    # test for withdrawing after logout
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'logout', 'withdraw'
        ],
        intput_valid_accounts=[
            '1234567','0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error prompt for login failed'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***']
    )

def test_R2T2(capsys):
    # --R2T2--deposit after logout
    # test for depositing after logout
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'logout', 'deposit'
        ],
        intput_valid_accounts=[
            '1234567','0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error! Error prompt for login failed'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***']
    )

def test_R2T3(capsys):
    # -- R2T3--transfer after logout
    # test for transferring after logout
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'logout', 'transfer'
        ],
        intput_valid_accounts=[
            '1234567','0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error prompt for login failed'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***']
    )

def test_R2T4(capsys):
    # --R2T4--create account after logout
    # test for creating account after logout
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'logout', 'createacct'
        ],
        intput_valid_accounts=[
            '1234567','0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error prompt for login failed'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***']
    )

def test_R2T5(capsys):
    # --R2T5--delete account after logout
    # test for deleting account after logout
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'logout', 'deleteacct'
        ],
        intput_valid_accounts=[
            '1234567','0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error prompt for login failed'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***']
    )

def test_R2T6(capsys):
    # -- R2T6--Login after logout
    # test for login out after logout
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'logout', 'logout'
        ],
        intput_valid_accounts=[
            '1234567','0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error prompt for login failed.', 'There are seven transaction operations:',
            '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***']
    )

def test_R3T1(capsys):
    # --R3T1--Invalid Input Operation
    # test for invalid input operation for logout
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'what?', 'logout'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter a valid transaction operation!',  'Please enter your transaction operations:', 'Log out successfully!', '', 
            'There are seven transaction operations:', '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***']
    )

def test_R3T2(capsys):
    # --R3T2--Logout before a successful login
    # test for logout is not accepted before login
    helper(
        capsys=capsys,
        terminal_input=[
            'logout', 'login', 'atm', 'logout'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error prompt for login failed.', 'There are seven transaction operations:', '',
            'Please enter your transaction operations:', 'There are two types of mode you can login:', '',
            'Enter [atm]: ----> for ATM mode', 'Enter [agent]: ----> for Agent or privileged (teller) mode', '',
            'Which mode do you want to login:', 'There are seven transaction operations:', '',
            'Please enter your transaction operations:', 'Log out successfully!', '',
            'There are seven transaction operations:', '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***']
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
