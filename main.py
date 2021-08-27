__author__ = 'Programmer Ayush'

# URL Shortener Designed by Programmer Ayush
# Orignal Link: https://smool.cf/

# Importing required modules
from flask import Flask, render_template, redirect, url_for, request
import string
import random
import sqlite3


# Making a Flask App
app = Flask(__name__)


# Home Page
@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


# Getting the Orginal Link using Requests
@app.route("/", methods=['POST', 'GET'])
@app.route("/home", methods=['POST', 'GET'])
def linkshort():
	if request.method == "POST":
		link = request.form["link"]
		
		
		# Generating a randon String
		code = "".join(random.choices(string.ascii_lowercase + string.digits, k = 7))


		# Putting the link and the code in a database
		with sqlite3.connect("database.db") as conn:
			c = conn.cursor()
			c.execute("""
	       	CREATE TABLE IF NOT EXISTS links (
	       	code TEXT,
	       	target TEXT
	       	)
	       	""")
	       	
			c.execute("INSERT INTO links VALUES (?, ?)", (code, link))

	else:
		return render_template("index.html")

	# Sending the generated link to the template
	return render_template("success.html", shorten=f"https://smool.cf/{code}")


# decoding a link and redirecting the user to the orignal link
@app.route("/<code>")
def decodeurl(code):
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        try:
        	c.execute("SELECT target FROM links WHERE code = ?", (code,))
        	target = c.fetchall()
        	
        except:
        	return redirect(url_for("index"))
        	
        try:
            return redirect(target[0][0], code=302)
            
        # if the link dosent exists, the user gets redirected to the home page
            
        except:
            return redirect(url_for("index"))
            
    
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)