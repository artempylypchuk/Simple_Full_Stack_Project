import psycopg2
import pandas as pd
import time
import numpy as np
import csv

#lists for count time of load
load_time = []
load_file = []

username = "Pylypchuk"
password = "3313"
database = "Lab1DB"
host = "db"
port = "5432"

#Creating a table
def create_table():
    while(True):
        try:
            conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)
            cur = conn.cursor()
            #cur.execute("drop table if exists zno;")
            cur.execute("""
                create table if not exists zno(
                    outid  varchar,
                    birth  smallint,
                    sextypename  varchar,
                    regname  varchar,
                    areaname  varchar,
                    tername  varchar,
                    regtypename  varchar,
                    tertypename  varchar,
                    classprofilename  varchar,
                    classlangname  varchar,
                    eoname  varchar,
                    eotypename  varchar,
                    eoregname  varchar,
                    eoareaname  varchar,
                    eotername  varchar,
                    eoparent  varchar,
                    ukrtest  varchar,
                    ukrteststatus  varchar,
                    ukrball100  decimal,
                    ukrball12 smallint,
                    ukrball smallint,
                    ukradaptscale  numeric,
                    ukrptname  varchar,
                    ukrptregname  varchar,
                    ukrptareaname  varchar,
                    ukrpttername  varchar,
                    histtest  varchar,
                    histlang  varchar,
                    histteststatus  varchar,
                    histball100  decimal,
                    histball12  smallint,
                    histball  smallint,
                    histptname  varchar,
                    histptregname  varchar,
                    histptareaname  varchar,
                    histpttername  varchar,
                    mathtest  varchar,
                    mathlang  varchar,
                    mathteststatus  varchar,
                    mathball100  decimal,
                    mathball12  smallint,
                    mathball  smallint,
                    mathptname  varchar,
                    mathptregname  varchar,
                    mathptareaname  varchar,
                    mathpttername  varchar,
                    mathdpalevel  varchar,
                    phystest  varchar,
                    physlang  varchar,
                    physteststatus  varchar,
                    physball100  decimal,
                    physball12  smallint,
                    physball  smallint,
                    physptname  varchar,
                    physptregname  varchar,
                    physptareaname  varchar,
                    physpttername  varchar,
                    chemtest  varchar,
                    chemlang  varchar,
                    chemteststatus  varchar,
                    chemball100  decimal,
                    chemball12  smallint,
                    chemball  smallint,
                    chemptname  varchar,
                    chemptregname  varchar,
                    chemptareaname  varchar,
                    chempttername varchar,
                    biotest  varchar,
                    biolang  varchar,
                    bioteststatus  varchar,
                    bioball100  decimal,
                    bioball12  smallint,
                    bioball  smallint,
                    bioptname  varchar,
                    bioptregname  varchar,
                    bioptareaname  varchar,
                    biopttername  varchar,
                    geotest  varchar,
                    geolang  varchar,
                    geoteststatus  varchar,
                    geoball100  decimal,
                    geoball12  smallint,
                    geoball  smallint,
                    geoptname  varchar,
                    geoptregname  varchar,
                    geoptareaname  varchar,
                    geopttername  varchar,
                    engtest  varchar,
                    engteststatus  varchar,
                    engball100  decimal,
                    engball12  smallint,
                    engdpalevel  varchar,
                    engball  smallint,
                    engptname  varchar,
                    engptregname  varchar,
                    engptareaname  varchar,
                    engpttername  varchar,
                    fratest  varchar,
                    frateststatus  varchar,
                    fraball100  decimal,
                    fraball12  smallint,
                    fradpalevel  varchar,
                    fraball  smallint,
                    fraptname  varchar,
                    fraptregname  varchar,
                    fraptareaname  varchar,
                    frapttername  varchar,
                    deutest  varchar,
                    deuteststatus  varchar,
                    deuball100  decimal,
                    deuball12  smallint,
                    deudpalevel  varchar,
                    deuball  smallint,
                    deuptname  varchar,
                    deuptregname  varchar,
                    deuptareaname varchar,
                    deupttername  varchar,
                    spatest  varchar,
                    spateststatus  varchar,
                    spaball100  decimal,
                    spaball12  smallint,
                    spadpalevel  varchar,
                    spaball  smallint,
                    spaptname  varchar,
                    spaptregname  varchar,
                    spaptareaname  varchar,
                    spapttername  varchar,
                    zno_year smallint);""")
            conn.commit()
            cur.close()
            conn.close()
            break
        except psycopg2.OperationalError:
            print("Connection lost\nConnecting...")
            time.sleep(5)
            continue

#Insert rows to DB
def insert_rows(df, columns, types, iteration):
    for n in range(0, len(df), iteration):
        while(True):
            try:
                conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)
                cur = conn.cursor()
                #Insert rows to DB
                for row in df.iloc[n:n + iteration].to_numpy():
                    cur.execute("INSERT INTO zno ({}) VALUES ({})".format(columns, types), tuple(row))
                conn.commit()
                print("Inserted rows: {}".format(iteration+n))
                cur.close()
                conn.close()
                break
            except psycopg2.OperationalError:
                print("Connection lost\nConnecting...")
                time.sleep(5)
                continue

    
#Loading all data from file to DB           
def load_data(fileName, encoding, year):
    #Get info from file, add a new column, change all null value.
    df = pd.read_csv(fileName, encoding=encoding, sep=';', decimal=',', low_memory=False, nrows=10000)
    df["zno_year"] = year
    df = df.replace([np.nan], [None])
    df.columns = df.columns.str.lower()

    #Input iteration num
    iteration = 200
    #Get column names to one string for insert data
    columns = ','.join(df.columns.values)
    #Count column and make a string of %s value for insert data
    types = ','.join(["%s" for s in df.columns.values])

    #Start to insert data to DB and count a time result of inserting
    print('Waiting for loading {}...'.format(fileName))
    start_time = time.perf_counter()
    insert_rows(df, columns, types, iteration)
    end_time = time.perf_counter()
    print('{} loaded\n'.format(fileName))

    load_time.append(end_time-start_time)
    load_file.append(fileName)

 #Write a result of inserting to time.txt file 
def write_time():
    with open('time.txt', 'w') as f:
        for i in range(len(load_file)):
            f.write("File {} time loading = {}\n".format(load_file[i], load_time[i]))

#Task function for variant - 5
def task():
    conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)
    cur = conn.cursor()
    with open('result.csv', 'w', encoding='utf-8') as file:
        while(True):
            try:
                cur.execute("""
                            SELECT regname, zno_year, 
                            ROUND(AVG(histball100), 3) AS avghistball100
                            FROM zno WHERE histteststatus = 'Зараховано'
                            GROUP BY regname, zno_year
                            ORDER BY regname, zno_year;
                            """)
                writer = csv.writer(file)
                writer.writerow([x[0] for x in cur.description])
                for row in cur:
                    writer.writerow(row)
                break
            except psycopg2.OperationalError:
                print("Connection lost\nConnecting...")
                time.sleep(5)
                continue
            cur.close()    
    conn.close()


if __name__ == "__main__":
    create_table()
    load_data('Odata2019File.csv', 'Windows-1251', 2019)
    load_data('Odata2020File.csv', 'cp1251', 2020)
    write_time()
    task()    
