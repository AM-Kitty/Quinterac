import sys


# class: TransactionFile
# create the Merged Transaction Summary File
# which is the concatenation of any number of Transaction Summary Files output from Front Ends
class TransactionFile:

    #  function for writing the transaction summary file
    @staticmethod
    def write_trans_summary(transaction_list, file):
        new_summary = ""
        space = " "
        try:
            file_data = open(file, "a")

            if transaction_list[1] == "DEP":
                new_summary += (transaction_list[1] + space)
                new_summary += (str(transaction_list[2]) + space)
                new_summary += (str(transaction_list[3]) + space)
                new_summary += "0000000 ***\n"
                file_data.write(new_summary)

            elif transaction_list[1] == "WDR":
                new_summary += (transaction_list[1] + space)
                new_summary += (str(transaction_list[2]) + space)
                new_summary += (str(transaction_list[3]) + space)
                new_summary += "0000000 ***\n"
                file_data.write(new_summary)

            elif transaction_list[1] == "XFR":
                new_summary += (transaction_list[1] + space)
                new_summary += (str(transaction_list[2]) + space)
                new_summary += (str(transaction_list[3]) + space)
                new_summary += (str(transaction_list[4]) + space)
                new_summary += "***\n"
                file_data.write(new_summary)

            elif transaction_list[1] == "NEW":
                new_summary += (transaction_list[1] + space)
                new_summary += (str(transaction_list[2]) + space)
                new_summary += "000 0000000 "
                new_summary += (transaction_list[3] + "\n")
                file_data.write(new_summary)

            elif transaction_list[1] == "DEL":
                new_summary += (transaction_list[1] + space)
                new_summary += (str(transaction_list[2]) + space)
                new_summary += "000 0000000 "
                new_summary += (transaction_list[3] + "\n")
                file_data.write(new_summary)

            elif transaction_list[1] == "EOS":
                new_summary += (transaction_list[1] + space)
                new_summary += "0000000 000 0000000 ***\n"
                file_data.write(new_summary)
            file_data.close()

        except FileNotFoundError as error:
            print(error)
            sys.exit(1)
        except ValueError as error:
            print(error)
            sys.exit(1)
        return [transaction_list[0]]

