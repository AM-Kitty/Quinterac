import os
import sys
import tempfile
from importlib import reload

import src.Backend as app

path = os.path.dirname(os.path.abspath(__file__))
# white box testing
# decision coverage and block coverage test cases for withdraw
#-----------------------------------------------------------
#---------------------- withdraw ----------------------------
#-----------------------------------------------------------

# -----------------T1(decision)--------------------
# decision point at 1: when 1 is true-> i[0] == "WDR"
def test_1(capsys):
    helper(capsys,
           input_transaction_summary_file=['WDR 1234567 100000 0000000 Theo\n', 'EOS 0000000 000 0000000 ***'],
           input_master_accounts_file=["1234567 200000 Theo"],
           expected_new_master_account=["1234567 100000 Theo"],
           expected_tail_of_terminal_output=["New Valid Accounts File created successfully!"]
           )

# -----------------T2(decision)--------------------
# decision point at 1: when 1 is false-> i[0] != "WDR"
def test_2(capsys):
    helper(capsys,
           input_transaction_summary_file=['DEP 1234567 100000 0000000 Theo\n', 'EOS 0000000 000 0000000 ***'],
           input_master_accounts_file=["1234567 200000 Theo"],
           expected_new_master_account=["1234567 300000 Theo"],
           expected_tail_of_terminal_output=["New Valid Accounts File created successfully!"]
           )

# -----------------T3(decision)--------------------
# decision point at 2: when 2 is false-> "1122334" (the account number does not exist)
# terminate and output nothing
def test_3(capsys):
    helper(capsys,
           input_transaction_summary_file=['WDR 1122334 100000 0000000 Theo\n', 'EOS 0000000 000 0000000 ***'],
           input_master_accounts_file=["1234567 200000 Theo"],
           expected_new_master_account=["1234567 200000 Theo"],
           expected_tail_of_terminal_output=['Error! 1122334 not in the master account file!']
           )

# -----------------T4(decision)--------------------
# decision point at 3: when 3 is true-> amount < 0 (the balance is negative)
# print error message and terminate
def test_4(capsys):
    helper(capsys,
           input_transaction_summary_file=['WDR 1234567 300000 0000000 Theo\n', 'EOS 0000000 000 0000000 ***'],
           input_master_accounts_file=["1234567 100000 Theo"],
           expected_new_master_account=["1234567 100000 Theo"],
           expected_tail_of_terminal_output=["Error! 1234567 have a negative balance!"]
           )

# -----------------T5(decision)-----------------------------
# decision point at 7: when 7 is true-> len(line) > 47
def test_9(capsys):
    helper(capsys,
           input_transaction_summary_file=['WDR 2233445 100000 0000000 KellyKellyKellyKe\n', 'EOS 0000000 000 0000000 ***'],
           input_master_accounts_file=["2233445 12345678901234567890123 KellyKellyKellyKe"],
           expected_new_master_account=["2233445 12345678901234567890123 KellyKellyKellyKe"],
           expected_tail_of_terminal_output=["Error! Each line is at most 47 characters!"]
           )

# -----------------T6(decision)-----------------------------
# decision point at 7: when 7 is false-> len(line) <= 47
def test_10(capsys):
    helper(capsys,
           input_transaction_summary_file=['WDR 2233445 100000 0000000 KellyKellyKellyKe\n', 'EOS 0000000 000 0000000 ***'],
           input_master_accounts_file=["2233445 1234567890123456789 KellyKellyKellyKe"],
           expected_new_master_account=["2233445 1234567890123356789 KellyKellyKellyKe"],
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
