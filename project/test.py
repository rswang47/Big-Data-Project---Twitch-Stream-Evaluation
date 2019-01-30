import json

with open('parsed_results/numofstream_eachframe/numofstream__everyday') as json_file:
	js = json.load(json_file)
	json_file.close()


jss = str(js)
jss = jss.replace('\'', '')
jss = jss.replace('\\', '\'')

print(jss)