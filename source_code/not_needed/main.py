#This is the main function for test.

import Frontend as f
import ValidAccountsFile as v


if __name__ == '__main__':
    print("Welcome to bank system!!!!\n")
    filedata = v.ValidAccountsFile()
    valid_account_list = filedata.readfile_ValidAccount()
    transaction_list = []
    create_acct_list = []
    use_daily_limit = []
    current_mode = None  # Not login, mode not start yet
    front = f.Frontend()
    front.check_trans(front.open_system(), current_mode, transaction_list, valid_account_list, create_acct_list, use_daily_limit)


