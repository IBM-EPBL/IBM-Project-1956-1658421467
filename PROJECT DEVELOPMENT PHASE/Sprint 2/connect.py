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
t = 1


def results(command):
    ret = []
    result = fetch_assoc(command)

    while result:
        ret.append(result)
        result = fetch_assoc(command)
    return ret


conn = ibm_db.pconnect(
    f"DATABASE={dbname};HOSTNAME={hostname};PORT={port};PROTOCOL={protocol};UID={username};PWD={password};SECURITY=SSL;SSLServerCertificate={cert};", "", "")


def execDB(cmd):
    return exec_immediate(conn, cmd)


def execReturn(cmd):
    return results(exec_immediate(conn, cmd))
