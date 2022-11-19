import uuid
from connect import execDB, execReturn
positive_money = ['Salary', 'Festival Bonus']
negative_money = ['EMI', 'Food', 'Transportation', 'Groceries',
                  'Clothing', 'Electronic', 'Entertainment', 'Rent', 'Vacations']


def triggerMail():
    print("mail triggered with send grid")


def getReminder(email):
    sql_fd = f"SELECT percent FROM reminders WHERE email='{email}'"
    r = execReturn(sql_fd)
    return r[0]['PERCENT']


def setReminder(email, limit):
    sql_fd = f"UPDATE reminder SET percent='{limit} WHERE email='{email}'"
    r = execReturn(sql_fd)


def isLimitReached(email):
    sql_fd1 = f"SELECT SUM(AMOUNT) FROM finance WHERE AMOUNT>0 AND email='{email}'"
    sql_fd2 = f"SELECT SUM(AMOUNT) FROM finance WHERE AMOUNT<0 AND email='{email}'"
    r1 = execReturn(sql_fd1)
    r2 = execReturn(sql_fd2)
    income = r1[0]['1']
    expense = -r2[0]['1']
    percent = expense/income

    sql_fd = f"SELECT percent FROM reminders WHERE email='{email}'"
    r = execReturn(sql_fd)
    limit = int(r[0]['PERCENT'])
    if limit < percent:
        triggerMail()


def addUser(name, email, password):
    print(name, email, password)
    sql_fd = f"SELECT * FROM user WHERE email='{email}'"
    r = execReturn(sql_fd)

    if r != []:
        return "Email Exists"

    sql_st = f"INSERT INTO user(name , email , password ) values ( '{name}' , '{email}' , '{password}' )"
    r = execDB(sql_st)
    sql_st = f"INSERT INTO reminders(email , percent ) values ( '{email}' , 90 )"
    # 90 is the default reminder percent
    r = execDB(sql_st)
    return "User registered successfully"


def getPassword(email):
    sql_fd = f"SELECT password FROM user WHERE email='{email}'"
    r = execReturn(sql_fd)
    # print(r[0])
    return r[0]['PASSWORD'].strip()


def fetchFinanceRecord(email):
    sql_fd = f"SELECT * FROM finance WHERE email='{email}' order by date desc"
    r = execReturn(sql_fd)
    return r


def getIncomeExpend(email):
    sql_fd1 = f"SELECT SUM(AMOUNT) FROM finance WHERE AMOUNT>0 AND email='{email}'"
    sql_fd2 = f"SELECT SUM(AMOUNT) FROM finance WHERE AMOUNT<0 AND email='{email}'"
    r1 = execReturn(sql_fd1)
    r2 = execReturn(sql_fd2)
    print(r1, r2)
    return {"income": r1[0]['1'], "expend": -r2[0]['1']}


def createFinanceRecord(email, category, amount, description, date):
    amount = int(amount)
    if category in negative_money:
        amount = -amount
    print("FINANCE", email, amount, category, description, date)
    sql_st = f"INSERT INTO finance(id,email , amount , category , description , date ) values ( '{uuid.uuid1()}','{email}' , {amount} , '{category}' , '{description}' , '{date}' )"
    r = execDB(sql_st)
    print(r)
    return "Record created successfully"
