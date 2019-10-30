import sys
'''
Class TransactionFile:
manage and write in transaction summary file for ending bank session
'''
class TransactionFile:

    def __init__(self, transaction_file):
        self.transaction_file = transaction_file
        self.transactions = []

    def write(self):
        self.transactions.append('EOS')
        with open(self.transaction_file, 'w') as of:
            of.writelines(self.transactions)

    # function for writing a transaction summary file
    def write_trans_summry(self, transaction_list):
        newsummary = ""
        space = " "
        try:
            global output_transaction_summary_file
            file_data = open("TransactionSummaryFile.txt", "a")

            if output_transaction_summary_file is None:
                output_transaction_summary_file =[]

            # try to store transaction summary in the transaction summary file
            if transaction_list[1] == "DEP":
                newsummary += (transaction_list[1] + space)
                newsummary += (str(transaction_list[2]) + space)
                newsummary += (str(transaction_list[3]) + space)
                newsummary += "0000000 ***\n"
                output_transaction_summary_file.append(newsummary)

            elif transaction_list[1] == "WDR":
                newsummary += (transaction_list[1] + space)
                newsummary += (str(transaction_list[2]) + space)
                newsummary += (str(transaction_list[3]) + space)
                newsummary += "0000000 ***\n"
                output_transaction_summary_file.append(newsummary)
            elif transaction_list[1] == "XFR":
                newsummary += (transaction_list[1] + space)
                newsummary += (str(transaction_list[2]) + space)
                newsummary += (str(transaction_list[3]) + space)
                newsummary += (str(transaction_list[4]) + space)
                newsummary += "***\n"
                output_transaction_summary_file.append(newsummary)

            elif transaction_list[1] == "NEW":
                newsummary += (transaction_list[1] + space)
                newsummary += (str(transaction_list[2]) + space)
                newsummary += "000 0000000 "
                newsummary += (transaction_list[3] + "\n")
                output_transaction_summary_file.append(newsummary)

            elif transaction_list[1] == "DEL":
                newsummary += (transaction_list[1] + space)
                newsummary += (str(transaction_list[2]) + space)
                newsummary += "000 0000000 "
                newsummary += (transaction_list[3] + "\n")
                output_transaction_summary_file.append(newsummary)

            elif transaction_list[1] == "EOS":
                newsummary += (transaction_list[1] + space)
                newsummary += "0000000 000 0000000 ***\n"
                output_transaction_summary_file.append(newsummary)

        except FileNotFoundError as error:
            print(error)
            sys.exit(1)
        except ValueError as error:
            print(error)
            sys.exit(1)
        return [transaction_list[0]]

