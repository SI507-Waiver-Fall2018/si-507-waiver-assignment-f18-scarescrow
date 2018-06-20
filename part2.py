# these should be the only imports you need
import sys
import sqlite3

# My full name is Sagnik Sinha Roy
# My UMich uniqname is sagniksr

# write your code here
# usage should be 
#  python3 part2.py customers
#  python3 part2.py employees
#  python3 part2.py orders cust=<customer id>
#  python3 part2.py orders emp=<employee last name>

DATABASE = "Northwind_small.sqlite"

if __name__ == "__main__":

    # First, connect to the DB and get a cursor

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Now parse arguments to see what output is required
    # Based on that perform appropriate query

    task = sys.argv[1]

    if task == "customers":

        print("ID\tCustomer Name")
        for row in cursor.execute("SELECT Id, ContactName FROM Customer"):
            print("{}\t{}".format(row[0], row[1]))

    elif task == "employees":

        print("ID\tEmployee Name")
        for row in cursor.execute("SELECT Id, LastName, FirstName FROM Employee"):
            print("{}\t{}".format(row[0], row[2] + " " + row[1]))

    elif task == "orders":

        print("Order dates")

        additional_parameter = sys.argv[2].split('=')
        condition = additional_parameter[0]
        value = additional_parameter[1]

        if condition == "cust":
            for row in cursor.execute("SELECT OrderDate FROM `Order` WHERE CustomerId=?", (value,)):
                print(row[0])

        elif condition == "emp":
            for row in cursor.execute("SELECT OrderDate From `Order` as O, Employee E WHERE E.LastName=? AND E.Id=O.EmployeeId", (value,)):
                print(row[0])

        else:
            pass

    else:
        pass

    cursor.close()
