# -*- coding: utf-8 -*-

import sqlite3
import re
import pdb

from util_data import update_ins
from mylogger import MLogger
from db import DIR_LOG
from db import DIR_LOG_ERR
from db import DB_FILE_YYYY as DB_FILE
from db import YYYY_CONTRACT_DIR as CONTRACT_DIR
from db import YYYY_ABS_DIR as ABS_DIR
from patterns import yyyy_e_instru as e_instru
from patterns import yyyy_e_price as e_price
from patterns import yyyy_e_deltap as e_deltap
from patterns import yyyy_e_volume as e_volume
from patterns import yyyy_e_deltaOpenint as e_deltaOpenint
from patterns import yyyy_pdata_option_included_2 as pdata_option_included_2
from patterns import yyyy_pyymm_option as pyymm_option

ERROR_DIR = "error.txt"
sqls_insertion="""
insert or ignore into monthly 
(instrumentid,open,high,low,close,settlementprice,deltaPrice,volume,openint,deltaOpenint,amount,month)
values (?,?,?,?,?,?,?,?,?,?,?,?);
"""
p_in = re.compile(e_instru)
p_pr = re.compile(e_price)
p_dep = re.compile(e_deltap)
p_vo = re.compile(e_volume)
p_deo = re.compile(e_deltaOpenint)
pp = [p_in,p_pr,p_pr,p_pr,p_pr,p_pr,p_dep,p_vo,p_vo,p_deo,p_pr]

formatter = '%(asctime)-15s %(name)-8s %(levelname)-6s - %(message)s'
mlog = MLogger.init_logger('log_yyyy', formatter, DIR_LOG, DIR_LOG_ERR)
c = None
cur = None
# print "pdftohtml -i -q 201604.pdf"
fun_print_ins = None


def init_print():
    global fun_print_ins
    from util_format_print import myfield
    from util_format_print import print_list_formatted
    p_instrumentid_opt = myfield("instrumentid","ins_opt", 12)
    p_lot = myfield("log","lot", 5)
    p_min_price_diff = myfield("min_price_diff", "min_diff", 6)
    p_d_listed = myfield("date_listed","d_listed",8)
    p_d_last = myfield("date_last","d_last",8)
    p_date_delivery_last = myfield("date_delivery_last","deliv_last",8)
    p_manual_flag = myfield("manual_flag", "m_flag", 1)
    p_update_time = myfield("update_time", "u_time", 19)

    fun_print_ins = lambda x: print_list_formatted((p_instrumentid_opt,p_lot,p_min_price_diff,p_d_listed,p_d_last,p_date_delivery_last,p_manual_flag,p_update_time), x)


def connect_db(db=DB_FILE):
    global c, cur
    try:
        c = sqlite3.connect(db)
    except sqlite3.Error as err:
        print "connection failed, ret=%s", err.args[0]
        raw_input("Failed connection. Press a key")
    else:
        cur = c.cursor()
        print "Connected with %s." % db

def cleanup():
    cur.close()
    c.close()
      

def main_ins():
    global cur, ERROR_DIR, CONTRACT_DIR, pdata_option_included_2, fun_print_ins
    lst_out = []
    print "Start reading from %s." % CONTRACT_DIR
    with open(ERROR_DIR, 'a') as fstr_err:
        with open(CONTRACT_DIR, 'r') as fstr:
            lines = fstr.readlines()
            for line in lines:
                tmp = pdata_option_included_2.search(line)
                if (tmp is None):
                    fstr_err.write(line+'\n')
                    print line
                    continue
                tmp1 = tmp.groups()
                tmp1_0 = (tmp1[0]).upper()
                if tmp1[1] is None:
                    lst_out.append((tmp1_0, tmp1[2], tmp1[3], tmp1[4], tmp1[5], tmp1[6]))
                else:
                    if verify_consistency_lastdate(tmp1) is False:
                        fstr_err.write(line+'\n')
                        print "PAUSED: wrong lastdate:%s." % line
                        pdb.set_trace()
                    lst_out.append((tmp1_0, tmp1[2], tmp1[3], tmp1[4], tmp1[5], 21001231))
    pdb.set_trace()
    update_ins(cur, lst_out, 'yyyy', 'gkt', fun_print_ins)
    mlog.debug("main_ins: finish scanning from %s and inserting into YYYYins: %s." % (CONTRACT_DIR, DB_FILE))
    print """main_ins: finish scanning from %s and inserting into YYYYins: %s.\nplease choose either one of the following to release savepoint or rollback:\n\ncur.execute("RELEASE SAVEPOINT sidp;")\n\nor\n\ncon.rollback()\n""" % (CONTRACT_DIR, DB_FILE)
# cur.execute("RELEASE SAVEPOINT sidp;")


def verify_consistency_lastdate(tmp1):
    global pyymm_option
    tmp_yymm = int(pyymm_option.match(tmp1[0]).group(2))
    tmp_cnt_in_months = tmp_yymm/100*12 + tmp_yymm%100
    if 0 == (tmp_cnt_in_months - 1)%12:
        tmp_yymm_minus = (tmp_cnt_in_months-1 - 12)/12*100 + 12
    else:
        tmp_yymm_minus = (tmp_cnt_in_months-1)/12*100 + (tmp_cnt_in_months-1)%12

    if tmp1[5][2:6] != str(tmp_yymm_minus):
        return False
    else:
        return True
