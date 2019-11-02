from importlib import reload
import io
import sys
import frontend.Frontend as app


# path = os.path.dirname(os.path.abspath(__file__))


def test_r2(capsys):
    """
    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """

    #-----------------------logout-------------------------------#
    # ---------------- R1T1------------------------------#
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
            "['login', 'logout', 'create account', 'delete account', 'deposit', 'withdraw', 'transfer']", '',
            'Please enter your transaction operations:'
        ]
    )

    # test for logout after login in agent
    # ---------------- R1T2------------------------------#
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
            "['login', 'logout', 'create account', 'delete account', 'deposit', 'withdraw', 'transfer']", '',
            'Please enter your transaction operations:'
        ]
    )

    # ---------------- R1T3------------------------------#
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

    # ---------------- R1T4------------------------------#
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

    # ---------------- R2T1------------------------------#
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

    # ---------------- R2T2------------------------------#
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

    # ---------------- R2T3------------------------------#
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

    # ---------------- R2T4------------------------------#
    # test for creating account after logout
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'logout', 'create account'
        ],
        intput_valid_accounts=[
            '1234567','0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error prompt for login failed'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***']
    )

    # ---------------- R2T5------------------------------#
    # test for deleting account after logout
    helper(
        capsys=capsys,
        terminal_input=[
            'login', 'atm', 'logout', 'delete account'
        ],
        intput_valid_accounts=[
            '1234567','0000000'
        ],
        expected_tail_of_terminal_output=[
            'Error prompt for login failed'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***']
    )

    # ---------------- R2T6------------------------------#
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
            "['login', 'logout', 'create account', 'delete account', 'deposit', 'withdraw', 'transfer']",
            '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***']
    )

    # ---------------- R3T1------------------------------#
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
            'Enter a valid transaction operation!',  'Please enter your transaction operations:', 'Log out successfully!', '', 'There are seven transaction operations:',
            "['login', 'logout', 'create account', 'delete account', 'deposit', 'withdraw', 'transfer']",
            '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***']
    )

<<<<<<< HEAD
=======
    # ---------------- R3T2------------------------------#
>>>>>>> fc33900d11f4e0c56aa3d56bdfec6d5fced78512
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
            'Error prompt for login failed.', 'There are seven transaction operations:',
            "['login', 'logout', 'create account', 'delete account', 'deposit', 'withdraw', 'transfer']", '',
            'Please enter your transaction operations:', 'There are two types of mode you can login:', '',
            'Enter [atm]: ----> for ATM mode', 'Enter [agent]: ----> for Agent or privileged (teller) mode', '',
            'Which mode do you want to login:', 'There are seven transaction operations:',
            "['login', 'logout', 'create account', 'delete account', 'deposit', 'withdraw', 'transfer']", '',
            'Please enter your transaction operations:', 'Log out successfully!', '',
            'There are seven transaction operations:', "['login', 'logout', 'create account', 'delete account', 'deposit', 'withdraw', 'transfer']",
            '', 'Please enter your transaction operations:'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***']
    )
<<<<<<< HEAD

=======
>>>>>>> fc33900d11f4e0c56aa3d56bdfec6d5fced78512

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
