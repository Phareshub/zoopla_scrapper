'''
These functions goes side by side to main app.py Python file
in the same folder.
'''
# ---------------------------------------------- #
# Project starts at: 2020 02 01                  #
# Lithuana, by Vytautas Bielinskas               #
# ---------------------------------------------- #

# Import modules and packages
import matplotlib.pyplot as plt
import numpy as np
import urllib.request as ur
#import cv2
import io
import requests
import json
import datetime, time
from PIL import Image


# System variables
BAD_CHARS = ['(', ')']


# download the image, convert it to a NumPy array, and then read 
# it into OpenCV format
def url_to_image(url):

	print('| Given URL: {}'.format(url))

	resp = ur.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
	#img_to_plot = .thumbnail((64, 64), Image.ANTIALIAS)
	#plt.imshow(image, interpolation='nearest', cmap='hot')
	#plt.show()

	# return the image
	return image


# Extracting data from image
# Read Image File
def extract_text(img, API_KEY):
	'''
	Args:
		-- image - a given image of floorplan.
	'''

	if type(img) != None:

		x = input('Debuging station')

		try:
			# Get Size of Image
			height, width, _ = img.shape

			# Cutting Image
			#roi = img[1: height-1, 1: width-1]
			roi = img

			# Ocr
			url_api = 'https://api.ocr.space/parse/image'
			_, compressedimage = cv2.imencode('.jpg', roi, [1, 90])
			file_bytes = io.BytesIO(compressedimage)
			time.sleep(3)
			result = requests.post(url_api,
			files = {'--.jpg': file_bytes},
					 data = {'apikey' : API_KEY})

			result = result.content.decode()
			result = json.loads(result)

			#print(result)

			try:
				text_detected = str(result.get('ParsedResults')[0].get('ParsedText')).split('\n')
				#print(text_detected)
				return text_detected
			except:
				print('Result = {}'.format(result))
				return None

			# Show the file
			#cv2.imshow('Img-Roi', roi)
			#cv2.waitKey(0)
			#cv2.destroyAllWindows()

			return result.get('ParsedResults')[0].get('ParsedText')

		except:
			x = input('Debuging station')
			return None

	else:
		print('No Image found.')
		return None


def has_numbers(line):
	'''
	Args:
		-- a given subset of whole string that possibly contains numbers
	'''
	return any(char.isdigit() for char in line)	


def get_float_numbers_from_string(line):
	'''
	Args:
		-- a given subset of whole string that possibly contains numbers
	'''
	if has_numbers(line):

		for this_bad_char in BAD_CHARS:
			line = line.replace(this_bad_char, '')

		print('line = {}'.format(line.split()))

		a = []
		for word in line.split():

			try:
				a.append(float(word))
			except ValueError:
				pass

		return a

	else:
		print('--> No found numbers here. <--')
		return None


def text_parse(extracted_text):
	'''
	Args:
		-- extracted_text : a list of string that has been extracted.
	'''
	possible_area = None

	for this_segment in extracted_text:
		if len(this_segment) > 5:

			x = input('Debuging station')

			print('--> {}'.format(this_segment))

			if 'total'.upper() in this_segment.upper() and 'area'.upper() in this_segment.upper() or\
			   'internal'.upper() in this_segment.upper() and 'area'.upper() in this_segment.upper() or\
			   'approximate'.upper() in this_segment.upper() and 'area'.upper() in this_segment.upper():
				print('----> {}'.format(this_segment))

				possible_area = get_float_numbers_from_string(this_segment)

	if possible_area != None and type(possible_area) != None:
		try:
			print('Possible area = {}'.format(possible_area))
			if len(possible_area) > 0:
				return possible_area
			else:
				print('\n(!) Possible area is not available (!).\n')
				return [float(0)]
		except:
			print('Possible area is not available.')
			return [float(0)]

	else:
		return None


def save_data(data):
	'''
	Args:
		-- data : a given Pandas DataFrame with extracted values
	'''
	timeNow = str(datetime.datetime.now()).replace(":","-")[:-10]
	date = '2020'
	filename = "{}-AreaValues_Zoopla.csv".format(timeNow)

	data.to_csv(filename, encoding='utf-8')
	print('\nThe file is saved to external CSV file: {}.'.format(filename))	

	return None