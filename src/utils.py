import inspect
import re

import sqlparse


def format(func):
    def inner1():
        # calling the actual function now
        # inside the wrapper function.
        qry = func()
        sql = qry.get_sql(quote_char='`')
        return sqlparse.format(sql, reindent=True)

    return inner1


def get_src_and_sql(func):
    sql = sqlparse.format(func(), reindent=True) + ';'
    src = inspect.getsource(func)
    result = re.findall('def\s+([^(]+)\\(', src)
    func_name = result[0]
    return func_name, src, sql
