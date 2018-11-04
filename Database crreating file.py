import pymysql
import datetime
now=datetime.datetime.now()
global today
today=now.strftime("%Y-%m-%d")
global mydbase
global cursor
mydbase=pymysql.connect(host="localhost",user="root",password="",database="saim_arms")
cursor=mydbase.cursor()
from tkinter import *
from tkinter import messagebox as ms



'''---------------------------------CLASS FOR CHECKING AND CREATING DATABASE AND ITS ACCESS----------------------------------------'''
class Database_access():
    def __init__(self,name_of_database):
        if name_of_database == "":
            print("not null")
            exit(0)
        self.name_of_database=name_of_database
        self.check_database_complete()
    def create_whole_database(self,mydb,cur):
        cur.execute("CREATE DATABASE "+self.name_of_database)
        mydb.close()
        mydb=pymysql.connect(host="localhost",user="root",password="",database=self.name_of_database)
        cur=mydb.cursor()
        tables_list=["CREATE TABLE admins(Name VARCHAR(50) NOT NULL,AdminCode VARCHAR(50) NOT NULL,UserName VARCHAR(50),Password VARCHAR(50),Date_Of_Joining DATE)",\
                     "CREATE TABLE clients(Name VARCHAR(50) NOT NULL,Email VARCHAR(50),ContactNo VARCHAR(50) NOT NULL,Purchased_Items LONGTEXT NOT NULL,Bill_Amount FLOAT(50,5),Date_Of_Purchase DATE,Time TIME NOT NULL)",\
                     "CREATE TABLE handguns(ModelName VARCHAR(50) NOT NULL,ProductCode VARCHAR(50) NOT NULL,Type VARCHAR(50),Caliber VARCHAR(50),Action VARCHAR(50),Capacity VARCHAR(50),BarrelLength VARCHAR(50),Grips VARCHAR(50),Stock INT NOT NULL,Price Float(50,3))",\
                     "CREATE TABLE airguns(ModelName VARCHAR(50) NOT NULL,ProductCode VARCHAR(50) NOT NULL,Caliber VARCHAR(50) NOT NULL,Action VARCHAR(50) DEFAULT 'Not Specified',FrontSight VARCHAR(50),RearSight VARCHAR(50),BarrelLength VARCHAR(50) NOT NULL,Safety VARCHAR(50) DEFAULT 'Not Specified',Stock INT NOT NULL,Price FLOAT(50,3))",\
                     "CREATE TABLE rifles(ModelName VARCHAR(50) NOT NULL,ProductCode VARCHAR(50) NOT NULL,Action VARCHAR(50),Caliber VARCHAR(50) NOT NULL,Capacity VARCHAR(50) NOT NULL,BarrelLength VARCHAR(50) NOT NULL,Weight VARCHAR(50),Sights VARCHAR(50),Stock INT NOT NULL,Price FLOAT(50,3))",\
                     "CREATE TABLE shotguns(ModelName VARCHAR(50) NOT NULL,ProductCode VARCHAR(50) NOT NULL,Action VARCHAR(50),Caliber VARCHAR(50) NOT NULL,Capacity VARCHAR(50) NOT NULL,BarrelLength VARCHAR(50) NOT NULL,OverAllLength VARCHAR(50) NOT NULL,Weight VARCHAR(50),Stock INT NOT NULL,Price FLOAT(50,3))",\
                     "CREATE TABLE parts(ModelName VARCHAR(50) NOT NULL,ProductCode VARCHAR(50),Category VARCHAR(50) NOT NULL,GunType VARCHAR(50) DEFAULT 'Not Specified',Stock INT NOT NULL,Price FLOAT(50,3))",\
                     "CREATE TABLE ammunition(ModelName VARCHAR(50) NOT NULL,ProductCode VARCHAR(50),Category VARCHAR(50) NOT NULL,GunType VARCHAR(50) DEFAULT 'Not Specified',Stock INT NOT NULL,Price FLOAT(50,3))",\
                     "CREATE TABLE magazines(ModelName VARCHAR(50) NOT NULL,ProductCode VARCHAR(50),Category VARCHAR(50) NOT NULL,GunType VARCHAR(50) DEFAULT 'Not Specified',Stock INT NOT NULL,Price FLOAT(50,3))"]
        for i in tables_list:
            cur.execute(i)
        today=datetime.datetime.now()
        today=today.strftime("%Y-%m-%d")
        sql="INSERT INTO admins(Name,AdminCode,UserName,Password,Date_Of_Joining) VALUES(%s,%s,%s,%s,%s)"
        values=('Saim Akhtar','SR-059','StackSR','node786',today)
        cur.execute(sql,values)
        mydb.commit()
    def check_database_complete(self):
        mydb=pymysql.connect(host="localhost",user="root",password="")
        cur=mydb.cursor()
        cur.execute("SHOW DATABASES")
        list1=[]
        for i in cur:
            list1.append(i[0])
            #print(i[0])
        if self.name_of_database in list1:
            print(self.name_of_database +" Database already present")
        else:
            self.create_whole_database(mydb,cur)
            print("created")
    def add_table(self):
        name_table=input("Enter the name of the table: ")
        table_cols=int(input("Enter the number of columns to add in the table: "))
        string="CREATE TABLE " + name_table + "("
        for i in range(0,table_cols):
            string_input=input("Enter the name of the column and the data type in Format(name varchar(5o)): ")
            if i == table_cols-1:
                string=string + string_input
            else:
                string=string + string_input + ","
        string=string+ ")"
        mydb=pymysql.connect(host="localhost",user="root",password="",database="saim_arms")
        cur=mydb.cursor()
        cur.execute(string)
        mydb.close()
    def drop_table(self,table_name):
        mydb=pymysql.connect(host="localhost",user="root",password="",database="saim_arms")
        cur=mydb.cursor()
        string="DROP TABLE " + table_name
        cur.execute(string)
        mydb.close()
    def add_column(self):
        name_table=input("Enter the name of the table: ")
        col_name=input("Enter the name of the column and the data type in Format(name varchar(50)): ")
        string="ALTER TABLE " + name_table + " ADD COLUMN " + col_name
        mydb=pymysql.connect(host="localhost",user="root",password="",database="saim_arms")
        cur=mydb.cursor()
        cur.execute(string)
        mydb.close()
    def drop_column(self,table_name,col_name):
        string="ALTER TABLE " + table_name+ " DROP COLUMN " + col_name
        cursor.execute(string)
'''------------------------------------------------------------------------------------------------------------------------------------ '''
def main():
    name_of_database="sr_arms_and_ammo"
    name_of_database=name_of_database.strip()
    access=Database_access(name_of_database)
if __name__ == "__main__":
    main()
