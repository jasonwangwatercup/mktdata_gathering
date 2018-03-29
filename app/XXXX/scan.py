# -*- coding: utf-8 -*-

import sqlite3
import re
import pdb
from datetime import datetime

from util_data import update_daily
from mylogger import MLogger
from db import DIR_LOG
from db import DIR_LOG_ERR
from db import DB_FILE_XXXX as DB_FILE
from db import XXXX_ABS_DIR as ABS_DIR
from db import XXXX_ABS_DIR_FUTOPT as ABS_DIR_FUTOPT
from patterns import p_daily as p
from patterns import p_daily_futopt as p_futopt
from patterns import xxxx_pyymm_option as p_futopt_ins

ERROR_DIR = "error.txt"
sqls_insertion="""
insert or ignore into daily 
(tradingday,instrumentid,presettlementprice,open,high,low,close,settlementprice,deltaPrice1,deltaPrice2,volume,openint,deltaOpenint,amount,settlementForDelivery)
values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
"""
formatter = '%(asctime)-15s %(name)-8s %(levelname)-6s - %(message)s'
mlog = MLogger.init_logger('logxxxx', formatter, DIR_LOG, DIR_LOG_ERR)
con = None
cur = None
fun_print_daily = None
fun_print_daily_opt = None
fun_print_ins = None


def connect_db(db=DB_FILE):
    global mlog, con, cur
    try:
        con = sqlite3.connect(db)
    except sqlite3.Error as err:
        print "connection failed, ret=%s", err.args[0]
        raw_input("Failed connection. Press a key")
    else:
        cur = con.cursor()
        print "Connected with %s." % db

def main_daily(n=10000000):
    global ERROR_DIR, ABS_DIR, p, cur, mlog, fun_print_daily
    ret_list = []
    with  open(ERROR_DIR,'a') as fstr_err:
        tmp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fstr_err.write("%s main_daily\n" % tmp)
        t_fun = lambda x: process_2(ret_list, x, fstr_err, p)
        with open(ABS_DIR, 'r') as fstr:
            lines = fstr.readlines()
            map(t_fun, lines[:n])

    pdb.set_trace()
    tmp = filter(lambda x: (20100101 > int(x[0])) or (6 != len(x[1])), ret_list)
    if 0 < len(tmp):
        print "stop! something is wrong with XXXX.daily.format!"
        pdb.set_trace()
    update_daily(cur, ret_list, 'xxxx', 'sss', fun_print_daily)
    tmp_d = get_lasttradingday_from_daily()
    mlog.debug("main_daily: finish scanning %s and inserting into daily: %s, upto %s" % (ABS_DIR, DB_FILE, tmp_d))
# cur.execute('RELEASE SAVEPOINT "sp_sidp2";')

def main_daily_futopt(n=10000000):
    global ERROR_DIR, ABS_DIR_FUTOPT, p_futopt, cur, mlog, fun_print_daily_opt
    ret_list = []
    with  open(ERROR_DIR,'a') as fstr_err:
        tmp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fstr_err.write("%s main_daily_future_option\n" % tmp)
        t_fun = lambda x: process_2(ret_list, x, fstr_err, p_futopt, True)
        with open(ABS_DIR_FUTOPT, 'r') as fstr:
            lines = fstr.readlines()
            map(t_fun, lines[:n])

    pdb.set_trace()
    tmp = filter(lambda x: (20170101 > int(x[0])) or (7> len(x[1])), ret_list)
    if 0 < len(tmp):
        print "stop! something is wrong with XXXX.daily_futopt.format!"
        pdb.set_trace()
    update_daily(cur, ret_list, 'xxxx_futopt', 'lkj', fun_print_daily_opt)
    tmp_d = get_lasttradingday_from_daily(True)
    mlog.debug("main_daily_futopt: finish scanning %s and inserting into daily_futopt: %s, upto %s" % (ABS_DIR_FUTOPT, DB_FILE, tmp_d))
# cur.execute('RELEASE SAVEPOINT "sp_sidp2";')
# con.rollback()

     
def process_1(re_lst, tmp, futopt):
    tmp_date = ''.join((tmp.group(1),tmp.group(2),tmp.group(3)))
    tmp_ins = '1'.join((tmp.group(4)[:2], tmp.group(4)[2:]))
    tmp_lst = None
    if futopt is False:
        tmp_lst = (tmp_date, tmp_ins,tmp.group(5),tmp.group(6),tmp.group(7),tmp.group(8),tmp.group(9),tmp.group(10),tmp.group(11),tmp.group(12),tmp.group(13),tmp.group(14),tmp.group(15),tmp.group(16),tmp.group(17))
    else:
        tmp_lst = (tmp_date, tmp_ins,tmp.group(5),tmp.group(6),tmp.group(7),tmp.group(8),tmp.group(9),tmp.group(10),tmp.group(11),tmp.group(12),tmp.group(13),tmp.group(14),tmp.group(15),tmp.group(16),tmp.group(17),tmp.group(18),tmp.group(19))

    re_lst.append(tmp_lst)
                        
def process_2(re_lst, line, fstr_err, p, futopt=False):
    line = line.strip().replace(',', '')
    tmp = p.match(line)
    if tmp is None:
        fstr_err.write(line+'\n')
        print line
        return
    process_1(re_lst, tmp, futopt)

def check_daily(futopt=False):
    global sql_deltaprice_1, sql_deltaprice_2, sql_deltaprice_opt_1, sql_deltaprice_opt_2
    if futopt is False:
        if 0 != (cur.execute(sql_deltaprice_1).fetchone())[0]:
            print "wrong deltaprice_1!!!!!! \n"
            pdb.set_trace()     
        if 0 != (cur.execute(sql_deltaprice_2).fetchone())[0]:
            print "wrong deltaprice_2!!!!! \n"
            pdb.set_trace() 
        print '\n'.join(map(lambda x:str(x), cur.execute("select tradingday, count(*) cnt from daily group by tradingday order by tradingday DESC limit 30;").fetchall()))
    else:
        if 0 != (cur.execute(sql_deltaprice_opt_1).fetchone())[0]:
            print "futopt: wrong deltaprice_1!!!!!! \n"
            pdb.set_trace()     
        if 0 != (cur.execute(sql_deltaprice_opt_2).fetchone())[0]:
            print "futopt: wrong deltaprice_2!!!!! \n"
            pdb.set_trace() 
        print '\n'.join(map(lambda x:str(x), cur.execute("select tradingday, count(*) cnt from daily_futopt group by tradingday order by tradingday DESC limit 30;").fetchall()))
        

def update_ins():
    pdb.set_trace()
    global cur, sqls_ins_xxxx, DB_FILE, mlog, p_futopt_ins
    sqls = sqls_ins_xxxx
    b_xxxxins_limitprint = False
    cur.execute('SAVEPOINT "sp_update_in";')

    tmp_d = get_lasttradingday_from_daily(False, True)
    try:
        cur.execute(sqls['create_tmp'])
    except sqlite3.Error as e:
        print "Failed to create tmp_XXXXins, %s. ... PAUSED..." % e.args[0]
        pdb.set_trace()
    cur.execute(sqls['delete_tmp'])
    try:
        cur.execute(sqls['insert_tmp'])
        cur.execute(sqls['insert_tmp_opt'])
    except sqlite3.Error as e:
        print "Failed to insert into tmp_XXXXins, %s. ... PAUSED..." % e.args[0]
        pdb.set_trace()

    tmp_d2 = cur.execute(sqls['max_xxxxins_fut_listed']).fetchall()
    if 0>= len(tmp_d2):
        print "failed to fetch max(date_listed) from XXXXins' fut.\nPAUSED & return.."
        pdb.set_trace()
        return
    else:
        max_date_listed_xxxxins_fut = max(tmp_d2[0][0], 19700101)
    tmp_d3 = cur.execute(sqls['date_lastevent']).fetchall()
    if 0>= len(tmp_d3):
        print "failed to fetch max(date_last) from XXXXins' non-21001231-date_last contracts.\nPAUSED & return.."
        pdb.set_trace()
        return
    else:
        date_lastevent = max(tmp_d3[0][0], 19700101)

    tmp_p0 = cur.execute(sqls['partition_0'],(max_date_listed_xxxxins_fut,)).fetchall()
    if 0 < len(tmp_p0):
        print "fut instrumentids from XXXXins fails consistency_check between still listing and unlisted.\nPAUSED. PLEASE refer followings:"
        for i in tmp_p0:
            print i
        pdb.set_trace()

    tmp_p1 = cur.execute(sqls['partition_1'],(date_lastevent,)).fetchone()
    if tmp_p1 is not None and 0 < tmp_p1[0]:
        print "tmp_XXXXins not consistent with XXXXins in instrumentids unlisted.\nPAUSED. PLEASE check:"
        pdb.set_trace()

    tmp_p2 = cur.execute(sqls['partition_2'],(date_lastevent,)).fetchone()
    if tmp_p2 is not None and 0 < tmp_p2[0]:
        print "tmp_XXXXins not consistent with XXXXins in instrumentids still listing .\nPAUSED. PLEASE check:"
        for i in tmp_p2:
            print i
        pdb.set_trace()

    tmp_p3 = cur.execute(sqls['partition_3'],(date_lastevent,)).fetchall()
    if 0 < len(tmp_p3):
        print "tmp_XXXXins not consistent with XXXXins in instrumentids newly listed and not added yet.\nPAUSED. PLEASE check:"
        for i in tmp_p3:
            print i
        pdb.set_trace()

    tmp_d1 = cur.execute(sqls['max_tmpins_d_last']).fetchone()
    if tmp_d1 is None:
        print "failed to fetch max(date_last) from tmp_XXXXins.\nPAUSED & return.."
        pdb.set_trace()
        return
    else:
        max_date_last_tmpins = tmp_d1[0]
        if max_date_last_tmpins!= tmp_d:
            print "stranger, max_date_last_tmpins!= tmp_d!\nPAUSED& have a look!"
            pdb.set_trace()

    tmp_u4p = cur.execute(sqls['update_4_preview2'], (date_lastevent, max_date_last_tmpins)).fetchall()
    if 0 >= len(tmp_u4p):
        print "no instrumentid from XXXXins are unlisted during (%s, %s), both ending tradingdays not included.\nPAUSED&CONTINUE." % (date_lastevent, max_date_last_tmpins)
        pdb.set_trace()
    else:
        b_xxxxins_limitprint = True
        print "|%4s|%12s|%11s|%11s|" % ("id","instrumentid", "date_listed", "date_last")
        for i in tmp_u4p:
            print "|%4s|%12s|%11s|%11s|" % (i[0], i[1], i[2], i[3])
        print "the above instrumentids are unlisted during (%s, %s), both ending tradingdays not included\nContinue to specify their date_last from 21001231, if nothing abnormal.\n\nIf there are some beginning with the id of -1, they are listed and **UNLISTED** after %s and before %s, who would **NOT** be updated here and insteadly, would be inserted in the following session of insertion." % (date_lastevent, max_date_last_tmpins, date_lastevent, max_date_last_tmpins)
        pdb.set_trace()
        try:
            cur.execute(sqls['update_4'], (date_lastevent, max_date_last_tmpins))
        except sqlite3.Error as e:
            print "Failed to update XXXXins.date_last, %s. ... PAUSED..." % e.args[0]
            pdb.set_trace()

    tmp_i5p = cur.execute(sqls['insert_5_preview'], (date_lastevent,)).fetchall()
    if 0 >= len(tmp_i5p):
        print "no instrumentid from XXXXins are listed during (%s, %s], right ending tradingday included.\nPAUSED&CONTINUE." % (date_lastevent, max_date_last_tmpins)
        pdb.set_trace()
    else:
        b_xxxxins_limitprint = True

        tmp_i5p2 = []
        tmp_i5p3 = []
        for i in xrange(len(tmp_i5p)):
            if tmp_i5p[i][2] < max_date_last_tmpins:
                tmp_i5p2.append(tmp_i5p[i])
                tmp_i5p3.append(i)
        if 0 < len(tmp_i5p3):
            tmp_i5p3.sort(None, None, True)
            for j in tmp_i5p3:
                tmp_i5p.pop(j)

        print "%12s|%11s|%18s|" % ("instrumentid", "date_listed", "date_last")
        for k in tmp_i5p2:
            print "%12s|%11s|%18s|" % (k[0], k[1], k[2])
        for i in tmp_i5p:
            print "%12s|%11s|21001231(%8s)|" % (i[0], i[1], i[2])
        print "the above instrumentids are listed during (%s, %s], right ending tradingday included.\nContinue to insert them into XXXXins if nothing abnormal." % (date_lastevent, max_date_last_tmpins)
        pdb.set_trace()
  
        if 0 < len(tmp_i5p2):
            try:
                cur.executemany(sqls['insert_5b'], tmp_i5p2)
            except sqlite3.Error as e:
                print "Failed to insert into XXXXins, %s. ... PAUSED..." % e.args[0]
                pdb.set_trace()
        try:
            cur.executemany(sqls['insert_5a'], map(lambda x: (x[0],x[1]), tmp_i5p))
        except sqlite3.Error as e:
            print "Failed to insert into XXXXins, %s. ... PAUSED..." % e.args[0]
            pdb.set_trace()

    # check consitency
    if 0 < len(cur.execute(sqls['consistency_lastcontracts'], (max_date_last_tmpins,)).fetchall()):
        print "InConsistency with lastcontracts... PAUSED...\nThis MAY NOT be a problem if 'max_date_last_tmpins' happens to be the date_last, for the following reasons\ndate_last is confirmed one day after its last tradingday, since this check may happen any day other than the event of newcontracts,\nbecause futopt's lastcontract info not recorded, and this check has to be carried out for each tradingday.\nyou cannot judge a contract's last tradingday simply by its trading info, without any other clues(info)."
        pdb.set_trace()
    if 0 < len(cur.execute(sqls['consistency_newcontracts'], (max_date_last_tmpins,)).fetchall()):
        print "InConsistency with newcontracts... PAUSED...\n(for future contracts only, and futopt not checked.)"
        pdb.set_trace()

    if 0 < (cur.execute(sqls['consistency_ticker_datelast']).fetchone())[0]:
        print "consistency_ticker_datelast failed..PAUSED..."
        pdb.set_trace()
    tmp_ck_opt = cur.execute(sqls['consistency_ticker_datelast_opt']).fetchall()
    if 0 < len(tmp_ck_opt):
        if len(tmp_ck_opt) > sum(map(lambda x:verify_consistency_lastdate(x, p_futopt_ins, 2), tmp_ck_opt)):
            print "consistency in futopt(unlisted) failed..\nPAUSED"
            pdb.set_trace()

    if b_xxxxins_limitprint is True:
        print "The updated XXXXins has %s records." % cur.execute(sqls['print_count']).fetchone()
        tmp_p = cur.execute(sqls['limited_print']).fetchall()
        if 0 < len(tmp_p):
            fun_print_ins(tmp_p)
        print "The above are the last 30 updated records from XXXXins:\nContinue if OK."
        pdb.set_trace()

    print "finally, if nothing unlisted or listed please rollback, and otherwise release the savepoint.\n\n%s\n\n%s" % ("con.rollback()","""cur.execute('RELEASE SAVEPOINT "sp_update_in";')""")
    mlog.debug("update_ins: XXXXins is updated, %s, and up to: %s." % (DB_FILE, tmp_d))
# con.commit()
# cur.execute('RELEASE SAVEPOINT "sp_update_in";')


def cleanup():
    cur.close()
    con.close()    
    print "cleaned up.\n"

def check_dates_preliminary():
    print "check for fut contracts only now...\nPAUSED.."
    print "the total counts of instrumentids should be constant, in most time.\nand this function is not implemented yet.\nreturn"
    pass


def get_lasttradingday_from_daily(futopt_only=False, fut_futopt_both=False):
    global cur
    if cur is None:
        print "No legal connection and return now."
        return
    re = None
    re1 = None

    sqls = "select max(tradingday) from daily;"
    re = cur.execute(sqls).fetchone()
    if re is None or 0 >= len(re):
        print "No feasible results from daily: %s..\nPAUSED&return." % re
        pdb.set_trace()
        return

    sqls1 = "select max(tradingday) from daily_futopt;"
    re1 = cur.execute(sqls1).fetchone()
    if re1 is None or 0 >= len(re1):
        print "No feasible results from daily_futopt: %s..\nPAUSED&return." % re1
        pdb.set_trace()
        return

    if futopt_only is False and fut_futopt_both is False:
        return re[0]
    elif futopt_only is False and fut_futopt_both is True:
        if re[0] != re1[0]:
            print "daily not coordinated with daily_futopt:\nmax(tday): daily(%s), daily_futopt(%s).\nPAUSED&check carefully, please." % (re[0], re1[0])
            pdb.set_trace()
            return
        else:
            return re[0]
    elif futopt_only is True and fut_futopt_both is False:
        return re1[0]
    else:
        print """the situation when 'futopt_only is True and fut_futopt_both is True' is impossible!\nPAUSED&return."""
        return


def verify_consistency_lastdate(tmp1, pyymm_option, diff=2):
    assert tmp1[1] > 19700101 and tmp1[1] < 21001231
    tmp_yymm = int(pyymm_option.match(tmp1[0]).group(2))
    tmp_cnt_in_months = tmp_yymm/100*12 + tmp_yymm%100
    if 0 == (tmp_cnt_in_months - diff)%12:
        tmp_yymm_minus = (tmp_cnt_in_months-diff - 12)/12*100 + 12
    else:
        tmp_yymm_minus = (tmp_cnt_in_months-diff)/12*100 + (tmp_cnt_in_months-diff)%12
    return str(tmp1[1])[2:6] == str(tmp_yymm_minus)


def init_print():
    global fun_print_daily, fun_print_daily_opt, fun_print_ins
    from util_format_print import myfield
    from util_format_print import print_list_formatted
    p_id = myfield("id","id",7)
    p_tday = myfield("tradingday","tday",8)
    p_instrumentid = myfield("instrumentid","ins",6)
    p_instrumentid_opt = myfield("instrumentid","ins_opt", 12)
    p_presettle = myfield("presettle","presettle",6)
    p_open = myfield("open","open",6)
    p_high = myfield("high","high",6)
    p_low = myfield("low","low",6)
    p_close = myfield("close","close",6)
    p_settle = myfield("settle","settle",6)
    p_deltap1 = myfield("deltap1","deltap1",6)
    p_deltap2 = myfield("deltap2","deltap2",6)
    p_vol = myfield("volume","vol",8)
    p_openint = myfield("openint","opnint",8)
    p_deltaopenint = myfield("deltaopenint","delta_openint",8)
    p_amount = myfield("amount","amount",9)
    p_settle4delivery = myfield("settle4delivery","settle4deliv",6)
    p_delta = myfield("delta","delta",7)
    p_impl_vol = myfield("impl_vol","impl_vol",6, '-')
    p_vol_exe = myfield("vol_exe","vol_exe",8)
    p_d_listed = myfield("date_listed","d_listed",8)
    p_d_last = myfield("date_last","d_last",8)
    p_manual_flag = myfield("manual_flag", "m_flag", 1)
    p_update_time = myfield("update_time", "u_time", 19)

    fun_print_daily = lambda x: print_list_formatted((p_id,p_tday,p_instrumentid,p_presettle,p_open,p_high,p_low,p_close,p_settle,p_deltap1,p_deltap2,p_vol,p_openint,p_deltaopenint,p_amount,p_settle4delivery), x)
    fun_print_daily_opt = lambda x: print_list_formatted((p_id,p_tday,p_instrumentid_opt,p_presettle,p_open,p_high,p_low,p_close,p_settle,p_deltap1,p_deltap2,p_vol,p_openint,p_deltaopenint,p_amount,p_delta,p_impl_vol,p_vol_exe), x)
    fun_print_ins = lambda x: print_list_formatted((p_id,p_instrumentid_opt, p_d_listed, p_d_last, p_manual_flag, p_update_time), x)

    print "print daily(_futop) is ready."


sql_deltaprice_1 = "select count(*) from daily where abs(close-presettlementprice-deltaprice1) > 1 and close != 0; -- close,presettlementprice,close-presettlementprice,deltaprice1,deltaprice2 "
sql_deltaprice_2 = "select count(*) from daily where abs(settlementprice - presettlementprice-deltaprice2) > 1 and close != 0;"
sql_deltaprice_opt_1 = "select count(*) from daily_futopt where abs(close-presettlementprice-deltaprice1) > 1 and close != 0; -- close,presettlementprice,close-presettlementprice,deltaprice1,deltaprice2 "
sql_deltaprice_opt_2 = "select count(*) from daily_futopt where abs(settlementprice - presettlementprice-deltaprice2) > 1 and close != 0;"


sqls_ins_xxxx = {
'create_tmp':"""
CREATE TEMP TABLE IF NOT EXISTS "tmp_XXXXins" (
    "instrumentid" TEXT UNIQUE NOT NULL CHECK( length("instrumentid") == 6 OR 8 <= LENGTH("instrumentid")),
    "date_listed" INT NOT NULL CHECK ("date_listed" > 19700101 AND "date_listed" < 21001231),
    "date_last" INT NOT NULL CHECK ("date_last" > 19700101 AND "date_last" < 21001231),
    CHECK("date_listed" <= "date_last")
    -- CHECK(substr("instrumentid",3,4) == substr(upper("date_delivery_first"),3,4))
);
""", 
'delete_tmp':
'DELETE FROM "tmp_XXXXins";',
'insert_tmp': """
INSERT INTO "tmp_XXXXins" ("instrumentid", "date_listed", "date_last")
 select "instrumentid", min("tradingday"), max("tradingday") from "daily" 
 group by "instrumentid";
""",
'insert_tmp_opt': """
INSERT INTO "tmp_XXXXins" ("instrumentid", "date_listed", "date_last")
 select "instrumentid",min("tradingday"),max("tradingday") from "daily_futopt"
 group by "instrumentid";
""",
'max_xxxxins_d_listed': 'SELECT max("date_listed") from "XXXXins";',
'max_xxxxins_fut_listed': """
SELECT max("date_listed") from "XXXXins" WHERE 6>= LENGTH(instrumentid);
""",
'date_lastevent': """
SELECT max(
 (SELECT max("date_last") from "XXXXins" WHERE 21001231 != "date_last"),
 (SELECT max("date_listed") from "XXXXins"));
""",
'partition_0': """
SELECT instrumentid, date_listed, date_last, manual_flag, update_time
 FROM XXXXins where date_last < 21001231 AND date_last >= ?1
 AND 6>= LENGTH(instrumentid);
""",
'partition_1':"""
SELECT COUNT(*) FROM (SELECT * FROM(
 SELECT instrumentid, date_listed, date_last FROM XXXXins WHERE date_last<= ?1
 UNION
 SELECT instrumentid, date_listed, date_last FROM tmp_XXXXins WHERE date_last <= ?1)
 EXCEPT SELECT * FROM(
 SELECT instrumentid, date_listed, date_last FROM XXXXins WHERE date_last<= ?1
 INTERSECT
 SELECT instrumentid, date_listed, date_last FROM tmp_XXXXins WHERE date_last <= ?1));
""",
'partition_2':"""
SELECT COUNT(*) FROM (SELECT * FROM(
 SELECT instrumentid, date_listed FROM XXXXins WHERE date_last == 21001231 
 UNION
 SELECT instrumentid, date_listed FROM tmp_XXXXins WHERE date_listed<= ?1
 AND date_last > ?1)
 EXCEPT SELECT * FROM(
 SELECT instrumentid, date_listed FROM XXXXins WHERE date_last == 21001231 
 INTERSECT
 SELECT instrumentid, date_listed FROM tmp_XXXXins WHERE date_listed<= ?1
 AND date_last > ?1));
""",
'partition_2_exception':"""
SELECT instrumentid, date_listed, date_last FROM tmp_XXXXins WHERE date_last== ?1;
""",
'partition_3':"""
SELECT instrumentid, date_listed, date_last FROM tmp_XXXXins
 WHERE instrumentid IN (
 SELECT instrumentid FROM tmp_XXXXins WHERE date_listed > ?1
 INTERSECT
 SELECT instrumentid FROM XXXXins);
""",
'max_tmpins_d_last':"""
SELECT max("date_last") from "tmp_XXXXins";
""",
'update_4_preview': """
SELECT c."id", t."instrumentid", t."date_listed", t."date_last"
 FROM "tmp_XXXXins" t
 JOIN "XXXXins" c ON t.instrumentid == c.instrumentid
 WHERE t.date_listed<= ?1 AND t.date_last > ?1 AND t.date_last < ?2
 ORDER BY t.date_last, t.instrumentid;
""",
'update_4_preview2': """
SELECT id, "instrumentid", "date_listed", "date_last" FROM( SELECT
 c."id", t."instrumentid", t."date_listed", t."date_last"
 FROM "tmp_XXXXins" t
 JOIN "XXXXins" c ON t.instrumentid == c.instrumentid
 WHERE t.date_listed<= ?1 AND t.date_last > ?1 AND t.date_last < ?2
 UNION
 SELECT -1, "instrumentid", "date_listed", "date_last" from "tmp_XXXXins"
 WHERE date_listed > ?1 AND date_last < ?2
 )
 ORDER BY date_last, date_listed, instrumentid;
""",
'update_4':"""
INSERT OR REPLACE INTO XXXXins (
 "id",  "instrumentid",   "date_listed",  "date_last", "manual_flag",  "update_time") SELECT
 c."id",t."instrumentid",t."date_listed",t."date_last",c."manual_flag",datetime()
 FROM "tmp_XXXXins" t
 JOIN "XXXXins" c ON t.instrumentid == c.instrumentid
 WHERE t.date_listed<= ?1 AND t.date_last > ?1 AND t.date_last < ?2;
""",
'insert_5_preview': """
SELECT "instrumentid", "date_listed", "date_last" from "tmp_XXXXins"
 WHERE date_listed > ?1 ORDER BY date_listed, instrumentid;
""",
'insert_5':"""
INSERT INTO XXXXins (
 "instrumentid", "date_listed", "date_last", "manual_flag", "update_time") SELECT
 "instrumentid", "date_listed",  21001231  , 0            , datetime() FROM "tmp_XXXXins"
 WHERE date_listed > ?1 ORDER BY date_listed, instrumentid;
""",
'insert_5a':"""
INSERT INTO XXXXins (
 "instrumentid", "date_listed", "date_last", "manual_flag", "update_time")
 VALUES (?,       ?,              21001231  , 0            , datetime());
""",
'insert_5b':"""
INSERT INTO XXXXins (
 "instrumentid", "date_listed", "date_last", "manual_flag", "update_time")
 VALUES (?,       ?,              ?  , 0            , datetime());
""",
'print_count': 'SELECT COUNT(*) FROM "XXXXins";',
'limited_print': 'SELECT id, instrumentid, date_listed, date_last, manual_flag,update_time FROM "XXXXins" ORDER BY "update_time" DESC LIMIT 30;',
'drop_diff_tmp_tabled': 'DROP TABLE IF EXISTS "tmp_diff_tmp";',
'consistency_lastcontracts': """
select "tradingday", UPPER("instrumentid") from "lastcontracts" where "tradingday" <= ?1
 except select "date_last", "instrumentid" from "XXXXins";
""",
'consistency_newcontracts': """
select "tradingday", UPPER("instrumentid") from "newcontracts" where "tradingday" <= ?
 except select "date_listed", "instrumentid" from "XXXXins";
""",
'consistency_ticker_datelast': """
select count(*) from "XXXXins" where not (substr("instrumentid",3,4) == substr(upper("date_last"),3,4) or "date_last" == 21001231)
 and 6 >= LENGTH(instrumentid);
-- select count(*) from "XXXXins" where not (substr("instrumentid",3,4) == substr(upper("date_delivery_first"),3,4) or "date_last" == 21001231);
""",
'consistency_ticker_datelast_opt': """
select instrumentid, date_last from "XXXXins" where 8 <= LENGTH("instrumentid") and 21001231> "date_last"; -- expired futopt only;
""",
}
