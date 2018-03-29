# -*- coding: utf-8 -*-

import sqlite3
import re
import pdb

from mylogger import MLogger
from db import DIR_LOG
from db import DIR_LOG_ERR
from db import DB_FILE_WWWW as DB_FILE
from patterns import wwww_expression as expression

ERROR_DIR = "error.txt"
sqls_insertion = """
insert or ignore into monthly (
instrumentid,open,high,low,close,deltaPrice,openint,deltaOpenint,settlementprice,volume,amount,month)
values (?,?,?,?,?,?,?,?,?,?,?,?);
"""
p = re.compile(expression)
formatter = '%(asctime)-15s %(name)-8s %(levelname)-6s - %(message)s'
mlog = MLogger.init_logger('l_WWWW', formatter, DIR_LOG, DIR_LOG_ERR)
wwwwins_fields = ('instrumentid','date_listed','date_last','date_delivery_first','date_delivery_last','price_listed','manual_flag','update_time')
wwwwins_format = "%12s|%11s|%9s|%19s|%18s|%12s|%11s|%19s|"


def connect_db():
    try:
        con=sqlite3.connect(DB_FILE)
    except sqlite3.Error as err:
        logger.warning("connection failed, ret=%s", err.args[0])
        raw_input("Failed connection. Press a key")
    cur=con.cursor()
    print "connected with %s." % DB_FILE
    return con, cur

c, cur = connect_db()


def update_from_lastcontracts():
    global cur, sqls_ins_wwww_1, mlog
    cur.execute("SAVEPOINT sp_2;")
    tmp = cur.execute(sqls_ins_wwww_1['diff_last_ins']).fetchall()
    if tmp is None:
        print "lastcontracts brings no changes to WWWWins. Did you update it?\nPAUSED & return.."
        pdb.set_trace()
        return
    latest_date_last = tmp[0][1]
    if 0 >= len(tmp):
        print "No bothering to update WWWWins.date_last. return."
        return
    if 0 < len(cur.execute(sqls_ins_wwww_1['consistent_lastcontracts_ins']).fetchall()):
        print "Instrumentid not included in WWWWins or if included, date_last != 21001231... PAUSED..."
        pdb.set_trace()
        return

    for i in tmp:
        print "To be updated: ins: %s date_last: %s." % (i[0], str(i[1]))
    print "PLS have a look and MUST NOT continue WITHOUT checking."
    pdb.set_trace()
    try:
        cur.execute(sqls_ins_wwww_1['update_from_lastcontracts'])
    except sqlite3.Error as e:
        print "Failed inseroin: %s." % e.args[0]
        pdb.set_trace()

    if 0 < len(cur.execute(sqls_ins_wwww_1['diff_last_ins']).fetchall()):
        print "Abnormaly! PAUSED."
        pdb.set_trace()
        return

    print "Lastcontracts updated: last 30 updated values from WWWWins."
    print wwwwins_format % wwwwins_fields
    for i in cur.execute('select * from "WWWWins" order by "update_time" desc limit 30;').fetchall():
        print wwwwins_format % i
    mlog.debug("Finish updating date_last until %s, WWWWins." % str(latest_date_last))
    print "savepoint release, pls."
# cur.execute("RELEASE SAVEPOINT sp_2;")


def insert_from_newcontracts():
    global cur, sqls_ins_wwww_2, mlog
    cur.execute("SAVEPOINT sp3;")
    tmp = cur.execute(sqls_ins_wwww_2['diff_new_ins']).fetchall()
    newest_date_listed = tmp[0][1]
    if 0 >= len(tmp):
        print "No bothering to update WWWWins.date_last. return."
        return
    if 0 < len(cur.execute(sqls_ins_wwww_2['consistent_newcontracts_ins']).fetchall()):
        print "Inconsistency between newcontract and WWWWins!! PAUSED..."
        pdb.set_trace()
        return

    for i in tmp:
        print "To be inserted: ins: %s date_listed: %s." % (i[0], str(i[1]))
    print "PLS have a look and NEVER continue WITHOUT checking."
    pdb.set_trace()

    try:
        cur.execute(sqls_ins_wwww_2['insert_newcontracts'])
    except sqlite3.Error as e:
        print "Failed inseroin: %s." % e.args[0]
        pdb.set_trace()

    if 0 < len(cur.execute(sqls_ins_wwww_2['diff_new_ins']).fetchall()):
        print "Abnormaly! PAUSED."
        pdb.set_trace()
        return
    print "Newcontracts inserted: last 30 updated values from WWWWins."
    print wwwwins_format % wwwwins_fields
    for i in cur.execute('select * from "WWWWins" order by "update_time" desc limit 30;').fetchall():
        print wwwwins_format % i
    mlog.debug("Finish inserting date_listed until %s, WWWWins." % str(newest_date_listed))
    print "savepoint release, pls."
# cur.execute("RELEASE SAVEPOINT sp3;")
# c.rollback()


def cleanup():
    cur.close()
    c.close()


sqls_ins_wwww_1 = {
'diff_last_ins': """
select "instrumentid", "tradingday" from (select "instrumentid", "tradingday" from "lastcontracts" except select "instrumentid", "date_last" from "WWWWins") order by "tradingday" desc;
""",

'consistent_lastcontracts_ins': """
SELECT "instrumentid" FROM (
select "instrumentid", "tradingday" from "lastcontracts" except
 select "instrumentid", "date_last" from "WWWWins")
EXCEPT
 select "instrumentid" from "WWWWins" where "date_last" == 21001231;
""",

'update_from_lastcontracts': """
INSERT or REPLACE INTO "WWWWins" (
 "instrumentid", "date_listed", "date_last", "date_delivery_first", "date_delivery_last",     "price_listed", "manual_flag", "update_time")
 SELECT
"c"."instrumentid", "c"."date_listed", "l"."tradingday",
CASE WHEN substr("c"."instrumentid",1,1)== 'T' THEN NULL ELSE "l"."tradingday" END, 
CASE WHEN substr("c"."instrumentid",1,1)== 'T' THEN NULL ELSE "l"."tradingday" END, 
 "c"."price_listed", 0    ,      datetime()
 from "WWWWins" "c" join "lastcontracts" "l" on "c"."instrumentid" == "l"."instrumentid" and "c"."date_last" != "l"."tradingday";
"""
}

sqls_ins_wwww_2 = {
'diff_new_ins': """
select "instrumentid", "tradingday" from (select "instrumentid", "tradingday" from "newcontracts" except select "instrumentid", "date_listed" from "WWWWins")
order by "tradingday" desc;
""",

'consistent_newcontracts_ins': 'select * from "newcontracts" "n" join "WWWWins" "c" on "n"."instrumentid" == "c"."instrumentid" and "n"."tradingday" != "c"."date_listed";',

'insert_newcontracts': """
INSERT INTO "WWWWins" (
 "instrumentid", "date_listed", "date_last","price_listed", "manual_flag", "update_time")
SELECT
 "instrumentid", "tradingday", 21001231, "price_listed", 0, datetime()
FROM "newcontracts" where "instrumentid" in (
 select "instrumentid" from "newcontracts" except select "instrumentid" from "WWWWins") order by "tradingday";
"""
}
