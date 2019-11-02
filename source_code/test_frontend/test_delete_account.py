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
    '''
    # ------------------------delete account-------------------------------------#
    # --R1T1--ATM delete mode
    # Cannot delete account in the ATM mode
    # Error prompt for deleting account in ATM mode - pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'delete account'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error prompt for ATM creat account or delete account! Please enter other operations!', '', 'There are seven transaction operations:', "['login', 'logout', 'create account', 'delete account', 'deposit', 'withdraw', 'transfer']",
            '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=[]
    )

    # --R1T2--agent mode createacct
    # Can create an account in agent mode
    # Successfully create account in agent mode - pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'create account', 'newUser', '1234561', 'logout',
            'login', 'agent', 'delete account', 'newUser', '1234561', 'logout'
        ],
        intput_valid_accounts=[
            '1234567', '1234561', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Please enter your transaction operations:'
        ],
        expected_output_transactions=['NEW 1234561 000 0000000 newUser', 'EOS 0000000 000 0000000 ***', 'DEL 1234561 000 0000000 newUser', 'EOS 0000000 000 0000000 ***']
    )

    # --R3T1--deleted account transfer transactions
    # Cannot do any other transactions on a deleted account
    # Error prompt for the account being deleted - pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'create account', 'newUser', '1234561', 'logout',
            'login', 'agent', 'delete account', 'newUser', '1234561', 'logout',
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

    # --R3T2--deleted account deposit transaction
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

    # --R3T3--deleted account withdraw transaction
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

    # --R3T4--delete a deleted account
    # Cannot do any other transactions such as withdraw on a deleted account
    # Error prompt for the account being deleted - pass
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'agent', 'delete account', 'newUser', '1234561'
        ],
        intput_valid_accounts=[
            '1234567', '0000000'
        ],
        expected_tail_of_terminal_output=[
            'Enter your account number:'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***']
    )
'''
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

    with open(transaction_summary_file, 'r') as of:
        content = of.read().splitlines()

        # print out the testing information for debugging
        # the following print content will only display if a
        # test case failed:
        print('output transactions:', content)
        print('output transactions (expected):', expected_output_transactions)

        for ind in range(len(content)):
            assert content[ind] == expected_output_transactions[ind]

        with open(transaction_summary_file, 'r') as of:
            content = of.read().splitlines()

            # print out the testing information for debugging
            # the following print content will only display if a
            # test case failed:
            print('output transactions:', content)
            print('output transactions (expected):', expected_output_transactions)

            for ind in range(len(content)):
                assert content[ind] == expected_output_transactions[ind]
