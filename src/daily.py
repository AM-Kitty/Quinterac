import sys
import Backend
import Frontend
import os


def main():
    number_of_transaction_sessions = 3
    for i in range(number_of_transaction_sessions):
        sys.argv = [
            'Frontend.py',
            'ValidAccountListFile.txt',
            'DailySession/TransactionSummaryFile' + str(i+1) + '.txt']
        Frontend.main()

    files = os.listdir("DailySession/")

    with open('TransactionSummaryFile.txt', 'w') as result:
        for f in files:
            for line in open("DailySession/" + f, 'r'):
                result.write(line)

    file = os.listdir("DailySession/")
    for i in file:
        os.remove("DailySession/" + i)

    sys.argv = [
        'Backend.py',
        'MasterAccountsFile.txt',
        'TransactionSummaryFile.txt']
    Backend.main()
    #os.remove("TransactionSummaryFile.txt")


if __name__ == "__main__":
    main()