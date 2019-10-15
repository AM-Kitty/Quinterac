"""
CISC 327
Banking System
Assignment 2
Scarlet FlashView
"""

import sys

# ask for the operation selection
def open_system():
    print("There have seven transaction operations:")
    print("1: login")
    print("2: logout")
    print("3: creat account")
    print("4: delete account")
    print("5: deposit")
    print("6: withdraw")
    print("7: transfer")
    while True:
        transaction = input("Please enter your transaction operations number:")
        try:
            transaction = int(transaction)
            if transaction < 1 or transaction > 7:
                print("Enter a valid number!")
            else:
                return transaction
        except ValueError:
            print("Enter a valid number!")


# select the 7 operations, and call the relative function
def check_trans(trans, mode_name, transaction_list, valid_account_list, create_acct_list, use_daily_limit):
    if trans == 1:
        transaction_list.append(trans)
        login(transaction_list, valid_account_list)
    elif trans == 2:
        transaction_list.append("EOS")
        logout(transaction_list, valid_account_list)
    elif trans == 3:
        transaction_list.append("NEW")
        createacct(transaction_list, mode_name, valid_account_list, create_acct_list)
    elif trans == 4:
        transaction_list.append("DEL")
        deleteacct(transaction_list, mode_name, valid_account_list, create_acct_list)
    elif trans == 5:
        transaction_list.append("DEP")
        deposit(transaction_list, mode_name, valid_account_list, create_acct_list, use_daily_limit)
    elif trans == 6:
        transaction_list.append("WDR")
        withdraw(transaction_list, mode_name, valid_account_list, create_acct_list, use_daily_limit)
    elif trans == 7:
        transaction_list.append("XFR")
        transfer(transaction_list, mode_name, valid_account_list, create_acct_list, use_daily_limit)


def mode_check(transaction_list, valid_account_list):
    print("\nThere have two types of session you can login:\n")
    print('Enter [m]: ----> for ATM mode')
    print('Enter [a]: ----> for Agent or privileged (teller) mode\n')
    mode_name = input("What kind of a type of session do you want login:")
    while mode_name != "m" and mode_name != "a":
        print("Please enter a valid mode!")
        mode_name = input("What kind of a type of session do you want login:")
    print()
    check_trans(open_system(), mode_name, transaction_list, valid_account_list, create_acct_list, use_daily_limit)


# login function; prompt error if login again after login
def login(transaction_list, valid_account_list):
    if transaction_list.count(1) > 1:
        print("Error! Error prompt for multiple login")
        transaction_list.remove(1)
        return 1
    else:
        mode_check(transaction_list, valid_account_list)


# logout function
def logout(transaction_list, valid_account_list):
    if transaction_list.count(1) == 0:  # can not logout before login
        print("Error! Error prompt for login failed")
        return 1
    else:
        transaction_list = write_trans_summry(transaction_list)
        transaction_list = []
        valid_account_list.append("0000000")
        modify_file_ValidAccount(valid_account_list)
        print("\nLog out successfully!")
        return 0


# allow the user to create an account in different modes(agent/ATM)
def createacct(transaction_list, mode, valid_account_list, create_acct_list):
    print()
    if transaction_list.count(1) == 0:
        print("Error! Error prompt for login failed")
        return 1
    else:
        if mode == "a":
            account_name = get_account_name()
            account_number = get_account_number()
            while account_number in valid_account_list:  # while
                print("Should not be same account number (account already exist)")
                account_number = get_account_number()

            valid_account_list.append(account_number)
            create_acct_list.append(account_number)

            transaction_list.append(account_number), transaction_list.append(account_name)
            transaction_list = write_trans_summry(transaction_list)  # account summary

            print("\nCreate an account successfully! Go back to main menu!\n")
            check_trans(open_system(), mode, transaction_list, valid_account_list, create_acct_list,use_daily_limit)
        else:
            print("Error prompt for ATM creat account or delete account! Please enter other operations!\n")
            check_trans(open_system(), "m", [transaction_list[0]], valid_account_list, create_acct_list, use_daily_limit)


# allow the user to delete an account in different modes(agent/ATM)
def deleteacct(transaction_list, mode, valid_account_list, create_acct_list):
    print()
    if transaction_list.count(1) == 0:
        print("Error! Error prompt for login failed")
        return 1
    else:
        if mode == "a":
            account_name = get_account_name()
            account_number = get_account_number()
            while account_number not in valid_account_list:  # while
                print("Account number not exist")
                account_number = get_account_number()

            valid_account_list.remove(account_number)
            if account_number in create_acct_list:
                create_acct_list.remove(account_number)
            transaction_list.append(account_number), transaction_list.append(account_name)
            transaction_list = write_trans_summry(transaction_list)  # account summary
            print("\nDelete an account successfully! Go back to main menu!\n")
            check_trans(open_system(), mode, transaction_list, valid_account_list, create_acct_list, use_daily_limit)
        else:
            print("Error prompt for ATM creat account or delete account! Please enter other operations!\n")
            check_trans(open_system(), "m", [transaction_list[0]], valid_account_list, create_acct_list, use_daily_limit)


# allow user to deposit limited money in agent or ATM mode
def deposit(transaction_list, mode, valid_account_list, create_acct_list, use_daily_limit):
    print()
    if transaction_list.count(1) == 0:
        print("Error! Error prompt for login failed")
        return 1

    account_number = get_account_number()
    while account_number not in valid_account_list:
        print("Account not exist! Enter a exist account to deposit!")
        account_number = get_account_number()
    if account_number in create_acct_list:
        print("Error! Account just create, cannot do anything!")
        return 1

    print()
    amount = get_amount()
    while amount > 2000 and mode == "m":
        print("Over deposit limit, enter a valid amount!")
        amount = get_amount()

    while amount > 999999.99 and mode == "a":
        print("Over deposit limit, enter a valid amount!")
        amount = get_amount()

    if use_daily_limit == [] and mode == "m":
        use_daily_limit.append([account_number, "DEP", amount])
    else:
        if mode == "m":
            for i in range(len(use_daily_limit)):
                if use_daily_limit[i][0] == account_number and use_daily_limit[i][1] == "DEP":
                    use_daily_limit[i][2] += amount
                    if use_daily_limit[i][2] > 5000:
                        print("Error! Over daily deposit limit!")
                        return 1
            use_daily_limit.append([account_number, "DEP", amount])


    transaction_list.append(account_number), transaction_list.append(amount)
    transaction_list = write_trans_summry(transaction_list)
    print("\nDeposit successfully! Go back to main menu!\n")

    check_trans(open_system(), mode, transaction_list, valid_account_list, create_acct_list, use_daily_limit)


# allow user to deposit limited money in agent or ATM mode
def withdraw(transaction_list, mode, valid_account_list, create_acct_list, use_daily_limit):
    print()
    if transaction_list.count(1) == 0:
        print("Error! Error prompt for login failed")
        return 1
    account_number = get_account_number()
    while account_number not in valid_account_list:
        print("Account not exist! Enter a exist account to deposit!")
        account_number = get_account_number()
    if account_number in create_acct_list:
        print("Error! Account just create, cannot do anything!")
        return 1
    print()   # daily limit
    amount = get_amount()
    while amount > 1000 and mode == "m":
        print("Over withdraw limit, enter a valid amount!")
        amount = get_amount()
    while amount > 999999.99 and mode == "a":
        print("Over withdraw limit, enter a valid amount!")
        amount = get_amount()

    if use_daily_limit == [] and mode == "m":
        use_daily_limit.append([account_number, "WDR", amount])
    else:
        if mode == "m":
            for i in range(len(use_daily_limit)):
                if use_daily_limit[i][0] == account_number and use_daily_limit[i][1] == "WDR":
                    use_daily_limit[i][2] += amount
                    if use_daily_limit[i][2] > 5000:
                        print("Error! Over daily withdraw limit!")
                        return 1
            use_daily_limit.append([account_number, "WDR", amount])


    transaction_list.append(account_number), transaction_list.append(amount)
    transaction_list = write_trans_summry(transaction_list)
    print("\nWithdraw successfully! Go back to main menu!\n")

    check_trans(open_system(), mode, transaction_list, valid_account_list, create_acct_list, use_daily_limit)


# allow user to transfer limited money in agent or ATM mode
def transfer(transaction_list, mode, valid_account_list, create_acct_list, use_daily_limit):
    print()
    if transaction_list.count(1) == 0:
        print("Error! Error prompt for login failed")
        return 1
    print("Transfer from ------>")
    account_number1 = get_account_number()
    print("\nTransfer to -------->")
    account_number2 = get_account_number()

    while account_number1 not in valid_account_list and account_number2 not in valid_account_list:
        print("Transfer from ------>")
        account_number1 = get_account_number()
        print("\nTransfer to -------->")
        account_number2 = get_account_number()

    if account_number1 in create_acct_list or account_number2 in create_acct_list:
        print("Error! Account just create, cannot do anything!")
        return 1

    print()
    amount = get_amount()
    while amount > 10000 and mode == "m":
        print("Over withdraw limit, enter a valid amount!")
        amount = get_amount()
    while amount > 999999.99 and mode == "a":
        print("Over withdraw limit, enter a valid amount!")
        amount = get_amount()

    if use_daily_limit == [] and mode == "m":
        use_daily_limit.append([account_number1, "XFR", amount])
    else:
        if mode == "m":
            for i in range(len(use_daily_limit)):
                if use_daily_limit[i][0] == account_number1 and use_daily_limit[i][1] == "XFR":
                    use_daily_limit[i][2] += amount
                    if use_daily_limit[i][2] > 10000:
                        print("Error! Over daily transfer limit!")
                        return 1
            use_daily_limit.append([account_number1, "XFR", amount])

    transaction_list.append(account_number1), transaction_list.append(amount), transaction_list.append(account_number2)
    transaction_list = write_trans_summry(transaction_list)
    print("\nTransfer successfully! Go back to main menu!\n")
    check_trans(open_system(), mode, transaction_list, valid_account_list, create_acct_list, use_daily_limit)


# get input of deposit or transfer amount from user
def get_amount():
    while True:
        amount = input("Enter your amount:")  # number check
        try:
            amount = float(amount)
            return amount
        except ValueError:
            print("Enter a valid amount!")


# get the input for account number from user
def get_account_number():
    while True:
        account_number = input("Enter your account number:")
        if not account_number.isdigit():
            print("Please enter a valid digit number!")
        elif len(account_number) != 7:
            print("Please enter a valid account number! (Only 7 digits)")
        else:
            if account_number[0] == "0":
                print("Account number first digit cannot be zero!")
            try:
                account_number = int(account_number)
                if len(str(account_number)) == 7:
                    return account_number
            except:
                print("Please enter a valid account number!")


# get the input for account name from user
def get_account_name():
    while True:
        account_name = input("Enter your account name:")
        if 2 < len(account_name) < 31:
            if account_name[0] != " " and account_name[-1] != " ":
                return account_name
            else:
                print("Enter a valid account name(no space for beginning or ending)!")
        else:
            print("Enter a valid account name!")


# read file from ValidAccountList file which contains a list of valid account number
# convert it into a list form
def readfile_ValidAccount():
    try:
        file_data = open("ValidAccountListFile.txt", "r")
        data = file_data.readlines()  # list type
        data = [int(i[:-1]) for i in data]
        return data[:-1]
    except OSError as error:
        print(error)
        sys.exit(1)


def write_trans_summry(transaction_list):
    newsummary = ""
    space = " "
    try:
        file_data = open("TransactionSummaryFile.txt", "a")

        if transaction_list[1] == "DEP":
            newsummary += (transaction_list[1] + space)
            newsummary += (str(transaction_list[2]) + space)
            newsummary += (str(transaction_list[3]) + space)
            newsummary += "0000000 ***\n"
            file_data.write(newsummary)

        elif transaction_list[1] == "WDR":
            newsummary += (transaction_list[1] + space)
            newsummary += (str(transaction_list[2]) + space)
            newsummary += (str(transaction_list[3]) + space)
            newsummary += "0000000 ***\n"
            file_data.write(newsummary)
        elif transaction_list[1] == "XFR":
            newsummary += (transaction_list[1] + space)
            newsummary += (str(transaction_list[2]) + space)
            newsummary += (str(transaction_list[3]) + space)
            newsummary += (str(transaction_list[4]) + space)
            newsummary += "***\n"
            file_data.write(newsummary)

        elif transaction_list[1] == "NEW":
            newsummary += (transaction_list[1] + space)
            newsummary += (str(transaction_list[2]) + space)
            newsummary += "0000000 000 "
            newsummary += (transaction_list[3] + "\n")
            file_data.write(newsummary)

        elif transaction_list[1] == "DEL":
            newsummary += (transaction_list[1] + space)
            newsummary += (str(transaction_list[2]) + space)
            newsummary += "0000000 000 "
            newsummary += (transaction_list[3] + "\n")
            file_data.write(newsummary)

        elif transaction_list[1] == "EOS":
            newsummary += (transaction_list[1] + space)
            newsummary += "0000000 000 0000000 ***\n"
            file_data.write(newsummary)
        file_data.close()

    except OSError as error:
        print(error)
        return 1
    except ValueError as error:
        print(error)
        return 1
    return [transaction_list[0]]


def modify_file_ValidAccount(valid_account_list):
    file = open("ValidAccountListFile.txt", "w")
    for i in valid_account_list:
        file.write(str(i) + "\n")
    file.close()


# entry for testing
if __name__ == '__main__':
    print("Welcome to bank system!!!!\n")
    valid_account_list = readfile_ValidAccount()
    create_acct_list = []
    use_daily_limit = []
    check_trans(open_system(), None, [], valid_account_list, create_acct_list, use_daily_limit)
