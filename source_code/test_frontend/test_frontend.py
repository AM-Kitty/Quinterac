from importlib import reload
import os
import io
import sys
import frontend.Frontend as app

path = os.path.dirname(os.path.abspath(__file__))


def test_r2(capsys):
    """Testing r2. Self-contained (i.e. everything in the code approach)
    [my favorite - all in one place with the code]

    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """
    helper(
        capsys=capsys,
        terminal_input=[
            '1','m','2'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_output_transactions=['EOS 0000000 000 0000000 ***'],
        expected_tail_of_terminal_output=[
            'Log out successfully!'
        ]
    )

'''

    helper(
        capsys=capsys,
        terminal_input=[
            '1', 'm', '7','1234567','7654321','100','2'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Log out successfully!'
        ],
        expected_output_transactions=['test']
    )
    helper(
        capsys=capsys,
        terminal_input=[
            '1','m','1'
        ],
        intput_valid_accounts=[
            '1234567'
        ],
        expected_tail_of_terminal_output=[
            'Error prompt for multiple login.'
        ],
        expected_output_transactions= "daedewdwqe"
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
    #temp_fd, temp_file = tempfile.mkstemp()
    transaction_summary_file = "frontend/TransactionSummaryFile.txt"

    # create a temporary file in the system to store the valid accounts:
    #temp_fd2, temp_file2 = tempfile.mkstemp()
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
