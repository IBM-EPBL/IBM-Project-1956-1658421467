from connect import execDB, execReturn


def addUser(name, email, password):
    print(name, email, password)
    sql_fd = f"SELECT * FROM user WHERE email='{email}'"
    r = execReturn(sql_fd)

    if r != []:
        return "Email Exists"

    sql_st = f"INSERT INTO user(name , email , password ) values ( '{name}' , '{email}' , '{password}' )"
    r = execDB(sql_st)
    return "User registered successfully"


def getPassword(email):
    sql_fd = f"SELECT password FROM user WHERE email='{email}'"
    r = execReturn(sql_fd)
    # print(r[0])
    return r[0]['PASSWORD'].strip()


def fetchFinanceRecord(email):
    sql_fd = f"SELECT * FROM finance WHERE email='{email}'"
    r = execReturn(sql_fd)
    return r


def createFinanceRecord(email, category, amount, description, date):
    amount = int(amount)
    amount = 100
    print("FINANCE", email, amount, category, description, date)
    sql_st = f"INSERT INTO finance(email , amount , category , description , date ) values ( '{email}' , {amount} , '{category}' , '{description}' , '{date}' )"
    r = execDB(sql_st)
    print(r)
    return "Record created successfully"
