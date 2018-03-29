# -*- coding: utf-8 -*-

import sqlite3
import re
import pdb
from datetime import datetime

from util_data import update_daily
from util_data import update_ins
from mylogger import MLogger
from db import DIR_LOG
from db import DIR_LOG_ERR
from db import DB_FILE_ZZZZ as DB_FILE
from db import ZZZZ_DATA_DIR as DATA_DIR
from db import ZZZZ_ABS_DIR as ABS_DIR
from patterns import zzzz_expression2 as expression
from patterns import zzzz_expression_data as expression_data

ERROR_DIR = "error.txt"
p=re.compile(expression)
pdata = re.compile(expression_data)
c = None
cur = None
formatter = '%(asctime)-15s %(name)-8s %(levelname)-6s - %(message)s'
mlog = MLogger.init_logger('logzzzz', formatter, DIR_LOG, DIR_LOG_ERR)
fun_print_daily = None
fun_print_ins = None


def init_print():
    global fun_print_ins, fun_print_daily
    from util_format_print import myfield
    from util_format_print import print_list_formatted

    p_instrumentid = myfield("instrumentid","ins",6)
    p_d_listed = myfield("date_listed","d_listed",8)
    p_d_last = myfield("date_last","d_last",8)
    p_date_delivery_1st = myfield("date_delivery_first","deliv_1st",8)
    p_date_delivery_last = myfield("date_delivery_last","deliv_last",8)
    p_p_listed = myfield("price_listed","p_listed",6)
    p_manual_flag = myfield("manual_flag", "m_flag", 1)
    p_update_time = myfield("update_time", "u_time", 19)

    p_tday = myfield("tradingday","tday",8)
    p_preclose = myfield("preclose","preclose",6)
    p_presettle = myfield("presettle","presettle",6)
    p_open = myfield("open","open",6)
    p_high = myfield("high","high",6)
    p_low = myfield("low","low",6)
    p_close = myfield("close","close",6)
    p_settle = myfield("settle","settle",6)
    p_deltap1 = myfield("deltap1","deltap1",6)
    p_deltap2 = myfield("deltap2","deltap2",6)
    p_vol = myfield("volume","vol",8)
    p_amount = myfield("amount","amount",9)
    p_openint = myfield("openint","opnint",8)

    fun_print_ins = lambda x: print_list_formatted((p_instrumentid,p_d_listed,p_d_last,p_date_delivery_1st,p_date_delivery_last,p_p_listed,p_manual_flag,p_update_time), x)
    fun_print_daily = lambda x: print_list_formatted((p_instrumentid,p_tday,p_preclose,p_presettle,p_open,p_high,p_low,p_close,p_settle,p_deltap1,p_deltap2,p_vol,p_amount,p_openint), x)
    print "init_print finished."


def connect_db(dbc=DB_FILE):
    global c, cur
    try:
        c = sqlite3.connect(dbc)
    except sqlite3.Error as err:
        print "connection failed, ret=%s" % err.args[0]
        raw_input("Failed connection. Press a key")
    else:
        cur = c.cursor()
        print "Connected with %s." % dbc

def main_daily(n=1000000):
    global ERROR_DIR, ABS_DIR, p, cur, fun_print_daily
    lastInstrumentid = [""]
    print id(lastInstrumentid)
    cnt = 0;
    ret_list = []
    with  open(ERROR_DIR,'a') as fstr_err:
        tmp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fstr_err.write("%s main_daily\n" % tmp)
        with open(ABS_DIR,'r') as fstr:
            lines=fstr.readlines()
            for line in lines:
                tmp = p.match(line)
                if (tmp is None):
                    fstr_err.write(line+'\n')
                    print line
                    continue
                if cnt < n:
                    process_1(ret_list, cur, tmp, lastInstrumentid) # reduce?
                    cnt = cnt + 1
    pdb.set_trace()
    update_daily(cur, ret_list, 'zzzz', 'alala', fun_print_daily)
    mlog.debug("main_daily: finish scanning %s and inserting into daily: %s." % (ABS_DIR, DB_FILE))
# c.commit()
# c.rollback()

def cleanup():
    global c, cur
    cur.close()
    c.close()
    cur = None
    c = None
      
def process_1(lst, cur, tmp, lastInstru):    
    tmp_lst = None
    tmp1 = tmp.groups()
    if tmp1[0] is not None:
        tmp_lst = (tmp1[0], tmp1[1],tmp1[2],tmp1[3],tmp1[4],tmp1[5],tmp1[6],tmp1[7],tmp1[8],tmp1[9],tmp1[10],tmp1[11],tmp1[12],tmp1[13])
        if lastInstru[0] != tmp1[0]:
            lastInstru[0] = tmp1[0]
    else:
        tmp_lst = (lastInstru[0], tmp1[1],tmp1[2],tmp1[3],tmp1[4],tmp1[5],tmp1[6],tmp1[7],tmp1[8],tmp1[9],tmp1[10],tmp1[11],tmp1[12],tmp1[13])
    lst.append(tmp_lst)


def main_ins():
    global cur, ERROR_DIR, DATA_DIR, pdata, DB_FILE, fun_print_ins
    lst_out = []
    with open(ERROR_DIR,'a') as fstr_err:
        tmp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fstr_err.write("%s  main_ins\n" % tmp)
        with open(DATA_DIR,'r') as fstr:
            lines = fstr.readlines()
            for line in lines:
                tmp = pdata.match(line)
                if (tmp is None):
                    fstr_err.write(line+'\n')
                    print line
                    continue
                tmp1 = tmp.groups()
                tmp1_0 = (tmp1[0]).upper()
                lst_out.append((tmp1_0, tmp1[1], tmp1[2], tmp1[3], tmp1[4], tmp1[5]))
    pdb.set_trace()
    update_ins(cur, lst_out, 'zzzz', 'ssss', fun_print_ins)
    mlog.debug("main_ins: finish scanning from %s and inserting into ZZZZins: %s." % (DATA_DIR, DB_FILE))
# cur.execute("RELEASE SAVEPOINT sidp;")
# c.rollback()


def print_afterwards_main_daily():
    global cur
    cur.execute("select count(*) from main.daily;");
    print "total counts: %s." % cur.fetchone()
    cur.execute("select max(tradingday) from main.daily;");
    print "max tradingday: %s " % cur.fetchone()
    cur.execute("select substr(tradingday,1,4) yy ,count(*) from daily group by yy order by yy;")
    tmp_adsa = cur.fetchall()
    for i in tmp_adsa: 
        print i


sql_consistency2 = "select count(*) from daily where open is NULL or high is NULL or low is NULL;"
sql_consistency3 = "select count(*) from daily where open is NULL and high is NULL and low is NULL;"
sql_consistency43 = """
select count(*) from (select * from (
select id from daily where open is NULL and high is NULL and low is NULL union 
select id from daily where open is NULL or high is NULL or low is NULL) 
except select * from (
select id from daily where open is NULL and high is NULL and low is NULL intersect
select id from daily where open is NULL or high is NULL or low is NULL) );
"""

sql_check1 = """select count(*)
-- close,presettlementprice,close-presettlementprice,deltaprice1,deltaprice2
 from daily where abs(close-presettlementprice-deltaprice1) > 1;
"""
sql_check2 = "select count(*) from daily where abs(settlementprice - presettlementprice-deltaprice2) > 1;"

checkdata = "select * from ZZZZIns order by date_listed ASC;"
