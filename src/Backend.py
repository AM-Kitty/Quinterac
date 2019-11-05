
'''
Class Backend:
reads in the previous day’s master accounts file and then applies all of the transactions
in a set of daily transaction files to the accounts to produce today’s new master accounts file
'''

class Backend:

    #  function for updating the master accounts file
    def write_master_accounts(self, transaction_list):
        newsummary = ""
        space = " "
        try:
            file_data = open("MasterAccountsFile.txt", "w")



        except FileNotFoundError as error:
            print(error)
            sys.exit(1)
        except ValueError as error:
            print(error)
            sys.exit(1)
        return [transaction_list[0]]

