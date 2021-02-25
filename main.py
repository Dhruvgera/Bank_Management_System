# Bank Management System by Dhruv Gera XII Sci A 5

import pymysql
import pickle

# Main menu function
def entry_manager():
    print("The available options are: ")
    print("1. Add entry for a new customer")
    print("2. Delete entries for a customer")
    print("3. Edit entries for an existing customer")
    print("4. Create Backup")
    print("5. Fetch entries")
    print("6. Transaction")
    print("7. Exit")
    option_selector=int(input("Which option do you want? (1-7)"))
    if option_selector==1:
        customer_register()
    elif option_selector==2:
        customer_remover()
    elif option_selector==3:
        customer_editor()
    elif option_selector==4:
        backup_creator()
    elif option_selector==5:
        fetch_entries()
    elif option_selector==6:
        transaction_placer()
    elif option_selector==7:
        exit()
    else:
        print("Invalid input")
        entry_manager()
        
# Making connection with SQL
conn=pymysql.connect(host="localhost",
                        user="root",
                        passwd="urpass",
                        db="bank_data")
cur=conn.cursor()
            
# Check if table exists, only then let user continue or create it
def table_checker():
    global tablename
    tablename=input("Enter the table name to use: ")
    try:
        rec_check="select * from "+tablename+";"
        cur.execute(rec_check)
        rec=cur.fetchall()
    except:
        table_optionals=input("Table doesn't exist, do you want to create a new one? \
                              (y/n)")
        if table_optionals=="y":
            table_creator="create table "+tablename+ \
            "(Name varchar(15) NOT NULL, Account_Type varchar(10) NOT NULL, \
            Registration_Number int(10) NOT NULL PRIMARY KEY, \
            Address varchar(100) NOT NULL, Bank_balance int(30) NOT NULL, Age int(3) \
            NOT NULL, Gender char(1) NOT NULL);"
            cur.execute(table_creator)
            conn.commit()
            print("Table has been created! Proceeding to entries!")
        else:
            exit()

# Create a new table for each customer and add their entries
def customer_table_gen(reg_no,balance):
    tablegen="create table "+reg_no+"_data (Balance int(30), Credit int(30), Debit \
    int(30), Date DATETIME);"
    cur.execute(tablegen)
    conn.commit()
    first_entry="insert into "+reg_no+"_data values("+balance+",NULL,NULL,NOW());"
    cur.execute(first_entry)
    conn.commit()
    
# Check table, if exists, continue, else go back
def table_existence_confirmer():
    global tablename2
    tablename2=input("Enter the table name to use: ")
    try:
        rec_check="select * from "+tablename2+";"
        cur.execute(rec_check)
        rec=cur.fetchall()
    except:
        table_optionals=input("Table doesn't exist")
        entry_manager()
            
# Add a new customer
def customer_register():
    table_checker()
    name=input("Enter name: ")
    acc_no=input("Enter account number: ")
    reg_no=input("Enter registration number: ")
    addrs=input("Enter address")
    balance=input("Enter bank balance: ")
    age=input("Enter age: ")
    gender=input("Enter gender(M/F/T): ")
    insert_statement="insert into "+tablename+" values(" \
    +"'"+name+"'"+','+acc_no+','+reg_no+','+"'"+addrs+"'"+','+balance+','+age+' \
    ,'+"'"+gender+"'"+");"
    cur.execute(insert_statement)
    conn.commit()
    customer_table_gen(reg_no,balance)
    entry_manager()
    
# Delete user from database
def customer_remover():
    table_existence_confirmer()
    reg_no=input("Enter registration number: ")
    confirmation=input("Do you want to proceed? (y/n)")
    if confirmation=="y":
        delete_statement="delete from "+tablename2+" where \
        Registration_Number="+reg_no+";"
        cur.execute(delete_statement)
        conn.commit()
        print("User has been removed from the database!")
        entry_manager()
    else:
        entry_manager()
    
# Edit details regarding a customer, except their balance and registeration number
def customer_editor():
    table_existence_confirmer()
    reg_no=input("Enter registration number: ")
    confirmation=input("Do you want to proceed? (y/n)")
    while confirmation=="y":
        edit_field_name=input("Enter the field name you want to edit: ")
        if edit_field_name=="Bank_Balance" or "Registration_Number":
            print("Sorry, you can't edit balance or Registeration Number, \
                  use transaction for balance updates")
        else:
            new_value=input("Enter the new value: ")
            value_replacer="update "+tablename+" set "+edit_field_name+"="+"'" \
            +new_value+"'"+" where Registration_Number="+reg_no+";"
            cur.execute(value_replacer)
            conn.commit()
        confirmation=input("Do you want to edit more values? (y/n)")
    entry_manager()
        
# Backup table data to a binary file
def backup_creator():
    tbname=input("Enter table name to backup: ")
    filename=input("Enter filename to backup the data to: ")
    backup_cmd="select * from "+tbname+";"
    cur.execute(backup_cmd)
    rec=cur.fetchall()
    for i in rec:
        with open(filename,'ab') as f:
            pickle.dump(i,f)
    print("Backup created!")
    entry_manager()
        
# Fetch entries of user data from a table
def fetch_entries():
    reg_no=input("Enter registration number of user: ")
    sorting_by=input("Enter the column on the basis of which to sort data: ")
    asc_desc=input("Enter whether you want the data to be in ascending or descending: ")
    col_name=input("Enter column names to fetch (Seperate names with commas): ")
    entry_finder_cmd="select "+col_name+" from "+reg_no+"_data order by "+sorting_by+" \
    "+asc_desc+";"
    cur.execute(entry_finder_cmd)
    rec=cur.fetchall()
    for i in rec:
        print(i)
    entry_manager()

# Add credit or debit
def transaction_placer():
    tablename=input("Enter main tablename: ")
    reg_no=input("Enter registration number of user: ")
    deb_or_cred=input("Enter whether you want to add Debit or Credit: ")
    if deb_or_cred=="Debit":
        amt=input("Enter amount to deduct: ")
        fetch_balance="select Balance from "+reg_no+"_data ORDER BY Date DESC LIMIT 1;"
        cur.execute(fetch_balance)
        rec=cur.fetchall()
        for i in rec:
            for j in i:
                print("Current amount: ",j)
        z=str(j-int(amt))
        print(type(z))
        debit_cmd="insert into "+reg_no+"_data values("+z+","+z+", NULL ,NOW());"
        cur.execute(debit_cmd)
        conn.commit()
        debit_main_table="update "+tablename+" set Bank_Balance="+z+" where \
        Registration_Number="+reg_no+";"
        cur.execute(debit_main_table)
        conn.commit()
    if deb_or_cred=="Credit":
        amt=input("Enter amount to add: ")
        fetch_balance="select Balance from "+reg_no+"_data ORDER BY Date DESC LIMIT 1;"
        cur.execute(fetch_balance)
        rec=cur.fetchall()
        for i in rec:
            for j in i:
                print("Current amount: ",j)
        z=str(j+int(amt))
        print(type(z))
        credit_cmd="insert into "+reg_no+"_data values("+z+", NULL,"+z+",NOW());"
        cur.execute(credit_cmd)
        conn.commit()
        credit_main_table="update "+tablename+" set Bank_Balance="+z+" where \
        Registration_Number="+reg_no+";"
        cur.execute(credit_main_table)
        conn.commit()
    entry_manager()
    
entry_manager()
