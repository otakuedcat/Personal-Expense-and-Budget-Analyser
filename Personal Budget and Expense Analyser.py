import csv # Import the CSV module for reading and writing CSV files
records=[]
try:  # Try to read existing data
    with open("expense.csv","r",newline="") as f:
        records=list(csv.DictReader(f))
except FileNotFoundError: # If file doesn't exist, we just continue with an empty list
    pass

def save(): # Save the records to a CSV file
    f=open("expense.csv","w",newline="")
    fields=["date","type","category","amount"]
    writer=csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(records)

def leap(y): # Check if a year is a leap year
    return y%4==0 and (y%100!=0 or y%400==0)

def days_in_month(y,m): # Return the number of days in a given month of a given year
    if m==2:
        return 29 if leap(y)else 28
    return 30 if m in (4,6,9,11) else 31
    
def get_valid_date(): # Get a valid date from the user
    while True:
        d=input("Enter date(YYYY-MM-DD): ").strip()
        parts=d.split('-')
        y,m,day=int(parts[0]),int(parts[1]),int(parts[2])
        if not 1<=m<=12 or not 1<=day<=days_in_month(y,m):
            print("invalid date")
            continue
        elif (y,m,day)>(2026,11,25):
            print("Future Date not allowed")
            continue
        return d
while True: # Main loop for user interaction
    print("\n1 Add Income \n2 Add Expense")
    print("3 View Summary \n4 Analyze Spending")
    print("5 Budget Comparison \n6 Exit")
    ch=input("Enter Choice:")
    if ch in ["1","2"]: # Add income or expense
        date = get_valid_date()
        category = input("Enter category:").capitalize()
        amount = float(input("Enter amount:"))
        records.append({"date": date,"type": "Income" if ch=="1" else "Expense","category": category,"amount": amount})
        save()
        print("Record added!")
    elif ch=="3": # View summary of income and expenses for a given month
        D=input("Enter date(YYYY-MM)")
        income=0.0
        expense=0.0
        for i in records: # Loop through all records
            if i['date'].startswith(D):
                if i['type'] == "Income":
                    income+=float(i['amount'])
                if i['type'] == "Expense":
                    expense+=float(i['amount'])
        print("Income:", income, "Expense:", expense)
        print("Balance:", income - expense)

    elif ch == "4": # Analyze spending for a given month
        month = input("Enter month (YYYY-MM): ")
        total = 0
        categories = {}

        for r in records: # Loop through all records
            if r["type"] == "Expense" and r["date"].startswith(month):
                total += float(r["amount"])
                c = r["category"]
                categories[c] = categories.get(c, 0) + float(r["amount"])

        print("Total spending:", total)
        print("Category spending:", categories)
        if categories:
            print("Highest spending:", max(categories, key=categories.get))

    elif ch == "5": # Compare spending against a budget for a given month
        month = input("Enter month (YYYY-MM): ")
        budget = float(input("Enter budget: "))
        spent = sum(float(r["amount"]) for r in records
                    if r["type"] == "Expense"
                    and r["date"].startswith(month))

        print("Spent:", spent, "Budget:", budget)
        if spent >= budget * 0.8:
            print("Alert: Budget 80% used or exceeded!")
        else:
            print("You are within budget.")

    elif ch == "6": # Exit the program
        save()
        print("Data saved. Goodbye!")
        break

    else: # Handle invalid choices
        print("Invalid choice!")
