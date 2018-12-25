import pyodbc

connection = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=warroom.stl.nfl.net;"
                      "Database=RadarDB;"
                      "Trusted_Connection=yes;")
cursor = connection.cursor()
cursor.execute("SELECT MasterPlayerID, ISNULL(FootballName, FirstName)FirstName, Lastname from POBase() where DraftYear > 2017")

results = cursor.fetchall()

for i in results:
    print(i)

cursor.close()
connection.close()