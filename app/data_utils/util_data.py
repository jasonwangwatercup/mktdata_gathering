# -*- coding: utf-8 -*-

import pdb
import sqlite3

MAX_LINE_TO_PRINT = 30
exchange_list = ('zzzz', 'xxxx', 'yyyy', 'wwww', 'xxxx_futopt')
ins_list = None
ins_tmp_list = None


def generate_params(add_fo=False):
    global exchange_list, ins_list, ins_tmp_list, sqls_daily, sqls_ins
    exchange_list = [ str(i).strip().lower() for i in exchange_list]
    ins_list = [i.upper()+'ins' for i in exchange_list]
    ins_tmp_list = ['tmp_' + i.upper() + 'ins' for i in exchange_list]
    if add_fo is True:
        exchange_list.append('xxxx_futopt')

def exchange_params(exchange_name, structs):
    global exchange_list
    assert len(exchange_list) == len(structs)
    exchange_name = str(exchange_name).strip().lower()
    try:
        idx = exchange_list.index(exchange_name)
    except ValueError as e:
        print "%s not in exchange_list, PLEASE have a look!" % exchange_name
        pdb.set_trace()
    return structs[idx]

def sp_insert_diff_print2 (cur, out_list, dict_, name_sp=None, fun_print=None):
    global MAX_LINE_TO_PRINT
    if len(out_list) > 0:
        if name_sp is not None:
            cur.execute("SAVEPOINT 'sp_sidp2';")
        cur.execute(dict_['create_tmp'])
        try:
            cur.execute(dict_['delete_tmp'])
        except sqlite3.Error as err:
            print "Failed deletion: %s." % repr(err)
            pdb.set_trace()

        try:
            cur.executemany(dict_['insert_tmp'], out_list)
        except sqlite3.Error as err:
            print "Failed insertion: %s | %s." % (dict_['insert_tmp'], repr(err))
            pdb.set_trace()
        tmpp = cur.execute(dict_['diff_tmp']).fetchall()
        if 0 >= len(tmpp):
            print "No bothering continuing since no changes at all. RETURN."
            pdb.set_trace()
            return
        elif MAX_LINE_TO_PRINT < len(tmpp):
            cur.execute(dict_['diff_tmp_grouped'])
            tmpp = cur.fetchall()
        print "Possible changes:"
        for ii in tmpp:
            print repr(ii)
        print "WILL the replacement be REASONABLE??!! .. PLS have a THOUROUGH look.!"
        print "NEVER REPLACE ANYTHING if you do NOT know the possible results."
        pdb.set_trace()

        try:
            cur.execute(dict_['insert'])
        except sqlite3.Error as err:
            print "Insert failed: %s." % (repr(err),)
            pdb.set_trace()

        print "After insertion total counts:  %s\n" % cur.execute(dict_['print_count']).fetchone()
        print "Print *last 30* records:"
        tmp_print = cur.execute(dict_['limited_print']).fetchall()
        if 0 < len(tmp_print) and fun_print is None:
            for i in tmp_print:
                print repr(i)
        elif 0 < len(tmp_print) and fun_print is not None:
            fun_print(tmp_print)
            
    print "Finish inserting. AND PLS DO NOT FORGET TO RELEASE THE SAVEPOINT if necessary."


def update_daily(cur, out_list, exchange_name, name_sp=None, fun_print=None):
    global sqls_daily
    dict_in = exchange_params(exchange_name, sqls_daily)
    sp_insert_diff_print2(cur, out_list, dict_in, name_sp, fun_print)

def update_ins(cur, out_list, exchange_name, name_sp=None, fun_print=None):
    global sqls_ins
    dict_in = exchange_params(exchange_name, sqls_ins)
    sp_insert_diff_print2(cur, out_list, dict_in, name_sp, fun_print)


sqls_sidp2 = {'create_tmp': None, 'delete_tmp': None, 'insert_tmp': None,
'diff_tmp': None, 'insert_replace': None, 'diff_tmp_grouped': None,
'print_count': None, 'limited_print': None, 'insert_ignore': None, 'insert': None}

sqls_ins_zzzz = {
'create_tmp':
""" CREATE TEMP TABLE IF NOT EXISTS tmp_ZZZZins (
  "instrumentid" TEXT UNIQUE NOT NULL,
  "date_listed" INT NOT NULL,
  "date_last" INT NOT NULL,
  "date_delivery_first" INT NOT NULL,
  "date_delivery_last" INT NOT NULL,
  "price_listed" FLOAT NOT NULL); """,

'delete_tmp':
'DELETE from "tmp_ZZZZins";',

'insert_tmp':
'INSERT INTO "tmp_ZZZZins" ("instrumentid", "date_listed", "date_last", "date_delivery_first", "date_delivery_last", "price_listed") values (?, ?, ?, ?, ?, ?);',

'diff_tmp':
""" select 
"instrumentid", "date_listed", "date_last", "date_delivery_first", "date_delivery_last", "price_listed" from "tmp_ZZZZins" except select
 "instrumentid", "date_listed", "date_last", "date_delivery_first", "date_delivery_last", "price_listed" from "ZZZZins"; """,

'insert_replace':
""" INSERT OR REPLACE INTO "ZZZZins" (
 "instrumentid", "date_listed", "date_last", "date_delivery_first", "date_delivery_last", "price_listed", "manual_flag", "update_time"
  ) select
 "instrumentid", "date_listed", "date_last", "date_delivery_first", "date_delivery_last", "price_listed", 0,           datetime()
 from ( select 
 "instrumentid", "date_listed", "date_last", "date_delivery_first", "date_delivery_last", "price_listed"
 from "tmp_ZZZZins" except select
 "instrumentid", "date_listed", "date_last", "date_delivery_first", "date_delivery_last", "price_listed" from "ZZZZins") ORDER BY "date_listed"; """,

'diff_tmp_grouped':
""" select "date_listed", count(*) "cnt" from (select 
 "instrumentid", "date_listed", "date_last", "date_delivery_first", "date_delivery_last", "price_listed"
 from tmp_ZZZZins except select
 "instrumentid", "date_listed", "date_last", "date_delivery_first", "date_delivery_last", "price_listed"
 from "ZZZZins") group by "date_listed" order by "date_listed"; """,

'print_count':
'select count(*) from "ZZZZins";',

'limited_print':"""
select 
"instrumentid", "date_listed", "date_last", "date_delivery_first", "date_delivery_last", "price_listed", "manual_flag", "update_time"
 from "ZZZZins" order by "update_time" desc limit 30;""",

'insert_ignore':
""" INSERT OR IGNORE INTO "ZZZZins" (
"instrumentid", "date_listed", "date_last", "date_delivery_first", "date_delivery_last", "price_listed", "manual_flag", "update_time")
select
"instrumentid", "date_listed", "date_last", "date_delivery_first", "date_delivery_last", "price_listed", 0            ,   datetime()
from "tmp_ZZZZins"; """,

'insert':"""
INSERT INTO "ZZZZins" (
 "instrumentid", "date_listed", "date_last", "date_delivery_first", "date_delivery_last", "price_listed", "manual_flag", "update_time"
  ) select
 "instrumentid", "date_listed", "date_last", "date_delivery_first", "date_delivery_last", "price_listed", 0,           datetime()
 from ( select 
 "instrumentid", "date_listed", "date_last", "date_delivery_first", "date_delivery_last", "price_listed"
 from "tmp_ZZZZins" except select
 "instrumentid", "date_listed", "date_last", "date_delivery_first", "date_delivery_last", "price_listed" from "ZZZZins") ORDER BY "date_listed";
""",

}
##
sqls_ins_xxxx = {}
##
sqls_ins_yyyy = {
'create_tmp':
""" CREATE TEMP TABLE IF NOT EXISTS "tmp_YYYYins" (
  "instrumentid" TEXT UNIQUE NOT NULL,
  "lot" INT NOT NULL,
  "min_price_diff" FLOAT NOT NULL,
  "date_listed" INT NOT NULL,
  "date_last" INT NOT NULL,
  "date_delivery_last" INT NOT NULL); """,

'delete_tmp':
'DELETE from "tmp_YYYYins";',

'insert_tmp':
'INSERT INTO "tmp_YYYYins"("instrumentid", "lot", "min_price_diff", "date_listed", "date_last", "date_delivery_last") values (?, ?, ?, ?, ?, ?);',

'diff_tmp':
""" select 
 "instrumentid", "lot", "min_price_diff", "date_listed", "date_last", "date_delivery_last"
 from "tmp_YYYYins" 
  where "instrumentid" not in ('S0001', 'S9901', 'S9909') 
 except select
 "instrumentid", "lot", "min_price_diff", "date_listed", "date_last", "date_delivery_last"
 from "YYYYins"; """,

'insert_replace':
""" INSERT OR REPLACE INTO "YYYYins"(
"instrumentid", "lot", "min_price_diff", "date_listed", "date_last", "date_delivery_last", "manual_flag", "update_time"
) select
"instrumentid", "lot", "min_price_diff", "date_listed", "date_last", "date_delivery_last", 0,           datetime()
from ( select 
 "instrumentid", "lot", "min_price_diff", "date_listed", "date_last", "date_delivery_last"
 from "tmp_YYYYins" except select
 "instrumentid", "lot", "min_price_diff", "date_listed", "date_last", "date_delivery_last"
 from "YYYYins") 
 where "instrumentid" not in ('S0001', 'S9901', 'S9909')
 ORDER BY "date_listed"; """,

'diff_tmp_grouped':
""" select "date_listed", count(*) cnt from (select 
 "instrumentid", "lot", "min_price_diff", "date_listed", "date_last", "date_delivery_last"
 from "tmp_YYYYins"
  where "instrumentid" not in ('S0001', 'S9901', 'S9909')
 except select
 "instrumentid", "lot", "min_price_diff", "date_listed", "date_last", "date_delivery_last"
 from "YYYYins") group by "date_listed" order by "date_listed"; """,

'print_count':
'select count(*) from "YYYYins";',

'limited_print':"""
select
 "instrumentid", "lot", "min_price_diff", "date_listed", "date_last", "date_delivery_last", "manual_flag", "update_time"
 from "YYYYins" order by "update_time" desc limit 30;""",

'insert_ignore':
""" INSERT OR IGNORE INTO YYYYins(
 "instrumentid", "lot", "min_price_diff", "date_listed", "date_last", "date_delivery_last", "manual_flag", "update_time"
 ) select
 "instrumentid", "lot", "min_price_diff", "date_listed", "date_last", "date_delivery_last", 0,           datetime()
 from "tmp_YYYYins"; """,

'insert':"""
INSERT INTO "YYYYins"(
 "instrumentid", "lot", "min_price_diff", "date_listed", "date_last", "date_delivery_last", "manual_flag", "update_time"
 ) select
 "instrumentid", "lot", "min_price_diff", "date_listed", "date_last", "date_delivery_last", 0,           datetime()
 from ( select 
 "instrumentid", "lot", "min_price_diff", "date_listed", "date_last", "date_delivery_last"
 from "tmp_YYYYins" except select
 "instrumentid", "lot", "min_price_diff", "date_listed", "date_last", "date_delivery_last"
 from "YYYYins") 
 where "instrumentid" not in ('S0001', 'S9901', 'S9909')
 ORDER BY "date_listed";
""",
}
##
sqls_ins_wwww = {}
sqls_ins_xxxx_fo = {}
sqls_ins =(sqls_ins_zzzz, sqls_ins_xxxx, sqls_ins_yyyy, sqls_ins_wwww, sqls_ins_xxxx_fo)


sqls_daily_zzzz = {
'create_tmp':
"""
CREATE TEMP TABLE IF NOT EXISTS "tmp_daily" (
    "tradingday" INT NOT NULL,
    "instrumentid" TEXT NOT NULL,
    "open" DOUBLE ,
    "high" DOUBLE ,
    "low" DOUBLE ,
    "close" DOUBLE NOT NULL,
    "volume" INT NOT NULL,
    "openint" INT NOT NULL,
    "settlementprice" DOUBLE NOT NULL,
    "amount" DOUBLE NOT NULL,
    "PreSettlementPrice" DOUBLE NOT NULL,
    "PreClosePrice" DOUBLE NOT NULL,
    "deltaPrice1" DOUBLE NOT NULL,
    "deltaPrice2" DOUBLE NOT NULL,
    UNIQUE ("tradingday", "instrumentid")
);
""",

'delete_tmp': 'DELETE FROM "tmp_daily";',
'insert_tmp':
"""INSERT INTO "tmp_daily" 
("instrumentid","tradingday","precloseprice","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","amount","openint")
values (?,?,?,?,?,?,?,?,?,?,?,?,?,?); """,
'diff_tmp':
""" select * from (select 
"instrumentid","tradingday","precloseprice","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","amount","openint"
 from "tmp_daily" except select
"instrumentid","tradingday","precloseprice","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","amount","openint"
 from "daily") order by "tradingday"; """,

'insert_replace':
""" INSERT OR REPLACE INTO "daily"(
"instrumentid","tradingday","precloseprice","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","amount","openint") select
"instrumentid","tradingday","precloseprice","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","amount","openint"
from ( select 
"instrumentid","tradingday","precloseprice","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","amount","openint"
 from "tmp_daily" except select
"instrumentid","tradingday","precloseprice","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","amount","openint"
 from "daily") order by "tradingday"; """,

'diff_tmp_grouped':
""" select "tradingday", count(*) "cnt" from ( select 
"instrumentid","tradingday","precloseprice","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","amount","openint"
 from "tmp_daily" except select
"instrumentid","tradingday","precloseprice","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","amount","openint"
 from "daily") group by "tradingday" order by "tradingday"; """,

'print_count': "select count(*) from daily;",
'limited_print': """select
 "instrumentid","tradingday","precloseprice","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","amount","openint"
 from daily order by id desc limit 30;""",

'insert_ignore':
""" INSERT OR IGNORE INTO "daily" (
 "instrumentid","tradingday","precloseprice","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","amount","openint"
 ) select 
 "instrumentid","tradingday","precloseprice","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","amount","openint"
 from "tmp_daily" order by "tradingday"; """,

'insert':"""
INSERT INTO "daily"(
 "instrumentid","tradingday","precloseprice","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","amount","openint") select
 "instrumentid","tradingday","precloseprice","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","amount","openint"
 from (select 
 "instrumentid","tradingday","precloseprice","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","amount","openint"
 from "tmp_daily" except select
 "instrumentid","tradingday","precloseprice","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","amount","openint"
 from "daily") order by "tradingday";
""",
}
##
sqls_daily_xxxx = {
'create_tmp':
"""
CREATE TEMP TABLE IF NOT EXISTS "tmp_daily" (
  "tradingday" INT NOT NULL,
  "instrumentid" TEXT NOT NULL,
  "open" DOUBLE NOT NULL,
  "high" DOUBLE NOT NULL,
  "low" DOUBLE NOT NULL,
  "close" DOUBLE NOT NULL,
  "volume" INT NOT NULL,
  "openint" INT NOT NULL,
  "settlementprice" DOUBLE NOT NULL,
  "amount" DOUBLE NOT NULL,
  "PreSettlementPrice" DOUBLE NOT NULL,
  -- PreClosePrice DOUBLE NOT NULL,
  "deltaPrice1" DOUBLE NOT NULL,
  "deltaPrice2" DOUBLE NOT NULL,
  "deltaOpenint" INT NOT NULL,
  "settlementForDelivery" DOUBLE NOT NULL,
  UNIQUE ("tradingday", "instrumentid"),
  CHECK (("open" between "low" and "high") and ("close" between "low" and "high")));
""",

'delete_tmp': 'DELETE FROM "tmp_daily";',
'insert_tmp':
"""INSERT INTO "tmp_daily"
("tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","settlementForDelivery") values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?); """,
'diff_tmp':
""" select * from (select
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","settlementForDelivery"
 from "tmp_daily" except select
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","settlementForDelivery"
 from "daily") order by "tradingday";""",

'insert_replace':
""" INSERT OR REPLACE INTO "daily" (
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","settlementForDelivery")
 select
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","settlementForDelivery"
from ( select 
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","settlementForDelivery"
 from "tmp_daily" except select
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","settlementForDelivery"
 from "daily") order by "tradingday"; """,

'diff_tmp_grouped':
""" select "tradingday", count(*) "cnt" from ( select 
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","settlementForDelivery"
 from "tmp_daily" except select
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","settlementForDelivery"
 from "daily") group by "tradingday" order by "tradingday"; """,

'print_count': 'select count(*) from "daily";',
'limited_print': """
select 
 "id","tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","settlementForDelivery"
 from "daily" where "volume" > 0 order by "id" desc limit 30;
""",

'insert_ignore':
""" INSERT OR IGNORE INTO "daily" (
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","settlementForDelivery"
 select 
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","settlementForDelivery"
 from "tmp_daily" order by "tradingday"; """,

'insert':"""
INSERT INTO "daily" (
 "tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","settlementForDelivery")
 select
 "tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","settlementForDelivery"
 from ( select 
 "tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","settlementForDelivery"
 from "tmp_daily" except select
 "tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","settlementForDelivery"
 from "daily") order by "tradingday";
""",

}
##
sqls_daily_yyyy = {}
##
sqls_daily_wwww = {}
##
sqls_daily_xxxx_fo = {
'create_tmp':
"""
CREATE TEMP TABLE IF NOT EXISTS "tmp_daily_futopt" (
  "tradingday" INT NOT NULL,
  "instrumentid" TEXT NOT NULL,
  "open" DOUBLE NOT NULL,
  "high" DOUBLE NOT NULL,
  "low" DOUBLE NOT NULL,
  "close" DOUBLE NOT NULL,
  "volume" INT NOT NULL,
  "openint" INT NOT NULL,
  "settlementprice" DOUBLE NOT NULL,
  "amount" DOUBLE NOT NULL,
  "PreSettlementPrice" DOUBLE NOT NULL,
  "deltaPrice1" DOUBLE NOT NULL,
  "deltaPrice2" DOUBLE NOT NULL,
  "deltaOpenint" INT NOT NULL,
  "delta" DOUBLE NOT NULL,
  "impl_vol" DOUBLE NOT NULL,
  "vol_exe" INTEGER NOT NULL,
  UNIQUE ("tradingday", "instrumentid"),
  CHECK (("open" between "low" and "high") and ("close" between "low" and "high")));
""",

'delete_tmp': 'DELETE FROM "tmp_daily_futopt";',
'insert_tmp':
"""INSERT INTO "tmp_daily_futopt"
("tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","delta","impl_vol","vol_exe") values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?); """,
'diff_tmp':
""" select * from (select
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","delta","impl_vol","vol_exe"
 from "tmp_daily_futopt" except select
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","delta","impl_vol","vol_exe"
 from "daily_futopt") order by "tradingday";""",

'insert_replace':
""" INSERT OR REPLACE INTO "daily_futopt" (
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","delta","impl_vol","vol_exe")
 select
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","delta","impl_vol","vol_exe"
from ( select 
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","delta","impl_vol","vol_exe"
 from "tmp_daily_futopt" except select
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","delta","impl_vol","vol_exe"
 from "daily_futopt") order by "tradingday"; """,

'diff_tmp_grouped':
""" select "tradingday", count(*) "cnt" from ( select 
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","delta","impl_vol","vol_exe"
 from "tmp_daily_futopt" except select
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","delta","impl_vol","vol_exe"
 from "daily_futopt") group by "tradingday" order by "tradingday"; """,

'print_count': 'select count(*) from "daily_futopt";',
'limited_print': """
select
 "id","tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","delta","impl_vol","vol_exe"
 from "daily_futopt" where "volume" > 0 order by "id" desc limit 30;
""",

'insert_ignore':
""" INSERT OR IGNORE INTO "daily_futopt" (
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","delta","impl_vol","vol_exe"
 select 
"tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","delta","impl_vol","vol_exe"
 from "tmp_daily_futopt" order by "tradingday"; """,

'insert':"""
INSERT INTO "daily_futopt" (
 "tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","delta","impl_vol","vol_exe")
 select
 "tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","delta","impl_vol","vol_exe"
 from ( select 
 "tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","delta","impl_vol","vol_exe"
 from "tmp_daily_futopt" except select
 "tradingday","instrumentid","presettlementprice","open","high","low","close","settlementprice","deltaPrice1","deltaPrice2","volume","openint","deltaOpenint","amount","delta","impl_vol","vol_exe"
 from "daily_futopt") order by "tradingday";
""",

}
sqls_daily = (sqls_daily_zzzz, sqls_daily_xxxx, sqls_daily_yyyy, sqls_daily_wwww, sqls_daily_xxxx_fo)
