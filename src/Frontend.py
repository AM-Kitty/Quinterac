import TransactionFile as t
import ValidAccountsFile as v
import Accountcheck as a
import sys


class Frontend:
    # ask for the operation selection
    @staticmethod
    def open_system():
        # print("There are seven transaction operations:\n")

        # while loop used to check valid input for number selction of operation
        check_list = ["login", "logout", "createacct", "deleteacct", "deposit", "withdraw", "transfer"]
        # print(check_list)
        try:
            transaction = str(input("Please enter your transaction operations:"))
            while transaction.lower() not in check_list:
                print("\nEnter a valid transaction operation!")
                transaction = input("Please enter your transaction operations:")
            return transaction
        except EOFError:
            quit

    # allow the user to choose ATM or agent mode
    def mode_check(self, transaction_list, valid_account_list, create_acct_list, use_daily_limit):
        print("\nThere are two types of mode you can login:\n")
        print('Enter [atm]: ----> for ATM mode')
        print('Enter [agent]: ----> for Agent or privileged (teller) mode\n')
        try:
            mode_name = input("Which mode do you want to login:")
            # while loop used to check valid input for mode
            while mode_name != "atm" and mode_name != "agent":
                print("\nPlease enter a valid mode!")
                mode_name = input("Which mode do you want to login:")
            print("")
            self.check_trans(self.open_system(), mode_name, transaction_list, valid_account_list, create_acct_list,
                             use_daily_limit)
        except EOFError:
            quit

    # select one of the 7 operations, and call the relative function
    def check_trans(self, trans, mode_name, transaction_list, valid_account_list, create_acct_list, use_daily_limit):
        if trans == "login":
            transaction_list.append(trans)
            if mode_name is not None:
                self.login(transaction_list, valid_account_list, create_acct_list, use_daily_limit, mode_name)
            else:
                self.login(transaction_list, valid_account_list, create_acct_list, use_daily_limit, None)
        elif trans == "logout":
            transaction_list.append("EOS")
            self.logout(transaction_list, valid_account_list, create_acct_list, use_daily_limit)
        elif trans == "createacct":
            transaction_list.append("NEW")
            self.createacct(transaction_list, mode_name, valid_account_list, create_acct_list, use_daily_limit)
        elif trans == "deleteacct":
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
    def login(self, transaction_list, valid_account_list, create_acct_list, use_daily_limit, mode):
        # check if multiple login or not
        if transaction_list.count("login") > 1:
            print("\nError prompt for multiple login.")
            transaction_list.remove("login")
            self.check_trans(self.open_system(), mode, transaction_list, valid_account_list, create_acct_list,
                             use_daily_limit)
        else:
            self.mode_check(transaction_list, valid_account_list, create_acct_list, use_daily_limit)

    # allow user to logout and issue error prompt
    def logout(self, transaction_list, valid_account_list, create_acct_list, use_daily_limit):
        # can not logout before login
        if transaction_list.count("login") == 0:
            print("\nError prompt for login failed.")
            self.check_trans(self.open_system(), None, transaction_list, valid_account_list, create_acct_list,
                             use_daily_limit)
        else:
            # get transaction file from TransactionFile class
            ws = t.TransactionFile()  # construct a new instance for transaction file
            ws.write_trans_summary(transaction_list, sys.argv[2])
            transaction_list = []
            # valid_account_list.append("0000000")
            # if valid_account_list.count("0000000") > 1:
            #     valid_account_list.remove("0000000")
            # updateFile = v.ValidAccountsFile()
            # updateFile.modify_file_ValidAccount(valid_account_list)
            print("\nLog out successfully!\n")
            #self.check_trans(self.open_system(), None, transaction_list, valid_account_list, create_acct_list,use_daily_limit)
            return True

    # allow the user to create an account in different modes(agent/ATM)
    def createacct(self, transaction_list, mode, valid_account_list, create_acct_list, use_daily_limit):
        print("")
        # cannot create account before login
        if transaction_list.count("login") == 0:
            print("\nError prompt for login failed")
            return 1
        else:
            # construct a new instance for transaction file
            ws = t.TransactionFile()
            account_check = a.AccountCheck()
            # create account in agent mode
            if mode == "agent":
                account_name = account_check.get_account_name()
                account_number = account_check.get_account_number()
                # check if account number is valid or not
                while account_number in valid_account_list:
                    print("\nShould not be same account number (account already exist)")
                    account_number = account_check.get_account_number()
                # add new account to the valid accounts list
                valid_account_list.append(account_number)
                create_acct_list.append(account_number)
                # add create account transaction to the transaction list
                transaction_list.append(account_number), transaction_list.append(account_name)
                transaction_list = ws.write_trans_summary(transaction_list, sys.argv[2])
                print("\nCreate an account successfully! Go back to main menu!\n")
                self.check_trans(self.open_system(), mode, transaction_list, valid_account_list, create_acct_list,
                                 use_daily_limit)
            else:
                print("\nError prompt for ATM create account or delete account! Please enter other operations!\n")
                self.check_trans(self.open_system(), "atm", [transaction_list[0]], valid_account_list, create_acct_list,
                                 use_daily_limit)

    # allow the user to delete an account in different modes(agent/ATM)
    def deleteacct(self, transaction_list, mode, valid_account_list, create_acct_list, use_daily_limit):
        print("")
        if transaction_list.count("login") == 0:
            print("\nError prompt for login failed")
            return 1
        else:
            # construct a new instance for transaction file
            ws = t.TransactionFile()
            account_check = a.AccountCheck()
            # delete account only in agent mode
            if mode == "agent":
                account_name = account_check.get_account_name()
                account_number = account_check.get_account_number()
                # while loop used to check for valid account number
                while account_number not in valid_account_list:
                    print("Account number not exist")
                    account_number = account_check.get_account_number()
                # remove account from valid accounts list
                valid_account_list.remove(account_number)
                if account_number in create_acct_list:
                    create_acct_list.remove(account_number)
                transaction_list.append(account_number), transaction_list.append(account_name)
                transaction_list = ws.write_trans_summary(transaction_list, sys.argv[2])  # account summary
                print("\nDelete an account successfully! Go back to main menu!\n")
                self.check_trans(self.open_system(), mode, transaction_list, valid_account_list, create_acct_list,
                                 use_daily_limit)
            else:
                print("\nError prompt for ATM create account or delete account! Please enter other operations!\n")
                self.check_trans(self.open_system(), "atm", [transaction_list[0]], valid_account_list, create_acct_list,
                                 use_daily_limit)

    # allow user to deposit limited money in agent or ATM mode
    def deposit(self, transaction_list, mode, valid_account_list, create_acct_list, use_daily_limit):
        print("")
        # construct a new instance for transaction file
        ws = t.TransactionFile()
        account_check = a.AccountCheck()
        # deposit before login
        if transaction_list.count("login") == 0:
            print("\nError! Error prompt for login failed")
            return 1
        account_number = account_check.get_account_number()
        # while loop used to check for valid account number
        while account_number not in valid_account_list:
            print("\nAccount not exist! Enter a exist account to deposit!")
            account_number = account_check.get_account_number()
        if account_number in create_acct_list:
            print("\nError! Account just create, cannot do anything!")
            return 1
        print("")
        amount = account_check.get_amount()
        # while loop used to check for valid amount in agent or ATM mode respectively
        while amount > 2000 and mode == "atm":
            print("\nOver deposit limit, enter a valid amount!")
            amount = account_check.get_amount()
        while amount > 999999.99 and mode == "agent":
            print("\nOver deposit limit, enter a valid amount!")
            amount = account_check.get_amount()
        exist = False
        # check daily deposit limit in ATM mode
        if use_daily_limit == [] and mode == "atm":
            use_daily_limit.append([account_number, "DEP", amount])
        else:
            if mode == "atm":
                for i in range(len(use_daily_limit)):
                    if use_daily_limit[i][0] == account_number and use_daily_limit[i][1] == "DEP":
                        exist = True
                        use_daily_limit[i][2] += amount
                        if use_daily_limit[i][2] > 5000:
                            print("\nError! Over daily deposit limit!")
                            return 1
            if not exist:
                use_daily_limit.append([account_number, "DEP", amount])
        # add transaction operation into transaction summary file
        transaction_list.append(account_number), transaction_list.append(int(amount * 100))
        transaction_list = ws.write_trans_summary(transaction_list, sys.argv[2])
        print("\nDeposit successfully! Go back to main menu!\n")
        self.check_trans(self.open_system(), mode, transaction_list, valid_account_list, create_acct_list,
                         use_daily_limit)

    # allow user to deposit limited money in agent or ATM mode
    def withdraw(self, transaction_list, mode, valid_account_list, create_acct_list, use_daily_limit):
        print("")
        ws = t.TransactionFile()  # construct a new instance for transaction file
        account_check = a.AccountCheck()
        # error if withdraw before login
        if transaction_list.count("login") == 0:
            print("\nError prompt for login failed")
            return 1
        account_number = account_check.get_account_number()
        # check if the user enter the valid account number
        while account_number not in valid_account_list:
            print("\nAccount not exist! Enter a existed account to withdraw!")
            account_number = account_check.get_account_number()
        if account_number in create_acct_list:
            print("\nError! Account just create, cannot do anything!")
            return 1
        print("")
        # check if the user enter the valid amount in ATM and agen mode respectively
        amount = account_check.get_amount()
        while amount > 1000 and mode == "atm":
            print("\nOver ATM withdraw per time limit, enter a valid amount!")
            amount = account_check.get_amount()
        while amount > 999999.99 and mode == "agent":
            print("\nOver withdraw limit, enter a valid amount!")
            amount = account_check.get_amount()
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
                if not exist:
                    use_daily_limit.append([account_number, "WDR", amount])
        # add the transaction operation into the transaction summary file
        transaction_list.append(account_number), transaction_list.append(int(amount * 100))
        transaction_list = ws.write_trans_summary(transaction_list, sys.argv[2])
        print("\nWithdraw successfully! Go back to main menu!\n")
        self.check_trans(self.open_system(), mode, transaction_list, valid_account_list, create_acct_list,
                         use_daily_limit)

    # allow user to transfer limited money in agent or ATM mode
    def transfer(self, transaction_list, mode, valid_account_list, create_acct_list, use_daily_limit):
        print("")
        account_check = a.AccountCheck()
        ws = t.TransactionFile()  # construct a new instance for transaction file
        # error if transfer before login
        if transaction_list.count("login") == 0:
            print("\nError prompt for login failed")
            return 1

        print("Transfer from ------>")
        account_number1 = account_check.get_account_number()

        while account_number1 not in valid_account_list:
            print("Account not exist! Enter a exist account to transfer!")
            print("Transfer from ------>")
            account_number1 = account_check.get_account_number()

        print("\nTransfer to -------->")
        account_number2 = account_check.get_account_number()
        while account_number2 not in valid_account_list:
            print("Account not exist! Enter a exist account to transfer!")
            print("Transfer to -------->")
            account_number2 = account_check.get_account_number()

        if account_number1 in create_acct_list or account_number2 in create_acct_list:
            print("\nError! Account just create, cannot do anything!")
            return 1
        print("")
        amount = account_check.get_amount()
        # check if the transfer amount is valid in ATM and agent mode respectively
        while amount > 10000 and mode == "atm":
            print("\nOver ATM transfer daily limit, enter a valid amount!")
            amount = account_check.get_amount()
        while amount > 999999.99 and mode == "agent":
            print("\nOver agent transfer daily limit, enter a valid amount!")
            amount = account_check.get_amount()
        exist = False
        if use_daily_limit == [] and mode == "atm":
            use_daily_limit.append([account_number1, "XFR", amount])
        else:
            if mode == "atm":
                for i in range(len(use_daily_limit)):
                    if use_daily_limit[i][0] == account_number1 and use_daily_limit[i][1] == "XFR":
                        exist = True
                        use_daily_limit[i][2] += amount
                        if use_daily_limit[i][2] > 10000:
                            print("\nError! Over atm daily transfer limit!")
                            return 1
            if not exist:
                use_daily_limit.append([account_number1, "XFR", amount])
        # add the transfer transaction operation in to the transaction summary file
        transaction_list.append(account_number1), transaction_list.append(int(amount * 100)), transaction_list.append(
            account_number2)
        transaction_list = ws.write_trans_summary(transaction_list, sys.argv[2])
        print("\nTransfer successfully! Go back to main menu!\n")
        self.check_trans(self.open_system(), mode, transaction_list, valid_account_list, create_acct_list,
                         use_daily_limit)


def main():
    print("Welcome to bank system!!!!\n")
    file_data = v.ValidAccountsFile()
    valid_account_list = file_data.readfile_ValidAccount(sys.argv[1])
    # transaction_list = []
    # create_acct_list = []
    # use_daily_limit = []
    # current_mode = None  # Not login, mode not start yet
    front = Frontend()
    front.check_trans(front.open_system(), None, [], valid_account_list, [], [])


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Invalid input, must include "ValidAccountListFile.txt TransactionSummaryFile.txt"')
        sys.exit(1)
    main()
