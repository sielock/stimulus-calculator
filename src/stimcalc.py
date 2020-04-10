from flask import Flask, render_template, request, redirect, url_for, session
import math

app = Flask(__name__)
app.secret_key ="test"

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
    return 500 * children

#home page
@app.route("/")
def home():
    return render_template("index.html")

#page that checks if user clears the basic eligibility requirements
@app.route("/eligibility", methods=["POST", "GET"])
def eligibility():
    if request.method == "POST":
        citizen = request.form["citizen"]
        dependent = request.form["UDep"]

        if citizen == "Yes" and dependent == "No":
            return redirect(url_for("calculator"))
        else:
            return redirect(url_for("denied"))

    else:
        return render_template("eligibility.html")

#page that takes in the user input for determining check amount
@app.route("/calculator", methods=["POST", "GET"])
def calculator():
    if request.method == "POST":
        income = request.form["income"]
        children = request.form["deps"]
        status = request.form["status"]

        chkamt = amount(income, status, childBoost(children))

        session["income"] = income
        session["children"] = children
        session["status"] = status
        session["amount"] = chkamt


        return redirect(url_for("results", amount = chkamt))
    else:
        return render_template("calculator.html")

#page that returns check results based on user input
@app.route("/results")
def results():
    if "amount" in session:
        inc = session["income"]
        amt = session["amount"]
        kids = session["children"]
        stat = session["status"]

        return render_template("results.html", income = inc, amount = amt, children = kids, status = stat)
    else:
        return redirect(url_for("calculator"))

#page for user that doesn't meet basic eligibility requirements
@app.route("/denied")
def denied():
    return render_template("denied.html")
        
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')