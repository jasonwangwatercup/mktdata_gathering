CREATE TABLE "ZZZZins" (
    "instrumentid" TEXT UNIQUE NOT NULL CHECK( length("instrumentid") == 6),
    "date_listed" INT NOT NULL CHECK ("date_listed" BETWEEN 19700101 AND 21001231),
    "date_last" INT NOT NULL CHECK ("date_last" BETWEEN 19700101 AND 21001231),
    "date_delivery_first" INT NOT NULL CHECK ("date_delivery_first" BETWEEN 19700101 AND 21001231),
    "date_delivery_last" INT NOT NULL CHECK ("date_delivery_last" BETWEEN 19700101 AND 21001231),
    "price_listed" FLOAT NOT NULL CHECK ("price_listed" BETWEEN 0.0 AND 1000000.0),
    "manual_flag" INT NOT NULL CHECK ("manual_flag" BETWEEN 0 AND 1), 
    "update_time" TEXT NOT NULL,
    CHECK("date_listed" < "date_last" and "date_last" < "date_delivery_first" and "date_delivery_first" < "date_delivery_last"),
    CHECK(substr("instrumentid",3,4) == substr(upper("date_delivery_first"),3,4))
);
CREATE TABLE "newcontracts" (
	"tradingday" INTEGER NOT NULL CHECK ("tradingday" BETWEEN 19700101 AND 21001231), 
	"instrumentid" TEXT UNIQUE NOT NULL CHECK( length("instrumentid") == 6), 
	"manual_flag" INT NOT NULL CHECK ("manual_flag" BETWEEN 0 AND 1),
	"update_time" TEXT NOT NULL
);
CREATE TABLE "daily" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  "tradingday" INT NOT NULL CHECK ("tradingday" BETWEEN 19700101 AND 21001231),
  "instrumentid" TEXT NOT NULL CHECK( length("instrumentid") == 6),
  "open" DOUBLE CHECK ("open" BETWEEN 0.0 AND 1000000.0),
  "high" DOUBLE CHECK ("high" BETWEEN 0.0 AND 1000000.0),
  "low" DOUBLE CHECK ("low" BETWEEN 0.0 AND 1000000.0),
  "close" DOUBLE NOT NULL CHECK ("close" BETWEEN 0.0 AND 1000000.0),
  "volume" INT NOT NULL CHECK ("volume" BETWEEN 0 AND 100000000000),
  "openint" INT NOT NULL CHECK ("openint" BETWEEN 0 AND 10000000000),
  "settlementprice" DOUBLE NOT NULL CHECK ("settlementprice" BETWEEN 0.0 AND 1000000.0),
  "amount" DOUBLE NOT NULL CHECK ("amount" BETWEEN 0.0 AND 10000000000.0),
  "PreSettlementPrice" DOUBLE NOT NULL CHECK ("PreSettlementPrice" BETWEEN 0.0 AND 1000000.0),
  "PreClosePrice" DOUBLE NOT NULL CHECK ("PreClosePrice" BETWEEN 0.0 AND 1000000.0),
  "deltaPrice1" DOUBLE CHECK ("deltaPrice1" BETWEEN -1000000.0 AND 1000000.0),
  "deltaPrice2" DOUBLE CHECK ("deltaPrice2" BETWEEN -1000000.0 AND 1000000.0),
  UNIQUE ("tradingday", "instrumentid"),
  CHECK (("open" between "low" and "high") and ("close" between "low" and "high"))
);
