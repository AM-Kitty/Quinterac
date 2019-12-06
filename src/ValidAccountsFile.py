import sys


# Class ValidAccountsFile:
# read valid accounts list file for frontend
# modify accounts to create a new valid accounts list for frontend to run
class ValidAccountsFile:

    # read file from ValidAccountList file which contains a list of valid account number
    # convert it into a list form
    @staticmethod
    def readfile_ValidAccount(file):
        try:
            file_data = open(file, "r")
            data = file_data.readlines()  # list type
            data = [int(i[:-1]) for i in data]
            return data[:-1]
        except:
            print("File not find! No such file or directory: 'ValidAccountListFile.txt'")
            sys.exit(1)

    # modify the valid account to update into the new accounts list file
    # def modify_file_ValidAccount(self, valid_account_list):
    #     file = open("ValidAccountListFile.txt", "w")
    #     # write all valid accounts into the valid account list file
    #     for i in valid_account_list:
    #         file.write(str(i) + "\n")
    #     file.close()
