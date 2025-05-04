from flask import Flask, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField

app = Flask(__name__)

# App Config for temp converter
app.config['SECRET_KEY'] = '...'

# Forms
class ConvertForm(FlaskForm):
    fahrenheit = IntegerField('Fahrenheit:')
    submit = SubmitField('Submit')

@app.route("/")
def main():
    return render_template("calculator.html")

#calculator backend
@app.route("/calculate", methods=["POST"])
def calculate():
    number_one = request.form["number_one"]
    number_two = request.form["number_two"]
    operation = request.form["operation"]

    if operation == "add":
        result = float(number_one) + float(number_two)
    elif operation == "subtract":
        result = float(number_one) - float(number_two)
    elif operation == "multiply":
        result = float(number_one) * float(number_two)
    elif operation == "divide":
        if float(number_two) == 0:
            result = "Error: Cannot divide by zero"
        else:
            result = float(number_one) / float(number_two)
    else:
        result = "Invalid operation"

    return render_template("calculator.html", result=result)

#temp convertor backend
@app.route('/convert', methods=['GET', 'POST'])
def convert():

    result_temp = None
    original_temp = ''
    from_temp = ''
    to_temp = ''

    if request.method == 'POST':
        value = float(request.form['tem_value'])
        from_temp = request.form['from_scale']
        to_temp = request.form['to_scale']
        original_temp = value

        if from_temp == to_temp:
            result_temp = value
        elif from_temp == 'celsius':
            if to_temp == 'fahrenheit':
                result_temp = value * 9 / 5 + 32
            elif to_temp == 'kelvin':
                result_temp = value + 273.15
        elif from_temp == 'fahrenheit':
            if to_temp == 'celsius':
                result_temp = (value - 32) * 5 / 9
            elif to_temp == 'kelvin':
                result_temp = (value - 32) * 5 / 9 + 273.15
        elif from_temp == 'kelvin':
            if to_temp == 'celsius':
                result_temp = value - 273.15
            elif to_temp == 'fahrenheit':
                result_temp = (value - 273.15) * 9 / 5 + 32

    

    return render_template('convert.html',
                       result=result_temp,
                       original=original_temp,
                       from_scale=from_temp,
                       to_scale=to_temp)

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", error=error)

@app.errorhandler(500)
def server_error(error):
    return render_template("500.html", error=error)

if __name__ == "__main__":
    app.run(debug=True, port=3000)
