import mysql.connector
from packages import grafics
from packages import command

# Reads the database credentials taken during initialization.
f=open("packages/data.txt","r")
s=f.readlines()[0]
user=s.split('`')[1]
pas=s.split('`')[2]
f.close()

# Makes the necessary database instances.
db = mysql.connector.connect(
    host="localhost",
    user=user,
    password=pas,
    database="Tickets"
)
cur=db.cursor()
trainsdb= mysql.connector.connect(
    host="localhost",
    user=user,
    password=pas,
    database="Trains"
)
cur_trains=trainsdb.cursor()

def book():
    destination=grafics.read("Where do you want to go?")
    source=grafics.read("What is your source location?")
    cur_trains.execute(f"SELECT name, cost FROM available WHERE source LIKE '{source}%' AND destination LIKE '{destination}%'")
    # Takes all the trains and numbers them 1,2,3..., for the user to choose
    trains=command.number([{"Name":t[0],"Cost":str(t[1])} for t in cur_trains.fetchall()])
    if len(trains) == 0:
        grafics.push("No Trains Available.")
        return
    grafics.showRow(trains)
    t=0
    while True:
        t=int(grafics.read("Which Train do you want to book (Enter Train No.) :"))
        if 0<t<=len(trains):
            break
        else:
            grafics.push("Not a proper Train.")
    n=0
    while True:
        n = int(grafics.read("How many tickets do you want to book:"))
        if n>0:
            break
        else:
            grafics.push("Enter a proper number.")
    date = ""
    # Validates the date.
    while True:
        date = grafics.read("Enter Date of Journey(DD/MM/YYYY)")
        if len(date) == 10 and date[2] == date[5] == "/":
            if int(date[3:5:]) < 13:
                if date[3:5:] in "02" and int(date[:2:]) < 29:
                    break
                elif date[3:5:] in "01 03 05 07 08 10 12" and int(date[:2:]) < 32:
                    break
                elif date[3:5:] in "04 06 09 11" and int(date[:2:]) < 31:
                    break
                else:
                    print("| Not a valid date. Please try again.")
            else:
                print("| Not a valid date. Please try again.")
        else:
            print("| Not a valid date. Please try again.")
    # Takes the required inputs
    tickets=grafics.readRow(["Name","Age","Gender(M/F)","Aadhar number"],n)
    grafics.showRow(tickets)
    while True:
        c=grafics.read("Confirm tickets (y/n):")
        if c.lower() in "y":
            break
        if c.lower() in "n":
            grafics.push("Booking aborted.")
            return
        else:
            grafics.push("Enter proper option.")
    # Make the queries to write the ticket details to the database.
    for ticket in tickets:
        query=f"INSERT INTO booked (name, age, gender, adh, date) VALUES ('{ticket['Name']}', {int(ticket['Age'])}, '{ticket['Gender(M/F)']}', {ticket['Aadhar number']}, '{date}');"
        cur.execute(query)
        db.commit()
    grafics.push(f"{len(tickets)} tickets booked.")
    while True:
        c=grafics.read("Want to book more tickets? (y/n):")
        if c.lower() in "y":
            book()
            break
        if c.lower() in "n":
            return
        else:
            grafics.push("Enter proper option.")

def listAll():
    cur.execute("SELECT * FROM booked ORDER BY date")
    # Takes the data and reforms them to a box-printable form.
    x=[{"Name":i[0],"Age":str(i[1]),"Gender":i[2],"Aadhar No.":str(i[3]),"Date":i[5]}
                     for i in cur.fetchall()]
    if len(x)==0:
        grafics.push("You do not have any tickets.")
        while True:
            c = grafics.read("Want to book some tickets? (y/n):")
            if c.lower() in "y":
                book()
                break
            if c.lower() in "n":
                return
            else:
                grafics.push("Enter proper option.")
    grafics.push("Here are all your Tickets:")
    grafics.showRow(x)

def cancel():
    cur.execute("SELECT * FROM booked ORDER BY id")
    x=cur.fetchall()
    if len(x)==0:
        grafics.push("You do not have any tickets.")
        while True:
            c = grafics.read("Want to book some tickets? (y/n):")
            if c.lower() in "y":
                book()
                break
            if c.lower() in "n":
                return
            else:
                grafics.push("Enter proper option.")
    tickets=command.number([{"Name": i[0], "Age": str(i[1]), "Gender": i[2], "Aadhar No.": str(i[3]), "Date": i[5]} for i in x])
    # Stores the ids in a separate list as ids are not printed, but will be needed later to address the specific ticket.
    ids=command.number([{"id":i[4]} for i in x])
    grafics.push("Select the ticket you want to cancel: ")
    grafics.showRow(tickets)
    t = 0
    while True:
        t = int(grafics.read("Enter the Ticket Number you want to cancel:"))
        if 0 < t <= len(tickets):
            break
        else:
            grafics.push("Not a proper Ticket.")
    while True:
        c=grafics.read(f"Confirm cancel of {tickets[t-1]['Name']}'s ticket (y/n):")
        if c.lower() in "y":
            break
        if c.lower() in "n":
            grafics.push("Cancelling aborted.")
            return
        else:
            grafics.push("Enter proper option.")
    # Makes required queries.
    cur.execute(f"DELETE FROM booked WHERE id={ids[t-1]['id']}")
    db.commit()
    grafics.push(f"{tickets[t-1]['Name']}'s ticket Cancelled.")
    while True:
        c=grafics.read("Want to cancel more tickets? (y/n):")
        if c.lower() in "y":
            cancel()
            break
        if c.lower() in "n":
            return
        else:
            grafics.push("Enter proper option.")

def main():
    while True:
        welcome=[{"Welcome": "This is MINC","Need help": "Just Type out your desired command"},
                 {"1": "Book tickets","2": "Cancel tickets","3": "See all booked tickets","4": "Exit"}]
        grafics.showRow(welcome)
        com=command.find_command(grafics.read("What do you want to do: "))
        if com=="booking":
            book()
        elif com=="canceling":
            cancel()
        elif com=="listAll":
            listAll()
        elif com=="exit":
            grafics.push("Taking you back to home screen.")
            import MINC
        else:
            grafics.push("Please enter a proper command")