/* Process: newcontracts
sp  
create_tmp_tbl  
.import
trim
possible_chg(diff)  
insert  
real_chg  
RELEASE
*/
savepoint "sp_zzzz";
CREATE temp TABLE "t_buf"(
  "tradingday" INTEGER NOT NULL, 
  "instrumentid" TEXT UNIQUE NOT NULL
);
.separator ','
.import 'monthly_parameters.csv' "t_buf"

UPDATE "t_buf"
 set "instrumentid" = trim("instrumentid");
select "tradingday", "instrumentid" from "t_buf" except select "tradingday", "instrumentid" from "newcontracts";

INSERT OR IGNORE INTO "newcontracts" 
("tradingday", "instrumentid", "manual_flag", "update_time") select 
 "tradingday", "instrumentid", 0,           datetime() from "t_buf" order by "tradingday";

select "tradingday", "instrumentid" from "t_buf" except select "tradingday", "instrumentid" from "newcontracts";
select * from "newcontracts" order by "update_time" desc limit 30;

select tradingday,count(*) from newcontracts group by tradingday order by tradingday;
RELEASE SAVEPOINT "sp_zzzz";


/* Check consistency:
-------------------------------------------------------------------------------------
newcontracts against ZZZZins in date_listed;
daily against ZZZZins in (date_listed, date_last);
-------------------------------------------------------------------------------------
*/
select "uid", "tradingday" from (
 select upper("instrumentid") "uid", "tradingday" from "newcontracts" except
 select "instrumentid", "date_listed" from "ZZZZins"
) order by "tradingday", "uid";

select count(*) from (
 select upper("d"."instrumentid") "uid", min("d"."tradingday") "mind", max("d"."tradingday") "maxd" from "daily" "d" join "ZZZZins" "s" on "uid" == "s"."instrumentid"
 group by "uid" having ("mind" < "s"."date_listed") or ("maxd" > "s"."date_last"));
