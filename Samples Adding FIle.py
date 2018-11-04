import pymysql
from tkinter import *
from tkinter import messagebox as ms
import datetime
now=datetime.datetime.now()
global today
today=now.strftime("%Y-%m-%d")
global time_now
time_now=now.strftime("%H:%M:%S")
mydbase=pymysql.connect(host="localhost",user="root",password="",database="sr_arms_and_ammo")
cursor=mydbase.cursor()

def add_into_handguns():
    sql="SELECT * FROM handguns"
    count=cursor.execute(sql)
    if count > 0:
        root=Tk()
        ms.showerror("Could Not Add","The Handguns Table Is Not Empty")
        root.destroy()
        return
    sql="INSERT INTO handguns(ModelName,ProductCode,Type,Caliber,Action,Capacity,BarrelLength,Grips,Stock,price) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    values=[("TAURUS MAGNUM 357","1465","REVOLVER",".357 MAGNUM","SINGLE/DOUBLE","5","2 IN","RUBBER","24","15000"),\
            ("MINI REVOLVER","14875","REVOLVER",".22 MAGNUM","SINGLE","5","15/8 IN","NONE","15","8000"),\
            ("TAURUS REVOLVER","14449","REVOLVER",".357 MAGNUM","SINGLE/DOUBLE","7","2 IN","SOLID WOOD","30","19000"),\
            ("SIG SAUER","10536","PISTOL",".9 MM","DOUBLE","17","4.7 IN","POLYMER","10","35000"),\
            ("CARACAL F","14950","PISTOL",".9MM ","SINGLE/DOUBLE","9","104 MM","POLYMER","28","32000")]
    cursor.executemany(sql,values)
    mydbase.commit()
def add_into_shotguns():
    sql="SELECT * FROM shotguns"
    count=cursor.execute(sql)
    if count > 0:
        root=Tk()
        ms.showerror("Could Not Add","The Shotguns Table Is Not Empty")
        root.destroy()
        return
    sql="INSERT INTO shotguns(ModelName,ProductCode,Action,Caliber,Capacity,BarrelLength,OverAllLength,Weight,Stock,price) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    values=[("SARSILMAZ","14587","PUMP ACTION","12 GAUGE","8","510 MM","51 IN","3.0 KG","19","54000"),\
            ("AKDAL MKA","14541","SEMI AUTO","12 GAUGE","5","470 MM","53 IN","3.25 KG","22","61000"),
            ("BERETTA","14781","SEMI AUTO","12 GAUGE","5","20 IN","42 CM","2.85 KG","6","72000"),\
            ("AKKAR CHURCHIL","10548","OVER UNDER","12 GAUGE","5","3 IN","365 MM","2.8 KG","17","43000"),\
            ("SARSILMAZ","14587","PUMP ACTION","12","8","5.1 IN","51 CM","3.0 KG","19","54000"),]
    cursor.executemany(sql,values)
    mydbase.commit()
def add_into_rifles():
    sql="SELECT * FROM rifles"
    count=cursor.execute(sql)
    if count > 0:
        root=Tk()
        ms.showerror("Could Not Add","The Rifles Table Is Not Empty")
        root.destroy()
        return
    sql="INSERT INTO rifles(ModelName,ProductCode,Action,Caliber,Capacity,BarrelLength,Weight,Sights,Stock,price) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    values=[("ARMSCOR AK","105457","SEMI AUTO",".22 LR","25","18 IN","6 LBS","FRONT HOODED","15","23000"),\
            ("WINCHESTER 70","14662","BOLT ACTION",".300 WIN","21","16 IN","9 LBS","NONE","13","34000"),\
            ("BRNO","14506","SEMI AUTO",".22 LR","10","15 IN","8 LBS","HOODED","17","26000"),\
            ("GSG AK","10043","SEMI AUTO",".22 LR","13","16.5 IN","9.6 LBS","ADJUSTABLE AK","14","21000"),\
            ("COLT M-4","14371","SEMI AUTO",".22 LR","22","14.5 IN","10 LBS","NONE","17","76000")]
    cursor.executemany(sql,values)
    mydbase.commit()
def add_into_airguns():
    sql="SELECT * FROM airguns"
    count=cursor.execute(sql)
    if count > 0:
        root=Tk()
        ms.showerror("Could Not Add","The Airguns Table Is Not Empty")
        root.destroy()
        return
    sql="INSERT INTO airguns(ModelName,ProductCode,Caliber,Action,FrontSight,RearSight,BarrelLength,Safety,Stock,price) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    values=[("HATSAN","15635",".177 MM","SINGLE","HOODED FRONT","NONE","21 IN","ANTI BEAR TRAP","21","37230"),\
            ("GAMO DELTA","14220",".177 PLT","SINGLE/BREAK","NORMAL","ADJUSATBLE","15.7 IN","MANUAL","15","24282"),\
            ("DIANA 31","15208",".177","BREAK","NONE","NONE","19.5 IN","AUTOMATIC","16","21486"),\
            ("BAIKAL","15193","5.5 MM","BREAK","NONE","NONE","480 MM","MANUAL","17","23862"),\
            ("CZ 634","0015",".634","BREAK","TUNNEL FRONT","NONE","20.5","AUTOMATIC","12","34321")]
    cursor.executemany(sql,values)
    mydbase.commit()
def add_into_ammunition():
    sql="SELECT * FROM ammunition"
    count=cursor.execute(sql)
    if count > 0:
        root=Tk()
        ms.showerror("Could Not Add","The Ammunition Table Is Not Empty")
        root.destroy()
        return
    sql="INSERT INTO ammunition(ModelName,ProductCode,Category,GunType,Stock,price) VALUES(%s,%s,%s,%s,%s,%s)"
    values=[("GAMO PELLET .22","14225","AIRGUN","NONE","18","1235"),\
            ("BULLET .45","10456","HANDGUN","PISTOL","17","890"),\
            ("WINCHESTER SS250","002","RIFLE","BOLT ACTION","16","2361"),\
            ("TORDO 12","14721","SHOTGUN","SEMI AUTO","12","2345"),\
            ("GAMO PLAT","10371","AIRGUN","NONE","13","2751")]
    cursor.executemany(sql,values)
    mydbase.commit()
def add_into_parts():
    sql="SELECT * FROM parts"
    count=cursor.execute(sql)
    if count > 0:
        root=Tk()
        ms.showerror("Could Not Add","The Parts Table Is Not Empty")
        root.destroy()
        return
    sql="INSERT INTO parts(ModelName,ProductCode,Category,GunType,Stock,price) VALUES(%s,%s,%s,%s,%s,%s)"
    values=[("AK DUST COVER","14251","RIFLE","BOLT ACTION","17","286"),\
            ("FLASH HIDER","15153","RIFLE","SEMI AUTO","12","864"),\
            ("RONI KIT","14260","HANDGUN","REVOLVER","21","9721"),\
            ("CHOCK","14262","SHOTGUN","PUMP ACTION","43","5000"),\
            ("BRASS CATCHER","14246","HANDGUN","PISTOL","47","7000")]
    cursor.executemany(sql,values)
    mydbase.commit()
def add_into_magazines():
    sql="SELECT * FROM magazines"
    count=cursor.execute(sql)
    if count > 0:
        root=Tk()
        ms.showerror("Could Not Add","The Magazines Table Is Not Empty")
        root.destroy()
        return
    sql="INSERT INTO magazines(ModelName,ProductCode,Category,GunType,Stock,price) VALUES(%s,%s,%s,%s,%s,%s)"
    values=[("GLOCK 9MM","10220","HANDGUN","PISTOL","18","15000"),\
            ("GLOCK 17","14386","HANDGUN","PISTOL","14","12000"),\
            ("RUGER","10158","RIFLE","SEMI AUTO","29","7500"),\
            ("ARMSCOR M16","14889","RIFLE","SEMI AUTO","28","10000"),\
            ("SAIGA 12","14984","SHOTGUN","SEMI AUTO","21","11999"),]
    cursor.executemany(sql,values)
    mydbase.commit()
def main():
        
        add_into_handguns()
        add_into_shotguns()
        add_into_rifles()
        add_into_airguns()
        add_into_ammunition()
        add_into_parts()
        add_into_magazines()
main()
