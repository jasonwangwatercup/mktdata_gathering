CREATE TABLE "newcontracts" (
	"tradingday" INTEGER NOT NULL CHECK ("tradingday" > 19700101 AND "tradingday" < 21001231), 
	"instrumentid" TEXT UNIQUE NOT NULL CHECK( length("instrumentid") == 6), 
	"manual_flag" INT NOT NULL CHECK ("manual_flag" BETWEEN 0 AND 1),
	"update_time" TEXT NOT NULL
);
CREATE TABLE "lastcontracts" (
  "tradingday" INTEGER NOT NULL CHECK ("tradingday" > 19700101 AND "tradingday" < 21001231), 
  "instrumentid" TEXT UNIQUE NOT NULL CHECK( length("instrumentid") == 6),
  "manual_flag" INT NOT NULL CHECK ("manual_flag" BETWEEN 0 AND 1),
  "update_time" TEXT NOT NULL,  
  CHECK (substr("instrumentid", length("instrumentid")-3, 4) == substr(UPPER("tradingday"), 3, 4))
);
CREATE TABLE "daily" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  "tradingday" INT NOT NULL CHECK ("tradingday" BETWEEN 19700101 AND 21001231),
  "instrumentid" TEXT NOT NULL CHECK( length("instrumentid") == 6),
  "open" DOUBLE NOT NULL CHECK ("open" BETWEEN 0.0 AND 1000000.0),
  "high" DOUBLE NOT NULL CHECK ("high" BETWEEN 0.0 AND 1000000.0),
  "low" DOUBLE NOT NULL CHECK ("low" BETWEEN 0.0 AND 1000000.0),
  "close" DOUBLE NOT NULL CHECK ("close" BETWEEN 0.0 AND 1000000.0),
  "volume" INT NOT NULL CHECK ("volume" BETWEEN 0 AND 100000000000),
  "openint" INT NOT NULL CHECK ("openint" BETWEEN 0 AND 10000000000),
  "settlementprice" DOUBLE NOT NULL CHECK ("settlementprice" BETWEEN 0.0 AND 1000000.0),
  "amount" DOUBLE NOT NULL CHECK ("amount" BETWEEN 0.0 AND 10000000000.0),
  "PreSettlementPrice" DOUBLE NOT NULL CHECK ("PreSettlementPrice" BETWEEN 0.0 AND 1000000.0),
  "deltaPrice1" DOUBLE NOT NULL CHECK ("deltaPrice1" BETWEEN -1000000.0 AND 1000000.0),
  "deltaPrice2" DOUBLE NOT NULL CHECK ("deltaPrice2" BETWEEN -1000000.0 AND 1000000.0),
  "deltaOpenint" INT NOT NULL CHECK ("deltaOpenint" BETWEEN 0 AND 1000000000),
  "settlementForDelivery" DOUBLE NOT NULL CHECK ("settlementForDelivery" BETWEEN 0.0 AND 1000000.0),
  UNIQUE ("tradingday", "instrumentid"),
  CHECK (("open" between "low" and "high") and ("close" between "low" and "high"))
);
CREATE TABLE "daily_futopt" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  "tradingday" INT NOT NULL CHECK ("tradingday" BETWEEN 19700101 AND 21001231),
  "instrumentid" TEXT NOT NULL CHECK( 7 <= length("instrumentid")),
  "open" DOUBLE NOT NULL CHECK ("open" BETWEEN 0.0 AND 1000000.0),
  "high" DOUBLE NOT NULL CHECK ("high" BETWEEN 0.0 AND 1000000.0),
  "low" DOUBLE NOT NULL CHECK ("low" BETWEEN 0.0 AND 1000000.0),
  "close" DOUBLE NOT NULL CHECK ("close" BETWEEN 0.0 AND 1000000.0),
  "volume" INT NOT NULL CHECK ("volume" BETWEEN 0 AND 100000000000),
  "openint" INT NOT NULL CHECK ("openint" BETWEEN 0 AND 10000000000),
  "settlementprice" DOUBLE NOT NULL CHECK ("settlementprice" BETWEEN 0.0 AND 1000000.0),
  "amount" DOUBLE NOT NULL CHECK ("amount" BETWEEN 0.0 AND 10000000000.0),
  "PreSettlementPrice" DOUBLE NOT NULL CHECK ("PreSettlementPrice" BETWEEN 0.0 AND 1000000.0),
  "deltaPrice1" DOUBLE NOT NULL CHECK ("deltaPrice1" BETWEEN -1000000.0 AND 1000000.0),
  "deltaPrice2" DOUBLE NOT NULL CHECK ("deltaPrice2" BETWEEN -1000000.0 AND 1000000.0),
  "deltaOpenint" INT NOT NULL CHECK ("deltaOpenint" BETWEEN 0 AND 1000000000),
  "delta" DOUBLE NOT NULL,
  "impl_vol" DOUBLE NOT NULL,
  "vol_exe" INTEGER NOT NULL CHECK(0 <= "vol_exe"),
  UNIQUE ("tradingday", "instrumentid"),
  CHECK (("open" between "low" and "high") and ("close" between "low" and "high"))
);
CREATE TABLE "XXXXins" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "instrumentid" TEXT UNIQUE NOT NULL CHECK(LENGTH("instrumentid") == 6 OR 8 <= LENGTH("instrumentid")),
  "date_listed" INTEGER NOT NULL CHECK ("date_listed" >= 19700101 AND "date_listed" < 21001231),
  "date_last" INTEGER NOT NULL CHECK ("date_last" BETWEEN 19700101 AND 21001231),
  "date_delivery_first" INTEGER CHECK ("date_delivery_first" BETWEEN 19700101 AND 21001231),
  "date_delivery_last" INTEGER CHECK ("date_delivery_last" BETWEEN 19700101 AND 21001231),
  "price_listed" FLOAT CHECK ("price_listed" BETWEEN 0.0 AND 1000000.0),
  "manual_flag" INTEGER NOT NULL CHECK ("manual_flag" BETWEEN 0 AND 1), 
  "update_time" TEXT NOT NULL,
  CHECK("date_listed" <= "date_last"),
  CHECK ("date_last" < "date_delivery_first" and "date_delivery_first" < "date_delivery_last"),
  CHECK (substr("instrumentid",3,4) == substr(upper("date_delivery_first"),3,4) or "date_last" == 21001231 OR 8 <= LENGTH("instrumentid"))
);
CREATE TABLE exch4physical (
 "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
 "tradingday" INTEGER NOT NULL CHECK ("tradingday" BETWEEN 19700101 AND 21001231),
 "instrumentid" TEXT NOT NULL,
 "volume" INTEGER NOT NULL CHECK (0< "volume"),
 UNIQUE ("instrumentid", "tradingday")
 );
