import ibm_db
from ibm_db import tables
from ibm_db import fetch_assoc
from ibm_db import exec_immediate

dbname = "bludb"
username = "zgy62002"
password = "EkD9WuGi9Q8PHyTM"
hostname = "0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud"
cert = "DigiCertGlobalRootCA.crt"
port = 31198
protocol = "TCPIP"
# establish connection


def establish():
    try:
        conn = db.connect(
            f"DATABASE={dbname};HOSTNAME={hostname};PORT={port};PROTOCOL={protocol};UID={username};PWD={password}; SECURITY=SSL; SSLServerCertificate={cert};",
            "", "")
        print("Connected to database")
        return conn
    except:
        print("Error connecting to database")

# to insert a new user


def insertuser(conn1, name, email, user, passw):
    sql = "INSERT INTO users(name,email,username,password) VALUES ('{}','{}','{}','{}')".format(
        name, email, user, passw)
    try:
        stmt = db.exec_immediate(conn1, sql)
        print("Number of affected rows: ", db.num_rows(stmt))
    except:
        print("cannot insert user to database")

# to check if user exists with given email


def useremail_check(conn, email):
    sql = "SELECT * FROM users WHERE email='{}' ".format(email)
    stmt = db.exec_immediate(conn, sql)
    results = db.fetch_assoc(stmt)
    if results == False:
        return True
    else:
        return False

# to check if user exists with given username and password


def user_check(conn, email, passw):
    sql = "SELECT * FROM users WHERE email='{}' AND password='{}'".format(
        email, passw)
    stmt = db.exec_immediate(conn, sql)
    results = db.fetch_both(stmt)
    return results

# set basic details of each user


def setuser(conn, money, budget, goal, email, pwd):
    sql = "UPDATE USERS SET(pocketmoney,budget,monthlygoal) = ('{}','{}','{}') WHERE email='{}' AND password='{}'".format(
        money, budget, goal, email, pwd)
    try:
        stmt = db.exec_immediate(conn, sql)
        print("Number of affected rows: ", db.num_rows(stmt))
    except:
        print("Error inserting data to database")

# insert a new transaction of a user


def inserttransac(conn, id, amt, des, cat):
    sql = "INSERT INTO TRANSACTIONS(user_id,amount,description,category) VALUES('{}','{}','{}','{}')".format(
        id, amt, des, cat)
    try:
        stmt = db.exec_immediate(conn, sql)
        print("Number of affected rows: ", db.num_rows(stmt))
    except:
        print("Error inserting data to database")

# to get the total mount spent for the month


def gettotalsum(conn, id):
    sql = "SELECT SUM(amount) as SUM FROM transactions WHERE MONTH(date) = MONTH(CURRENT DATE) AND YEAR(date) = YEAR(CURRENT DATE) AND user_id='{}'".format(id)
    try:
        stmt = db.exec_immediate(conn, sql)
        res = db.fetch_both(stmt)
        return res
    except:
        print("Error while fetching")

# to get all transactions of a user


def getalltransac(conn, id):
    sql = "SELECT * FROM transactions WHERE MONTH(date) = MONTH(CURRENT DATE) AND YEAR(date) = YEAR(CURRENT DATE) AND user_id='{}' ORDER BY date DESC".format(id)
    try:
        stmt = db.exec_immediate(conn, sql)
        res = db.fetch_both(stmt)
        if (res == False):
            return []
        else:
            res['DATE'] = res['DATE'].date()
            dict = [{'id': res['ID'], 'date': res['DATE'], 'amt': res['AMOUNT'],
                     'cat': res['CATEGORY'], 'des':res['DESCRIPTION']}]
            res = db.fetch_both(stmt)
            while (res != False):
                res['DATE'] = res['DATE'].date()
                dict.append({'id': res['ID'], 'date': res['DATE'], 'amt': res['AMOUNT'],
                            'cat': res['CATEGORY'], 'des': res['DESCRIPTION']})
                res = db.fetch_both(stmt)
            return dict
    except:
        print("Error while fetching")

# to delete a transaction


def deletetrans(conn, id):
    sql = "DELETE FROM transactions WHERE id='{}'".format(id)
    try:
        stmt = db.exec_immediate(conn, sql)
        print("Number of affected rows: ", db.num_rows(stmt))
    except:
        print("Error deleting data from database")

# to update a transaction


def updateTrans(conn, id, amt, des):
    sql = "UPDATE transactions SET AMOUNT='{}',DESCRIPTION = '{}' WHERE ID='{}'".format(
        amt, des, id)
    try:
        stmt = db.exec_immediate(conn, sql)
        print("Number of affected rows: ", db.num_rows(stmt))
    except:
        print("Successfully updated transaction")


def get_budget(conn, id):
    sql = "SELECT POCKETMONEY FROM users WHERE ID='{}' ".format(id)
    stmt = db.exec_immediate(conn, sql)
    results = db.fetch_assoc(stmt)
    return results
