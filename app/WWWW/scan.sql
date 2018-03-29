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
savepoint 'sp_wwww1';
CREATE temp TABLE "t_buf" (
  "tradingday" INTEGER NOT NULL, 
  "instrumentid" TEXT UNIQUE NOT NULL,
  "price_listed" DOUBLE NOT NULL
);
.separator ','
.import 'tmp_lastcontracts.csv' "t_buf"

UPDATE "t_buf"
 set "instrumentid" = trim("instrumentid");

select "tradingday", "instrumentid", "price_listed" from "t_buf" except select "tradingday", "instrumentid", "price_listed" from "lastcontracts";

INSERT INTO "lastcontracts" 
("tradingday", "instrumentid", "price_listed", "manual_flag", "update_time") select 
 "tradingday", "instrumentid", "price_listed", 0,            datetime() from (
select "tradingday", "instrumentid", "price_listed" from "t_buf" except select "tradingday", "instrumentid", "price_listed" from "lastcontracts"
) order by "tradingday";

select "tradingday", "instrumentid", "price_listed" from "t_buf" except select "tradingday", "instrumentid", "price_listed" from "lastcontracts";
select count(*) from "lastcontracts";
select * from "lastcontracts" order by "update_time" desc limit 30;

-- RELEASE SAVEPOINT 'sp_wwww1';


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
savepoint sp_wwww;
CREATE temp TABLE "t_buf" (
  "tradingday" INTEGER NOT NULL, 
  "instrumentid" TEXT UNIQUE NOT NULL,
  "price_listed" DOUBLE NOT NULL
);

.separator ','
.import 'tmp_newcontracts.csv' "t_buf"

UPDATE "t_buf"
 set "instrumentid" = trim("instrumentid");
select "tradingday", "instrumentid", "price_listed" from "t_buf" except select "tradingday", "instrumentid", "price_listed" from "newcontracts";

INSERT INTO "newcontracts" 
("tradingday", "instrumentid", "price_listed", "manual_flag", "update_time") select 
 "tradingday", "instrumentid", "price_listed", 0,            datetime() from (
select "tradingday", "instrumentid", "price_listed" from "t_buf" except select "tradingday", "instrumentid", "price_listed" from "newcontracts"
) order by "tradingday";

select "tradingday", "instrumentid", "price_listed" from "t_buf" except select "tradingday", "instrumentid", "price_listed" from "newcontracts";
select count(*) from "newcontracts";
select * from "newcontracts" order by "update_time" desc limit 30;

-- RELEASE SAVEPOINT 'sp_wwww';
