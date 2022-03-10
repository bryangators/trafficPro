import os
import sys
import cx_Oracle
from .db_credentials import username, password

try:
    if sys.platform.startswith("darwin"):
        lib_dir = os.path.join(os.environ.get("HOME"), "Downloads",
                               "instantclient_19_8")
        cx_Oracle.init_oracle_client(lib_dir=lib_dir)
    elif sys.platform.startswith("win32"):
        lib_dir=r"C:\oracle\instantclient_19_9"
        cx_Oracle.init_oracle_client(lib_dir=lib_dir)
except Exception as err:
    error, = err.args
    print(error.code, error.message)
    

connection = cx_Oracle.connect(user = username,
                               password = password,
                               dsn = "//oracle.cise.ufl.edu/orcl")