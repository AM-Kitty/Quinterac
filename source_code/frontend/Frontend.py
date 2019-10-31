
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
        check_list = ["login", "logout", "create account", "delete account", "deposit", "withdraw", "transfer"]
        print(check_list)
        print()
        transaction = input("Please enter your transaction operations:")
        while transaction.lower() not in check_list:
            print("Enter a valid transaction operation!")
            transaction = input("Please enter your transaction operations:")
        return transaction

    # allow the user to choose machine or agent mode
    def mode_check(self, transaction_list, valid_account_list, create_acct_list, use_daily_limit):
        print("\nThere have two types of session you can login:\n")
        print('Enter [atm]: ----> for ATM mode')
        print('Enter [agent]: ----> for Agent or privileged (teller) mode\n')
        mode_name = input("What kind of a type of session do you want login:")
        while mode_name.lower() != "atm" and mode_name.lower() != "agent":
            print("Please enter a valid mode!")
            mode_name = input("What kind of a type of session do you want login:")
        print()
        self.check_trans(self.open_system(), mode_name, transaction_list, valid_account_list, create_acct_list,
                         use_daily_limit)

    # select the 7 operations, and call the relative function
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


    # login function; prompt error if login again after login
    def login(self, transaction_list, valid_account_list, create_acct_list, use_daily_limit):
        if transaction_list.count("login") > 1:
            print("Error! Error prompt for multiple login")
            transaction_list.remove("login")
            return 1
        else:
            self.mode_check(transaction_list, valid_account_list, create_acct_list, use_daily_limit)

    # logout function
    def logout(self, transaction_list, valid_account_list):
        if transaction_list.count("login") == 0:  # can not logout before login
            print("Error! Error prompt for login failed")
            return 1
        else:
            ws = t.TransactionFile()
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
        if transaction_list.count("login") == 0:
            print("Error! Error prompt for login failed")
            return 1
        else:
            ws = t.TransactionFile()
            accoun_check = a.AccountCheck()
            if mode == "agent":
                account_name = accoun_check.get_account_name()
                account_number = accoun_check.get_account_number()
                while account_number in valid_account_list:  # while
                    print("Should not be same account number (account already exist)")
                    account_number = accoun_check.get_account_number()

                valid_account_list.append(account_number)
                create_acct_list.append(account_number)

                transaction_list.append(account_number), transaction_list.append(account_name)
                transaction_list = ws.write_trans_summry(transaction_list)  # account summary

                print("\nCreate an account successfully! Go back to main menu!\n")
                self.check_trans(self.open_system(), mode, transaction_list, valid_account_list, create_acct_list,
                                 use_daily_limit)
            else:
                print("Error prompt for ATM creat account or delete account! Please enter other operations!\n")
                self.check_trans(self.open_system(), "m", [transaction_list[0]], valid_account_list, create_acct_list,
                                 use_daily_limit)

    # allow the user to delete an account in different modes(agent/ATM)
    def deleteacct(self, transaction_list, mode, valid_account_list, create_acct_list, use_daily_limit):
        print()
        if transaction_list.count("login") == 0:
            print("Error! Error prompt for login failed")
            return 1
        else:
            ws = t.TransactionFile()
            accoun_check = a.AccountCheck()
            if mode == "agent":
                account_name = accoun_check.get_account_name()
                account_number = accoun_check.get_account_number()
                while account_number not in valid_account_list:  # while
                    print("Account number not exist")
                    account_number = accoun_check.get_account_number()

                valid_account_list.remove(account_number)
                if account_number in create_acct_list:
                    create_acct_list.remove(account_number)
                transaction_list.append(account_number), transaction_list.append(account_name)
                transaction_list = ws.write_trans_summry(transaction_list)  # account summary
                print("\nDelete an account successfully! Go back to main menu!\n")
                self.check_trans(self.open_system(), mode, transaction_list, valid_account_list, create_acct_list,
                                 use_daily_limit)
            else:
                print("Error prompt for ATM creat account or delete account! Please enter other operations!\n")
                self.check_trans(self.open_system(), "m", [transaction_list[0]], valid_account_list, create_acct_list,
                                 use_daily_limit)

    # allow user to deposit limited money in agent or ATM mode
    def deposit(self, transaction_list, mode, valid_account_list, create_acct_list, use_daily_limit):
        print()
        ws = t.TransactionFile()
        accoun_check = a.AccountCheck()

        if transaction_list.count("login") == 0:
            print("Error! Error prompt for login failed")
            return 1

        account_number = accoun_check.get_account_number()
        while account_number not in valid_account_list:
            print("Account not exist! Enter a exist account to deposit!")
            account_number = accoun_check.get_account_number()
        if account_number in create_acct_list:
            print("Error! Account just create, cannot do anything!")
            return 1

        print()
        amount = accoun_check.get_amount()
        while amount > 2000 and mode == "atm":
            print("Over deposit limit, enter a valid amount!")
            amount = accoun_check.get_amount()

        while amount > 999999.99 and mode == "agent":
            print("Over deposit limit, enter a valid amount!")
            amount = accoun_check.get_amount()

        exist = False
        if use_daily_limit == [] and mode == "atm":
            use_daily_limit.append([account_number, "DEP", amount])
        else:
            if mode == "m":
                for i in range(len(use_daily_limit)):
                    if use_daily_limit[i][0] == account_number and use_daily_limit[i][1] == "DEP":
                        exist == True
                        use_daily_limit[i][2] += amount
                        if use_daily_limit[i][2] > 5000:
                            print("Error! Over daily deposit limit!")
                            return 1
            if exist == False:
                use_daily_limit.append([account_number, "DEP", amount])

        transaction_list.append(account_number), transaction_list.append(amount)
        transaction_list = ws.write_trans_summry(transaction_list)
        print("\nDeposit successfully! Go back to main menu!\n")

        self.check_trans(self.open_system(), mode, transaction_list, valid_account_list, create_acct_list,
                         use_daily_limit)

    # allow user to deposit limited money in agent or ATM mode
    def withdraw(self, transaction_list, mode, valid_account_list, create_acct_list, use_daily_limit):
        print()
        ws = t.TransactionFile()
        accoun_check = a.AccountCheck()

        if transaction_list.count("login") == 0:
            print("Error! Error prompt for login failed")
            return 1
        account_number = accoun_check.get_account_number()
        while account_number not in valid_account_list:
            print("Account not exist! Enter a exist account to deposit!")
            account_number = accoun_check.get_account_number()
        if account_number in create_acct_list:
            print("Error! Account just create, cannot do anything!")
            return 1

        print()
        amount = accoun_check.get_amount()
        while amount > 1000 and mode == "atm":
            print("Over withdraw limit, enter a valid amount!")
            amount = accoun_check.get_amount()
        while amount > 999999.99 and mode == "agent":
            print("Over withdraw limit, enter a valid amount!")
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

        transaction_list.append(account_number), transaction_list.append(amount)
        transaction_list = ws.write_trans_summry(transaction_list)
        print("\nWithdraw successfully! Go back to main menu!\n")

        self.check_trans(self.open_system(), mode, transaction_list, valid_account_list, create_acct_list,
                         use_daily_limit)

    # allow user to transfer limited money in agent or ATM mode
    def transfer(self, transaction_list, mode, valid_account_list, create_acct_list, use_daily_limit):
        print()
        accoun_check = a.AccountCheck()
        ws = t.TransactionFile()

        if transaction_list.count("login") == 0:
            print("Error! Error prompt for login failed")
            return 1
        print("Transfer from ------>")
        account_number1 = accoun_check.get_account_number()
        print("\nTransfer to -------->")
        account_number2 = accoun_check.get_account_number()

        while account_number1 not in valid_account_list and account_number2 not in valid_account_list:
            print("Transfer from ------>")
            account_number1 = accoun_check.get_account_number()
            print("\nTransfer to -------->")
            account_number2 = accoun_check.get_account_number()

        if account_number1 in create_acct_list or account_number2 in create_acct_list:
            print("Error! Account just create, cannot do anything!")
            return 1

        print()
        amount = accoun_check.get_amount()
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
                            print("Error! Over daily transfer limit!")
                            return 1
            if exist == False:
                use_daily_limit.append([account_number1, "XFR", amount])

        transaction_list.append(account_number1), transaction_list.append(amount), transaction_list.append(account_number2)
        transaction_list = ws.write_trans_summry(transaction_list)
        print("\nTransfer successfully! Go back to main menu!\n")
        self.check_trans(self.open_system(), mode, transaction_list, valid_account_list, create_acct_list,use_daily_limit)


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