import sys


# Class for backend
# used to produce new master accounts file and new valid accounts list file
# based on the inputs of merged transaction summary file and old master accounts file
# input:  merged transaction summary file and old master accounts file
# output: new master accounts file and new valid account file
class Backend:

    # function use to read master account file
    # function input old master account file
    # organized the data to a dictionary then return the dictionary
    @staticmethod
    def read_master_accounts(file):
        dict = {}
        try:
            file_data = open(file, "r")
            data = file_data.readlines()
            data = [i.split(" ") for i in data]
            for i in data:
                if "\n" in i[2]:
                    i[2] = i[2][0:-1]
                dict[i[0]] = [i[1], i[2]]
            return dict
        except:
            print("File not find! No such file or directory: 'MasterAccountsFile.txt'")
            sys.exit(1)

    # function use to read transaction summary file
    # function input transaction summary file
    # organized the data to a list then return the list
    @staticmethod
    def read_transaction(file):
        try:
            file_data = open(file, "r")
            data = file_data.readlines()
            data = [i.split(" ") for i in data]
            return data
        except:
            print("File not find! No such file or directory: 'TransactionSummaryFile.txt'")
            sys.exit(1)

    # function use to go through the transaction summary
    # function input transaction summary file and master account file
    # if transaction summary valid then return valid master account file data (data type: dictionary)
    # if transaction summary not valid then immediately stop
    def get_new_master_accounts(self, file1, file2):
        master_list = self.read_master_accounts(file1)
        trans_list = self.read_transaction(file2)
        for i in trans_list:
            if i[0] == "DEP":
                if i[1] in master_list:
                    balance = int(master_list[i[1]][0]) + int(i[2])
                    master_list[i[1]][0] = str(balance)
                else:
                    print("Error! " + str(i[1]) + " not in the master account file!")
                    return False

            elif i[0] == "WDR":
                if i[1] in master_list:
                    balance = int(master_list[i[1]][0]) - int(i[2])
                    if balance < 0:
                        print("Error! " + str(i[1]) + " have a negative balance!")
                        return False
                    else:
                        master_list[i[1]][0] = str(balance)
                else:
                    print("Error! " + str(i[1]) + " not in the master account file!")
                    return False

            elif i[0] == "XFR":
                if i[1] in master_list and i[3] in master_list:
                    balance = int(master_list[i[1]][0]) - int(i[2])
                    balance2 = int(master_list[i[3]][0]) + int(i[2])
                    if balance < 0:
                        print("Error! " + str(i[1]) + " have a negative balance!")
                        return False
                    else:
                        master_list[i[1]][0] = str(balance)
                        master_list[i[3]][0] = str(balance2)
                else:
                    print("Account not in the master account file!")
                    return False

            elif i[0] == "NEW":
                if i[1] in master_list:
                    print(i[1])
                    print("Error! New account must have an unused account number!")
                    return False
                if len(i) > 5:  # if user name have space, then reevaluate name (include space)
                    name = ""
                    for letter in i[4:]:
                        name += letter + " "
                    master_list[i[1]] = ["0000", name[0:-2]]
                else:
                    master_list[i[1]] = ["0000", i[-1][0:-1]]

            elif i[0] == "DEL":
                if i[1] in master_list:
                    if len(i) > 5:  # if user name have space, then reevaluate name (include space)
                        name = ""
                        for letter in i[4:]:
                            name += letter + " "
                        i[4] = name[0:-1]
                    if master_list[i[1]][1] == i[4][0:-1] and int(master_list[i[1]][0]) == 0:
                        del master_list[i[1]]
                        # name, account are match each of them and balance is zero, then can be delete
                    elif master_list[i[1]][1] == i[-1][0:-1] and int(master_list[i[1]][0]) != 0:
                        print("Error! Balance is not zero, cannot delete!")
                        return False
                    else:
                        print("Error! Name not match the deleted account!")
                        return False
                else:
                    print("Error! " + str(i[1]) + " not in the master account file!")
                    return False

            elif i[0] == "EOS":
                pass

        for i in master_list:
            line = str(i) + " " + master_list[i][0] + " " + master_list[i][1] + "\n"
            if len(line) > 47:  # check each line have more than 47 characters or not
                print("Error! Each line is at most 47 characters!")
                return False

        return master_list  # return a valid master dictionary

    # function use to write new master account file
    # function input master account file data (data type: dictionary) and new master account file
    @staticmethod
    def write_new_master(data, file):
        keys = sorted(data.keys())  # ascending order write account number to file
        file_data = open(file, "w")
        for i in keys:
            line = str(i) + " " + data[i][0] + " " + data[i][1] + "\n"
            file_data.write(line)
        file_data.close()  # finish write new master account file
        print("New Master Accounts File created successfully!")

    # function use to write new valid account file
    # function input master account file data, data type dictionary
    @staticmethod
    def write_ValidAccount(data):
        keys = sorted(data.keys())  # ascending order write account number to file
        file_data = open("ValidAccountListFile.txt", "w")
        for i in keys:
            line = str(i) + "\n"
            file_data.write(line)
        file_data.write("0000000\n")
        file_data.close()  # finish write new valid account file
        print("New Valid Accounts File created successfully!")


# main function
# run Backend with the two input files, Old Master Accounts and Merged Transaction Summary Files
def main():
    back = Backend()
    new_master = back.get_new_master_accounts(sys.argv[1], sys.argv[2])

    if new_master:  # if transaction summary is valid, write new master account file and new valid account file
        back.write_new_master(new_master, sys.argv[1])
        back.write_ValidAccount(new_master)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Invalid input, must include "MasterAccountsFile.txt TransactionSummaryFile.txt"')
        sys.exit(1)
    main()
