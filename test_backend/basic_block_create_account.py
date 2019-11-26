import os
import sys
import tempfile
from importlib import reload

import src.Backend as app

path = os.path.dirname(os.path.abspath(__file__))

# decision coverage and block coverage test cases for create account and withdraw
# test cases for decision coverage cover the test cases for block coverage, which will be labeled as comment below
#-----------------------------------------------------------
#---------------------- withdraw ----------------------------
#-----------------------------------------------------------

# -----------------T1(block)-----------------------
# block point at 1: when the account has existed
# the account has existed
# print error message and terminate
def test_4(capsys):
    helper(capsys,
           input_transaction_summary_file=['NEW 1234567 000 0000000 Theo\n', 'EOS 0000000 000 0000000 ***'],
           input_master_accounts_file=["1234567 0 Theo"],
           expected_new_master_account=["1234567 0 Theo"],
           expected_tail_of_terminal_output=["Error! New account must have an unused account number!"]
           )

# -----------------T5(block)-----------------------
# block point at 4: when the account is created successfully
def test_5(capsys):
    helper(capsys,
           input_transaction_summary_file=['NEW 1122334 000 0000000 theoXiao\n', 'EOS 0000000 000 0000000 ***'],
           input_master_accounts_file=["1234567 400000 Theo"],
           expected_new_master_account=["1122334 0 theoXiao", "1234567 400000 Theo"],
           expected_tail_of_terminal_output=["New Valid Accounts File created successfully!"]
           )

def helper(capsys,
           input_transaction_summary_file,
           input_master_accounts_file,
           expected_new_master_account,
           expected_tail_of_terminal_output
           ):

    # cleanup package
    reload(app)

    # create a temporary file in the system to store the valid accounts in masterAccountsFile:
    temp_fd2, temp_file2 = tempfile.mkstemp()
    master_accounts_file = temp_file2
    with open(master_accounts_file, 'w') as wf:
        wf.write('\n'.join(input_master_accounts_file))
    temp_fd, temp_file = tempfile.mkstemp()
    merged_transaction_file = temp_file
    with open(merged_transaction_file, 'w') as wf:
        wf.write('\n'.join(input_transaction_summary_file))

    # prepare program parameters
    sys.argv = [
        'Backend.py',
        master_accounts_file,
        merged_transaction_file]

    # run the program
    app.main()

    # capture terminal output / errors
    # assuming that in this case we don't use stderr
    out, err = capsys.readouterr()

    # split terminal output in lines
    out_lines = out.splitlines()

    # compare terminal outputs at the end.`
    for i in range(1, len(expected_tail_of_terminal_output) + 1):
        index = i * -1
        assert expected_tail_of_terminal_output[index] == out_lines[index]

    # compare transactions:
    with open(master_accounts_file, 'r') as of:
        content = of.read().splitlines()
        for ind in range(len(content)):
            assert content[ind] == expected_new_master_account[ind]

    # clean up
    os.close(temp_fd)
    os.remove(temp_file)
    os.close(temp_fd2)
    os.remove(temp_file2)
