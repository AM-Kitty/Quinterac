import sys

'''
Class ValidAccountsFile:
read valid accounts list file and write in new accounts
'''


class ValidAccountsFile:

    # read file from ValidAccountList file which contains a list of valid account number
    # convert it into a list form
    def readfile_ValidAccount(self):
        try:
            file_data = open("ValidAccountListFile.txt", "r")
            data = file_data.readlines()  # list type
            data = [int(i[:-1]) for i in data]
            return data[:-1]
        except FileNotFoundError:
            print("File not find! No such file or directory: 'ValidAccountListFile.txt'")
            sys.exit(1)

    # modify the valid account
    def modify_file_ValidAccount(self, valid_account_list):
        file = open("ValidAccountListFile.txt", "w")
        # write all valid accounts into the valid account list file
        for i in valid_account_list:
            file.write(str(i) + "\n")
        file.close()