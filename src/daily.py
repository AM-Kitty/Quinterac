import sys
import Backend
import Frontend
import os


# create a “Daily” script to run frontend and backend
def main():
    # runs Front End over 3 transaction sessions
    number_of_transaction_sessions = 3
    # save the output Transaction Summary File for each session in a separate file
    for i in range(number_of_transaction_sessions):
        sys.argv = [
            'Frontend.py',
            'ValidAccountListFile.txt',
            'DailySession/TransactionSummaryFile' + str(i + 1) + '.txt']
        Frontend.main()

    # concatenates the separate Transaction Summary Files into a Merged Transaction Summary file
    files = os.listdir("DailySession/")
    with open('TransactionSummaryFile.txt', 'w') as result:
        for f in files:
            for line in open("DailySession/" + f, 'r'):
                if "EOS" not in line:
                    result.write(line)
        result.write("EOS 0000000 000 0000000 ***\n")
        result.close()

    # remove separate Transaction Summary Files
    file = os.listdir("DailySession/")
    for i in file:
        os.remove("DailySession/" + i)

    # runs your Back Office with the Merged Transaction Summary File as input
    sys.argv = [
        'Backend.py',
        'MasterAccountsFile.txt',
        'TransactionSummaryFile.txt']
    Backend.main()


if __name__ == "__main__":
    main()
