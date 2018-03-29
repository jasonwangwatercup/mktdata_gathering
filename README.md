“Finance is data.” 

      ---Folk
      
There are some public and free data available from exchanges around the worlds. A simple glance is not enough and years of accumulation of data will pay you more premium relative to the costs thus rendered, in the long run. For long-term maintenance of the data, coherence and consistency are among the most important factors of success. Thus it is better to keep the data in a database rather than in text files. A single file database system, such as SQLite, may be enough to meet general needs from a single user. This program provides a primitive solution for organizing the data based on SQLite and Python scripts.


1) Purposes and Functions: what to store, why and how.

1.1) Trading instrument, market trading information and events

Generally there are three kinds of information available from future exchanges:

    .instruments (id, dates of listed and unlisted, etc.),
  
    .market trading data (open, high, low, close, volume, amount, open interest, etc.),
  
    .important events for an instrument such as being listed or unlisted.

1.2) Coherence and consistency

Besides value ranges limits and constraints imposed on table definitions, extra requirements are raised:

    .counts of instruments listed belong to the same sector per trading day are relative constant;

    .the duration of a instrument coincides with the events of the same instrument, such as being listed or unlisted.

1.3) Extensive

This program is general, and NOT SPECIFIED FOR ANY EXCHANGE DATA&DATA FORMATS. Several stereotype samples for possible data and data formats are provided. This program is licensed under MIT and you can adapt it to your own data and data formats. Overall this program is well suited for long-term accumulation of market data from an exchange.


2) Setting Up

2.1) Root

Choose a directory as the root and keep all the directories and files under it.
Currently these directories are included: “app”, “data” and “Downloads”, where “app” for Python and SQLite scripts, “data” for local database and text files, and “Downloads” is where data downloaded from Internet are stored.
The root directory is named DIR_ROOT and please remember it for the following parameterizing.

2.2) Databases

Create each sample database file in its own directory, all under the directory named data:

    DIR_ROOT\data\WWWW\WWWW.db,
  
    DIR_ROOT\data\XXXX\XXXX.db,
  
    DIR_ROOT\data\YYYY\YYYY.db,
  
    DIR_ROOT\data\ZZZZ\ZZZZ.db

Please keep them as the above, so as for the program to find them.

Here “WWWW”, “XXXX”, “YYYY” and “ZZZZ” are just symbols and bear no real meanings.

2.3) Installing schema

For each sample database separately, run following in the sqlite command lines:
  
    .read fullschema.zzzz.sql
  
    .read fullschema.yyyy.sql
  
    .read fullschema.xxxx.sql
  
    .read fullschema.wwww.sql

Then you can find that all the sample databases and tables are ready, with definitions and constraints on value ranges and other logics for consistency.


3) Parameterizing

3.1) db.py

Open the file “DIR_ROOT\app\data_utils\db.py”, and fill “DIR_”, the root directory, with the absolute path for the project, namely the value for DIR_ROOT.

3.2) patterns.py

Here are the regex patterns for the data, namely the instruments and other trading information, in Python scripts. The sample databases are from real exchange data, and in order to keep anonymousness these specific patterns are deleted, since even the names of the exchange should not be mentioned due to concerns raised in “Copy Rights and Other Issues” parts. Kindly please write out these detailed pattens by yourself, perhaps after many trials and errors.


4) Data Sources

To keep simplicity, this program ignores the data collection process and you should do it by yourself in your own way. It is advised to download your data manually, since fundamentally we are human and the understanding of data is far more important than collecting tons of data that are beyond your management and understanding. This program is more friendly towards a research analyst, who are bored in the ocean of data.


5) Run

5.1) Subprograms

Currently there are four sample databases: ZZZZ, YYYY, XXXX and WWWW, each for a stereotype of data and data formats from an exchange. So this program is divided into several separated sub programs, each run separately, and one checking consistency across different exchanges(still under test, not included now).

Except “DIR_ROOT\app\data_utils” where utilities are provided, each directory under “DIR_ROOT\app” contains a subprogram completely and exclusively, where one sql script maintains the informations about instrumentids, and Python scripts maintain other informations for market tradinging. These scripts should be be run manually and interactively in SQLite or Python command lines, and it is not hard to automate them. In most occasions functions are easy to understand and run, and in case of complexity a file named “log_run.py” is provided for convenience where the order to run the functions is specified, such as “DIR_ROOT\app\XXXX\log_run.py”, which is an example for you to explore.

5.2) Environmental variables

Environmental variables should be set before running sub programs, as demonstrated in “PRE_LOAD” part from “DIR_ROOT\app\XXXX\log_run.py”. Kindly please do it by yourself, since simplicity and easiness to maintain are included in the ideals of this program, and that is why Python and SQLite are chosen for implementation.

5.3) Downloads

You may download your data and keep them in “DIR_ROOT\Downloads”. In addition you may need to fill the temporary files in sub folders such as “DIR_ROOT\data\WWWW\tmp_lastcontracts.csv”, with the data extracted from files in “DIR_ROOT\Downloads”. Then the data will be processed and inserted or updated into the databases.

5.4) Getting your hands dirty

Repeatedly it is advised to get your hands dirty by elaborating over every details, before knowing the data and your peculiar needs and optimizing your process in your own scripts. Maybe it would cost your time and energy, but it pays off in the long run by accumulating data adjusted to your own needs and characteristics.


6) Copy Rights, Disclaims and Other Issues

Please pay attention to the copyrights and disclaims from your data source:

  .Generally speaking, the public and free data from an exchange belong to it and nobody else has any right to make a profit from it, in a certain way.
  
  .Any resource from the Internet is NOT guaranteed for its accuracy and completeness.
  
This program itself is licensed under MIT license.

6.1) Why named “mktdata_gathering”

As mentioned in the above, the data available from an exchange belong to itself, and you are only allowed to “eat” it but not to make a profit by “reselling” it or “planting as seeds”, as in the early hunting and gathering age of human kind.
