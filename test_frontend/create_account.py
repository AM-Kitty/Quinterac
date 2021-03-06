import tempfile
from importlib import reload
import os
import io
import sys
import src.Frontend as app

path = os.path.dirname(os.path.abspath(__file__))

# test for create account
# ------------------------create account----------------------------------#
def test_R1T1(capsys):
    # --R1T1--ATM mode createacct
    # Cannot create account in the ATM mode
    # Error prompt for creating account in ATM mode - pass
    """
    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'createacct'
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
    # --R1T2--agent mode create account
    # Can create an account in agent mode
    # Successfully create account in agent mode - pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'createacct', 'newUser', '3333444', 'logout',
            'login', 'agent', 'deleteacct', 'newUser', '3333444', 'logout'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Create an account successfully! Go back to main menu!', '', 'There are seven transaction operations:', '', 'Please enter your transaction operations:',
            'Log out successfully!', '', 'There are seven transaction operations:', '',
            'Please enter your transaction operations:', 'There are two types of mode you can login:', '',
            'Enter [atm]: ----> for ATM mode', 'Enter [agent]: ----> for Agent or privileged (teller) mode', '',
            'Which mode do you want to login:', 'There are seven transaction operations:', '',
            'Please enter your transaction operations:', 'Enter your account name:Enter your account number:',
            'Delete an account successfully! Go back to main menu!', '', 'There are seven transaction operations:', '',
            'Please enter your transaction operations:', 'Log out successfully!', '',
            'There are seven transaction operations:', '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=['NEW 3333444 000 0000000 newUser', 'EOS 0000000 000 0000000 ***',
                                      'DEL 3333444 000 0000000 newUser', 'EOS 0000000 000 0000000 ***']
    )

def test_R2(capsys):
    # --R2T1--invalid number create
    # Cannot create an account number beginning with 0
    # Error prompt for account number beginning with 0 - pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'createacct', 'newUser', '0333444'
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
    # --R2T2--over create
    # Cannot have same account number with exist account
    # Error prompt for account number with the same account number - pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'createacct', 'newUser', '2333444', 'logout',
            'login', 'agent', 'createacct', 'newUser', '2333444'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Should not be same account number (account already exist)', 'Enter your account number:'
        ],
        expected_output_transactions=['NEW 2333444 000 0000000 newUser', 'EOS 0000000 000 0000000 ***']
    )

def test_R2T3(capsys):
    # --R2T3--invalid name create with less than 3 letters
    # Cannot create the account if the name character number is less than 3
    # Error prompt for invalid account name not over 3 characters - pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'createacct', 'te'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter your account name:Enter a valid account name!', 'Enter your account name:'
        ],
        expected_output_transactions=['NEW 2333444 000 0000000 newUser', 'EOS 0000000 000 0000000 ***']
    )

def test_R2T4(capsys):
    # --R2T4--invalid name create with over 30 letters
    # Cannot create the account if the name character number is larger than 30
    # Error prompt for invalid account name not over 3 characters - pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'createacct', 'abcdefghijklmnopqrstuvwxyzqwert'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter your account name:Enter a valid account name!', 'Enter your account name:'
        ],
        expected_output_transactions=[]
    )



def test_R2T5(capsys):
    # --R2T5--invalid name create with space in the beginning or end
    # Cannot create the account if the name contains space in the beginning or end
    # Error prompt for name with space in the beginning or end - pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'createacct', ' abc '
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter your account name:Enter a valid account name(no space for beginning or ending)!', 'Enter your account name:'
        ],
        expected_output_transactions=[]
    )


def test_R2T6(capsys):
    # --R2T6--valid name create within space in the name
    # can create account name containing space-successfully created
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'createacct', 'a b c', '1234563', 'logout',
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
             'Create an account successfully! Go back to main menu!', '',
            'There are seven transaction operations:', '',
            'Please enter your transaction operations:', 'Log out successfully!', '',
            'There are seven transaction operations:', '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=['NEW 1234563 000 0000000 a b c', 'EOS 0000000 000 0000000 ***']
    )

    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'deleteacct', 'a b c', '1234563', 'logout'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter your transaction operations:'
        ],
        expected_output_transactions=['DEL 1234563 000 0000000 a b c', 'EOS 0000000 000 0000000 ***']
    )


def test_R3T1(capsys):
    # --R3T1--new account, can not do other transactions in agent mode - pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'createacct', 'newUser', '1234522', 'logout', 'login', 'agent', 'deposit', '1234522'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error! Account just create, cannot do anything!'
        ],
        expected_output_transactions=['NEW 1234522 000 0000000 newUser', 'EOS 0000000 000 0000000 ***']
    )

    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'deleteacct', 'newUser', '1234522', 'logout'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter your transaction operations:'
        ],
        expected_output_transactions=['DEL 1234522 000 0000000 newUser', 'EOS 0000000 000 0000000 ***']
    )

def test_R3T2(capsys):
    # --R3T2--in agent mode, new account, can not do other transactions in atm mode - pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'createacct', 'newUser', '1234523', 'logout', 'login', 'atm', 'deposit', '1234523'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error! Account just create, cannot do anything!'
        ],
        expected_output_transactions=['NEW 1234523 000 0000000 newUser', 'EOS 0000000 000 0000000 ***']
    )

    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'deleteacct', 'newUser', '1234523', 'logout'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter your transaction operations:'
        ],
        expected_output_transactions=['DEL 1234523 000 0000000 newUser', 'EOS 0000000 000 0000000 ***']
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
