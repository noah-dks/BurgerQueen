import sqlite3

dbName = "BQv2.db"

def runSqlFile(dbConnection, filename):
    with open(filename, "r", encoding="utf-8") as f:
        dbConnection.executescript(f.read())

def main():
    dbConnection = sqlite3.connect(dbName)

    runSqlFile(dbConnection, "schema.sql")
    runSqlFile(dbConnection, "seed.sql")

    dbConnection.commit()
    dbConnection.close()
    print(f"✅ Created/updated {dbName} using schema.sql + seed.sql")

if __name__ == "__main__":
    main()
