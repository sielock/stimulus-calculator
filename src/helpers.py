#helper functions to determine stimulus check amount
def amount(income, status, kids):
    income = float(income)
    amt = 0

    if status == "Single" and income < 75000:
        amt = 1200 + kids
    elif status == "Single" and 75000 <= income < 99000 :
        amt = 1200 - abs((income - 75000)*0.05) + kids
    elif status == "Married" and income < 150000:
        amt = 2400 + kids
    elif status == "Married" and 150000 <= income <198000:
        amt = 2400 - abs((income - 150000)*0.05) + kids

    
    return round(amt, 2)

#calculates how much additional funding comes from eligible children
def childBoost(kids):
    children = float(kids)
    return 500 * kids
