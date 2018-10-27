from flask import Flask, render_template, request
import json 
import mysql.connector
import sqlite3 




mydb = sqlite3.connect('CodeForGood.db')
cursor = mydb.cursor()
app = Flask(__name__)

def register():
	retunJSON = {}
	if request.method == 'POST':
		user = request.json
		email = user['email']
		name = user['name']
		school = user['school']

		cursor.execute('SELECT (%s) FROM STUDENTS', email)
		if cursor.fetch():
			return "User already exist :("
		else:
			cursor.execute('INSERT INTO STUDENTS (ID, EMAIL, NAME, SCHOOL, POINTS) VALUES (NULL, (%s), (%s), (%s), 0', email, name, school)
			d1 = {'totalPoints': 0}
			d2 = {'items': None}
			d3 = {'school': school}
			retunJSON.update(d1)
			retunJSON.update(d2)
			retunJSON.update(d3)
			return retunJSON




@app.route('/dashboard', methods=['GET', 'POST'])
def login():
	#list of dictionaries to return 
	dictionaryList = []
	#the return will go into here
	returnJSON = {}
	
	if request.method == 'POST':
		
		user = request.json 
		username = user['username']
		cursor.execute('SELECT (%s) FROM STUDENTS', username)

		if cursor.fetchone():

    		# gets student ID, total points and school name

		    cursor.execute("SELECT ID, POINTS, SCHOOL FROM STUDENTS WHERE NAME = ?", (name,))
		    query = cursor.fetchone()
		    if query:

		        studentID = query[0]
		        totalPoints = query[1]
		        school = query[2]
		        tasks = []

		        # gets the tasks done by student & points
		        cursor.execute("SELECT KEYWORD FROM STUDENTTASKS WHERE ID = ?", (studentID,))
		        keywords = cursor.fetchall()
		        if keywords:


		            for word in keywords:
		                cursor.execute("SELECT TASKDESC, POINTVALUE FROM TASKSIDS WHERE KEYWORD = ?", (word[0],))
		                tasks.append(cursor.fetchall())

		            for counter, task in enumerate(tasks):
		                # the dictionaries that will be turned into jsons
		                dictionary = {}
		                # this will give name of the thing
		                item = keywords[counter][0]
		                # this will give description of item
		                itemDescrip = task[0][0]
		                # this will add to return dictionary

		                d1 = {'itemID': item}
		                d2 = {'itemDescrip': itemDescrip}
		                d3 = {'itemPoint': task[0][1]}
		                dictionary.update(d1)
		                dictionary.update(d2)
		                dictionary.update(d3)

		                dictionaryList.append(dictionary)

		            d1 = {'totalPoints': totalPoints}
		            d2 = {'items': json.dumps(dictionaryList)}
		            d3 = {'school': school}

		            returnJSON.update(d1)
		            returnJSON.update(d2)
		            returnJSON.update(d3)

		            print(returnJSON)

		        else:
		            d1 = {'totalPoints': 0}
		            d3 = {'school': school}
		            returnJSON.update(d1)
		            returnJSON.update({})
		            returnJSON.update(d3)
		            print(returnJSON)

		    else:
		        print("Student info was empty for some reason")

		else:
		    print("Invalid Username")


app.run()
		




