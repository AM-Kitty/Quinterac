import sys


class TransactionFile:

    #  function for writing a transaction summary file
    def write_trans_summry(self, transaction_list):
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
                newsummary += "000 0000000 "
                newsummary += (transaction_list[3] + "\n")
                file_data.write(newsummary)

            elif transaction_list[1] == "DEL":
                newsummary += (transaction_list[1] + space)
                newsummary += (str(transaction_list[2]) + space)
                newsummary += "000 0000000 "
                newsummary += (transaction_list[3] + "\n")
                file_data.write(newsummary)

            elif transaction_list[1] == "EOS":
                newsummary += (transaction_list[1] + space)
                newsummary += "0000000 000 0000000 ***\n"
                file_data.write(newsummary)
            file_data.close()

        except FileNotFoundError as error:
            print(error)
            sys.exit(1)
        except ValueError as error:
            print(error)
            sys.exit(1)
        return [transaction_list[0]]

