import subprocess as sp
import pymysql
import pymysql.cursors
import random
import getpass

def newPurchase():
    global cur
    print("Enter new purchase details: ")
    row = {}
    cur.execute("SELECT MAX(Purchase_id) FROM Purchase")
    dic = cur.fetchall()
    if dic[0]['MAX(Purchase_id)'] == None:
        row["Purchase_id"] = '1'
    else:
        row["Purchase_id"] = str(int(dic[0]['MAX(Purchase_id)']) + 1)
    row["Item_id"] = input("Item ID: ")
    row["Buyer_id"] = input("Buyer ID: ")
    cur.execute("SELECT COUNT(*) FROM Driver")
    dic = cur.fetchall()
    row["Driver_id"] = str((int(row["Purchase_id"]) - 1) % dic[0]['COUNT(*)'] + 1)
    row["Time_of_purchase"] = input("Time of purchase: ") # TO BE CORRECTED
    cur.execute("INSERT INTO Purchase(Purchase_id, Time_of_delivery, Buyer_id, Time_of_purchase, Driver_id) VALUES('" + row["Purchase_id"] + "', NULL, '" + row["Buyer_id"] + "', '" + row["Time_of_purchase"] + "', '" + row["Driver_id"] + "')")
    con.commit()
    return

def newItem():
    global cur
    print("Enter item information: ")
    row = {}
    cur.execute("SELECT MAX(Item_id) FROM Item")
    dic = cur.fetchall()
    if dic[0]['MAX(Item_id)'] == None:
        row["Item_id"] = '1'
    else:
        row["Item_id"] = str(int(dic[0]['MAX(Item_id)']) + 1)
    row["Item_name"] = input("Item name: ")
    row["Cat_name"] = input("Category name: ")
    cur.execute("SELECT Cat_id FROM Category WHERE Cat_name = '" + row["Cat_name"] +"'")
    dic = cur.fetchall()
    row["Cat_id"] = dic[0]['Cat_id']
    cur.execute("INSERT INTO Item(Item_id,Item_name,Cat_id) VALUES('" + row["Item_id"] + "', '" + row["Item_name"] + "', '" + row["Cat_id"] + "')")
    row["Seller_id"] = input("Seller id: ")
    row["Item_cost"] = input("Item cost: ")
    print(row)
    cur.execute("INSERT INTO ItemCost(Item_id,Seller_id,Item_cost) VALUES('" + row["Item_id"] + "', '" + row["Seller_id"] + "', '" + row["Item_cost"] + "')")
    row["Item_Sale_Price"] = str(int(float(row["Item_cost"]) * (1.05 + random.random() / 10)))
    print(row)
    cur.execute("INSERT INTO ItemSellPrice(Item_id,Item_sale_price) VALUES('" + row["Item_id"] + "', '" + row["Item_Sale_Price"] + "')")
    con.commit()
    return

def updateSellerInfo():
    global cur
    print("Update seller information: ")
    row = {}
    row["Seller_id"] = input("Enter Seller id: ")
    row["Seller_contact"] = input("Enter Seller contact: ")
    cur.execute("UPDATE SellerContacts SET Seller_contact = " + row["Seller_contact"] + " WHERE Seller_id = " + row["Seller_id"])
    row["Seller_address"] = input("Enter Seller address: ")
    cur.execute("UPDATE Seller SET Seller_address = " + row["Seller_address"] + " WHERE Seller_id = " + row["Seller_id"])
    con.commit()
    return

def deliveryComplete():
    global cur
    print("Enter delivery details: ")
    row = {}
    row["Purchase_id"] = input("Purchase id: ")
    row["Item_id"] = cur.execute("SELECT Item_id FROM Payment WHERE Purchase_id = " + row["Purchase_id"])
    row["Sale_Price"] = cur.execute("SELECT Sale_price FROM ItemSellPrice WHERE ItemSellPrice.Item_id = " + row["Item_id"])
    row["Item_cost"] = cur.execute("SELECT Item_cost FROM ItemCost WHERE ItemCost.Item_id = " + row["Item_id"])
    row["Profit"] = str(int(row["Sale_Price"]) - int(row["Item_cost"]))
    cur.execute("INSERT INTO Payment('Purchase_id','Profit','Item_id') values ('" + row["Purchase_id"] + "', '" + row["Profit"] + "', '" + row["Item_id"] + "')")
    # update time_of_delivery
    row["Delivery_time"] = str(float(cur.execute("SELECT Time_of_delivery FROM Purchase")) - float(cur.execute("SELECT Time_of_purchase FROM Purchase")))
    row["Driver_id"] = cur.execute("SELECT Driver_id FROM Purchase WHERE Purchase_id = " + row["Purchase_id"])
    cur.execute("INSERT INTO Delivery('Purchase_id','Driver_id','Delivery_time') values ('" + row["Purchase_id"] + "', '" + row["Driver_id"] + "', '" + row["Delivery_time"] + "')")
    con.commit()
    return

def updateDriverInfo():
    global cur
    print("Update driver information: ")
    row = {}
    row["Driver_id"] = input("Enter Driver id:")
    row["Driver_contact"] = input("Enter Driver contact:")
    cur.execute("UPDATE DriverContact SET Driver_contact = " + row["Driver_contact"] + " WHERE Driver_id = " + row["Driver_id"])
    con.commit()
    return

def itemSold():
    global cur
    print("Enter item information: ")
    row = {}
    row["Item_id"] = input("Enter the id of the sold item: ")
    cur.execute("DELETE FROM Item where Item_id = " + row["Item_id"])
    cur.execute("DELETE FROM ItemCost where Item_id = " + row["Item_id"])
    cur.execute("DELETE FROM ItemSellPrice where Item_id = " + row["Item_id"])
    con.commit()
    return

def calculateAverageDeliveryTime():
    global cur
    row = {}
    row["Driver_id"] = input("Driver id: ")
    cur.execute("SELECT AVG(Delivery_time) FROM ItemPayment GROUP BY Driver_id HAVING Driver_id = " + row["Driver_id"])
    con.commit()
    return

def calculateTotalProfit():
    global cur
    cur.execute("SELECT SUM(Profit) FROM Payment")
    con.commit()
    return

optionFunctionMapping = {
        1: newPurchase,
        2: newItem,
        3: updateSellerInfo,
        4: deliveryComplete,
        5: updateDriverInfo,
        6: itemSold,
        7: calculateAverageDeliveryTime,
        8: calculateTotalProfit,
        }

while(1):
    tmp = sp.call('clear', shell = True)
    #username = input("Username: ")
    #password = getpass.getpass("Password: ")

    try:
        con = pymysql.connect(host = 'localhost',
                user = 'root',
                password = 'test',
                db = 'Online_Shopping',
                cursorclass = pymysql.cursors.DictCursor)
        with con:
            cur = con.cursor()
            while(1):
                tmp = sp.call('clear', shell = True)
                print("1. Add new Purchase")
                print("2. Add new item")
                print("3. Update Seller Info")
                print("4. Update Time of Delivery")
                print("5. Update Driver Info")
                print("6. Delete Item Sold")
                print("7. Calculate Average Delivery Time")
                print("8. Calculate Total Profit")
                print("9. Logout")
                c = int(input("Enter choice> "))
                tmp = sp.call('clear', shell = True)
                if c == 9:
                    break
                else:
                    optionFunctionMapping[c]()

    except:
        tmp = sp.call('clear', shell = True)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
