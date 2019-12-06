import sys
import daily
import io

# create a “Weekly” script that runs the Daily script five separate times, simulating five days of operation
def main():
    # Begin Weekly run with an empty Valid Accounts List and an empty Master Accounts File
    open("ValidAccountListFile.txt", 'w').close()
    open("MasterAccountsFile.txt", 'w').close()
    # day one terminal input
    day_one = [
        'login', 'agent', 'createacct', 'Theo', '6666666', 'logout',
         'login', 'agent', 'createacct', 'Kelly', '8888888', 'logout',
         'login', 'agent', 'createacct', 'Sunny', '8888886', 'logout'
    ]
    # day two terminal input
    day_two = [
        'login', 'agent', 'deposit', '6666666', '500', 'logout',
        'login', 'agent', 'deposit', '8888888', '600', 'logout',
        'login', 'agent', 'deposit', '8888886', '200', 'logout'
    ]
    # day three terminal input
    day_three = [
        'login', 'atm', 'deposit', '6666666', '500', 'logout',
        'login', 'atm', 'deposit', '8888888', '600', 'logout',
        'login', 'atm', 'withdraw', '8888886', '200', 'logout'
    ]
    # day four terminal input
    day_four = [

        'login', 'agent', 'deleteacct', 'Sunny', '8888886', 'logout',
        'login', 'agent', 'transfer', '8888888', '6666666', '600', 'logout',
        'login', 'agent', 'deposit', '6666666', '200', 'logout'
    ]
    # day five terminal input
    day_five = [
        'login', 'agent', 'deposit', '6666666', '500', 'logout',
        'login', 'agent', 'deposit', '6666666', '600', 'logout',
        'login', 'agent', 'deposit', '6666666', '600', 'logout',
    ]
    days = [day_one, day_two, day_three, day_four, day_five]
    for i in days:
        sys.stdin = io.StringIO(
            '\n'.join(i))
        # run the daily program
        daily.main()


if __name__ == '__main__':
    main()
