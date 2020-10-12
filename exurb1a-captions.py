import requests 
import xml.etree.ElementTree as ET 
import json

# Exurb1a caption dataset: An attempt to train GPT-2 language model using exurb1a's writings
# date: 21-8-2020 
# author: @odinshell

API_KEY = "API_KEY"

def loadXML(name, id):
	if id != None:
		try:
			resp = requests.get("http://video.google.com/timedtext?lang=en&v=" + str(id)) 

			if(resp.content == ''):
				return False
			# write the captions file with respective video title
			with open('captions/' + str(name) + '.xml', 'wb') as f: 
				f.write(resp.content)

		except requests.exceptions.RequestException as e:
			print("Error occured: " + e)
	return True


def parseXML(xmlfile, title):  
	tree = ET.parse(xmlfile)  
	root = tree.getroot() 

	with open('corpus.txt', 'a+') as f: 
		f.write('Title: ' + title + '\n\n')
		for item in root.findall('./text'): 
			f.write(item.text.encode('utf8') + '\n') 
		f.write('===================================\n\n')
	
def main():  
	# get all videos in json 
	api_call = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&maxResults=100&playlistId=UUimiUgDLbi6P17BdaCZpVbg&key=' + API_KEY
	resp = requests.get(api_call)
	data = resp.json()

	total = data['pageInfo']['totalResults']
	print("Total: " + str(total)) # if > 50, use pageToken for next page results.
	if(total > 49):
		nextPageToken = data['nextPageToken']
		print("[+] Next page token: " + nextPageToken)

	# find each videoIDs
	for video in data['items']:
		videoName = video['snippet']['title']
		videoId =  video['snippet']['resourceId']['videoId']
		print(videoName)

		# get the XML file of each video and parse
		done = loadXML(videoName, videoId)
		if(done):
			parseXML('captions/'+ videoName + '.xml', videoName)
		else:
			print("[!] Issues in downloading: " + videoName)
	
	# if another page exists, do shit again.
	if(nextPageToken != None):
		api_call = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&maxResults=100&playlistId=UUimiUgDLbi6P17BdaCZpVbg&key=' + API_KEY +'&pageToken=' + nextPageToken
		resp = requests.get(api_call)
		data = resp.json()
	
		# find each videoIDs on the next page
		for video in data['items']:
			videoName = video['snippet']['title']
			videoId =  video['snippet']['resourceId']['videoId']
			print(videoName)

			# get the XML file of each video and parse
			done = loadXML(videoName, videoId)
			if(done):
				parseXML('captions/'+ videoName + '.xml', videoName)
			else:
				print("[!] Issues in downloading: " + videoName)


	print("[+] Text corpus created.")	

if __name__ == "__main__": 
	main() 
