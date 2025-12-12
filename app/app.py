from flask import Flask, request, render_template
import calc  # <-- THIS matches calc.py

app = Flask(__name__)

@app.route("/calculator", methods=["GET", "POST"])
def calculator_page():
    result = None
    error = None

    if request.method == "POST":
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])
        operator = request.form["operator"]

        try:
            if operator == "+":
                result = calc.add(num1, num2)
            elif operator == "-":
                result = calc.subtract(num1, num2)
            elif operator == "*":
                result = calc.multiply(num1, num2)
            elif operator == "/":
                if num2 == 0:
                    error = "Cannot divide by zero"
                else:
                    result = calc.divide(num1, num2)
        except:
            error = "Invalid input"

    return render_template("calculator.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)
