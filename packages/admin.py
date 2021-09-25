import mysql.connector
import grafics
import command_admin as command

db = mysql.connector.connect(
    host="localhost",
    user="Putin",
    password="sar0403nya",
    database="Trains"
)
cur=db.cursor()

def add():
    n=0
    while True:
        n = int(grafics.read("How many trains do you want to add:"))
        if n>0:
            break
        else:
            grafics.push("Enter a proper number.")
    trains=grafics.readRow(["Name","Cost","Source","Destination","Year"],n)
    grafics.showRow(trains)
    while True:
        c=grafics.read("Confirm addition (y/n):")
        if c.lower() in "y":
            break
        if c.lower() in "n":
            grafics.push("Addition aborted.")
            return
        else:
            grafics.push("Enter proper option.")
    for ticket in trains:
        query=f"INSERT INTO available (name, cost, source, destination, yr) VALUES ('{ticket['Name']}', {int(ticket['Cost'])}, '{ticket['Source']}', '{ticket['Destination']}', {ticket['Year']});"
        cur.execute(query)
        db.commit()
    grafics.push(f"{len(trains)} Trains added.")
    while True:
        c=grafics.read("Want to add more trains? (y/n):")
        if c.lower() in "y":
            add()
            break
        if c.lower() in "n":
            return
        else:
            grafics.push("Enter proper option.")

def listAll():
    grafics.push("Here are all the Trains:")
    cur.execute("SELECT * FROM available ORDER BY id")
    grafics.showRow([{"Name":i[0],"Cost":str(i[1]),"Source":i[2],"Destination":i[3],"Year":str(i[4])}
                     for i in cur.fetchall()])

def cancel():
    cur.execute("SELECT * FROM available ORDER BY id")
    x = cur.fetchall()
    if len(x) == 0:
        grafics.push("There are no trains.")
        while True:
            c = grafics.read("Want to add some trains? (y/n):")
            if c.lower() in "y":
                add()
                break
            if c.lower() in "n":
                return
            else:
                grafics.push("Enter proper option.")
    trains = command.number(
        [{"Name": i[0], "Cost": str(i[1]), "Source": i[2], "Destination": i[3], "Year": str(i[4])} for i in x])
    ids = command.number([{"id": i[5]} for i in x])
    grafics.push("Select the train you want to edit: ")
    grafics.showRow(trains)
    t = 0
    while True:
        t = int(grafics.read("Enter the Train Number you want to cancel:"))
        if 0 < t <= len(trains):
            break
        else:
            grafics.push("Not a proper Train.")
    while True:
        c=grafics.read(f"Confirm removal of {trains[t-1]['Name']} (y/n):")
        if c.lower() in "y":
            break
        if c.lower() in "n":
            grafics.push("Removal aborted.")
            return
        else:
            grafics.push("Enter proper option.")
    cur.execute(f"DELETE FROM available WHERE id={ids[t-1]['id']}")
    db.commit()
    grafics.push(f"{trains[t - 1]['Name']} Removed.")
    while True:
        c=grafics.read("Want to remove more trains? (y/n):")
        if c.lower() in "y":
            cancel()
            break
        if c.lower() in "n":
            return
        else:
            grafics.push("Enter proper option.")

def mod():
    cur.execute("SELECT * FROM available ORDER BY id")
    x = cur.fetchall()
    if len(x)==0:
        grafics.push("There are no trains.")
        while True:
            c = grafics.read("Want to add some trains? (y/n):")
            if c.lower() in "y":
                add()
                break
            if c.lower() in "n":
                return
            else:
                grafics.push("Enter proper option.")
    trains = command.number(
        [{"Name": i[0], "Cost": str(i[1]), "Source": i[2], "Destination": i[3], "Year": str(i[4])} for i in x])
    ids = command.number([{"id": i[5]} for i in x])
    grafics.push("Select the train you want to edit: ")
    grafics.showRow(trains)
    t = 0
    while True:
        t = int(grafics.read("Enter the Train Number you want to edit:"))
        if 0 < t <= len(trains):
            break
        else:
            grafics.push("Not a proper Train.")
    grafics.push("Enter new details:")
    train = grafics.readRow(["Name", "Cost", "Source", "Destination", "Year"], 1)
    grafics.showRow(train)
    while True:
        c = grafics.read(f"Confirm edit of {trains[t - 1]['Name']} (y/n):")
        if c.lower() in "y":
            break
        if c.lower() in "n":
            grafics.push("Edit aborted.")
            return
        else:
            grafics.push("Enter proper option.")
    cur.execute(f"UPDATE available SET name='{train[0]['Name']}', cost={int(train[0]['Cost'])}, source='{train[0]['Source']}', destination='{train[0]['Destination']}', yr={int(train[0]['Year'])} WHERE id={ids[t - 1]['id']}")
    db.commit()
    grafics.push(f"{trains[t - 1]['Name']} Edited.")
    while True:
        c = grafics.read("Want to edit more trains? (y/n):")
        if c.lower() in "y":
            cancel()
            break
        if c.lower() in "n":
            return
        else:
            grafics.push("Enter proper option.")

def age():
    grafics.push("Here are all the ages of all the Trains:")
    cur.execute("SELECT * FROM available ORDER BY id")
    trains=command.age([{"Name": i[0], "Year": str(i[4])} for i in cur.fetchall()])
    grafics.showRow(trains)

def main():
    while True:
        welcome=[{"Welcome": "This is MINC","Need help": "Just Type out your desired command"},
                 {"1": "Add new trains","2": "Remove trains","3": "Check age of trains","4":"Change train details", "5": "Exit"}]
        grafics.showRow(welcome)
        com=command.find_command(grafics.read("What do you want to do: "))
        if com=="add":
            add()
        elif com=="remove":
            cancel()
        elif com=="listAll":
            listAll()
        elif com=="mod":
            mod()
        elif com=="age":
            age()
        elif com=="exit":
            grafics.push("Taking you back to home screen.")
            import MINC
        else:
            grafics.push("Please enter a proper command")