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

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    """formula C = 5/9 * (F -32) Fahrenheit to Celsius"""
    table = []
    for f in range(30, 101, 2):
        c = 5 / 9 * (f - 32)
        c = round(c, 1)
        table.append((f, c))

    form = ConvertForm()

    if form.validate_on_submit():
        f = form.fahrenheit.data
        c = 5 / 9 * (f - 32)
        c = round(c, 1)
        session['fa'] = f
        session['celsius'] = c
        form.fahrenheit.data = ''
        return redirect(url_for('convert'))

    return render_template('convert.html', table=table, form=form,
                           f=session.get('fa', ''),
                           c=session.get('celsius', ''))

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", error=error)

@app.errorhandler(500)
def server_error(error):
    return render_template("500.html", error=error)

if __name__ == "__main__":
    app.run(debug=True, port=3000)
