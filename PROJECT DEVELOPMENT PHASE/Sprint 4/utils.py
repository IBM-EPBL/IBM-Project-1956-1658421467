from sendgrid.helpers.mail import Mail, Email, To, Content
import os
import sendgrid
import uuid
from connect import execDB, execReturn

from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

sendGripdAPI = os.getenv("sendGripdAPI")
sendgridSender = os.getenv("sendgridSender")

positive_money = ['Salary Credited', 'Festival Bonus']
negative_money = ['EMI', 'Food', 'Transportation', 'Groceries',
                  'Clothing', 'Electronic', 'Entertainment', 'Rent', 'Vacations']


def getGraphDetails(email):
    sql_fd = f"SELECT * FROM finance WHERE email='{email}' order by date desc"
    r = execReturn(sql_fd)
    d = dict()
    s = 0
    n = 0
    for i in negative_money:
        d[i] = 0
    for i in r:
        if i['CATEGORY'].strip() in negative_money:
            d[i['CATEGORY'].strip()] += abs(int(i['AMOUNT']))
            n = n + abs(int(i['AMOUNT']))
        else:
            s = s + int(i['AMOUNT'])
    if (s > n):
        d["Money Left"] = s-n
    else:
        d["Money Left"] = 0
    k = ""
    for i in list(d.keys()):
        k = k+i+","

    v = ""
    for i in list(d.values()):
        v = v+str(i)+","
    return {"x": k[:-1], "y": v[:-1]}


def triggerMail(email):
    sg = sendgrid.SendGridAPIClient(sendGripdAPI)
    # Change to your verified sender
    from_email = Email(sendgridSender)
    to_email = To(email)  # Change to your recipient
    subject = "Expense Limit Reminder"
    content = Content(
        "text/plain", "Your expense limit is reached. Please check and manage your funds")
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    # print("mail triggered with send grid")


# triggerMail("vinokrish001@gmail.com")


def getReminder(email):
    sql_fd = f"SELECT percent FROM reminders WHERE email='{email}'"
    r = execReturn(sql_fd)
    return r[0]['PERCENT']


def setReminder(email, limit):
    limit = int(limit)
    s = f"UPDATE reminders SET percent={limit} WHERE email='{email}'"
    r = execDB(s)


def isLimitReached(email):
    sql_fd1 = f"SELECT SUM(AMOUNT) FROM finance WHERE AMOUNT>0 AND email='{email}'"
    sql_fd2 = f"SELECT SUM(AMOUNT) FROM finance WHERE AMOUNT<0 AND email='{email}'"
    r1 = execReturn(sql_fd1)
    r2 = execReturn(sql_fd2)
    income = r1[0]['1']
    expense = -r2[0]['1']
    percent = expense/income
    percent = percent*100
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
    if not r1[0]['1']:
        r1[0]['1'] = 0
    if not r2[0]['1']:
        r2[0]['1'] = 0
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
