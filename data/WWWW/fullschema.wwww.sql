CREATE TABLE monthly (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        month INT MOT NULL,
	instrumentid TEXT NOT NULL,
	open DOUBLE NOT NULL,
	high DOUBLE NOT NULL,
	low DOUBLE NOT NULL,
	close DOUBLE NOT NULL,
	volume INT NOT NULL,
	openint INT NOT NULL,
	settlementprice DOUBLE,
	amount DOUBLE NOT NULL,
        deltaPrice DOUBLE NOT NULL, 
        deltaOpenint INT NOT NULL,
	UNIQUE (month, instrumentid)
);
CREATE TABLE "newcontracts" (
    "tradingday" INTEGER NOT NULL CHECK ("tradingday" > 19700101 AND "tradingday" < 21001231), 
    "instrumentid" TEXT UNIQUE NOT NULL CHECK(length("instrumentid") in (5,6)), 
    "price_listed" DOUBLE NOT NULL CHECK("price_listed" BETWEEN 0.0 AND 1000000.0),	
    "manual_flag" INT NOT NULL CHECK ("manual_flag" BETWEEN 0 AND 1),
    "update_time" TEXT NOT NULL
	-- UNIQUE(tradingday, instrumentid)
);
CREATE TABLE "WWWWins" (
  "instrumentid" TEXT UNIQUE NOT NULL CHECK(length("instrumentid") in (5,6)),
  "date_listed" INT NOT NULL CHECK ("date_listed" > 19700101 AND "date_listed" < 21001231),
  "date_last" INT NOT NULL CHECK ("date_last" BETWEEN 19700101 AND 21001231),
  "date_delivery_first" INT CHECK ("date_delivery_first" BETWEEN 19700101 AND 21001231),
  "date_delivery_last" INT CHECK ("date_delivery_last" BETWEEN 19700101 AND 21001231),
  "price_listed" FLOAT CHECK ("price_listed" BETWEEN 0.0 AND 1000000.0),
  "manual_flag" INT NOT NULL CHECK ("manual_flag" BETWEEN 0 AND 1), 
  "update_time" TEXT NOT NULL,
  CHECK("date_listed" < "date_last"),
  CHECK ("date_last" <= "date_delivery_last"),
  CHECK ("date_delivery_first" <= "date_delivery_last"),
  -- CHECK(substr("instrumentid",length("instrumentid")-3,4) == substr(upper("date_delivery_first"),3,4))
  CHECK((substr("instrumentid",length("instrumentid")-3,4) == substr(upper("date_last"),3,4)) OR "date_last"== 21001231)
);
CREATE TABLE "lastcontracts" (
  "tradingday" INTEGER NOT NULL CHECK ("tradingday" > 19700101 AND "tradingday" < 21001231), 
  "instrumentid" TEXT UNIQUE NOT NULL CHECK( length("instrumentid") between 5 and 6),
  "price_listed" DOUBLE NOT NULL CHECK("price_listed" BETWEEN 0.0 AND 1000000.0),	
  "manual_flag" INT NOT NULL CHECK ("manual_flag" BETWEEN 0 AND 1),
  "update_time" TEXT NOT NULL,  
  CHECK (substr("instrumentid", length("instrumentid")-3, 4) == substr(UPPER("tradingday"), 3, 4))
);
/* No STAT tables available */
