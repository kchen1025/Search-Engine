from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def hello():
	return render_template('home.html')

@app.route('/', methods=['POST'])
def my_form_post():
	ptext = request.form['text']
	
    #take the test and return a list of searches
	try:
		j = search(ptext)

	except:

		j = []

	return render_template('search_results.html',text=j)





def search(input):
	import json

	split_input = input.split()


	with open('tf_idf.txt') as data_file:
		data = json.load(data_file)

	matched_set = set()

	#check for exact match of word
	for key in data[split_input[0]]:
		matched_set.add((key,data[split_input[0]][key]))
	
	#check for patial matches
	for i in data:
		if split_input[0] in i:
			for key in data[i]:
				matched_set.add((key,data[i][key]))

	matched_words = []
	matched_words = sorted(matched_set,key=lambda x:x[1])



	#get the url from the word matches
	with open('html_files.json') as html_files_data:
 		html_data = json.load(html_files_data)

	url_set = set()
	url_list = []
	for i in matched_words:
		url = html_data[i[0]]['url']
		if url not in url_set:
			url_list.append(url)
		url_set.add(url)
		
	

	return url_list



if __name__ == "__main__":
	app.debug = True
	app.run()
