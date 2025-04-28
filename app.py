from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import pyttsx3
import datetime
import math
import re
from basic_calculation import add, sub, multiply, divide
from functions_for_power_calculation import find_sqrt, cube_root, power, square, cube
from factorial import fact
from trigonometry import sin_value, sinh_value, cos_value, cosh_value, tan_value, tanh_value, log

app = Flask(__name__)

# Function to process commands
def process_command(command):
    try:
        command = command.lower()
        if any(op in command for op in ["+", "-", "*", "/", "(", ")"]):
            sanitized_command = re.sub(r"[^0-9+\-*/(). ]", "", command)
            try:
                res = eval(sanitized_command, {"__builtins__": None}, {"math": math})
                res = round(res,3)
                return f"Result is: {res}"
            except Exception as e:
                return f"Error in evaluating expression: {str(e)}"

        if "+" in command or "sum" in command or "add" in command:
            res = add(list(map(str, re.findall(r"[-+]?\d*\.?\d+", command))))
            return f"Total is: {res}"
        if "minus" in command or "subtract" in command:
            res = sub(list(map(str, re.findall(r"[-+]?\d*\.?\d+", command))))
            return f"Result is: {res}"
        if 'multiply' in command or "product" in command or "x" in command:
            res = multiply(list(map(str, re.findall(r"[-+]?\d*\.?\d+", command))))
            return f"Product is: {res}"
        if "divide by" in command or "division" in command or "/" in command:
            nums = list(map(str, re.findall(r"[-+]?\d*\.?\d+", command)))
            res = divide(nums)
            return f"Result is: {res}"
        if "square root" in command:
            res = find_sqrt(list(map(str, re.findall(r"[-+]?\d*\.?\d+", command))))
            return f"Square root is: {res}"
        if "square" in command:
            res = square(list(map(str, re.findall(r"[-+]?\d*\.?\d+", command))))
            return f"Square is: {res}"
        if "cube of" in command:
            res = cube(list(map(str, re.findall(r"[-+]?\d*\.?\d+", command))))
            return f"Cube is {res}"
        if "is to the power" in command or "power" in command or "^" in command:
            res = power(list(map(str, re.findall(r"[-+]?\d*\.?\d+", command))))
            return f"Result is {res}"
        if "cube root" in command:
            res = cube_root(list(map(str, re.findall(r"[-+]?\d*\.?\d+", command))))
            return f"Cube root is: {res}"
        if "factorial" in command:
            res = fact(list(map(str, re.findall(r"[-+]?\d*\.?\d+", command))))
            return f"Factorial is: {res}"
        if re.search("Hyperbolic sin", command):
            res = sinh_value(list(map(str, re.findall(r"[-+]?\d*\.?\d+", command))))
            return f"Hyperbolic sine is: {res}"
        if re.search("hyperbolic cos", command):
            res = cosh_value(list(map(str, re.findall(r"[-+]?\d*\.?\d+", command))))
            return f"Hyperbolic cos is: {res}"
        if re.search("Hyperbolic tan", command):
            res = tanh_value(list(map(str, re.findall(r"[-+]?\d*\.?\d+", command))))
            return f"Hyperbolic tan is: {res}"
        if re.search("sin", command):
            res = sin_value(list(map(str, re.findall(r"[-+]?\d*\.?\d+", command))))
            return f"Sine value is: {res}"
        if re.search("cos", command):
            res = cos_value(list(map(str, re.findall(r"[-+]?\d*\.?\d+", command))))
            return f"Cos value is: {res}"
        if re.search("tan", command):
            res = tan_value(list(map(str, re.findall(r"[-+]?\d*\.?\d+", command))))
            return f"Tan value is: {res}"
        if re.search("log of", command):
            num = list(map(str, re.findall(r"[-+]?\d*\.?\d+", command)))
            res = log(num)
            return f"Log of {num[0]} base {num[1]} is: {res}"
        return "Command not recognized"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    command = data.get("command", "")
    result = process_command(command)
    return jsonify({"response": result})

if __name__ == "__main__":
    app.run(debug=True)
