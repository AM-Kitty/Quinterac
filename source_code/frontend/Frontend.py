
import frontend.TransactionFile as t
import frontend.ValidAccountsFile as v
import frontend.Accountcheck as a

'''
Class Frontend:
overall bank interface to allow user to do transactions
'''


class Frontend:
    # ask for the operation selection
    def open_system(self):
        print("There are seven transaction operations:")

        # while loop used to check valid input for number selction of operation
        check_list = ["login", "logout", "create account", "delete account", "deposit", "withdraw", "transfer"]
        print(check_list)
        print()
        try:
            transaction = input("Please enter your transaction operations:")
            return transaction
        except:
            quit()

    # allow the user to choose ATM or agent mode
    def mode_check(self, transaction_list, valid_account_list, create_acct_list, use_daily_limit):
        print("\nThere are two types of mode you can login:\n")
        print('Enter [atm]: ----> for ATM mode')
        print('Enter [agent]: ----> for Agent or privileged (teller) mode\n')
        mode_name = input("Which mode do you want to login:")
        # while loop used to check valid input for mode
        while mode_name != "atm" and mode_name != "agent":
            print("\nPlease enter a valid mode!")
            mode_name = input("Which mode do you want to login:")
        print()
        self.check_trans(self.open_system(), mode_name, transaction_list, valid_account_list, create_acct_list,
                         use_daily_limit)

    # select one of the 7 operations, and call the relative function
    def check_trans(self, trans, mode_name, transaction_list, valid_account_list, create_acct_list, use_daily_limit):
        if trans == "login":
            transaction_list.append(trans)
            self.login(transaction_list, valid_account_list, create_acct_list, use_daily_limit)
        elif trans == "logout":
            transaction_list.append("EOS")
            self.logout(transaction_list, valid_account_list)
        elif trans == "create account":
            transaction_list.append("NEW")
            self.createacct(transaction_list, mode_name, valid_account_list, create_acct_list, use_daily_limit)
        elif trans == "delete account":
            transaction_list.append("DEL")
            self.deleteacct(transaction_list, mode_name, valid_account_list, create_acct_list, use_daily_limit)
        elif trans == "deposit":
            transaction_list.append("DEP")
            self.deposit(transaction_list, mode_name, valid_account_list, create_acct_list, use_daily_limit)
        elif trans == "withdraw":
            transaction_list.append("WDR")
            self.withdraw(transaction_list, mode_name, valid_account_list, create_acct_list, use_daily_limit)
        elif trans == "transfer":
            transaction_list.append("XFR")
            self.transfer(transaction_list, mode_name, valid_account_list, create_acct_list, use_daily_limit)

    # allow user to login and issue error prompt
    def login(self, transaction_list, valid_account_list, create_acct_list, use_daily_limit):
        # check if multiple login or not
        if transaction_list.count("login") > 1:
            print("\nError prompt for multiple login.")
            transaction_list.remove("login")
            return 1
        else:
            self.mode_check(transaction_list, valid_account_list, create_acct_list, use_daily_limit)

    # allow user to logout and issue error prompt
    def logout(self, transaction_list, valid_account_list):
        # can not logout before login
        if transaction_list.count("login") == 0:
            print("\nError prompt for login failed.")
            return 1
        else:
            # get transaction file from TransactionFile class
            ws = t.TransactionFile()  # construct a new instance for transaction file
            transaction_list = ws.write_trans_summry(transaction_list)
            transaction_list = []
            valid_account_list.append("0000000")
            updateFile = v.ValidAccountsFile()
            updateFile.modify_file_ValidAccount(valid_account_list)
            print("\nLog out successfully!")
            return 0

    # allow the user to create an account in different modes(agent/ATM)
    def createacct(self, transaction_list, mode, valid_account_list, create_acct_list, use_daily_limit):
        print()
        # cannot create account before login
        if transaction_list.count("login") == 0:
            print("\nError prompt for login failed")
            return 1
        else:
            # construct a new instance for transaction file
            ws = t.TransactionFile()
            accoun_check = a.AccountCheck()
            # create account in agent mode
            if mode == "atm":
                account_name = accoun_check.get_account_name()
                account_number = accoun_check.get_account_number()
                # check if account number is valid or not
                while account_number in valid_account_list:
                    print("\nShould not be same account number (account already exist)")
                    account_number = accoun_check.get_account_number()
                # add new account to the valid accounts list
                valid_account_list.append(account_number)
                create_acct_list.append(account_number)
                # add create account transaction to the transaction list
                transaction_list.append(account_number), transaction_list.append(account_name)
                transaction_list = ws.write_trans_summry(transaction_list)
                print("\nCreate an account successfully! Go back to main menu!\n")
                self.check_trans(self.open_system(), mode, transaction_list, valid_account_list, create_acct_list,
                                 use_daily_limit)
            else:
                print("\nError prompt for ATM creat account or delete account! Please enter other operations!\n")
                self.check_trans(self.open_system(), "atm", [transaction_list[0]], valid_account_list, create_acct_list,
                                 use_daily_limit)

    # allow the user to delete an account in different modes(agent/ATM)
    def deleteacct(self, transaction_list, mode, valid_account_list, create_acct_list, use_daily_limit):
        print()
        if transaction_list.count("login") == 0:
            print("\nError prompt for login failed")
            return 1
        else:
            # construct a new instance for transaction file
            ws = t.TransactionFile()
            accoun_check = a.AccountCheck()
            # delete account only in agent mode
            if mode == "atm":
                account_name = accoun_check.get_account_name()
                account_number = accoun_check.get_account_number()
                # while loop used to check for valid account number
                while account_number not in valid_account_list:
                    print("Account number not exist")
                    account_number = accoun_check.get_account_number()
                # remove account from valid accounts list
                valid_account_list.remove(account_number)
                if account_number in create_acct_list:
                    create_acct_list.remove(account_number)
                transaction_list.append(account_number), transaction_list.append(account_name)
                transaction_list = ws.write_trans_summry(transaction_list)  # account summary
                print("\nDelete an account successfully! Go back to main menu!\n")
                self.check_trans(self.open_system(), mode, transaction_list, valid_account_list, create_acct_list,
                                 use_daily_limit)
            else:
                print("\nError prompt for ATM creat account or delete account! Please enter other operations!\n")
                self.check_trans(self.open_system(), "atm", [transaction_list[0]], valid_account_list, create_acct_list,
                                 use_daily_limit)

    # allow user to deposit limited money in agent or ATM mode
    def deposit(self, transaction_list, mode, valid_account_list, create_acct_list, use_daily_limit):
        print()
        # construct a new instance for transaction file
        ws = t.TransactionFile()
        accoun_check = a.AccountCheck()
        # deposit before login
        if transaction_list.count("login") == 0:
            print("\nError! Error prompt for login failed")
            return 1
        account_number = accoun_check.get_account_number()
        # while loop used to check for valid account number
        while account_number not in valid_account_list:
            print("\nAccount not exist! Enter a exist account to deposit!")
            account_number = accoun_check.get_account_number()
        if account_number in create_acct_list:
            print("\nError! Account just create, cannot do anything!")
            return 1
        print()
        amount = accoun_check.get_amount()
        # while loop used to check for valid amount in agent or ATM mode respectively
        while amount > 2000 and mode == "atm":
            print("\nOver deposit limit, enter a valid amount!")
            amount = accoun_check.get_amount()
        while amount > 999999.99 and mode == "agent":
            print("\nOver deposit limit, enter a valid amount!")
            amount = accoun_check.get_amount()
        exist = False
        # check daily deposit limit in ATM mode
        if use_daily_limit == [] and mode == "atm":
            use_daily_limit.append([account_number, "DEP", amount])
        else:
            if mode == "atm":
                for i in range(len(use_daily_limit)):
                    if use_daily_limit[i][0] == account_number and use_daily_limit[i][1] == "DEP":
                        exist == True
                        use_daily_limit[i][2] += amount
                        if use_daily_limit[i][2] > 5000:
                            print("Error! Over daily deposit limit!")
                            return 1
            if exist == False:
                use_daily_limit.append([account_number, "DEP", amount])
        # add trnasaction operation into transaction summary file
        transaction_list.append(account_number), transaction_list.append(amount)
        transaction_list = ws.write_trans_summry(transaction_list)
        print("\nDeposit successfully! Go back to main menu!\n")
        self.check_trans(self.open_system(), mode, transaction_list, valid_account_list, create_acct_list,
                         use_daily_limit)

    # allow user to deposit limited money in agent or ATM mode
    def withdraw(self, transaction_list, mode, valid_account_list, create_acct_list, use_daily_limit):
        print()
        ws = t.TransactionFile()  # construct a new instance for transaction file
        accoun_check = a.AccountCheck()
        # error if withdraw before login
        if transaction_list.count("login") == 0:
            print("\nError prompt for login failed")
            return 1
        account_number = accoun_check.get_account_number()
        # check if the user enter the valid account number
        while account_number not in valid_account_list:
            print("\nAccount not exist! Enter a existed account to withdraw!")
            account_number = accoun_check.get_account_number()
        if account_number in create_acct_list:
            print("\nError! Account just create, cannot do anything!")
            return 1
        print()
        # check if the user enter the valid amount in ATM and agen mode respectively
        amount = accoun_check.get_amount()
        while amount > 1000 and mode == "atm":
            print("\nOver withdraw limit, enter a valid amount!")
            amount = accoun_check.get_amount()
        while amount > 999999.99 and mode == "agent":
            print("\nOver withdraw limit, enter a valid amount!")
            amount = accoun_check.get_amount()
        exist = False
        if use_daily_limit == [] and mode == "atm":
            use_daily_limit.append([account_number, "WDR", amount])
        else:
            if mode == "atm":
                for i in range(len(use_daily_limit)):
                    if use_daily_limit[i][0] == account_number and use_daily_limit[i][1] == "WDR":
                        exist = True
                        use_daily_limit[i][2] += amount
                        if use_daily_limit[i][2] > 5000:
                            print("Error! Over daily withdraw limit!")
                            return 1
                if exist == False:
                    use_daily_limit.append([account_number, "WDR", amount])
        # add the transaction operation into the transaction summary file
        transaction_list.append(account_number), transaction_list.append(amount)
        transaction_list = ws.write_trans_summry(transaction_list)
        print("\nWithdraw successfully! Go back to main menu!\n")
        self.check_trans(self.open_system(), mode, transaction_list, valid_account_list, create_acct_list,
                         use_daily_limit)

    # allow user to transfer limited money in agent or ATM mode
    def transfer(self, transaction_list, mode, valid_account_list, create_acct_list, use_daily_limit):
        print()
        accoun_check = a.AccountCheck()
        ws = t.TransactionFile()  # construct a new instance for transaction file
        # error if transfer before login
        if transaction_list.count("login") == 0:
            print("\nError prompt for login failed")
            return 1
        print("Transfer from ------>")
        account_number1 = accoun_check.get_account_number()
        print("\nTransfer to -------->")
        account_number2 = accoun_check.get_account_number()
        # check if the account numbers are both valid
        while account_number1 not in valid_account_list and account_number2 not in valid_account_list:
            print("Transfer from ------>")
            account_number1 = accoun_check.get_account_number()
            print("\nTransfer to -------->")
            account_number2 = accoun_check.get_account_number()
        if account_number1 in create_acct_list or account_number2 in create_acct_list:
            print("\nError! Account just create, cannot do anything!")
            return 1
        print()
        amount = accoun_check.get_amount()
        # check if the transfer amount is valid in ATM and agent mode respectively
        while amount > 10000 and mode == "atm":
            print("Over withdraw limit, enter a valid amount!")
            amount = accoun_check.get_amount()
        while amount > 999999.99 and mode == "agent":
            print("Over withdraw limit, enter a valid amount!")
            amount = accoun_check.get_amount()
        exist = False
        if use_daily_limit == [] and mode == "atm":
            use_daily_limit.append([account_number1, "XFR", amount])
        else:
            if mode == "m":
                for i in range(len(use_daily_limit)):
                    if use_daily_limit[i][0] == account_number1 and use_daily_limit[i][1] == "XFR":
                        exist = True
                        use_daily_limit[i][2] += amount
                        if use_daily_limit[i][2] > 10000:
                            print("\nError! Over daily transfer limit!")
                            return 1
            if exist == False:
                use_daily_limit.append([account_number1, "XFR", amount])
        # add the transfer transaction operation in to the transaction summary file
        transaction_list.append(account_number1), transaction_list.append(amount), transaction_list.append(
            account_number2)
        transaction_list = ws.write_trans_summry(transaction_list)
        print("\nTransfer successfully! Go back to main menu!\n")
        self.check_trans(self.open_system(), mode, transaction_list, valid_account_list, create_acct_list,
                         use_daily_limit)


def main():
    print("Welcome to bank system!!!!\n")
    filedata = v.ValidAccountsFile()
    valid_account_list = filedata.readfile_ValidAccount()
    transaction_list = []
    create_acct_list = []
    use_daily_limit = []
    current_mode = None  # Not login, mode not start yet
    front = Frontend()
    front.check_trans(front.open_system(), current_mode, transaction_list, valid_account_list, create_acct_list, use_daily_limit)
