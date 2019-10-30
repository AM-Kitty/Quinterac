class AccountCheck:

    # get input of deposit or transfer amount from user
    def get_amount(self):
        while True:
            amount = input("Enter your amount:")  # number check
            try:
                amount = float(amount)
                return amount
            except ValueError:
                print("Enter a valid amount!")

    # get the input for account number from user
    def get_account_number(self):
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
                except ValueError:
                    print("Please enter a valid account number!")

    # get the input for account name from user
    def get_account_name(self):
        while True:
            account_name = input("Enter your account name:")
            if 2 < len(account_name) < 31:
                if account_name[0] != " " and account_name[-1] != " ":
                    return account_name
                else:
                    print("Enter a valid account name(no space for beginning or ending)!")
            else:
                print("Enter a valid account name!")
