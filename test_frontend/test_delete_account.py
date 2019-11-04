import tempfile
from importlib import reload
import os
import io
import sys
import frontend.Frontend as app

path = os.path.dirname(os.path.abspath(__file__))

# test for delete account
# ------------------------delete account-------------------------------------#
def test_R1T1(capsys):
    # --R1T1--ATM delete mode
    # Cannot delete account in the ATM mode
    # Error prompt for deleting account in ATM mode - pass
    """
    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'deleteacct'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error prompt for ATM create account or delete account! Please enter other operations!', '',
            'There are seven transaction operations:', '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=[]
    )

def test_R1T2(capsys):
    # --R1T2--agent mode delete
    # Can delete an account in agent mode
    # Successfully create account in agent mode - pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'createacct', 'newUser', '1234561', 'logout',
            'login', 'agent', 'deleteacct', 'newUser', '1234561', 'logout'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter your transaction operations:'
        ],
        expected_output_transactions=['NEW 1234561 000 0000000 newUser', 'EOS 0000000 000 0000000 ***', 'DEL 1234561 000 0000000 newUser', 'EOS 0000000 000 0000000 ***']
    )

def test_R2T1(capsys):
    # --R2T1--transfer on deleted account
    # Cannot do any other transactions on a deleted account
    # Error prompt for the account being deleted - pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'createacct', 'newUser', '1234561', 'logout',
            'login', 'agent', 'deleteacct', 'newUser', '1234561', 'logout',
            'login', 'agent', 'transfer', 'newUser', '1234561'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter your account number:'
        ],
        expected_output_transactions=['NEW 1234561 000 0000000 newUser', 'EOS 0000000 000 0000000 ***', 'DEL 1234561 000 0000000 newUser', 'EOS 0000000 000 0000000 ***']
    )

def test_R2T2(capsys):
    # --R2T2--deposit on deleted account
    # Cannot do any other transactions on a deleted account
    # Error prompt for the account being deleted - pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'deposit', 'newUser', '1234561'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter your account number:'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***']
    )

def test_R2T3(capsys):
    # --R2T3--withdraw on deleted account
    # Cannot do any other transactions such as withdraw on a deleted account
    # Error prompt for the account being deleted - pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'withdraw', 'newUser', '1234561'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter your account number:'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***']
    )

def test_R2T4(capsys):
    # --R2T4--delete on a deleted account
    # Cannot do any other transactions such as withdraw on a deleted account
    # Error prompt for the account being deleted - pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'deleteacct', 'newUser', '1234561'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter your account number:'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***']
    )

def test_R3T1(capsys):
    # --R3T1--delete account with account number less than 7 digits
    # Error prompt for delete account (with account number less than 7)
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'deleteacct', 'newUser', '123456'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R3T2(capsys):
    # --R3T2--delete account with account number being larger than 7
    # Error prompt for delete account (with account number more than 7)
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'deleteacct', 'newUser', '12345678'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter your account number:'
        ],
        expected_output_transactions=[]
    )

def test_R3T3(capsys):
    # --R3T3--delete account with account number containing letters
    # Error prompt for account number containing letters
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'deleteacct', 'newUser', '12345s7'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter your account number:'
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
