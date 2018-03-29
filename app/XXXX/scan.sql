/* Process: lastcontracts
sp  
create_tmp_tbl  
.import  
trim
possible_chg(diff)  
insert  
real_chg  
RELEASE
*/
savepoint "sp_xxxx1";
CREATE temp TABLE "t_buf" (
  "tradingday" INTEGER NOT NULL, 
  "instrumentid" TEXT UNIQUE NOT NULL
);
.separator ','
.import 'param_last.csv' "t_buf"

UPDATE "t_buf"
 set "instrumentid" = trim("instrumentid");
select "tradingday", "instrumentid" from "t_buf" except select "tradingday", "instrumentid" from "lastcontracts";

INSERT INTO "lastcontracts" 
("tradingday", "instrumentid", "manual_flag", "update_time") select 
 "tradingday", "instrumentid", 0,           datetime() from (
select "tradingday", "instrumentid" from "t_buf" except select "tradingday", "instrumentid" from "lastcontracts");

select "tradingday", "instrumentid" from "t_buf" except select "tradingday", "instrumentid" from "lastcontracts";
select * from "lastcontracts" order by "update_time" desc limit 30;

RELEASE SAVEPOINT "sp_xxxx1";


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
savepoint "sp_xxxx";
CREATE temp TABLE "t_buf" (
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

-- RELEASE SAVEPOINT "sp_xxxx";


/* Check consistency:
-------------------------------------------------------------------------------------
newcontracts against XXXXins in date_listed
lastcontracts against XXXXins in date_last
-------------------------------------------------------------------------------------
*/
select "instrumentid", "tradingday" from "newcontracts" except
 select "instrumentid", "date_listed" from "XXXXins";

select date_listed, count(*) cnt from XXXXins group by date_listed order by date_listed;
select date_last, count(*) cnt from XXXXins group by date_last order by date_last;

select "instrumentid", "tradingday" from "lastcontracts" except
 select "instrumentid", "date_last" from "XXXXins";


/* exchange for physical:
*/
savepoint "sp_efg";
CREATE temp TABLE "t_buf" (
 "tradingday" INTEGER NOT NULL, 
 "instrumentid" TEXT NOT NULL,
 "volume" INTEGER NOT NULL CHECK (0< "volume")
);
.separator '|'
.import 'tmp_exch4physical.txt' "t_buf"

UPDATE "t_buf"
 set "instrumentid" = trim("instrumentid");
select "tradingday", "instrumentid", "volume" from "t_buf"
 except select "tradingday", "instrumentid", "volume" from "exch4physical";

INSERT INTO "exch4physical"
 ("tradingday", "instrumentid", "volume") select 
  "tradingday", "instrumentid", "volume" from (
 select "tradingday", "instrumentid", "volume" from "t_buf"
 except
 select "tradingday", "instrumentid", "volume" from "exch4physical"
 );

select "tradingday", "instrumentid", "volume" from "t_buf"
 except
 select "tradingday", "instrumentid", "volume" from "exch4physical";

select * from "exch4physical" order by "tradingday" desc limit 30;

-- RELEASE SAVEPOINT "sp_efg";
