/* (1) insert into newcontracs_buf && newcontracts 
sp1
select_count
.import
trim
possible_chg(diff)  
insert  
real_chg  
RELEASE
 */
savepoint "sp1";
select "tradingday",count(*) from "newcontracts" group by "tradingday" order by "tradingday";
select count(*) from "newcontracts_buf";
-- delete from "newcontracts_buf"

.separator ','
.import 'tmp_newcontracts.csv' "newcontracts_buf"

UPDATE "newcontracts_buf"
 set "instrumentid" = trim("instrumentid");

select "tradingday", "instrumentid", "price_listed","uratio" from "newcontracts_buf" except
 select "tradingday", "instrumentid", "price_listed","uratio" from "newcontracts";

INSERT INTO "newcontracts"
("tradingday", "instrumentid", "price_listed", "manual_flag", "update_time","uratio") select
 "tradingday", "instrumentid", "price_listed", 0            ,  datetime(),"uratio" from (
select "tradingday", "instrumentid","price_listed","uratio" from "newcontracts_buf" except
 select "tradingday","instrumentid","price_listed","uratio" from "newcontracts") order by "tradingday";

select "tradingday", "instrumentid", "price_listed","uratio" from "newcontracts_buf" except
 select "tradingday", "instrumentid", "price_listed","uratio" from "newcontracts";
select count(*) from "newcontracts";
select * from "newcontracts" order by "update_time" desc limit 30;
delete from "newcontracts_buf";
RELEASE SAVEPOINT "sp1";

/* (2) insert into lastcontracts_buf && lastcontracts 
sp1
select_count
.import
trim
possible_chg(diff)  
insert  
real_chg  
RELEASE
 */
savepoint "sp2";
select "tradingday",count(*) from "lastcontracts" group by "tradingday" order by "tradingday";
delete from "lastcontracts_buf";

.separator ','
.import 'tmp_lastcontracts.csv' "lastcontracts_buf"
UPDATE "lastcontracts_buf"
 set "instrumentid" = trim("instrumentid");

select "tradingday", "instrumentid" from "lastcontracts_buf" except
 select "tradingday", "instrumentid" from "lastcontracts";

INSERT INTO "lastcontracts"
("tradingday", "instrumentid", "manual_flag", "update_time") select
 "tradingday", "instrumentid", 0            ,  datetime() from (
select "tradingday", "instrumentid" from "lastcontracts_buf" except
 select "tradingday","instrumentid" from "lastcontracts") order by "tradingday";

select "tradingday", "instrumentid" from "lastcontracts_buf" except
 select "tradingday", "instrumentid" from "lastcontracts";
select count(*) from "lastcontracts";
select * from "lastcontracts" order by "update_time" desc limit 30;
delete from "lastcontracts_buf";
-- RELEASE SAVEPOINT "sp2";


/* Check consistency:
-------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------
*/
select "uid", "tradingday" from (
 select upper("instrumentid") "uid", "tradingday" from "newcontracts" except
 select "instrumentid", "date_listed" from "YYYYins"
) order by "tradingday", "uid";
