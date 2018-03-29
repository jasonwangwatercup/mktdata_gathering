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
	settlementprice DOUBLE NOT NULL,
	amount DOUBLE NOT NULL,
        deltaPrice DOUBLE NOT NULL,
        deltaOpenint INT, 
	UNIQUE (month, instrumentid)
);
CREATE TABLE daily (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        tradingday INT MOT NULL,
	instrumentid TEXT NOT NULL,
	preclose DOUBLE NOT NULL,
	presettlement DOUBLE NOT NULL,

	open DOUBLE NOT NULL,
	high DOUBLE NOT NULL,
	low DOUBLE NOT NULL,
	close DOUBLE NOT NULL,
	volume INT NOT NULL,
	openint INT NOT NULL,
	settlement DOUBLE NOT NULL,
	amount DOUBLE NOT NULL,
        deltaprice1 DOUBLE NOT NULL,
        deltaprice2 DOUBLE NOT NULL,
	UNIQUE (tradingday, instrumentid)
);
CREATE TABLE "YYYYins" (
    "instrumentid" TEXT UNIQUE NOT NULL CHECK(length("instrumentid") in (5,6) or length("instrumentid") between 11 and 16),
    "lot" INT NOT NULL CHECK("lot" > 0),
    "min_price_diff" FLOAT NOT NULL CHECK ("min_price_diff" > 0.0),
    "date_listed" INT NOT NULL CHECK ("date_listed" > 19700101 AND "date_listed" < 21001231),
    "date_last" INT NOT NULL CHECK ("date_last" > 19700101 AND "date_last" < 21001231),
    "date_delivery_last" INT NOT NULL CHECK ("date_delivery_last" BETWEEN 19700101 AND 21001231),
    "manual_flag" INT NOT NULL CHECK ("manual_flag" BETWEEN 0 AND 1), 
    "update_time" TEXT NOT NULL,
    CHECK("date_listed" < "date_last" and "date_last" < "date_delivery_last"),
    CHECK (substr("instrumentid",length("instrumentid")-3,4) == substr(upper("date_last"),3,4) or length("instrumentid") between 11 and 16)
    -- consistency_check of options is done in python scripts.
);
CREATE TABLE "lastcontracts_buf" (
      "tradingday" INT NOT NULL CHECK ("tradingday" BETWEEN 19700101 AND 21001231),
      "instrumentid" TEXT UNIQUE NOT NULL CHECK(length("instrumentid") in (5,6) or length("instrumentid") in (11,16))
);
CREATE TABLE "lastcontracts" (
      "tradingday" INT NOT NULL CHECK ("tradingday" BETWEEN 19700101 AND 21001231),
      "instrumentid" TEXT UNIQUE NOT NULL CHECK(length("instrumentid") in (5,6) or length("instrumentid") in (11,16)),
      "manual_flag" INT NOT NULL CHECK ("manual_flag" between 0 and 1),
      "update_time" TEXT NOT NULL,
      CHECK (length("instrumentid") in (11,16) OR substr("instrumentid", length("instrumentid")-3, 4) == substr(UPPER("tradingday"), 3, 4))
);
CREATE TABLE "newcontracts" (
  "tradingday" INT NOT NULL CHECK ("tradingday" BETWEEN 19700101 AND 21001231)
  ,"instrumentid" TEXT UNIQUE NOT NULL CHECK(LENGTH("instrumentid") in (5,6) or 8 < LENGTH("instrumentid"))
  ,"manual_flag" INT NOT NULL CHECK ("manual_flag" in (0, 1))
  ,"update_time" TEXT NOT NULL
  ,"price_listed" FLOAT CHECK ("price_listed" > 0.0)
  ,"uratio" FLOAT NOT NULL DEFAULT 0.0 CHECK("uratio" BETWEEN 0.0 AND 1.0)
);
CREATE TABLE "newcontracts_buf" (
  "instrumentid" TEXT UNIQUE NOT NULL,
  "tradingday" INTEGER NOT NULL,
  "price_listed" FLOAT,
  "uratio" FLOAT
);
/* No STAT tables available */
