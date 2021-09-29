# This file handles all IO and graphics.
# Interface methods:
# read(detail) ; readRow(details, no) ;
# show(detail,value) ; showRow(details) ; push(detail) ;

'''
Input restriction methods have been baked in. So use this module for IO.
Restriction Methods like : Age is numerical, Name will be full name, Checking of valid date, Proper gender, etc.

readRow(["Name", "Age","Gender"],4) : will take the input in the lost 4 times.
read("Enter age:") : same as input("Enter age:"), but structured.

showRow(details) : Prints the details in boxed form.
show(detail, value): Prints a single line in a box form.
push(detail) : same as print(detail), but structured.
'''

def find_needed_space(details):
    # Finds the space needed to fit all the data in the list in a proper box type structure.
    spaces=[]
    space=0
    for data in details:
        for line in data:
            if len(str(line) + str(data[line]) + " : ") > space:
                space = len(str(line) + str(data[line]) + " : ")
        spaces.append(space)
    return space

def throwOutput(details):
    # Details is the list of dictionaries containing all data that needs to be displayed.
    # Displays all the items in the list as a structured box form.
    space = find_needed_space(details) + 5
    number=len(details)
    s,m = "",""
    for a in range(space + 1):
        s += "-"
        m+="="
    print(s)
    cnt=0
    for data in details:
        for line in data:
            s1 = "| " + line + " : " + data[line]
            for a in range(space - len(s1)):
                s1 += " "
            s1 += "|"
            print(s1)
        cnt+=1
        if cnt!=number:
            print(m)
    print(s)

def getInput(details):
    # Details is the list of dictionaries containing all data that needs input.
    # Takes input of all the items in the list as a structured box form and returns a direct box-printable list.
    space = find_needed_space(details) + 30
    number = len(details)
    s, m = "", ""
    for a in range(space + 1):
        s += "-"
        m += "="
    print(s)
    cnt = 0
    for data in details:
        for line in data:
            s1 = "| " + line + " : "
            if line.lower() in "cost per ticket year age aadhar number number of people enter train number enter ticket number":
                while True:
                    details[cnt][line] = input(s1).strip()
                    if details[cnt][line].isnumeric():
                        break
                    else:
                        print(f"| Not A Valid {line}. Please Enter Again")
            elif line.lower() in "name":
                while True:
                    details[cnt][line] = input(s1).strip()
                    if " " not in details[cnt][line]:
                        print(f"| Please Enter Your Full {line}.")
                    else:
                        break
            elif line.lower() in "gender(m/f)":
                while True:
                    details[cnt][line] = input(s1).strip().lower()
                    if details[cnt][line] not in "male female":
                        print(f"| Please Enter A Valid {line}.")
                    else:
                        break
            elif line.lower() in "food preference(veg/non-veg)":
                while True:
                    details[cnt][line] = input(s1).strip().lower()
                    if details[cnt][line] not in "veg non-veg":
                        print(f"| Please Enter A Valid {line}.")
                    else:
                        break
            elif line.lower() in "birth preference(upper/lower/middle)":
                while True:
                    details[cnt][line] = input(s1).strip().lower()
                    if details[cnt][line] not in "lower middle upper":
                        print(f"| Please Enter A Valid {line}.")
                    else:
                        break
            elif line.lower() in "is that all?(y/n) only one available. choose this one?(y,n)":
                while True:
                    details[cnt][line] = input(s1).strip().lower()
                    if details[cnt][line] not in "y n":
                        print(f"| Please Enter A Valid {line}.")
                    else:
                        break
            else:
                details[cnt][line] = input(s1).strip()
        cnt += 1
        if cnt != number:
            print(m)
    print(s)
    return details

def read(detail):
    # detail what u want to input
    det=[{detail: ""}]
    return getInput(det)[0][detail]

def readRow(detail,no):
    # detail is a list of stuff u need multiple times
    det={}
    details=[]
    for i in detail:
        det[i] = ""
    for _ in range(no):
        details.append(det.copy())
    i=getInput(details)
    return i

def push(data):
    print("|",data)

def show(detail,value):
    det=[{detail:value}]
    throwOutput(det)

def showRow(details):
    throwOutput(details)

# showRow(readRow(["Name","Year","Month"],2))
# print(readRow(["Name","Year","Month"],2))
# show("Name",read("Name"))
# d=read([{"Train Name":"","year":"","cost":""},{"Train Name":"","year":""},{"Train Name":"","year":""}])
# d1=getInput([{"Name":"","Age":"","Gender":"","Aadhar number":""},{"Name":"","Age":"","Gender":"","Aadhar number":""}])
# showRow(d1)
# d1=getInput([{'Name': '', 'Year': '', 'Month': ''}, {'Name': '', 'Year': '', 'Month': ''}])
# showRow(d1)
# print(getInput([{'Name': '', 'Year': '', 'Month': ''}, {'Name': '', 'Year': '', 'Month': ''}]))