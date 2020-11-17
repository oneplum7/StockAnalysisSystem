

tmp = str(2020-11-12)

# mycursor = mydb.cursor()

# #mycursor.execute("CREATE DATABASE mydatabase")

# mycursor.execute("SHOW DATABASES")

# for x in mycursor:
#   print(x)

def loadDatabase(self):
        self.mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="mysql",
        charset='utf8'
        )

        self.mycursor = self.mydb.cursor()