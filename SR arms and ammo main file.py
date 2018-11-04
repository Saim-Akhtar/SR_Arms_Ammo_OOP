import pymysql
from tkinter import *
from tkinter import messagebox as ms
from tkinter import ttk
import tkinter
from os import system
import time
import sys
import random
import datetime
now=datetime.datetime.now()
global today
today=now.strftime("%Y-%m-%d")
global mydbase
global cursor
mydbase=pymysql.connect(host="localhost",user="root",password="",database="sr_arms_and_ammo")
cursor=mydbase.cursor()
global login_boolean
login_boolean=False
global login_name
global login_user
root=Tk()
root.geometry("1400x820+100+0")
root.resizable(width=False,height=False)
root_pic=PhotoImage(file="guns ammo 4.gif")
root_label=Label(root,image=root_pic)
root_label.image=root_pic
root_label.place(x=0,y=0)



'''---------------------------------CLASS FOR FIREARMS STARTS HERE----------------------------------------------------------------------'''
class FireArms:
    no_of_firearms=0
    def __init__(self):
        self.gundisplay_frame=Frame(root)
        self.gundetail_frame=Frame(root)
        self.gunmodify_frame=Frame(root)
        self.guninput_frame=Frame(root)
        self.go_back_b=Button(root)
    def input_gun(self,category):
        if category == "handguns":
            one_key="Type"
            addition="(Pistol/Revolver)"
        elif category == "shotguns":
            one_key="Action"
            addition="(Pump-Action/Semi-Auto/Over Under)"
        elif category == "rifles":
            one_key="Action"
            addition="(Bolt-Action/Semi-Auto/Lever-Actiom)"
        elif category == "airguns":
            one_key="Action"
            addition=""
        self.gundisplay_frame.destroy()
        self.gundetail_frame.destroy()
        self.guninput_frame=Frame(root,width=1000,height=720,bd=10,relief=SOLID,bg='light blue')
        self.guninput_frame.place(x=200,y=70)
        try:
            imge=PhotoImage(file="input firearms.gif")
            img=Label(self.guninput_frame,image=imge)
            self.guninput_frame.image=imge
            img.place(x=0,y=0)
        except:
            True
        self.g1=StringVar()
        self.g2=StringVar()
        self.g3=StringVar()
        self.g4=StringVar()
        self.g5=StringVar()
        self.g6=StringVar()
        self.g7=StringVar()
        self.g8=StringVar()
        self.g9=StringVar()
        self.g10=StringVar()
        self.g11=StringVar()
        self.g12=StringVar()
        self.g13=StringVar()
        self.g14=StringVar()
        self.g15=StringVar()
        list_stringvars=[self.g1,self.g2,self.g3,self.g4,self.g5,self.g6,self.g7,self.g8,self.g9,self.g10,self.g11,self.g12,self.g13,self.g14,self.g15]
        sql="SHOW COLUMNS FROM " + category
        no_of_col=cursor.execute(sql)
        list_stringvars=list_stringvars[:no_of_col]
        string="("
        string1=""
        input_coy=40
        strs_count=0
        
        for cols in cursor:
            if cols[0] == one_key:
                input_label=Label(self.guninput_frame,text=cols[0]+ addition +"::",font=("Georgia",12),bd=10,relief=FLAT)
                input_label.place(x=60,y=input_coy)
            else:
                input_label=Label(self.guninput_frame,text=cols[0]+"::",font=("Georgia",12),bd=10,relief=FLAT)
                input_label.place(x=60,y=input_coy)
            input_entry=Entry(self.guninput_frame,textvariable=list_stringvars[strs_count],bd=8,relief=SUNKEN,width=50,justify="center")
            input_entry.place(x=450,y=input_coy)
            strs_count+=1
            input_coy+=50
            string+=cols[0] + ","
            string1+="%s" + ","
        string=string[:len(string)-1]
        string+=")"
        string1=string1[:len(string1)-1]
        entry_button=Button(self.guninput_frame,text="ADD To Record",bd=9,relief=RAISED,bg='brown',fg='white',font='Impact',\
                            command=lambda:self.entry_check(category,list_stringvars,string,string1),cursor="hand2")
        entry_button.place(x=400,y=620)
        entry_button=Button(self.guninput_frame,text="Cancel And Go Back",bd=9,relief=RAISED,bg='brown',fg='white',font='Impact',\
                            command=lambda:self.display_guns(category,self.col_list,self.clt),cursor="hand2")
        entry_button.place(x=700,y=620)
    def entry_check(self,category,list_stringvars,string,string1):
        
        check=list(map(lambda x: True if x.get() != '' else False,list_stringvars))
        ql="SELECT ProductCode From "+ category
        cursor.execute(ql)
        productcodeslist=[]
        for pros in cursor:
            productcodeslist.append(pros[0])

        if list_stringvars[1].get() in productcodeslist:
            ms.showerror("Can't Assign","ProductCode Already Available,Please Try Another")

        elif False in check:
            ms.showwarning("Data input Error","Entries Not Filled")
                    
        else:
            self.input(category,list_stringvars,string,string1)
        
    def input(self,category,list_stringvars,string,string1):
        sql="INSERT INTO " + category + string + " VALUES (" + string1 + ")"
        val=tuple(map(lambda x:x.get().upper(),list_stringvars))
        
        cursor.execute(sql,val)
        mydbase.commit()

        self.guninput_frame.destroy()
        self.go_back_b.destroy()
        self.display_guns(category,self.col_list,self.clt)
        
    def display_guns(self,category,col_list,clt):
        self.clt=clt
        self.category=category
        self.col_list=col_list
        self.guninput_frame.destroy()
        self.go_back_b.destroy()
        string=""
        for col in col_list:
            string+=col + ","
        string=string[:len(string)-1]
        sql="SELECT " + string + " FROM " + category
        no_of_el=cursor.execute(sql)
        self.mylist=cursor.fetchall()
        self.gundisplay_frame=Frame(root,width=800,height=760,bd=12,relief=SUNKEN)
        self.gundisplay_frame.place(x=40,y=40)
        try:
            imge=PhotoImage(file="display firearms.gif")
            img=Label(self.gundisplay_frame,image=imge)
            self.gundisplay_frame.image=imge
            img.place(x=0,y=0)
        except:
            True
        category_heading=Label(self.gundisplay_frame,text=category.upper() + " DISPLAY LIST",font=("stencil",25,"bold","italic"),fg="red")
        category_heading.place(x=220,y=10)
        serial_heading=Label(self.gundisplay_frame,text="S.NO",font=("Times",8),relief=RIDGE,bd=8,width=6)
        serial_heading.place(x=20,y=50)
        model_heading=Label(self.gundisplay_frame,text="ModelName",font=("Impact",11),relief=RIDGE,bd=8,width=18)
        model_heading.place(x=120,y=50)
        code_heading=Label(self.gundisplay_frame,text="ProductCode",font=("Impact",11),relief=RIDGE,bd=8,width=13)
        code_heading.place(x=280,y=50)
        type_heading=Label(self.gundisplay_frame,text="Type",font=("Impact",11),relief=RIDGE,bd=8,width=13)
        type_heading.place(x=410,y=50)
        stock_heading=Label(self.gundisplay_frame,text="Stock",font=("Impact",11),relief=RIDGE,bd=8,width=10)
        stock_heading.place(x=530,y=50)
        price_heading=Label(self.gundisplay_frame,text="Price RS",font=("Impact",11),relief=RIDGE,bd=8,width=13)
        price_heading.place(x=620,y=50)
        self.gundisplay_list=Frame(self.gundisplay_frame,bd=6,relief=SOLID,bg='brown')
        self.gundisplay_list.place(x=10,y=90)
        scroll_display=Scrollbar(self.gundisplay_list,orient="vertical")
        scroll_display.pack(side=RIGHT,fill=Y)
        self.Lb_sno=Listbox(self.gundisplay_list)
        self.Lb_model=Listbox(self.gundisplay_list)
        self.Lb_productcode=Listbox(self.gundisplay_list)
        self.Lb_type=Listbox(self.gundisplay_list)
        self.Lb_stock=Listbox(self.gundisplay_list)
        self.Lb_price=Listbox(self.gundisplay_list)
        self.guns_list=[self.Lb_sno,self.Lb_model,self.Lb_productcode,self.Lb_type,self.Lb_stock,self.Lb_price]
        for elem_list in self.guns_list:
            elem_list.config(width=12,bd=5,font=("Franklin Gothic Demi",10),bg="grey",\
                  fg='white',highlightthickness=7,\
                  highlightcolor='midnight blue',\
                  relief=SOLID,height=18,yscrollcommand=scroll_display.set)
            elem_list.pack(side=LEFT,fill=Y)
        self.Lb_sno.config(width=5,highlightcolor='red',highlightthickness=12,selectbackground='brown',cursor="hand2")
        self.Lb_stock.config(width=5)
        self.Lb_model.config(width=23)
        self.Lb_productcode.config(width=10)
        self.Lb_type.config(width=15)
        self.Lb_sno.bind('<<ListboxSelect>>',self.get_listelement)
        count_serials=1
        for row in self.mylist:
            self.Lb_sno.insert(END,count_serials)
            self.Lb_model.insert(END,row[0])
            self.Lb_productcode.insert(END,row[1])
            self.Lb_type.insert(END,row[2])
            self.Lb_stock.insert(END,row[3])
            self.Lb_price.insert(END,row[4])
            count_serials+=1
        
        scroll_display.config(command=self.scroll_view)
        
        if login_boolean == True:
            self.add_button=Button(self.gundisplay_frame,text="ADD A RECORD",bg="green",fg="black",relief=SOLID,bd=12,\
                                   command=lambda:self.input_gun(category),cursor="hand2")
            self.add_button.place(x=370,y=680)
        self.go_back_b=Button(root,text="RETURN TO MAIN DISPLAY",cursor="hand2",\
                              command=self.go_back,relief=RAISED,bd=15,bg='light blue',fg='black')
        self.go_back_b.place(x=1200,y=7)
    def scroll_view(self,*args):
        for elem in self.guns_list:
            elem.yview(*args)
    def go_back(self):
        self.gundetail_frame.destroy()
        self.gundisplay_frame.destroy()
        self.go_back_b.destroy()
        self.gunmodify_frame.destroy()
        self.guninput_frame.destroy()
        self.return_main_display()
    def get_listelement(self,Lb_sno):
        try:
            index=self.Lb_sno.curselection()[0]
            print(index)
            self.detail_gun(self.category,self.mylist[index][0],self.mylist[index][1])
        except:
            True
    
    def detail_gun(self,category,model,productcode):
        sql="SELECT * FROM "+ category + " WHERE ModelName = %s AND ProductCode = %s"
        val=(model,productcode)
        cursor.execute(sql,val)
        myres=cursor.fetchone()
        sql="SHOW COLUMNS FROM "+category
        cursor.execute(sql)
        self.gundetail_frame.destroy()
        self.gundetail_frame=Frame(root,width=460,height=600,bd=20,relief=GROOVE)
        self.gundetail_frame.place(x=920,y=200)
        top_head=Label(self.gundetail_frame,text=model,font=("Impact",25,"normal","italic"),width=20,relief=SOLID)
        top_head.place(x=70,y=10)
        try:
            self.dict={}
            i=0
            for inc in cursor:
                self.dict[inc[0]]=myres[i]
                i+=1
            attributes_y=60
            for key,value in self.dict.items():
                keys=Label(self.gundetail_frame,text=key + "-->",font=("calibri",12,"bold"),relief=FLAT)
                keys.place(x=40,y=attributes_y)
                values=Label(self.gundetail_frame,text=value,font=("georgia",12,"bold"),relief=FLAT)
                values.place(x=170,y=attributes_y)
                attributes_y+=35
            cancel_button=Button(self.gundetail_frame,text="CANCEL",cursor="hand2",\
                                 command=lambda: self.gundetail_frame.destroy(),relief=RAISED,bd=5,width=7)
            cancel_button.place(x=250,y=530)
            if login_boolean == False:
                self.clt.buy_button(self.gundetail_frame,category,self.dict['ModelName'],self.dict['ProductCode'],self.dict['Stock'],self.dict['Price'])
            elif login_boolean == True:
                update_button=Button(self.gundetail_frame,text="UPDATE",cursor="hand2",\
                                     command=lambda: self.modify_gun(category,model,productcode),relief=RAISED,bd=5,width=7)
                update_button.place(x=30,y=530)
                delete_button=Button(self.gundetail_frame,text="DELETE",cursor="hand2",\
                                     command=lambda: self.delete_gun(category,model,productcode),relief=RAISED,bd=5,width=7)
                delete_button.place(x=130,y=530)
        except:
            True
    def delete_gun(self,category,model,productcode):
        ask=ms.askyesno("DELETE","Are You Sure You Want To Delete It?")
        if ask == YES:
            self.gundetail_frame.destroy()
            self.gundisplay_frame.destroy()
            sql="DELETE  FROM "+ category +" WHERE ModelName = %s AND ProductCode = %s"
            val=val=(model,productcode)
            cursor.execute(sql,val)
            mydbase.commit()
            self.display_guns(category,self.col_list,self.clt)
            ms.showinfo("DELETED",model +" Deleted Successfully")
    def goto_display(self):
        self.guninput_frame.destroy()
        self.gunmodify_frame.destroy()
        self.go_back_b.destroy()
        self.display_guns(self.category,self.col_list,self.clt)
    def modify_gun(self,category,model_name,productcode):
        self.gundetail_frame.destroy()
        self.gundisplay_frame.destroy()
        self.gunmodify_frame=Frame(root,width=1050,height=720,bd=7,relief=SOLID)
        self.gunmodify_frame.place(x=150,y=60)
        try:
            imge=PhotoImage(file="modify firearms.gif")
            img=Label(self.gunmodify_frame,image=imge)
            self.gunmodify_frame.image=imge
            img.place(x=0,y=0)
        except:
            True
        cancel_mod=Button(self.gunmodify_frame,text="Cancel And Go Back",command=self.goto_display,relief=RAISED,bd=8,cursor="hand2")
        cancel_mod.place(x=500,y=650)
        update_R1=Radiobutton(self.gunmodify_frame)
        update_R2=Radiobutton(self.gunmodify_frame)
        update_R3=Radiobutton(self.gunmodify_frame)
        update_R4=Radiobutton(self.gunmodify_frame)
        update_R5=Radiobutton(self.gunmodify_frame)
        update_R6=Radiobutton(self.gunmodify_frame)
        update_R7=Radiobutton(self.gunmodify_frame)
        update_R8=Radiobutton(self.gunmodify_frame)
        update_R9=Radiobutton(self.gunmodify_frame)
        update_R10=Radiobutton(self.gunmodify_frame)
        update_R11=Radiobutton(self.gunmodify_frame)
        update_R12=Radiobutton(self.gunmodify_frame)
        update_R13=Radiobutton(self.gunmodify_frame)
        update_R14=Radiobutton(self.gunmodify_frame)
        update_R15=Radiobutton(self.gunmodify_frame)
        update_R16=Radiobutton(self.gunmodify_frame)
        update_R17=Radiobutton(self.gunmodify_frame)
        update_R18=Radiobutton(self.gunmodify_frame)
        update_R19=Radiobutton(self.gunmodify_frame)
        update_R20=Radiobutton(self.gunmodify_frame)
        update_Rlist=[update_R1,update_R2,update_R3,update_R4,update_R5,update_R6,update_R7,update_R8,update_R9,update_R10,\
                      update_R11,update_R12,update_R13,update_R14,update_R15,update_R16,update_R17,update_R18,update_R19,update_R20]
        
        sql="SELECT * FROM "+ category + " WHERE ModelName = %s AND ProductCode = %s"
        val=(model_name,productcode)
        cursor.execute(sql,val)
        myres=cursor.fetchone()
        sql="SHOW COLUMNS FROM "+category
        cursor.execute(sql)
        self.dict={}
        i=0
        for inc in cursor:
            self.dict[inc[0]]=myres[i]
            i+=1
        header=Label(self.gunmodify_frame,text="Choose The Attribute To Modify: ",font=("britannic bold",15,"bold","italic"),fg="red")
        header.place(x=5,y=10)
        update_count=0
        mod_element=StringVar()
        attributes_y=40
        for key,value in self.dict.items():
                keys=Label(self.gunmodify_frame,text=key + ":-",font=("calibri",12,"bold"),relief=FLAT)
                keys.place(x=20,y=attributes_y)
                values=Label(self.gunmodify_frame,text=value,font=("Times",12,"bold"),relief=FLAT)
                values.place(x=150,y=attributes_y)
                update_Rlist[update_count].config(variable=mod_element,value=key,\
                                                  command=lambda:self.mod_enter(category,model_name,productcode,mod_element.get()))
                update_Rlist[update_count].place(x=5,y=attributes_y)
                attributes_y+=35
                update_count+=1
        self.enter_new_label=Label(self.gunmodify_frame)
        self.enter_new=Entry(self.gunmodify_frame)
        self.mod_button=Button(self.gunmodify_frame)
    def mod_enter(self,category,model_name,productcode,mod_element):
        self.enter_new_label.destroy()
        self.enter_new.destroy()
        self.mod_button.destroy()
        list_tempup=[]
        list_tempup.extend(self.dict.keys())
        index_y=list_tempup.index(mod_element)
        self.enter_new_label=Label(self.gunmodify_frame,text="Enter Modified Value of "+ mod_element,relief=RIDGE,bd=10)
        self.enter_new_label.place(x=340,y=40+(index_y*35))
        self.enter_new=Entry(self.gunmodify_frame,relief=GROOVE,bd=5,width=30)
        self.enter_new.place(x=580,y=42+(index_y*35))
        self.mod_button=Button(self.gunmodify_frame,text="Modify "+ mod_element,relief=RAISED,bd=8,cursor="hand2",\
                           command=lambda:self.mod_entrycheck(category,model_name,productcode,mod_element,self.enter_new.get()))
        self.mod_button.place(x=780,y=40+(index_y*35))
    def mod_entrycheck(self,category,model_name,productcode,mod_element,mod_value):
        ql="SELECT ProductCode From "+ category
        cursor.execute(ql)
        productcodeslist=[]
        for pros in cursor:
            productcodeslist.append(pros[0])

        if mod_value in productcodeslist:
            ms.showerror("Can't Assign","ProductCode Already Available,Please Try Another")
            
        elif mod_value == "":
            ms.showwarning("Error","Entry Not Filled")
        else:
            self.modify_done(category,model_name,productcode,mod_element,mod_value)
    def modify_done(self,category,model_name,productcode,mod_element,mod_value):
        sql="UPDATE " + category + " SET " + mod_element + " = %s WHERE ModelName = %s AND ProductCode = %s"  
        val=(mod_value.upper(),model_name,productcode)
        cursor.execute(sql,val)
        mydbase.commit()
        self.gunmodify_frame.destroy()
        if mod_element == "ModelName" or mod_element == "ProductCode":
            if mod_element == "ModelName":
                model_name=mod_value
            elif mod_element == "ProductCode":
                productcode=mod_value
        self.modify_gun(category,model_name,productcode)
        ms.showinfo("Task Done",mod_element +" Updated Successfully")
class HandGuns(FireArms):
    def display_handguns(self,clt,main_display):
        self.return_main_display=main_display
        FireArms.display_guns(self,'handguns',['ModelName','ProductCode','Type','Stock','Price'],clt)
class AirGuns(FireArms):
    def display_airguns(self,clt,main_display):
        self.return_main_display=main_display
        FireArms.display_guns(self,'airguns',['ModelName','ProductCode','Action','Stock','Price'],clt)
    
class ShotGuns(FireArms):
    def display_shotguns(self,clt,main_display):
        self.return_main_display=main_display
        FireArms.display_guns(self,'shotguns',['ModelName','ProductCode','Action','Stock','Price'],clt)
    
class Rifles(FireArms):
    def display_rifles(self,clt,main_display):
        self.return_main_display=main_display
        FireArms.display_guns(self,'rifles',['ModelName','ProductCode','Action','Stock','Price'],clt)
    
'''-----------------------------------------------END OF FIREARM CLASS AND IT's CHILD CLASSES---------------------------------------------'''
'''------------------------------------------------START OF AMMUNITION CLASS--------------------------------------------------------------'''
class Ammunition:
    no_of_ammunition=0
    def __init__(self):
        self.ammodisplay_frame=Frame(root)
        self.ammodetail_frame=Frame(root)
        self.ammomodify_frame=Frame(root)
        self.ammoinput_frame=Frame(root)
        self.go_back_b=Button(root)

    def input_ammo(self,category):
        ammo_cat_dict={"HANDGUN":"(Pistol/Revolver)","SHOTGUN":"(Pump-Action/Semi-Auto/Over-Under)",\
                       "RIFLE":"(Bolt-Action/Semi-Auto/Lever-Action)"}
        
        self.ammodisplay_frame.destroy()
        self.ammodetail_frame.destroy()
        self.ammoinput_frame=Frame(root,width=1000,height=720,bd=10,relief=SOLID,bg='light blue')
        self.ammoinput_frame.place(x=200,y=70)
        try:
            imge=PhotoImage(file="input ammo.gif")
            img=Label(self.ammoinput_frame,image=imge)
            self.ammoinput_frame.image=imge
            img.place(x=0,y=0)
        except:
            True
        self.g1=StringVar()
        self.g2=StringVar()
        self.g3=StringVar()
        self.g4=StringVar()
        self.g5=StringVar()
        self.g6=StringVar()
        self.g7=StringVar()
        self.g8=StringVar()
        self.g9=StringVar()
        self.g10=StringVar()
        self.g11=StringVar()
        self.g12=StringVar()
        self.g13=StringVar()
        self.g14=StringVar()
        self.g15=StringVar()
        list_stringvars=[self.g1,self.g2,self.g3,self.g4,self.g5,self.g6,self.g7,self.g8,self.g9,self.g10,self.g11,self.g12,self.g13,self.g14,self.g15]
        sql="SHOW COLUMNS FROM ammunition"
        no_of_col=cursor.execute(sql)
        list_stringvars=list_stringvars[:no_of_col]
        string="("
        string1=""
        input_coy=40
        strs_count=0
        if category == "AIRGUN":
            for cols in cursor:
                if cols[0] == "Category":
                    list_stringvars[strs_count].set(category)
                elif cols[0] == "GunType":
                    list_stringvars[strs_count].set("NONE")
                elif cols[0] != "Category" and cols != "GunType":
                    input_label=Label(self.ammoinput_frame,text=cols[0] +"::",font=("Georgia",12),bd=10,relief=FLAT)
                    input_label.place(x=60,y=input_coy)
                    input_entry=Entry(self.ammoinput_frame,textvariable=list_stringvars[strs_count],bd=8,relief=SUNKEN,width=50,justify="center")
                    input_entry.place(x=450,y=input_coy)
                    input_coy+=50
                strs_count+=1    
                string+=cols[0] + ","
                string1+="%s" + ","
        elif category != "AIRGUN":
            for cols in cursor:
                if cols[0] == "Category":
                    list_stringvars[strs_count].set(category)
                elif cols[0] != "Category":
                    if cols[0] == "GunType":
                        input_label=Label(self.ammoinput_frame,text=cols[0]+ ammo_cat_dict[category] +"::",font=("Georgia",12),bd=10,relief=FLAT)
                        input_label.place(x=60,y=input_coy)
                    else:
                        input_label=Label(self.ammoinput_frame,text=cols[0] +"::",font=("Georgia",12),bd=10,relief=FLAT)
                        input_label.place(x=60,y=input_coy)
                    input_entry=Entry(self.ammoinput_frame,textvariable=list_stringvars[strs_count],bd=8,relief=SUNKEN,width=50,justify="center")
                    input_entry.place(x=450,y=input_coy)
                    input_coy+=50
                strs_count+=1    
                string+=cols[0] + ","
                string1+="%s" + ","
        string=string[:len(string)-1]
        string+=")"
        string1=string1[:len(string1)-1]
        entry_button=Button(self.ammoinput_frame,text="ADD To Record",bd=9,relief=RAISED,bg='brown',fg='white',font='Impact',\
                            command=lambda:self.entry_check(category,list_stringvars,string,string1),cursor="hand2")
        entry_button.place(x=400,y=620)
        entry_button=Button(self.ammoinput_frame,text="Cancel And Go Back",bd=9,relief=RAISED,bg='brown',fg='white',font='Impact',\
                            command=lambda:self.display_ammo(category,self.col_list,self.clt),cursor="hand2")
        entry_button.place(x=700,y=620)

    def entry_check(self,category,list_stringvars,string,string1):
        
        check=list(map(lambda x: True if x.get() != '' else False,list_stringvars))

        ql="SELECT ProductCode From ammunition"
        cursor.execute(ql)
        productcodeslist=[]
        for pros in cursor:
            productcodeslist.append(pros[0])

        if list_stringvars[1].get() in productcodeslist:
            ms.showerror("Can't Assign","ProductCode Already Available,Please Try Another")
            
        elif False in check:
            ms.showwarning("Data input Error","Entries Not Filled")
        else:
            self.input(category,list_stringvars,string,string1)
    def input(self,category,list_stringvars,string,string1):
        sql="INSERT INTO ammunition" + string + " VALUES (" + string1 + ")"
        val=tuple(map(lambda x:x.get().upper(),list_stringvars))
        
        cursor.execute(sql,val)
        mydbase.commit()

        self.ammoinput_frame.destroy()
        self.go_back_b.destroy()
        self.display_ammo(category,self.col_list,self.clt)
    
    def display_ammo(self,category,col_list,clt):
        self.clt=clt
        self.category=category
        self.col_list=col_list
        self.go_back_b.destroy()
        self.ammoinput_frame.destroy()
        string=""
        for col in col_list:
            string+=col + ","
        string=string[:len(string)-1]
        sql="SELECT " + string + " FROM ammunition WHERE Category = %s"
        no_of_el=cursor.execute(sql,category)
        self.mylist=cursor.fetchall()
        
        self.ammodisplay_frame=Frame(root,width=800,height=760,bd=12,relief=SUNKEN)
        self.ammodisplay_frame.place(x=40,y=40)
        try:
            imge=PhotoImage(file="display ammo.gif")
            img=Label(self.ammodisplay_frame,image=imge)
            self.ammodisplay_frame.image=imge
            img.place(x=0,y=0)
        except:
            True
        category_heading=Label(self.ammodisplay_frame,text=category.upper() + " DISPLAY LIST",font=("stencil",25,"bold","italic"),fg="red")
        category_heading.place(x=220,y=10)
        serial_heading=Label(self.ammodisplay_frame,text="S.NO",font=("Times",8),relief=RIDGE,bd=8,width=6)
        serial_heading.place(x=20,y=50)
        model_heading=Label(self.ammodisplay_frame,text="ModelName",font=("Impact",11),relief=RIDGE,bd=8,width=18)
        model_heading.place(x=120,y=50)
        code_heading=Label(self.ammodisplay_frame,text="ProductCode",font=("Impact",11),relief=RIDGE,bd=8,width=13)
        code_heading.place(x=280,y=50)
        stock_heading=Label(self.ammodisplay_frame,text="Stock",font=("Impact",11),relief=RIDGE,bd=8,width=10)
        stock_heading.place(x=410,y=50)
        price_heading=Label(self.ammodisplay_frame,text="Price RS",font=("Impact",11),relief=RIDGE,bd=8,width=13)
        price_heading.place(x=530,y=50)
        self.ammodisplay_list=Frame(self.ammodisplay_frame,bd=6,relief=SOLID,bg='brown')
        self.ammodisplay_list.place(x=10,y=90)
        scroll_display=Scrollbar(self.ammodisplay_list,orient="vertical")
        scroll_display.pack(side=RIGHT,fill=Y)
        self.Lb_sno=Listbox(self.ammodisplay_list)
        self.Lb_model=Listbox(self.ammodisplay_list)
        self.Lb_productcode=Listbox(self.ammodisplay_list)
        self.Lb_stock=Listbox(self.ammodisplay_list)
        self.Lb_price=Listbox(self.ammodisplay_list)
        self.ammo_list=[self.Lb_sno,self.Lb_model,self.Lb_productcode,self.Lb_stock,self.Lb_price]
        for elem_list in self.ammo_list:
            elem_list.config(width=12,bd=5,font=("Franklin Gothic Demi",10),bg="grey",\
                  fg='white',highlightthickness=7,\
                  highlightcolor='midnight blue',\
                  relief=SOLID,height=18,yscrollcommand=scroll_display.set)
            elem_list.pack(side=LEFT,fill=Y)
        self.Lb_sno.config(width=5,highlightcolor='red',highlightthickness=12,selectbackground='brown',cursor="hand2")
        self.Lb_stock.config(width=5)
        self.Lb_model.config(width=23)
        self.Lb_productcode.config(width=10)
        self.Lb_sno.bind('<<ListboxSelect>>',self.get_listelement)
        count_serials=1
        for row in self.mylist:
            self.Lb_sno.insert(END,count_serials)
            self.Lb_model.insert(END,row[0])
            self.Lb_productcode.insert(END,row[1])
            self.Lb_stock.insert(END,row[2])
            self.Lb_price.insert(END,row[3])
            count_serials+=1
        
        scroll_display.config(command=self.scroll_view)
        if login_boolean == True:
            self.add_button=Button(self.ammodisplay_frame,text="ADD A RECORD",bg="green",fg="black",relief=SOLID,bd=12,\
                                   command=lambda:self.input_ammo(category),cursor="hand2")
            self.add_button.place(x=370,y=680)
        self.go_back_b=Button(root,text="RETURN TO MAIN DISPLAY",cursor="hand2",\
                              command=self.go_back,relief=RAISED,bd=15,bg='light blue',fg='black')
        self.go_back_b.place(x=1200,y=7)

    def scroll_view(self,*args):
        for elem in self.ammo_list:
            elem.yview(*args)
    def go_back(self):
        self.ammodetail_frame.destroy()
        self.ammodisplay_frame.destroy()
        self.go_back_b.destroy()
        self.ammomodify_frame.destroy()
        self.ammoinput_frame.destroy()
        self.return_main_display()
    def get_listelement(self,Lb_sno):
        try:
            index=self.Lb_sno.curselection()[0]
            self.detail_ammo(self.category,self.mylist[index][0],self.mylist[index][1])
        except:
            True
    
    def detail_ammo(self,category,model,productcode):
        sql="SELECT * FROM ammunition WHERE ModelName = %s AND ProductCode = %s AND Category = %s"
        val=(model,productcode,category)
        cursor.execute(sql,val)
        myres=cursor.fetchone()
        sql="SHOW COLUMNS FROM ammunition"
        cursor.execute(sql)
        self.ammodetail_frame.destroy()
        self.ammodetail_frame=Frame(root,width=460,height=600,bd=20,relief=GROOVE)
        self.ammodetail_frame.place(x=920,y=200)
        top_head=Label(self.ammodetail_frame,text=model,font=("Impact",25,"normal","italic"),width=20,relief=SOLID)
        top_head.place(x=70,y=10)
        try:
            self.dict={}
            i=0
            for inc in cursor:
                self.dict[inc[0]]=myres[i]
                i+=1
            attributes_y=60
            for key,value in self.dict.items():
                keys=Label(self.ammodetail_frame,text=key + "-->",font=("calibri",12,"bold"),relief=FLAT)
                keys.place(x=20,y=attributes_y)
                values=Label(self.ammodetail_frame,text=value,font=("georgia",12,"bold"),relief=FLAT)
                values.place(x=150,y=attributes_y)
                attributes_y+=35
            cancel_button=Button(self.ammodetail_frame,text="CANCEL",cursor="hand2",\
                                 command=lambda: self.ammodetail_frame.destroy(),relief=RAISED,bd=5,width=7)
            cancel_button.place(x=250,y=530)
            if login_boolean == False:
                self.clt.buy_button(self.ammodetail_frame,"ammunition",self.dict['ModelName'],self.dict['ProductCode'],self.dict['Stock'],self.dict['Price'])
            elif login_boolean == True:
                update_button=Button(self.ammodetail_frame,text="UPDATE",cursor="hand2",\
                                     command=lambda: self.modify_ammo(category,model,productcode),relief=RAISED,bd=5,width=7)
                update_button.place(x=30,y=530)
                delete_button=Button(self.ammodetail_frame,text="DELETE",cursor="hand2",\
                                     command=lambda: self.delete_ammo(category,model,productcode),relief=RAISED,bd=5,width=7)
                delete_button.place(x=130,y=530)
        except:
            True
            
    def delete_ammo(self,category,model,productcode):
        ask=ms.askyesno("DELETE","Are You Sure You Want To Delete It?")
        if ask == YES:
            self.ammodetail_frame.destroy()
            self.ammodisplay_frame.destroy()
            sql="DELETE  FROM ammunition WHERE ModelName = %s AND ProductCode = %s AND Category = %s"
            val=val=(model,productcode,category)
            cursor.execute(sql,val)
            mydbase.commit()
            self.display_ammo(category,self.col_list,self.clt)
            ms.showinfo("DELETED",model +" Deleted Successfully")
        
    def goto_display(self):
        self.ammoinput_frame.destroy()
        self.ammomodify_frame.destroy()
        self.go_back_b.destroy()
        self.display_ammo(self.category,self.col_list,self.clt)

    def modify_ammo(self,category,model_name,productcode):
        self.ammodetail_frame.destroy()
        self.ammodisplay_frame.destroy()
        self.ammomodify_frame=Frame(root,width=1050,height=720,bd=7,relief=SOLID)
        self.ammomodify_frame.place(x=150,y=60)
        try:
            imge=PhotoImage(file="modify ammo.gif")
            img=Label(self.ammomodify_frame,image=imge)
            self.ammomodify_frame.image=imge
            img.place(x=0,y=0)
        except:
            True
        cancel_mod=Button(self.ammomodify_frame,text="Cancel And Go Back",command=self.goto_display,relief=RAISED,bd=8,cursor="hand2")
        cancel_mod.place(x=500,y=650)
        update_R1=Radiobutton(self.ammomodify_frame)
        update_R2=Radiobutton(self.ammomodify_frame)
        update_R3=Radiobutton(self.ammomodify_frame)
        update_R4=Radiobutton(self.ammomodify_frame)
        update_R5=Radiobutton(self.ammomodify_frame)
        update_R6=Radiobutton(self.ammomodify_frame)
        update_R7=Radiobutton(self.ammomodify_frame)
        update_R8=Radiobutton(self.ammomodify_frame)
        update_R9=Radiobutton(self.ammomodify_frame)
        update_R10=Radiobutton(self.ammomodify_frame)
        update_R11=Radiobutton(self.ammomodify_frame)
        update_R12=Radiobutton(self.ammomodify_frame)
        update_R13=Radiobutton(self.ammomodify_frame)
        update_R14=Radiobutton(self.ammomodify_frame)
        update_R15=Radiobutton(self.ammomodify_frame)
        update_R16=Radiobutton(self.ammomodify_frame)
        update_R17=Radiobutton(self.ammomodify_frame)
        update_R18=Radiobutton(self.ammomodify_frame)
        update_R19=Radiobutton(self.ammomodify_frame)
        update_R20=Radiobutton(self.ammomodify_frame)
        update_Rlist=[update_R1,update_R2,update_R3,update_R4,update_R5,update_R6,update_R7,update_R8,update_R9,update_R10,\
                      update_R11,update_R12,update_R13,update_R14,update_R15,update_R16,update_R17,update_R18,update_R19,update_R20]
        
        sql="SELECT * FROM ammunition WHERE ModelName = %s AND ProductCode = %s AND Category = %s"
        val=(model_name,productcode,category)
        cursor.execute(sql,val)
        myres=cursor.fetchone()
        sql="SHOW COLUMNS FROM ammunition"
        cursor.execute(sql)
        self.dict={}
        i=0
        if category == "AIRGUN":
            for inc in cursor:
                if inc[0] != "Category" and inc[0] != "GunType":
                    self.dict[inc[0]]=myres[i]
                i+=1
        else:
            for inc in cursor:
                if inc[0] != "Category":
                    self.dict[inc[0]]=myres[i]
                i+=1
        header=Label(self.ammomodify_frame,text="Choose The Attribute To Modify: ",font=("britannic bold",15,"bold","italic"),fg="red")
        header.place(x=5,y=10)
        update_count=0
        mod_element=StringVar()
        attributes_y=40
        for key,value in self.dict.items():
                keys=Label(self.ammomodify_frame,text=key + ":-",font=("calibri",12,"bold"),relief=FLAT)
                keys.place(x=20,y=attributes_y)
                values=Label(self.ammomodify_frame,text=value,font=("Times",12,"bold"),relief=FLAT)
                values.place(x=150,y=attributes_y)
                update_Rlist[update_count].config(variable=mod_element,value=key,cursor="hand2",\
                                                  command=lambda:self.mod_enter(category,model_name,productcode,mod_element.get()))
                update_Rlist[update_count].place(x=5,y=attributes_y)
                attributes_y+=35
                update_count+=1
        self.enter_new_label=Label(self.ammomodify_frame)
        self.enter_new=Entry(self.ammomodify_frame)
        self.mod_button=Button(self.ammomodify_frame,cursor="hand2")
    def mod_enter(self,category,model_name,productcode,mod_element):
        self.enter_new_label.destroy()
        self.enter_new.destroy()
        self.mod_button.destroy()
        list_tempup=[]
        list_tempup.extend(self.dict.keys())
        index_y=list_tempup.index(mod_element)
        self.enter_new_label=Label(self.ammomodify_frame,text="Enter Modified Value of "+ mod_element,relief=RIDGE,bd=10)
        self.enter_new_label.place(x=340,y=40+(index_y*35))
        self.enter_new=Entry(self.ammomodify_frame,relief=GROOVE,bd=5,width=30)
        self.enter_new.place(x=580,y=42+(index_y*35))
        self.mod_button=Button(self.ammomodify_frame,text="Modify "+ mod_element,relief=RAISED,bd=8,cursor="hand2",\
                           command=lambda:self.mod_entrycheck(category,model_name,productcode,mod_element,self.enter_new.get()))
        self.mod_button.place(x=780,y=40+(index_y*35))
    def mod_entrycheck(self,category,model_name,productcode,mod_element,mod_value):
        ql="SELECT ProductCode From ammunition"
        cursor.execute(ql)
        productcodeslist=[]
        for pros in cursor:
            productcodeslist.append(pros[0])

        if mod_value in productcodeslist:
            ms.showerror("Can't Assign","ProductCode Already Available,Please Try Another")
            
        elif mod_value == "":
            ms.showwarning("Error","Entry Not Filled")
        else:
            self.modify_done(category,model_name,productcode,mod_element,mod_value)
    def modify_done(self,category,model_name,productcode,mod_element,mod_value):
        sql="UPDATE ammunition  SET " + mod_element + " = %s WHERE ModelName = %s AND ProductCode = %s AND Category = %s"  
        val=(mod_value.upper(),model_name,productcode,category)
        cursor.execute(sql,val)
        mydbase.commit()
        self.ammomodify_frame.destroy()
        if mod_element == "ModelName" or mod_element == "ProductCode":
            if mod_element == "ModelName":
                model_name=mod_value
            elif mod_element == "ProductCode":
                productcode=mod_value
        self.modify_ammo(category,model_name,productcode)
        ms.showinfo("Task Done",mod_element +" Updated Successfully")
    

class Handguns_ammo(Ammunition):
    def display_handguns_ammo(self,clt,main_display):
        self.return_main_display=main_display
        Ammunition.display_ammo(self,'HANDGUN',['ModelName','ProductCode','Stock','Price'],clt)
    
class Shotguns_ammo(Ammunition):
    def display_shotguns_ammo(self,clt,main_display):
        self.return_main_display=main_display
        Ammunition.display_ammo(self,'SHOTGUN',['ModelName','ProductCode','Stock','Price'],clt)
    
class Airguns_ammo(Ammunition):
    def display_airguns_ammo(self,clt,main_display):
        self.return_main_display=main_display
        Ammunition.display_ammo(self,'AIRGUN',['ModelName','ProductCode','Stock','Price'],clt)
    
class Rifles_ammo(Ammunition):
    def display_rifles_ammo(self,clt,main_display):
        self.return_main_display=main_display
        Ammunition.display_ammo(self,'RIFLE',['ModelName','ProductCode','Stock','Price'],clt)
    
'''------------------------------------------------END OF AMMUNITION CLASS----------------------------------------------------------------'''
'''------------------------------------------------START OF PARTS CLASS--------------------------------------------------------------'''
class Parts:
    no_of_parts=0
    def __init__(self):
        self.partsdisplay_frame=Frame(root)
        self.partsdetail_frame=Frame(root)
        self.partsmodify_frame=Frame(root)
        self.partsinput_frame=Frame(root)
        self.go_back_b=Button(root)

    def input_parts(self,category):
        parts_cat_dict={"HANDGUN":"(Pistol/Revolver)","SHOTGUN":"(Pump-Action/Semi-Auto/Over-Under)",\
                       "RIFLE":"(Bolt-Action/Semi-Auto/Lever-Action)"}
        self.partsdisplay_frame.destroy()
        self.partsdetail_frame.destroy()
        self.partsinput_frame=Frame(root,width=1000,height=720,bd=10,relief=SOLID,bg='light blue')
        self.partsinput_frame.place(x=200,y=70)
        try:
            imge=PhotoImage(file="input parts.gif")
            img=Label(self.partsinput_frame,image=imge)
            self.partsinput_frame.image=imge
            img.place(x=0,y=0)
        except:
            True
        self.g1=StringVar()
        self.g2=StringVar()
        self.g3=StringVar()
        self.g4=StringVar()
        self.g5=StringVar()
        self.g6=StringVar()
        self.g7=StringVar()
        self.g8=StringVar()
        self.g9=StringVar()
        self.g10=StringVar()
        self.g11=StringVar()
        self.g12=StringVar()
        self.g13=StringVar()
        self.g14=StringVar()
        self.g15=StringVar()
        list_stringvars=[self.g1,self.g2,self.g3,self.g4,self.g5,self.g6,self.g7,self.g8,self.g9,self.g10,self.g11,self.g12,self.g13,self.g14,self.g15]
        sql="SHOW COLUMNS FROM parts"
        no_of_col=cursor.execute(sql)
        list_stringvars=list_stringvars[:no_of_col]
        string="("
        string1=""
        input_coy=40
        strs_count=0
        for cols in cursor:
            if cols[0] == "Category":
                list_stringvars[strs_count].set(category)
            elif cols[0] != "Category":
                if cols[0] == "GunType":
                    input_label=Label(self.partsinput_frame,text=cols[0]+ parts_cat_dict[category] +"::",font=("Georgia",12),bd=10,relief=FLAT)
                    input_label.place(x=60,y=input_coy)
                else:
                    input_label=Label(self.partsinput_frame,text=cols[0] +"::",font=("Georgia",12),bd=10,relief=FLAT)
                    input_label.place(x=60,y=input_coy)
                input_entry=Entry(self.partsinput_frame,textvariable=list_stringvars[strs_count],bd=8,relief=SUNKEN,width=50,justify="center")
                input_entry.place(x=450,y=input_coy)
                input_coy+=50
            strs_count+=1    
            string+=cols[0] + ","
            string1+="%s" + ","
        string=string[:len(string)-1]
        string+=")"
        string1=string1[:len(string1)-1]
        entry_button=Button(self.partsinput_frame,text="ADD To Record",bd=9,relief=RAISED,bg='brown',fg='white',font='Impact',\
                            command=lambda:self.entry_check(category,list_stringvars,string,string1),cursor="hand2")
        entry_button.place(x=400,y=620)
        entry_button=Button(self.partsinput_frame,text="Cancel And Go Back",bd=9,relief=RAISED,bg='brown',fg='white',font='Impact',\
                            command=lambda:self.display_parts(category,self.col_list,self.clt),cursor="hand2")
        entry_button.place(x=700,y=620)

    def entry_check(self,category,list_stringvars,string,string1):
        
        check=list(map(lambda x: True if x.get() != '' else False,list_stringvars))
        ql="SELECT ProductCode From parts"
        cursor.execute(ql)
        productcodeslist=[]
        for pros in cursor:
            productcodeslist.append(pros[0])

        if list_stringvars[1].get() in productcodeslist:
            ms.showerror("Can't Assign","ProductCode Already Available,Please Try Another")
            
        elif False in check:
            ms.showwarning("Data input Error","Entries Not Filled")
        else:
            self.input(category,list_stringvars,string,string1)
    def input(self,category,list_stringvars,string,string1):
        sql="INSERT INTO parts" + string + " VALUES (" + string1 + ")"
        val=tuple(map(lambda x:x.get().upper(),list_stringvars))
        
        cursor.execute(sql,val)
        mydbase.commit()

        self.partsinput_frame.destroy()
        self.go_back_b.destroy()
        self.display_parts(category,self.col_list,self.clt)

    def display_parts(self,category,col_list,clt):
        self.clt=clt
        self.category=category
        self.col_list=col_list
        self.go_back_b.destroy()
        self.partsinput_frame.destroy()
        string=""
        for col in col_list:
            string+=col + ","
        string=string[:len(string)-1]
        sql="SELECT " + string + " FROM parts WHERE Category = %s"
        no_of_el=cursor.execute(sql,category)
        self.mylist=cursor.fetchall()

        self.partsdisplay_frame=Frame(root,width=800,height=760,bd=12,relief=SUNKEN)
        self.partsdisplay_frame.place(x=40,y=40)
        try:
            imge=PhotoImage(file="display parts.gif")
            img=Label(self.partsdisplay_frame,image=imge)
            self.partsdisplay_frame.image=imge
            img.place(x=0,y=0)
        except:
            True
        category_heading=Label(self.partsdisplay_frame,text=category.upper() + " DISPLAY LIST",font=("stencil",25,"bold","italic"),fg="red")
        category_heading.place(x=220,y=10)
        serial_heading=Label(self.partsdisplay_frame,text="S.NO",font=("Times",8),relief=RIDGE,bd=8,width=6)
        serial_heading.place(x=20,y=50)
        model_heading=Label(self.partsdisplay_frame,text="ModelName",font=("Impact",11),relief=RIDGE,bd=8,width=18)
        model_heading.place(x=120,y=50)
        code_heading=Label(self.partsdisplay_frame,text="ProductCode",font=("Impact",11),relief=RIDGE,bd=8,width=13)
        code_heading.place(x=280,y=50)
        stock_heading=Label(self.partsdisplay_frame,text="Stock",font=("Impact",11),relief=RIDGE,bd=8,width=10)
        stock_heading.place(x=410,y=50)
        price_heading=Label(self.partsdisplay_frame,text="Price RS",font=("Impact",11),relief=RIDGE,bd=8,width=13)
        price_heading.place(x=530,y=50)
        self.partsdisplay_list=Frame(self.partsdisplay_frame,bd=6,relief=SOLID,bg='brown')
        self.partsdisplay_list.place(x=10,y=90)
        scroll_display=Scrollbar(self.partsdisplay_list,orient="vertical")
        scroll_display.pack(side=RIGHT,fill=Y)
        self.Lb_sno=Listbox(self.partsdisplay_list)
        self.Lb_model=Listbox(self.partsdisplay_list)
        self.Lb_productcode=Listbox(self.partsdisplay_list)
        self.Lb_stock=Listbox(self.partsdisplay_list)
        self.Lb_price=Listbox(self.partsdisplay_list)
        self.parts_list=[self.Lb_sno,self.Lb_model,self.Lb_productcode,self.Lb_stock,self.Lb_price]
        for elem_list in self.parts_list:
            elem_list.config(width=12,bd=5,font=("Franklin Gothic Demi",10),bg="grey",\
                  fg='white',highlightthickness=7,\
                  highlightcolor='midnight blue',\
                  relief=SOLID,height=18,yscrollcommand=scroll_display.set)
            elem_list.pack(side=LEFT,fill=Y)
        self.Lb_sno.config(width=5,highlightcolor='red',highlightthickness=12,selectbackground='brown',cursor="hand2")
        self.Lb_stock.config(width=5)
        self.Lb_model.config(width=23)
        self.Lb_productcode.config(width=10)
        self.Lb_sno.bind('<<ListboxSelect>>',self.get_listelement)
        count_serials=1
        for row in self.mylist:
            self.Lb_sno.insert(END,count_serials)
            self.Lb_model.insert(END,row[0])
            self.Lb_productcode.insert(END,row[1])
            self.Lb_stock.insert(END,row[2])
            self.Lb_price.insert(END,row[3])
            count_serials+=1
        
        scroll_display.config(command=self.scroll_view)
        if login_boolean == True:
            self.add_button=Button(self.partsdisplay_frame,text="ADD A RECORD",bg="green",fg="black",relief=SOLID,bd=12,\
                                   command=lambda:self.input_parts(category),cursor="hand2")
            self.add_button.place(x=370,y=680)
        self.go_back_b=Button(root,text="RETURN TO MAIN DISPLAY",cursor="hand2",command=self.go_back,relief=RAISED,bd=15,bg='light blue',fg='black')
        self.go_back_b.place(x=1200,y=7)

    def scroll_view(self,*args):
        for elem in self.parts_list:
            elem.yview(*args)
    def go_back(self):
        self.partsdetail_frame.destroy()
        self.partsdisplay_frame.destroy()
        self.go_back_b.destroy()
        self.partsmodify_frame.destroy()
        self.partsinput_frame.destroy()
        self.return_main_display()
    def get_listelement(self,Lb_sno):
        try:
            index=self.Lb_sno.curselection()[0]
            self.detail_parts(self.category,self.mylist[index][0],self.mylist[index][1])
        except:
            True
    
    def detail_parts(self,category,model,productcode):
        sql="SELECT * FROM parts WHERE ModelName = %s AND ProductCode = %s AND Category = %s"
        val=(model,productcode,category)
        cursor.execute(sql,val)
        myres=cursor.fetchone()
        sql="SHOW COLUMNS FROM parts"
        cursor.execute(sql)
        self.partsdetail_frame.destroy()
        self.partsdetail_frame=Frame(root,width=460,height=600,bd=20,relief=GROOVE)
        self.partsdetail_frame.place(x=920,y=200)
        top_head=Label(self.partsdetail_frame,text=model,font=("Impact",25,"normal","italic"),width=20,relief=SOLID)
        top_head.place(x=70,y=10)
        try:
            self.dict={}
            i=0
            for inc in cursor:
                self.dict[inc[0]]=myres[i]
                i+=1
            attributes_y=60
            for key,value in self.dict.items():
                keys=Label(self.partsdetail_frame,text=key + "-->",font=("calibri",12,"bold"),relief=FLAT)
                keys.place(x=20,y=attributes_y)
                values=Label(self.partsdetail_frame,text=value,font=("georgia",12,"bold"),relief=FLAT)
                values.place(x=150,y=attributes_y)
                attributes_y+=35
            cancel_button=Button(self.partsdetail_frame,text="CANCEL",cursor="hand2",\
                                 command=lambda: self.partsdetail_frame.destroy(),relief=RAISED,bd=5,width=7)
            cancel_button.place(x=250,y=530)
            if login_boolean == False:
                self.clt.buy_button(self.partsdetail_frame,"parts",self.dict['ModelName'],self.dict['ProductCode'],self.dict['Stock'],self.dict['Price'])
            elif login_boolean == True:
                update_button=Button(self.partsdetail_frame,text="UPDATE",cursor="hand2",\
                                     command=lambda: self.modify_parts(category,model,productcode),relief=RAISED,bd=5,width=7)
                update_button.place(x=30,y=530)
                delete_button=Button(self.partsdetail_frame,text="DELETE",cursor="hand2",\
                                     command=lambda: self.delete_parts(category,model,productcode),relief=RAISED,bd=5,width=7)
                delete_button.place(x=130,y=530)
        except:
            True
            
    def delete_parts(self,category,model,productcode):
        ask=ms.askyesno("DELETE","Are You Sure You Want To Delete It?")
        if ask == YES:
            self.partsdetail_frame.destroy()
            self.partsdisplay_frame.destroy()
            sql="DELETE  FROM parts WHERE ModelName = %s AND ProductCode = %s AND Category = %s"
            val=val=(model,productcode,category)
            cursor.execute(sql,val)
            mydbase.commit()
            self.display_parts(category,self.col_list,self.clt)
            ms.showinfo("DELETED",model +" Deleted Successfully")

    def goto_display(self):
        self.partsinput_frame.destroy()
        self.partsmodify_frame.destroy()
        self.go_back_b.destroy()
        self.display_parts(self.category,self.col_list,self.clt)

    def modify_parts(self,category,model_name,productcode):
        self.partsdetail_frame.destroy()
        self.partsdisplay_frame.destroy()
        self.partsmodify_frame=Frame(root,width=1050,height=720,bd=7,relief=SOLID)
        self.partsmodify_frame.place(x=150,y=60)
        try:
            imge=PhotoImage(file="modify parts.gif")
            img=Label(self.partsmodify_frame,image=imge)
            self.partsmodify_frame.image=imge
            img.place(x=0,y=0)
        except:
            True
        cancel_mod=Button(self.partsmodify_frame,text="Cancel And Go Back",command=self.goto_display,relief=RAISED,bd=8,cursor="hand2")
        cancel_mod.place(x=500,y=650)
        update_R1=Radiobutton(self.partsmodify_frame)
        update_R2=Radiobutton(self.partsmodify_frame)
        update_R3=Radiobutton(self.partsmodify_frame)
        update_R4=Radiobutton(self.partsmodify_frame)
        update_R5=Radiobutton(self.partsmodify_frame)
        update_R6=Radiobutton(self.partsmodify_frame)
        update_R7=Radiobutton(self.partsmodify_frame)
        update_R8=Radiobutton(self.partsmodify_frame)
        update_R9=Radiobutton(self.partsmodify_frame)
        update_R10=Radiobutton(self.partsmodify_frame)
        update_R11=Radiobutton(self.partsmodify_frame)
        update_R12=Radiobutton(self.partsmodify_frame)
        update_R13=Radiobutton(self.partsmodify_frame)
        update_R14=Radiobutton(self.partsmodify_frame)
        update_R15=Radiobutton(self.partsmodify_frame)
        update_R16=Radiobutton(self.partsmodify_frame)
        update_R17=Radiobutton(self.partsmodify_frame)
        update_R18=Radiobutton(self.partsmodify_frame)
        update_R19=Radiobutton(self.partsmodify_frame)
        update_R20=Radiobutton(self.partsmodify_frame)
        update_Rlist=[update_R1,update_R2,update_R3,update_R4,update_R5,update_R6,update_R7,update_R8,update_R9,update_R10,\
                      update_R11,update_R12,update_R13,update_R14,update_R15,update_R16,update_R17,update_R18,update_R19,update_R20]
        
        sql="SELECT * FROM parts WHERE ModelName = %s AND ProductCode = %s AND Category = %s"
        val=(model_name,productcode,category)
        cursor.execute(sql,val)
        myres=cursor.fetchone()
        sql="SHOW COLUMNS FROM parts"
        cursor.execute(sql)
        self.dict={}
        i=0
        for inc in cursor:
            if inc[0] != "Category":
                self.dict[inc[0]]=myres[i]
            i+=1
        header=Label(self.partsmodify_frame,text="Choose The Attribute To Modify: ",font=("britannic bold",15,"bold","italic"),fg="red")
        header.place(x=5,y=10)
        update_count=0
        mod_element=StringVar()
        attributes_y=40
        for key,value in self.dict.items():
                keys=Label(self.partsmodify_frame,text=key + ":-",font=("calibri",12,"bold"),relief=FLAT)
                keys.place(x=20,y=attributes_y)
                values=Label(self.partsmodify_frame,text=value,font=("Times",12,"bold"),relief=FLAT)
                values.place(x=150,y=attributes_y)
                update_Rlist[update_count].config(variable=mod_element,value=key,cursor="hand2",\
                                                  command=lambda:self.mod_enter(category,model_name,productcode,mod_element.get()))
                update_Rlist[update_count].place(x=5,y=attributes_y)
                attributes_y+=35
                update_count+=1
        self.enter_new_label=Label(self.partsmodify_frame)
        self.enter_new=Entry(self.partsmodify_frame)
        self.mod_button=Button(self.partsmodify_frame)
    def mod_enter(self,category,model_name,productcode,mod_element):
        self.enter_new_label.destroy()
        self.enter_new.destroy()
        self.mod_button.destroy()
        list_tempup=[]
        list_tempup.extend(self.dict.keys())
        index_y=list_tempup.index(mod_element)
        self.enter_new_label=Label(self.partsmodify_frame,text="Enter Modified Value of "+ mod_element,relief=RIDGE,bd=10)
        self.enter_new_label.place(x=340,y=40+(index_y*35))
        self.enter_new=Entry(self.partsmodify_frame,relief=GROOVE,bd=5,width=30)
        self.enter_new.place(x=580,y=42+(index_y*35))
        self.mod_button=Button(self.partsmodify_frame,text="Modify "+ mod_element,relief=RAISED,bd=8,cursor="hand2",\
                           command=lambda:self.mod_entrycheck(category,model_name,productcode,mod_element,self.enter_new.get()))
        self.mod_button.place(x=780,y=40+(index_y*35))
    def mod_entrycheck(self,category,model_name,productcode,mod_element,mod_value):
        ql="SELECT ProductCode From parts"
        cursor.execute(ql)
        productcodeslist=[]
        for pros in cursor:
            productcodeslist.append(pros[0])

        if mod_value in productcodeslist:
            ms.showerror("Can't Assign","ProductCode Already Available,Please Try Another")
        
        elif mod_value == "":
            ms.showwarning("Error","Entry Not Filled")
        else:
            self.modify_done(category,model_name,productcode,mod_element,mod_value)
    def modify_done(self,category,model_name,productcode,mod_element,mod_value):
        sql="UPDATE parts  SET " + mod_element + " = %s WHERE ModelName = %s AND ProductCode = %s AND Category = %s"  
        val=(mod_value.upper(),model_name,productcode,category)
        cursor.execute(sql,val)
        mydbase.commit()
        self.partsmodify_frame.destroy()
        if mod_element == "ModelName" or mod_element == "ProductCode":
            if mod_element == "ModelName":
                model_name=mod_value
            elif mod_element == "ProductCode":
                productcode=mod_value
        self.modify_parts(category,model_name,productcode)
        ms.showinfo("Task Done",mod_element +" Updated Successfully")


class Handguns_parts(Parts):
    def display_handguns_parts(self,clt,main_display):
        self.return_main_display=main_display
        Parts.display_parts(self,'HANDGUN',['ModelName','ProductCode','Stock','Price'],clt)
    
class Shotguns_parts(Parts):
    def display_shotguns_parts(self,clt,main_display):
        self.return_main_display=main_display
        Parts.display_parts(self,'SHOTGUN',['ModelName','ProductCode','Stock','Price'],clt)
    
class Rifles_parts(Parts):
    def display_rifles_parts(self,clt,main_display):
        self.return_main_display=main_display
        Parts.display_parts(self,'RIFLE',['ModelName','ProductCode','Stock','Price'],clt)
    
'''------------------------------------------------END OF PARTS CLASS----------------------------------------------------------------'''
'''------------------------------------------------START OF MAGAZINES CLASS--------------------------------------------------------------'''
class Magazines:
    no_of_mag=0
    def __init__(self):
        self.magdisplay_frame=Frame(root)
        self.magdetail_frame=Frame(root)
        self.magmodify_frame=Frame(root)
        self.maginput_frame=Frame(root)
        self.go_back_b=Button(root)

    def input_mag(self,category):
        mag_cat_dict={"HANDGUN":"(Pistol/Revolver)","SHOTGUN":"(Pump-Action/Semi-Auto/Over-Under)",\
                       "RIFLE":"(Bolt-Action/Semi-Auto/Lever-Action)"}
        self.magdisplay_frame.destroy()
        self.magdetail_frame.destroy()
        self.maginput_frame=Frame(root,width=1000,height=720,bd=10,relief=SOLID,bg='light blue')
        self.maginput_frame.place(x=200,y=70)
        try:
            imge=PhotoImage(file="input mag.gif")
            img=Label(self.maginput_frame,image=imge)
            self.maginput_frame.image=imge
            img.place(x=0,y=0)
        except:
            True
        self.g1=StringVar()
        self.g2=StringVar()
        self.g3=StringVar()
        self.g4=StringVar()
        self.g5=StringVar()
        self.g6=StringVar()
        self.g7=StringVar()
        self.g8=StringVar()
        self.g9=StringVar()
        self.g10=StringVar()
        self.g11=StringVar()
        self.g12=StringVar()
        self.g13=StringVar()
        self.g14=StringVar()
        self.g15=StringVar()
        list_stringvars=[self.g1,self.g2,self.g3,self.g4,self.g5,self.g6,self.g7,self.g8,self.g9,self.g10,self.g11,self.g12,self.g13,self.g14,self.g15]
        sql="SHOW COLUMNS FROM magazines"
        no_of_col=cursor.execute(sql)
        list_stringvars=list_stringvars[:no_of_col]
        string="("
        string1=""
        input_coy=40
        strs_count=0
        for cols in cursor:
            if cols[0] == "Category":
                list_stringvars[strs_count].set(category)
            elif cols[0] != "Category":
                if cols[0] == "GunType":
                    input_label=Label(self.maginput_frame,text=cols[0]+mag_cat_dict[category] +"::",font=("Georgia",12),bd=10,relief=FLAT)
                    input_label.place(x=60,y=input_coy)
                else:
                    input_label=Label(self.maginput_frame,text=cols[0] +"::",font=("Georgia",12),bd=10,relief=FLAT)
                    input_label.place(x=60,y=input_coy)
                input_entry=Entry(self.maginput_frame,textvariable=list_stringvars[strs_count],bd=8,relief=SUNKEN,width=50,justify="center")
                input_entry.place(x=450,y=input_coy)
                input_coy+=50
            strs_count+=1    
            string+=cols[0] + ","
            string1+="%s" + ","
        string=string[:len(string)-1]
        string+=")"
        string1=string1[:len(string1)-1]
        entry_button=Button(self.maginput_frame,text="ADD To Record",bd=9,relief=RAISED,bg='brown',fg='white',font='Impact',\
                            command=lambda:self.entry_check(category,list_stringvars,string,string1),cursor="hand2")
        entry_button.place(x=400,y=620)
        entry_button=Button(self.maginput_frame,text="Cancel And Go Back",bd=9,relief=RAISED,bg='brown',fg='white',font='Impact',\
                            command=lambda:self.display_mag(category,self.col_list,self.clt),cursor="hand2")
        entry_button.place(x=700,y=620)

    def entry_check(self,category,list_stringvars,string,string1):
        
        check=list(map(lambda x: True if x.get() != '' else False,list_stringvars))
        ql="SELECT ProductCode From magazines"
        cursor.execute(ql)
        productcodeslist=[]
        for pros in cursor:
            productcodeslist.append(pros[0])

        if list_stringvars[1].get() in productcodeslist:
            ms.showerror("Can't Assign","ProductCode Already Available,Please Try Another")
            
        if False in check:
            ms.showwarning("Data input Error","Entries Not Filled")
        else:
            self.input(category,list_stringvars,string,string1)
    def input(self,category,list_stringvars,string,string1):
        sql="INSERT INTO magazines" + string + " VALUES (" + string1 + ")"
        val=tuple(map(lambda x:x.get().upper(),list_stringvars))
        
        cursor.execute(sql,val)
        mydbase.commit()

        self.maginput_frame.destroy()
        self.go_back_b.destroy()
        self.display_mag(category,self.col_list,self.clt)

    def display_mag(self,category,col_list,clt):
        self.clt=clt
        self.category=category
        self.col_list=col_list
        self.go_back_b.destroy()
        self.maginput_frame.destroy()
        string=""
        for col in col_list:
            string+=col + ","
        string=string[:len(string)-1]
        sql="SELECT " + string + " FROM magazines WHERE Category = %s"
        no_of_el=cursor.execute(sql,category)
        self.mylist=cursor.fetchall()

        self.magdisplay_frame=Frame(root,width=800,height=760,bd=12,relief=SUNKEN)
        self.magdisplay_frame.place(x=40,y=40)
        try:
            imge=PhotoImage(file="display mag.gif")
            img=Label(self.magdisplay_frame,image=imge)
            self.magdisplay_frame.image=imge
            img.place(x=0,y=0)
        except:
            True
        category_heading=Label(self.magdisplay_frame,text=category.upper() + " DISPLAY LIST",font=("stencil",25,"bold","italic"),fg="red")
        category_heading.place(x=220,y=10)
        serial_heading=Label(self.magdisplay_frame,text="S.NO",font=("Times",8),relief=RIDGE,bd=8,width=6)
        serial_heading.place(x=20,y=50)
        model_heading=Label(self.magdisplay_frame,text="ModelName",font=("Impact",11),relief=RIDGE,bd=8,width=18)
        model_heading.place(x=120,y=50)
        code_heading=Label(self.magdisplay_frame,text="ProductCode",font=("Impact",11),relief=RIDGE,bd=8,width=13)
        code_heading.place(x=280,y=50)
        stock_heading=Label(self.magdisplay_frame,text="Stock",font=("Impact",11),relief=RIDGE,bd=8,width=10)
        stock_heading.place(x=410,y=50)
        price_heading=Label(self.magdisplay_frame,text="Price RS",font=("Impact",11),relief=RIDGE,bd=8,width=13)
        price_heading.place(x=530,y=50)
        self.magdisplay_list=Frame(self.magdisplay_frame,bd=6,relief=SOLID,bg='brown')
        self.magdisplay_list.place(x=10,y=90)
        scroll_display=Scrollbar(self.magdisplay_list,orient="vertical")
        scroll_display.pack(side=RIGHT,fill=Y)
        self.Lb_sno=Listbox(self.magdisplay_list)
        self.Lb_model=Listbox(self.magdisplay_list)
        self.Lb_productcode=Listbox(self.magdisplay_list)
        self.Lb_stock=Listbox(self.magdisplay_list)
        self.Lb_price=Listbox(self.magdisplay_list)
        self.mag_list=[self.Lb_sno,self.Lb_model,self.Lb_productcode,self.Lb_stock,self.Lb_price]
        for elem_list in self.mag_list:
            elem_list.config(width=12,bd=5,font=("Franklin Gothic Demi",10),bg="grey",\
                  fg='white',highlightthickness=7,\
                  highlightcolor='midnight blue',\
                  relief=SOLID,height=18,yscrollcommand=scroll_display.set)
            elem_list.pack(side=LEFT,fill=Y)
        self.Lb_sno.config(width=5,highlightcolor='red',highlightthickness=12,selectbackground='brown',cursor="hand2")
        self.Lb_stock.config(width=5)
        self.Lb_model.config(width=23)
        self.Lb_productcode.config(width=10)
        self.Lb_sno.bind('<<ListboxSelect>>',self.get_listelement)
        count_serials=1
        for row in self.mylist:
            self.Lb_sno.insert(END,count_serials)
            self.Lb_model.insert(END,row[0])
            self.Lb_productcode.insert(END,row[1])
            self.Lb_stock.insert(END,row[2])
            self.Lb_price.insert(END,row[3])
            count_serials+=1
        
        scroll_display.config(command=self.scroll_view)
        if login_boolean == True:
            self.add_button=Button(self.magdisplay_frame,text="ADD A RECORD",bg="green",fg="black",relief=SOLID,bd=12,\
                                   command=lambda:self.input_mag(category),cursor="hand2")
            self.add_button.place(x=370,y=680)
        self.go_back_b=Button(root,text="RETURN TO MAIN DISPLAY",command=self.go_back,relief=RAISED,cursor="hand2",\
                              bd=15,bg='light blue',fg='black')
        self.go_back_b.place(x=1200,y=7)

    def scroll_view(self,*args):
        for elem in self.mag_list:
            elem.yview(*args)
    def go_back(self):
        self.magdetail_frame.destroy()
        self.magdisplay_frame.destroy()
        self.go_back_b.destroy()
        self.magmodify_frame.destroy()
        self.maginput_frame.destroy()
        self.return_main_display()
    def get_listelement(self,Lb_sno):
        try:
            index=self.Lb_sno.curselection()[0]
            self.detail_mag(self.category,self.mylist[index][0],self.mylist[index][1])
        except:
            True
    
    def detail_mag(self,category,model,productcode):
        sql="SELECT * FROM magazines WHERE ModelName = %s AND ProductCode = %s AND Category = %s"
        val=(model,productcode,category)
        cursor.execute(sql,val)
        myres=cursor.fetchone()
        sql="SHOW COLUMNS FROM magazines"
        cursor.execute(sql)
        self.magdetail_frame.destroy()
        self.magdetail_frame=Frame(root,width=460,height=600,bd=20,relief=GROOVE)
        self.magdetail_frame.place(x=920,y=200)
        top_head=Label(self.magdetail_frame,text=model,font=("Impact",25,"normal","italic"),width=20,relief=SOLID)
        top_head.place(x=70,y=10)
        try:
            self.dict={}
            i=0
            for inc in cursor:
                self.dict[inc[0]]=myres[i]
                i+=1
            attributes_y=60
            for key,value in self.dict.items():
                keys=Label(self.magdetail_frame,text=key + "-->",font=("calibri",12,"bold"),relief=FLAT)
                keys.place(x=20,y=attributes_y)
                values=Label(self.magdetail_frame,text=value,font=("georgia",12,"bold"),relief=FLAT)
                values.place(x=150,y=attributes_y)
                attributes_y+=35
            cancel_button=Button(self.magdetail_frame,text="CANCEL",cursor="hand2",\
                                 command=lambda: self.magdetail_frame.destroy(),relief=RAISED,bd=5,width=7)
            cancel_button.place(x=250,y=530)
            if login_boolean == False:
                self.clt.buy_button(self.magdetail_frame,"magazines",self.dict['ModelName'],self.dict['ProductCode'],self.dict['Stock'],self.dict['Price'])
            elif login_boolean == True:
                update_button=Button(self.magdetail_frame,text="UPDATE",cursor="hand2",\
                                     command=lambda: self.modify_mag(category,model,productcode),relief=RAISED,bd=5,width=7)
                update_button.place(x=30,y=530)
                delete_button=Button(self.magdetail_frame,text="DELETE",cursor="hand2",\
                                     command=lambda: self.delete_mag(category,model,productcode),relief=RAISED,bd=5,width=7)
                delete_button.place(x=130,y=530)
        except:
            True
            
    def delete_mag(self,category,model,productcode):
        ask=ms.askyesno("DELETE","Are You Sure You Want To Delete It?")
        if ask == YES:
            self.magdetail_frame.destroy()
            self.magdisplay_frame.destroy()
            sql="DELETE  FROM magazines WHERE ModelName = %s AND ProductCode = %s AND Category = %s"
            val=val=(model,productcode,category)
            cursor.execute(sql,val)
            mydbase.commit()
            self.display_mag(category,self.col_list,self.clt)
            ms.showinfo("DELETED",model +" Deleted Successfully")

    def goto_display(self):
        self.maginput_frame.destroy()
        self.magmodify_frame.destroy()
        self.go_back_b.destroy()
        self.display_mag(self.category,self.col_list,self.clt)

    def modify_mag(self,category,model_name,productcode):
        self.magdetail_frame.destroy()
        self.magdisplay_frame.destroy()
        self.magmodify_frame=Frame(root,width=1050,height=720,bd=7,relief=SOLID)
        self.magmodify_frame.place(x=150,y=60)
        cancel_mod=Button(self.magmodify_frame,text="Cancel And Go Back",command=self.goto_display,relief=RAISED,bd=8,cursor="hand2")
        cancel_mod.place(x=500,y=650)
        try:
            imge=PhotoImage(file="modify mag.gif")
            img=Label(self.magmodify_frame,image=imge)
            self.magmodify_frame.image=imge
            img.place(x=0,y=0)
        except:
            True
        update_R1=Radiobutton(self.magmodify_frame)
        update_R2=Radiobutton(self.magmodify_frame)
        update_R3=Radiobutton(self.magmodify_frame)
        update_R4=Radiobutton(self.magmodify_frame)
        update_R5=Radiobutton(self.magmodify_frame)
        update_R6=Radiobutton(self.magmodify_frame)
        update_R7=Radiobutton(self.magmodify_frame)
        update_R8=Radiobutton(self.magmodify_frame)
        update_R9=Radiobutton(self.magmodify_frame)
        update_R10=Radiobutton(self.magmodify_frame)
        update_R11=Radiobutton(self.magmodify_frame)
        update_R12=Radiobutton(self.magmodify_frame)
        update_R13=Radiobutton(self.magmodify_frame)
        update_R14=Radiobutton(self.magmodify_frame)
        update_R15=Radiobutton(self.magmodify_frame)
        update_R16=Radiobutton(self.magmodify_frame)
        update_R17=Radiobutton(self.magmodify_frame)
        update_R18=Radiobutton(self.magmodify_frame)
        update_R19=Radiobutton(self.magmodify_frame)
        update_R20=Radiobutton(self.magmodify_frame)
        update_Rlist=[update_R1,update_R2,update_R3,update_R4,update_R5,update_R6,update_R7,update_R8,update_R9,update_R10,\
                      update_R11,update_R12,update_R13,update_R14,update_R15,update_R16,update_R17,update_R18,update_R19,update_R20]
        
        sql="SELECT * FROM magazines WHERE ModelName = %s AND ProductCode = %s AND Category = %s"
        val=(model_name,productcode,category)
        cursor.execute(sql,val)
        myres=cursor.fetchone()
        sql="SHOW COLUMNS FROM magazines"
        cursor.execute(sql)
        self.dict={}
        i=0
        for inc in cursor:
            if inc[0] != "Category":
                self.dict[inc[0]]=myres[i]
            i+=1
        header=Label(self.magmodify_frame,text="Choose The Attribute To Modify: ",font=("britannic bold",15,"bold","italic"),fg="red")
        header.place(x=5,y=10)
        update_count=0
        mod_element=StringVar()
        attributes_y=40
        for key,value in self.dict.items():
                keys=Label(self.magmodify_frame,text=key + ":-",font=("calibri",12,"bold"),relief=FLAT)
                keys.place(x=20,y=attributes_y)
                values=Label(self.magmodify_frame,text=value,font=("Times",12,"bold"),relief=FLAT)
                values.place(x=150,y=attributes_y)
                update_Rlist[update_count].config(variable=mod_element,value=key,cursor="hand2",\
                                                  command=lambda:self.mod_enter(category,model_name,productcode,mod_element.get()))
                update_Rlist[update_count].place(x=5,y=attributes_y)
                attributes_y+=35
                update_count+=1
        self.enter_new_label=Label(self.magmodify_frame)
        self.enter_new=Entry(self.magmodify_frame)
        self.mod_button=Button(self.magmodify_frame)
    def mod_enter(self,category,model_name,productcode,mod_element):
        self.enter_new_label.destroy()
        self.enter_new.destroy()
        self.mod_button.destroy()
        list_tempup=[]
        list_tempup.extend(self.dict.keys())
        index_y=list_tempup.index(mod_element)
        self.enter_new_label=Label(self.magmodify_frame,text="Enter Modified Value of "+ mod_element,relief=RIDGE,bd=10)
        self.enter_new_label.place(x=340,y=40+(index_y*35))
        self.enter_new=Entry(self.magmodify_frame,relief=GROOVE,bd=5,width=30)
        self.enter_new.place(x=580,y=42+(index_y*35))
        self.mod_button=Button(self.magmodify_frame,text="Modify "+ mod_element,relief=RAISED,bd=8,cursor="hand2",\
                           command=lambda:self.mod_entrycheck(category,model_name,productcode,mod_element,self.enter_new.get()))
        self.mod_button.place(x=780,y=40+(index_y*35))
    def mod_entrycheck(self,category,model_name,productcode,mod_element,mod_value):
        ql="SELECT ProductCode From magazines"
        cursor.execute(ql)
        productcodeslist=[]
        for pros in cursor:
            productcodeslist.append(pros[0])

        if mod_value in productcodeslist:
            ms.showerror("Can't Assign","ProductCode Already Available,Please Try Another")
            
        if mod_value == "":
            ms.showwarning("Error","Entry Not Filled")
        else:
            self.modify_done(category,model_name,productcode,mod_element,mod_value)
    def modify_done(self,category,model_name,productcode,mod_element,mod_value):
        sql="UPDATE magazines  SET " + mod_element + " = %s WHERE ModelName = %s AND ProductCode = %s AND Category = %s"  
        val=(mod_value.upper(),model_name,productcode,category)
        cursor.execute(sql,val)
        mydbase.commit()
        self.magmodify_frame.destroy()
        if mod_element == "ModelName" or mod_element == "ProductCode":
            if mod_element == "ModelName":
                model_name=mod_value
            elif mod_element == "ProductCode":
                productcode=mod_value
        self.modify_mag(category,model_name,productcode)
        ms.showinfo("Task Done",mod_element +" Updated Successfully")
    

class Handguns_mag(Magazines):
    def display_handguns_mag(self,clt,main_display):
        self.return_main_display=main_display
        Magazines.display_mag(self,'HANDGUN',['ModelName','ProductCode','Stock','Price'],clt)
    
class Shotguns_mag(Magazines):
    def display_shotguns_mag(self,clt,main_display):
        self.return_main_display=main_display
        Magazines.display_mag(self,'SHOTGUN',['ModelName','ProductCode','Stock','Price'],clt)
    
class Rifles_mag(Magazines):
    def display_rifles_mag(self,clt,main_display):
        self.return_main_display=main_display
        Magazines.display_mag(self,'RIFLE',['ModelName','ProductCode','Stock','Price'],clt)
    
'''------------------------------------------------END OF MAGAZINES CLASS----------------------------------------------------------------'''


'''-------------------------------------------PERSON->PARENT CLASS OF ADMIN AND CLIENT------------------------------------------------------'''
class Person():
    def __init__(self):
        pass
'''-------------------------------------------------------------START OF ADMIN CLASS-------------------------------------------------------'''
class Admin(Person):
    def __init__(self):
        self.frame=Frame(root)
        self.login_dataframe=Frame(root)
        self.create_dataframe=Frame(root)
        self.admins_displayframe=Frame(root)
        self.mydetails_frame=Frame(root)
        
    def own_details(self,main_display):
        self.return_main_display=main_display
        sql="SELECT * FROM admins WHERE Name = %s AND UserName =%s"
        val=(login_name,login_user)
        cursor.execute(sql,val)
        self.mydetails=cursor.fetchone()
        sql="SHOW COLUMNS FROM admins"
        cursor.execute(sql)
        admins_columns=[]
        for colss in cursor:
            admins_columns.append(colss[0])
        self.go_back_b=Button(root,text="RETURN TO MAIN DISPLAY",cursor="hand2",\
                              command=self.go_back,relief=RAISED,bd=15,bg='light blue',fg='black')
        self.go_back_b.place(x=1200,y=7)
        self.mydetails_frame=Frame(root,width=400,height=500,relief=RIDGE,bd=20)
        self.mydetails_frame.place(x=300,y=180)
        detail_head=Label(self.mydetails_frame,text="MY DETAILS",font=("forte",20,"bold"))
        detail_head.place(x=80,y=10)
        for ad_counts in range(len(admins_columns)):
            tags=Label(self.mydetails_frame,text=admins_columns[ad_counts] + ":::",font=("times",10,"bold"))
            tags.place(x=50,y=(ad_counts+1)*40)
        ad_counts=0
        for row in self.mydetails:
            print(row)
            detail=Label(self.mydetails_frame,text=row,font=("times",15,"bold"))
            detail.place(x=180,y=(ad_counts+1)*40)
            ad_counts+=1
        
    
    def display_all(self,main_display):
        self.return_main_display=main_display
        sql="SELECT Name,AdminCode,Date_Of_Joining FROM admins"
        ad_counts=cursor.execute(sql)
        self.all_admins=cursor.fetchall()
        self.go_back_b=Button(root,text="RETURN TO MAIN DISPLAY",cursor="hand2",\
                              command=self.go_back,relief=RAISED,bd=15,bg='light blue',fg='black')
        self.go_back_b.place(x=1200,y=7)
        self.admins_displayframe=Frame(root,width=500,height=300,relief=SOLID,bd=30)
        self.admins_displayframe.place(x=500,y=200)
        shname=Label(self.admins_displayframe,text="Admins",relief=GROOVE,bd=5,font=("impact",12))
        shname.place(x=50,y=10)
        shcode=Label(self.admins_displayframe,text="AdminCode",relief=GROOVE,bd=5,font=("impact",12))
        shcode.place(x=190,y=10)
        shdate=Label(self.admins_displayframe,text="Date-Of-Joining",relief=GROOVE,bd=5,font=("impact",12))
        shdate.place(x=300,y=10)
        for cts in range(ad_counts):
            showname=Label(self.admins_displayframe,text=self.all_admins[cts][0],font=("calibri",11,"bold")).place(x=50,y=(cts+1)*50)
            showcode=Label(self.admins_displayframe,text=self.all_admins[cts][1],font=("calibri",11,"bold")).place(x=190,y=(cts+1)*50)
            showdate=Label(self.admins_displayframe,text=self.all_admins[cts][2],font=("calibri",11,"bold")).place(x=300,y=(cts+1)*50)
        
    
    def add_account(self):
        sql="INSERT INTO admins(Name,AdminCode,UserName,Password,Date_Of_Joining) VALUES(%s,%s,%s,%s,%s)"
        val=(self.name.get(),self.admincode,self.user_name,self.password_trial.get(),self.doj)
        cursor.execute(sql,val)
        mydbase.commit()
        self.go_back_b.destroy()
        self.accounts(self.create_dataframe)
    def pass_match(self):
        if self.password_trial.get() != self.confirm.get():
            ms.showwarning("Error","Password Did Not match")
        else:
            self.add_account()
    def entry_check(self):
        list_str=[self.name,self.password_trial,self.confirm]
        check=list(map(lambda x: True if x.get() != '' else False,list_str))
        if False in check:
            ms.showwarning("Input Error","Entries not filled")
        else:
            self.pass_match()
    def create_account(self,row_count):
        self.frame.destroy()
        self.create_dataframe=Frame(root,width=600,height=400,bd=12,relief=SUNKEN)
        self.create_dataframe.place(x=300,y=300)
        self.name=StringVar()
        self.password_trial=StringVar()
        self.confirm=StringVar()
        listusers=['StackSR','LinkedList','QueueSR']
        if row_count == 1:
            self.user_name=listusers[1]
        elif row_count == 0:
            self.user_name=listusers[0]
        elif row_count == 2:
            self.user_name=listusers[2]
        self.admincode="SR-0" + str(random.randint(60,99))
        codelabel=Label(self.create_dataframe,text=self.admincode,relief='raised')
        codelabel.place(x=250,y=30)
        userlabel=Label(self.create_dataframe,text=self.user_name,relief='raised')
        userlabel.place(x=250,y=60)
        namelabel=Label(self.create_dataframe,text="Enter The Name: ",relief='raised')
        namelabel.place(x=200,y=100)
        passwordlabel=Label(self.create_dataframe,text="Create Password",relief='raised')
        passwordlabel.place(x=200,y=140)
        confirmlabel=Label(self.create_dataframe,text="Confirm Password",relief='raised')
        confirmlabel.place(x=200,y=180)
        nameentry=Entry(self.create_dataframe,text=self.name,relief='raised')
        nameentry.place(x=360,y=100)
        passentry=Entry(self.create_dataframe,text=self.password_trial,relief='raised')
        passentry.place(x=360,y=140)
        conentry=Entry(self.create_dataframe,text=self.confirm,relief='raised')
        conentry.place(x=360,y=180)
        today=datetime.datetime.now()
        today=today.strftime("%Y-%m-%d")
        self.doj=today
        go=Button(self.create_dataframe,text="GO",command=lambda :self.entry_check(),relief='raised',cursor="hand2")
        go.place(x=350,y=350)
    def create_check(self):
        sql="SELECT UserName FROM admins"
        row_count=cursor.execute(sql)
        if row_count == 3:
            ms.showwarning("Sorry!"," The Accounts limit is full")
        else:
            self.create_account(row_count)
    def logout(self,main_frame):
        time.sleep(1)
        global login_boolean
        login_boolean=False
        self.button_logout.destroy()
        self.main_title.destroy()
        main_frame.destroy()
        self.clientinfo_button.destroy()
        self.loggedin_button.destroy()
        self.admininfo_button.destroy()
        self.normal_main()
    def logout_button(self,main_frame,normal_main,main_title,clientinfo_button,admininfo_button,loggedin_admin_button):
        self.normal_main=normal_main
        self.main_title=main_title
        self.clientinfo_button=clientinfo_button
        self.admininfo_button=admininfo_button
        self.loggedin_button=loggedin_admin_button
        self.button_logout=Button(root,text="LOGOUT",command=lambda:self.logout(main_frame),\
                                  relief=RAISED,width=6,bd=8,bg='red',fg='white',font='Impact',cursor="hand2")
        self.button_logout.place(x=1200,y=30)
    def login_check(self,name_login):
        if self.us.get() == self.check_admin[0] and self.pw.get() == self.check_admin[1]:
            global login_boolean
            login_boolean=True
            global login_name
            login_name=name_login
            global login_user
            login_user=self.check_admin[0]
            self.login_dataframe.destroy()
            self.go_back_b.destroy()
            self.main_title.destroy()
            self.admin_main()
        else:
            ms.showwarning("Login Error","Wrong username/password")
    def login(self,name_login):
        
        self.frame.destroy()
        self.login_dataframe=Frame(root,width=600,height=400,bd=12,relief=SUNKEN)
        self.login_dataframe.place(x=300,y=300)
        ql="SELECT UserName,Password FROM admins WHERE Name = %s"
        cursor.execute(ql,name_login)
        self.check_admin=cursor.fetchone()
        login_user=Label(self.login_dataframe,text="Enter your user name: ",relief=GROOVE,width=20,font="TImes")
        login_user.place(x=90,y=80)
        login_pass=Label(self.login_dataframe,text="Enter your password: ",relief=GROOVE,width=20,font="TImes")
        login_pass.place(x=90,y=120)
        self.us=Entry(self.login_dataframe,relief=FLAT)
        self.us.place(x=280,y=80)
        self.pw=Entry(self.login_dataframe,relief=FLAT,show="*")
        self.pw.place(x=280,y=120)
        self.us.focus_set()
        login_go=Button(self.login_dataframe,text="Login Account",command=lambda:self.login_check(name_login),\
                        relief='raised',bg="blue",font="georgia",cursor="hand2")
        login_go.place(x=200,y=180)
    def login_enter(self):
        log_b=Button(self.frame,text="Login As " +self.login_var.get(),command=lambda:self.login(self.login_var.get()),\
                     width=25,cursor="hand2",relief=SOLID,bd=8)
        log_b.place(x=200,y=10)
    def accounts(self,main_frame):
        self.button_login.destroy()
        main_frame.destroy()
        
        self.go_back_b=Button(root,text="RETURN TO MAIN DISPLAY",command=self.go_back,cursor="hand2",relief=RAISED,bd=15,bg='light blue',fg='black')
        self.go_back_b.place(x=1200,y=7)
        sql="SELECT Name FROM admins"
        no=cursor.execute(sql)
        accounts_name=cursor.fetchall()
        count_name=0
        count_acc=50
        self.login_var=StringVar()
        self.frame=Frame(root,width=600,height=400,bd=12,relief=SUNKEN)
        self.frame.place(x=300,y=300)
        acc_b1=Radiobutton(self.frame)
        acc_b2=Radiobutton(self.frame)
        acc_b3=Radiobutton(self.frame)
        list_buttons=[acc_b1,acc_b2,acc_b3]
        for count in range(len(accounts_name)):
            list_buttons[count].config(text=accounts_name[count][0],variable=self.login_var,value=accounts_name[count][0],\
                                       command=self.login_enter,width=12,cursor="hand2",relief=SOLID)
            list_buttons[count].place(x=200,y=count_acc)
            count_acc+=40
        self.cr=Button(self.frame,text="CREATE ACCOUNT",command=lambda:self.create_check(),relief='raised',bd=4,cursor="hand2")
        self.cr.place(x=180,y=250)
    def go_back(self):
        self.go_back_b.destroy()
        self.frame.destroy()
        self.login_dataframe.destroy()
        self.create_dataframe.destroy()
        self.main_title.destroy()
        self.admins_displayframe.destroy()
        self.mydetails_frame.destroy()
        self.return_main_display()
    def login_button(self,main_frame,main_title,admin_main,normal_main):
        self.admin_main=admin_main
        self.main_title=main_title
        self.return_main_display=normal_main
        self.button_login=Button(root,text="LOGIN",command=lambda:self.accounts(main_frame),relief=RAISED,\
                                 width=6,bd=8,bg='blue',fg='white',font='Impact',cursor="hand2")
        self.button_login.place(x=1200,y=30)
'''---------------------------------------------------END OF ADMIN CLASS--------------------------------------------------------------------'''

'''---------------------------------------------------START OF CLIENT CLASS------------------------------------------------------------------'''
class Client(Person):
    def __init__(self):
        self.tables=[]
        self.products=[]
        self.ids=[]
        self.items=[]
        self.stocks=[]
        self.prices=[]
        self.purchasing=""
        self.total_price=0.0
        self.cardlist_frame=Frame(root)
        self.input_frame=Frame(root)
        self.edit_frame=Frame(root)

    def display_all(self,main_display):
        self.return_main_display=main_display
        sql="SELECT * FROM clients"
        cursor.execute(sql)
        self.all_clients=cursor.fetchall()
        sql="SHOW COLUMNS FROM clients"
        cursor.execute(sql)
        self.clients_columns=[]
        for colss in cursor:
            self.clients_columns.append(colss[0])
        self.go_back_b=Button(root,text="RETURN TO MAIN DISPLAY",cursor="hand2",\
                              command=self.go_back_from,relief=RAISED,bd=15,bg='light blue',fg='black')
        self.go_back_b.place(x=1200,y=7)
        self.clients_displayframe=Frame(root,width=1350,height=700,bd=12,relief=SOLID)
        self.clients_displayframe.place(x=10,y=80)
        sno_l=Label(self.clients_displayframe,text="Serial No",font=("times",15,"bold")).place(x=40,y=70)
        name_l=Label(self.clients_displayframe,text="Clients",font=("times",15,"bold")).place(x=230,y=70)
        dates_l=Label(self.clients_displayframe,text="Dates of Purchase",font=("times",15,"bold")).place(x=390,y=70)
        amounts_l=Label(self.clients_displayframe,text="Bill Amoumts",font=("times",15,"bold")).place(x=600,y=70)
        self.clientslist_frame=Frame(self.clients_displayframe,bd=10,relief=SOLID)
        self.clientslist_frame.place(x=5,y=100)
        scroll_clients=Scrollbar(self.clientslist_frame,orient="vertical")
        scroll_clients.pack(side=RIGHT,fill=Y)
        self.client_serials=Listbox(self.clientslist_frame)
        self.client_names=Listbox(self.clientslist_frame)
        self.client_dates=Listbox(self.clientslist_frame)
        self.client_amounts=Listbox(self.clientslist_frame)
        self.clients_list=[self.client_serials,self.client_names,self.client_dates,self.client_amounts]
        for ch in self.clients_list:
            ch.config(width=20,bd=5,font=("Franklin Gothic Demi",10),bg="grey",\
                  fg='white',highlightthickness=7,\
                  highlightcolor='midnight blue',\
                  relief=SOLID,height=15,yscrollcommand=scroll_clients.set)
            ch.pack(side=LEFT,fill=Y)
        self.client_serials.bind('<<ListboxSelect>>',self.display_client)
        sno=1
        for row in self.all_clients:
            self.client_serials.insert(END,sno)
            self.client_names.insert(END,row[0])
            self.client_dates.insert(END,row[5])
            self.client_amounts.insert(END,row[4])
            sno+=1
        scroll_clients.config(command=self.scroll_view)

    def scroll_view(self,*args):
        for elem in self.clients_list:
            elem.yview(*args)
    def go_back_from(self):
        self.go_back_b.destroy()
        self.clients_displayframe.destroy()
        self.return_main_display()

    def display_client(self,client_serials):
        try:
            index=self.client_serials.curselection()[0]
            self.cl_display=Frame(self.clients_displayframe,relief=FLAT,width=1000,height=200)
            self.cl_display.place(x=10,y=430)
            for cts in range(7):
                showit=Label(self.cl_display,text=self.clients_columns[cts]+"  :> "+str(self.all_clients[index][cts]),font=("ariel",12,"bold"))
                showit.place(x=10,y=(cts+1)*25)
        except:
            print("now showing")
            True
    
    def bill(self):
        length=len(self.tables)
        newwindow=Tk()
        newwindow.title("BILL")
        size="500x"+str(70*length)
        newwindow.geometry(size)
        newwindow.config(bg="white")
        bill_hd=Label(newwindow,text="----SR ARMS AND AMMO----",font=("algerian",11,"bold"),bg="white")
        bill_hd.place(x=140,y=1)
        bill_h=Label(newwindow,text="<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   BILL   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",font=("times",10),bg="white")
        bill_h.place(x=0,y=24)
        inc_y=45
        for bitems in range(len(self.tables)):
            b_items=Label(newwindow,text=self.items[bitems] +" "+ self.products[bitems]+" "+self.ids[bitems]+" "+str(self.prices[bitems]),bg="white")
            b_items.place(x=10,y=inc_y)
            inc_y+=22
        total=Label(newwindow,text="TOTAL PRICE: " +str(self.total_price))
        total.place(x=350,y=inc_y+25)
    def purchase(self):
        ql="INSERT INTO clients(Name,Email,ContactNo,Purchased_Items,Bill_Amount,Date_Of_Purchase,Time) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        value=(self.nameentry.get(),self.emailentry.get(),self.contactentry.get(),self.purchasing,self.total_price,self.datep,self.timep)
        cursor.execute(ql,value)
        mydbase.commit()
        for counts in range(len(self.tables)):
            sql="SELECT Stock FROM "+self.tables[counts]+" WHERE ProductCode = %s"
            cursor.execute(sql,self.ids[counts])
            stock=cursor.fetchone()
            stocks=int(stock[0]) - int(self.items[counts])
            sql="UPDATE "+self.tables[counts] + " SET Stock = %s WHERE ProductCode = %s"
            val=(str(stocks),self.ids[counts])
            cursor.execute(sql,val)
            mydbase.commit()
        self.bill()
        self.tables=[]
        self.products=[]
        self.ids=[]
        self.items=[]
        self.prices=[]
        self.purchasing=""
        self.total_price=0.0
        self.go_back()
    
    def entry_check(self):
        list_str=[self.nameentry.get(),self.emailentry.get(),self.contactentry.get()]
        check=list(map(lambda x: True if x != '' else False,list_str))
        if False in check:
            ms.showwarning("Input Error","Entries not filled")
        else:
            for counts in range(len(self.tables)):
                self.purchasing=self.purchasing +self.items[counts]+ " " + self.products[counts] + ','
            self.purchase()

    def input_client(self):
        self.edit_frame.destroy()
        self.input_frame.destroy()
        self.input_frame=Frame(root,width=500,height=400,bd=10,relief=RAISED,bg="silver")
        self.input_frame.place(x=800,y=200)
        namelabel=Label(self.input_frame,text="Enter Name: ",font=("cooper black",14),relief=RIDGE,bd=4)
        namelabel.place(x=20,y=70)
        emaillabel=Label(self.input_frame,text="Enter Email Address: ",font=("cooper black",14),relief=RIDGE,bd=4)
        emaillabel.place(x=20,y=140)
        contactlabel=Label(self.input_frame,text="Enter Contact No: ",font=("cooper black",14),relief=RIDGE,bd=4)
        contactlabel.place(x=20,y=210)
        self.nameentry=Entry(self.input_frame,bd=3,width=20,justify=CENTER,font=("arial black",10),relief=RIDGE)
        self.nameentry.place(x=270,y=70)
        self.nameentry.focus_set()
        self.emailentry=Entry(self.input_frame,bd=3,width=20,justify=CENTER,font=("arial black",10),relief=RIDGE)
        self.emailentry.place(x=270,y=140)
        self.contactentry=Entry(self.input_frame,bd=3,width=20,justify=CENTER,font=("arial black",10),relief=RIDGE)
        self.contactentry.place(x=270,y=210)
        today=datetime.datetime.now()
        self.datep=today.strftime("%Y-%m-%d")
        self.timep=today.strftime("%H:%M:%S")
        b_input=Button(self.input_frame,text="DONE",state=ACTIVE,command=lambda :self.entry_check(),cursor="hand2")
        b_input.place(x=150,y=350)
        b1=Button(self.input_frame,text="CANCEL",command=lambda:self.input_frame.destroy(),cursor="hand2")
        b1.place(x=400,y=350)

    def cardlist(self,main_display):
        self.return_main_display=main_display
        self.go_back_b=Button(root,text="RETURN TO MAIN DISPLAY",command=self.go_back,cursor="hand2",relief=RAISED,bd=15,bg='light blue',fg='black')
        self.go_back_b.place(x=1200,y=7)
        self.cardlist_frame=Frame(root,width=750,height=460,relief=RAISED,bd=20,bg="blue")
        self.cardlist_frame.place(x=10,y=100)
        self.card_label=Label(root,text="    CARDLIST    ",font=("elephant",25),bd=4,relief=GROOVE,bg='silver',fg='black')
        self.card_label.place(x=600,y=20)
        self.cardelements_frame=Frame(self.cardlist_frame,bg="midnight blue",relief=SOLID)
        self.cardelements_frame.place(x=5,y=60)
        self.element_name=Label(self.cardlist_frame,text="Product Name",width=15,font=("impact",15),relief=SOLID,bg="black",fg="white")
        self.element_name.place(x=35,y=15)
        self.element_items=Label(self.cardlist_frame,text="Items",width=15,font=("impact",15),relief=SOLID,bg="black",fg="white")
        self.element_items.place(x=250,y=15)
        self.element_price=Label(self.cardlist_frame,text="Calculated Price",width=15,font=("impact",15),relief=SOLID,bg="black",fg="white")
        self.element_price.place(x=480,y=15)
        self.product_lb=Listbox(self.cardelements_frame)
        self.item_lb=Listbox(self.cardelements_frame)
        self.price_lb=Listbox(self.cardelements_frame)
        list_lb=[self.product_lb,self.item_lb,self.price_lb]
        x1=20
        for lb_count in range(len(list_lb)):
            list_lb[lb_count].config(width=25,height=14,bd=12,font=("ariel",9,"bold"),bg="white",\
                  fg='black',highlightthickness=12,\
                  highlightcolor='midnight blue',\
                  relief=GROOVE,selectbackground='brown')
            list_lb[lb_count].pack(side=LEFT,fill=Y)
        
        for counts in range(len(self.tables)):
            self.product_lb.insert(END,self.products[counts])
            self.item_lb.insert(END,self.items[counts])
            per_prize=float(float(self.prices[counts])/int(self.items[counts]))
            self.price_lb.insert(END,str(per_prize) +"X"+self.items[counts]+" = "+str(self.prices[counts]))
        
        scroll_list=Scrollbar(self.cardelements_frame)
        scroll_list.pack(side=RIGHT,fill=Y)
        self.product_lb.config(yscrollcommand=scroll_list.set)
        self.item_lb.config(yscrollcommand=scroll_list.set)
        self.price_lb.config(yscrollcommand=scroll_list.set)
        scroll_list.config(command=self.cardlist_view)
        self.product_lb.bind("<<ListboxSelect>>",self.edit_cardlist)
        self.totalprice_label=Label(self.cardlist_frame,text="Total Price =" + str(self.total_price),font=("Franklin Gothic Heavy",13),\
                                    bg="red",fg="white",width=25,relief=SUNKEN,bd=10)
        self.totalprice_label.place(x=180,y=360)
        self.final_purchase=Button(root,text="Purchase And Bill",relief=RAISED,bd=8,bg="bisque",fg="black",cursor="hand2",\
                              command=lambda:self.input_client())
        self.final_purchase.place(x=100,y=570)
        self.demolish=Button(root,text="Demolish Cardlist",relief=RAISED,bd=8,bg="azure",fg="black",cursor="hand2",\
                              command=lambda:self.demolish_cardlist())
        self.demolish.place(x=250,y=570)
        if len(self.tables) == 0:
            self.final_purchase.config(state=DISABLED,cursor="arrow")
            self.demolish.config(state=DISABLED,cursor="arrow")
            
    def cardlist_view(self,*args):
        self.product_lb.yview(*args)
        self.item_lb.yview(*args)
        self.price_lb.yview(*args)

    def demolish_cardlist(self):
        self.tables=[]
        self.products=[]
        self.ids=[]
        self.items=[]
        self.stocks=[]
        self.prices=[]
        self.purchasing=""
        self.total_price=0.0
        self.go_back()

    def edit_cardlist(self,product_lb):
        try:
            index=self.product_lb.curselection()[0]
            self.input_frame.destroy()
            self.edit_frame.destroy()
            self.edit_frame=Frame(root,width=500,height=300,bd=7,relief=GROOVE,bg="silver")
            self.edit_frame.place(x=800,y=200)
            per_prize=float(float(self.prices[index])/int(self.items[index]))
            pr_label=Label(self.edit_frame,text="Product: " + self.products[index],font=("ariel",10,"bold"),bg="silver").place(x=10,y=50)
            id_label=Label(self.edit_frame,text="ProductID: " + self.ids[index],font=("ariel",10,"bold"),bg="silver").place(x=10,y=90)
            tb_label=Label(self.edit_frame,text="Category: " + self.tables[index],font=("ariel",10,"bold"),bg="silver").place(x=10,y=130)
            ed_label=Label(self.edit_frame,text="Edit items to change order if you want(Set To 0(ZERO) to remove it from cardlist))",bg="silver",fg="red").place(x=3,y=180)
            it_label=Label(self.edit_frame,text="Items: " + self.items[index],font=("ariel",10,"bold"),bg="silver").place(x=10,y=230)
            it_var=StringVar()
            it_var.set(self.items[index])
            self.item_sp=Spinbox(self.edit_frame,from_ = 0,to = self.stocks[index],textvariable=it_var)
            self.item_sp.place(x=90,y=230)
            item_bt=Button(self.edit_frame,text="Set",relief=RAISED,bd=5,command=lambda:self.edit_items(index,per_prize)).place(x=230,y=230)
        except:
            True
    def edit_items(self,index,per_prize):
        if int(self.item_sp.get()) == 0:
            self.total_price=self.total_price - self.prices[index]
            self.items.pop(index)
            self.tables.pop(index)
            self.ids.pop(index)
            self.products.pop(index)
            self.prices.pop(index)
            self.stocks.pop(index)
            self.product_lb.delete(index)
            self.item_lb.delete(index)
            self.price_lb.delete(index)
            self.totalprice_label.config(text="Total Price =" + str(self.total_price))
            if len(self.tables) == 0:
                self.final_purchase.config(state=DISABLED,cursor="arrow")
                self.demolish.config(state=DISABLED,cursor="arrow")
            self.edit_frame.destroy()
        elif int(self.item_sp.get()) <= self.stocks[index] and int(self.item_sp.get()) != 0:
            self.total_price=self.total_price - self.prices[index]
            self.items[index]=self.item_sp.get()
            self.prices[index]=float(int(self.items[index])* per_prize)
            self.total_price=self.total_price + self.prices[index]
            self.item_lb.delete(index)
            self.item_lb.insert(index,self.items[index])
            self.price_lb.delete(index)
            self.price_lb.insert(index,str(per_prize) + "X"+self.items[index] + "=" +str(self.prices[index]))
            self.totalprice_label.config(text="Total Price =" + str(self.total_price))
            self.edit_frame.destroy()
        else:
            ms.showwarning("OUT OF STOCK","Items out of stock")
        
    def go_back(self):
        self.cardlist_frame.destroy()
        self.card_label.destroy()
        self.input_frame.destroy()
        self.edit_frame.destroy()
        self.final_purchase.destroy()
        self.demolish.destroy()
        self.go_back_b.destroy()
        self.return_main_display()
    def addtocardlist(self,table_name,productname,productid,stock,items,price):
        if int(items) <= stock:
            if productname in self.products and productid in self.ids and table_name in self.tables:
                index=self.products.index(productname)
                items_added=int(self.items[index]) + int(items)
                if items_added <= stock:
                    self.items[index]=str(items_added)
                    price_of_items=float(int(items)*float(price))
                    self.prices[index]=self.prices[index] + price_of_items
                    self.total_price=self.total_price + price_of_items
                    ms.showinfo("Added To Cardlist",self.items[index]+ " "+ productname + " added to Cardlist")
                    self.purchase_b.destroy()
                    self.enter_items.destroy()
                else:
                    ms.showwarning("OUT OF STOCK","Items out of stock")
            else:
                print(table_name)
                self.tables.append(table_name)
                self.products.append(productname)
                self.ids.append(productid)
                self.items.append(items)
                self.stocks.append(stock)
                price_of_items=float(int(items)*float(price))
                self.prices.append(price_of_items)
                self.total_price=self.total_price + price_of_items
                ms.showinfo("Added To Cardlist",items+ " "+ productname + " added to Cardlist")
                self.purchase_b.destroy()
                self.enter_items.destroy()
        else:
            ms.showwarning("OUT OF STOCK","Items out of stock")
    def purchase_button(self,frm,table_name,productname,productid,stock,price):
        self.enter_items=ttk.Combobox(frm,values=list(range(1,int(stock)+1)))
        self.enter_items.set(1)
        self.enter_items.place(x=60,y=500)
        self.purchase_b=Button(frm,text="PURCHASE(Add To CardList)",command=lambda:self.addtocardlist(table_name,productname,productid,stock,str(self.enter_items.get()),price),\
                               width=25,cursor="hand2",relief=RAISED,bd=5)
        self.purchase_b.place(x=20,y=530)
        
    def buy_button(self,frm,table_name,productname,productid,stock,price):
        buy_b=Button(frm,text="BUY",command=lambda:self.purchase_button(frm,table_name,productname,productid,stock,price),cursor="hand2",width=10,relief=RAISED,bd=5)
        buy_b.place(x=20,y=530)
        if int(stock) == 0:
            buy_b.config(state=DISABLED,cursor="arrow")
'''--------------------------------------------------------END OF CLIENT CLASS--------------------------------------------------------'''


'''-----------------------------------------------------------MAIN CLASS OF SR ARMS-------------------------------------------------------'''
class SR_arms:
    def __init__(self):
        #Declaring the variable of Client and Admin class
        self.client_var=Client()
        self.admin_var=Admin()
        #Declaring the variables of Guns classes here
        self.handguns_var=HandGuns()
        self.airguns_var=AirGuns()
        self.rifles_var=Rifles()
        self.shotguns_var=ShotGuns()
        #Declaring the variables of Ammo classes here
        self.hand_ammo=Handguns_ammo()
        self.shot_ammo=Shotguns_ammo()
        self.air_ammo=Airguns_ammo()
        self.rif_ammo=Rifles_ammo()
        #Declaring the variables of Parts classes here
        self.hand_pt=Handguns_parts()
        self.shot_pt=Shotguns_parts()
        self.rif_pt=Rifles_parts()
        #Declaring the variables of Magazines classes here
        self.hand_mag=Handguns_mag()
        self.shot_mag=Shotguns_mag()
        self.rif_mag=Rifles_mag()

    def guest(self):
        self.main_title=Frame(root,bg="grey",width=1000,height=200,relief=RIDGE,bd=12)
        self.main_title.place(x=100,y=10)
        self.title_label=Label(self.main_title,text="   SR ARMS AND AMMO   ",font=("algerian",50,"bold"),fg="black",relief=SUNKEN,bd=12,bg="indian red")
        self.title_label.place(x=70,y=25)
        self.slogan=Label(self.main_title,text="A PROJECT BY SAIM AKHTAR",font=("baskerville old face",20,"normal","italic"),bg="grey",fg="white")
        self.slogan.place(x=290,y=130)
        
    def remove_firearms_options(self,options_frame):
        options_frame.destroy()
        self.firearms_button.config(command=lambda : self.firearms_options(self.main_display,self.log_button))
    def remove_ammo_options(self,options_frame):
        options_frame.destroy()
        self.ammo_button.config(command=lambda : self.ammo_options(self.main_display,self.log_button))
    def remove_magazine_options(self,options_frame):
        options_frame.destroy()
        self.magazine_button.config(command=lambda : self.magazine_options(self.main_display,self.log_button))
    def remove_parts_options(self,options_frame):
        options_frame.destroy()
        self.parts_button.config(command=lambda : self.parts_options(self.main_display,self.log_button))
    def destroy_then_go(self,func,main_display):
        if login_boolean == True:
            self.clientinfo_button.destroy()
            self.admininfo_button.destroy()
            self.loggedin_admin_button.destroy()
        self.main_frame.destroy()
        self.log_button.destroy()
        self.main_title.destroy()
        func(self.client_var,main_display)
    def destroy_then_cardlist(self,func,main_display,log_button):
        self.main_frame.destroy()
        log_button.destroy()
        self.main_title.destroy()
        func(main_display)
    def destroy_then_info(self,func,main_display,log_button):
        self.main_frame.destroy()
        log_button.destroy()
        self.main_title.destroy()
        self.clientinfo_button.destroy()
        self.admininfo_button.destroy()
        self.loggedin_admin_button.destroy()
        func(main_display)
    
    def firearms_options(self,main_display,log_button):
        options_frame=Frame(self.main_frame,bg="silver",width=600,height=50,relief=FLAT)
        options_frame.place(x=210,y=90)
        self.main_display=main_display
        self.log_button=log_button
        handgun_button=Button(options_frame,text="Handguns",relief=RIDGE,bd=3,width=8,font=("cooper black",12),bg="khaki",cursor="hand2",\
                              command= lambda:self.destroy_then_go(self.handguns_var.display_handguns,main_display))
        handgun_button.place(x=10,y=10)
        shotgun_button=Button(options_frame,text="Shotguns",relief=RIDGE,bd=3,width=8,font=("cooper black",12),bg="khaki",cursor="hand2",\
                              command= lambda:self.destroy_then_go(self.shotguns_var.display_shotguns,main_display))
        shotgun_button.place(x=140,y=10)
        rifle_button=Button(options_frame,text="Rifles",relief=RIDGE,bd=3,width=8,font=("cooper black",12),bg="khaki",cursor="hand2",\
                            command= lambda:self.destroy_then_go(self.rifles_var.display_rifles,main_display))
        rifle_button.place(x=270,y=10)
        airgun_button=Button(options_frame,text="Airguns",relief=RIDGE,bd=3,width=8,font=("cooper black",12),bg="khaki",cursor="hand2",\
                             command= lambda:self.destroy_then_go(self.airguns_var.display_airguns,main_display))
        airgun_button.place(x=400,y=10)
        self.firearms_button.config(command= lambda:self.remove_firearms_options(options_frame))
    def ammo_options(self,main_display,log_button):
        options_frame=Frame(self.main_frame,bg="silver",width=680,height=50,relief=FLAT)
        options_frame.place(x=120,y=215)
        self.main_display=main_display
        self.log_button=log_button
        handgun_button=Button(options_frame,text="Handguns Ammo",relief=RIDGE,bd=3,width=13,font=("cooper black",12),bg="khaki",cursor="hand2",\
                              command= lambda:self.destroy_then_go(self.hand_ammo.display_handguns_ammo,main_display))
        handgun_button.place(x=10,y=10)
        shotgun_button=Button(options_frame,text="Shotguns Ammo",relief=RIDGE,bd=3,width=13,font=("cooper black",12),bg="khaki",cursor="hand2",\
                              command= lambda:self.destroy_then_go(self.shot_ammo.display_shotguns_ammo,main_display))
        shotgun_button.place(x=180,y=10)
        rifle_button=Button(options_frame,text="Rifles Ammo",relief=RIDGE,bd=3,width=13,font=("cooper black",12),bg="khaki",cursor="hand2",\
                              command= lambda:self.destroy_then_go(self.rif_ammo.display_rifles_ammo,main_display))
        rifle_button.place(x=350,y=10)
        airgun_button=Button(options_frame,text="Airguns Ammo",relief=RIDGE,bd=3,width=13,font=("cooper black",12),bg="khaki",cursor="hand2",\
                              command= lambda:self.destroy_then_go(self.air_ammo.display_airguns_ammo,main_display))
        airgun_button.place(x=520,y=10)
        self.ammo_button.config(command= lambda:self.remove_ammo_options(options_frame))
    def magazine_options(self,main_display,log_button):
        options_frame=Frame(self.main_frame,bg="silver",width=580,height=50,relief=FLAT)
        options_frame.place(x=180,y=335)
        self.main_display=main_display
        self.log_button=log_button
        handgun_button=Button(options_frame,text="Handguns Magazine",relief=RIDGE,bd=3,width=15,font=("cooper black",12),bg="khaki",cursor="hand2",\
                              command= lambda:self.destroy_then_go(self.hand_mag.display_handguns_mag,main_display))
        handgun_button.place(x=10,y=10)
        shotgun_button=Button(options_frame,text="Shotguns Magazine",relief=RIDGE,bd=3,width=15,font=("cooper black",12),bg="khaki",cursor="hand2",\
                              command= lambda:self.destroy_then_go(self.shot_mag.display_shotguns_mag,main_display))
        shotgun_button.place(x=200,y=10)
        rifle_button=Button(options_frame,text="Rifles Magazine",relief=RIDGE,bd=3,width=15,font=("cooper black",12),bg="khaki",cursor="hand2",\
                              command= lambda:self.destroy_then_go(self.rif_mag.display_rifles_mag,main_display))
        rifle_button.place(x=390,y=10)
        self.magazine_button.config(command= lambda:self.remove_magazine_options(options_frame))
    def parts_options(self,main_display,log_button):
        options_frame=Frame(self.main_frame,bg="silver",width=550,height=50,relief=FLAT)
        options_frame.place(x=180,y=455)
        self.main_display=main_display
        self.log_button=log_button
        handgun_button=Button(options_frame,text="Handguns Parts",relief=RIDGE,bd=3,width=13,font=("cooper black",12),bg="khaki",cursor="hand2",\
                              command= lambda:self.destroy_then_go(self.hand_pt.display_handguns_parts,main_display))
        handgun_button.place(x=10,y=10)
        shotgun_button=Button(options_frame,text="Shotguns Parts",relief=RIDGE,bd=3,width=13,font=("cooper black",12),bg="khaki",cursor="hand2",\
                              command= lambda:self.destroy_then_go(self.shot_pt.display_shotguns_parts,main_display))
        shotgun_button.place(x=180,y=10)
        rifle_button=Button(options_frame,text="Rifles Parts",relief=RIDGE,bd=3,width=13,font=("cooper black",12),bg="khaki",cursor="hand2",\
                              command= lambda:self.destroy_then_go(self.rif_pt.display_rifles_parts,main_display))
        rifle_button.place(x=350,y=10)
        self.parts_button.config(command= lambda:self.remove_parts_options(options_frame))
    def admin_main(self):
        self.guest()
        self.main_frame=Frame(root,bg="silver",width=900,height=560,relief=SOLID,bd=5)
        self.main_frame.place(x=100,y=250)
        self.admin_lab=Label(self.main_frame,text="ADMIN DISPLAY",relief=GROOVE,bd=5,font=("Bahnschrift SemiBold",13))
        self.admin_lab.place(x=10,y=10)

        self.firearms_button=Button(self.main_frame,text="FIREARMS",font=("Gill Sans Ultra Bold",15),bg="silver",cursor="hand2",\
                                    command= lambda:self.firearms_options(self.admin_main,self.admin_var.button_logout),relief=RAISED,bd=3)
        self.firearms_button.place(x=350,y=30)
        self.ammo_button=Button(self.main_frame,text="AMMUNITIONS",font=("Gill Sans Ultra Bold",15),bg="silver",cursor="hand2",\
                                command= lambda:self.ammo_options(self.admin_main,self.admin_var.button_logout),relief=RAISED,bd=3)
        self.ammo_button.place(x=330,y=155)
        self.magazine_button=Button(self.main_frame,text="MAGAZINES",font=("Gill Sans Ultra Bold",15),bg="silver",cursor="hand2",\
                                    command= lambda:self.magazine_options(self.admin_main,self.admin_var.button_logout),relief=RAISED,bd=3)
        self.magazine_button.place(x=340,y=275)
        self.parts_button=Button(self.main_frame,text="PARTS",font=("Gill Sans Ultra Bold",15),bg="silver",cursor="hand2",\
                                 command= lambda:self.parts_options(self.admin_main,self.admin_var.button_logout),relief=RAISED,bd=3)
        self.parts_button.place(x=360,y=395)

        self.clientinfo_button=Button(root,text="CLIENTS",relief=RAISED,bd=12,width=14,bg="cyan",cursor="hand2",\
                                    command=lambda:self.destroy_then_info(self.client_var.display_all,self.admin_main,self.admin_var.button_logout))
        self.clientinfo_button.place(x=1000,y=400)
        self.admininfo_button=Button(root,text="ADMINS",relief=RAISED,bd=12,width=14,bg="cyan",cursor="hand2",\
                                    command=lambda:self.destroy_then_info(self.admin_var.display_all,self.admin_main,self.admin_var.button_logout))
        self.admininfo_button.place(x=1000,y=600)
        
        self.loggedin_admin_button=Button(root,text=login_name,relief=GROOVE,bd=4,bg="royal blue",cursor="hand2",font=("times",14,"bold"),\
                                          command=lambda:self.destroy_then_info(self.admin_var.own_details,self.admin_main,self.admin_var.button_logout))
        self.loggedin_admin_button.place(x=1200,y=120)
        
        self.admin_var.logout_button(self.main_frame,self.normal_main,self.main_title,self.clientinfo_button,self.admininfo_button,\
                                     self.loggedin_admin_button)
        
        
    def normal_main(self):
        self.guest()
        self.main_frame=Frame(root,bg="silver",width=900,height=560,relief=SOLID,bd=5)
        self.main_frame.place(x=100,y=250)
        self.user_lab=Label(self.main_frame,text="USER DISPLAY-->",relief=GROOVE,bd=5,font=("Bahnschrift SemiBold",10))
        self.user_lab.place(x=10,y=10)
        self.firearms_button=Button(self.main_frame,text="FIREARMS",font=("Gill Sans Ultra Bold",15),bg="silver",cursor="hand2",\
                                    command= lambda:self.firearms_options(self.normal_main,self.admin_var.button_login),relief=RAISED,bd=3)
        self.firearms_button.place(x=350,y=30)
        self.ammo_button=Button(self.main_frame,text="AMMUNITIONS",font=("Gill Sans Ultra Bold",15),bg="silver",cursor="hand2",\
                                command= lambda:self.ammo_options(self.normal_main,self.admin_var.button_login),relief=RAISED,bd=3)
        self.ammo_button.place(x=330,y=155)
        self.magazine_button=Button(self.main_frame,text="MAGAZINES",font=("Gill Sans Ultra Bold",15),bg="silver",cursor="hand2",\
                                    command= lambda:self.magazine_options(self.normal_main,self.admin_var.button_login),relief=RAISED,bd=3)
        self.magazine_button.place(x=340,y=275)
        self.parts_button=Button(self.main_frame,text="PARTS",font=("Gill Sans Ultra Bold",15),bg="silver",cursor="hand2",\
                                 command= lambda:self.parts_options(self.normal_main,self.admin_var.button_login),relief=RAISED,bd=3)
        self.parts_button.place(x=360,y=395)
        self.cardlist_button=Button(self.main_frame,text="VIEW CARDLIST",relief=RAISED,bd=12,width=14,bg="slate grey",cursor="hand2",\
                                    command=lambda:self.destroy_then_cardlist(self.client_var.cardlist,self.normal_main,self.admin_var.button_login))
        self.cardlist_button.place(x=750,y=10)
        self.admin_var.login_button(self.main_frame,self.main_title,self.admin_main,self.normal_main)
'''----------------------------------------------------END OF MAIN CLASS SR ARMS----------------------------------------------------------'''

class Title_display:
    def check_signin(self,name,passcode,frame_login):
        if name.get() == "Saim" and passcode.get() == "saim786":
            frame_login.destroy()
            main=SR_arms()
            main.normal_main()
        else:
            ms.showwarning("Sign In Denied","Invalid Owner Data")
    def title_start(self):
        frame_login=Frame(root,bg='blue',width=1400,height=800)
        frame_login.place(x=0,y=0)
        back=PhotoImage(file="ned gate 2.gif")
        back_label=Label(frame_login,image=back)
        back_label.image=back
        back_label.place(x=0,y=0)
        pic=PhotoImage(file="saim.gif")
        pic_label=Label(frame_login,image=pic,bd=9,relief=RIDGE)
        pic_label.image=pic
        pic_label.place(x=300,y=330)
        logo=PhotoImage(file="ned logo 2.gif")
        logo_label=Label(frame_login,image=logo,bd=8,relief=RIDGE)
        logo_label.image=logo
        logo_label.place(x=1230,y=650)
        title_label=Label(frame_login,text="SIGN IN TO START THE PROJECT",font=("Helvetica",16,"bold","italic"),bg="light blue",bd=2,relief=SOLID)
        title_label.place(x=650,y=330)
        signin_nlabel=Label(frame_login,text="Name: ",font=("Courier",10,"normal"),relief=RAISED,bd=5)
        signin_nlabel.place(x=600,y=380)
        signin_plabel=Label(frame_login,text="PassCode: ",font=("Courier",10,"normal"),relief=RAISED,bd=5)
        signin_plabel.place(x=600,y=420)
        signin_name=Entry(frame_login,relief=RIDGE,bd=2)
        signin_name.place(x=670,y=380)
        signin_pass=Entry(frame_login,show="*",relief=RIDGE,bd=2)
        signin_pass.place(x=670,y=420)
        signin_name.focus_set()
        signin_button=Button(frame_login,text="SIGN IN",cursor="hand2",command= lambda:self.check_signin(signin_name,signin_pass,frame_login),relief=RAISED,bd=7)
        signin_button.place(x=700,y=460)
if __name__ == "__main__":
    title=Title_display()
    title.title_start()
    #main=SR_arms()
    #main.normal_main()
    root.mainloop()
