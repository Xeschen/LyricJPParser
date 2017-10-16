import io
import hashlib
import requests
import re

def extractLyric(filename):
	f = open(filename, 'rb')
	fs = bytearray(f.read())
	f.close()

	# Find ID3v2 tag and skip it
	fileSize = len(fs)
	position = 0
	for i in range(500000):
		if position+3 < fileSize and fs[position:position+3]==bytearray(b"ID3"):
			sizeByte = bytearray()
			position += 6
			sizeByte += fs[position:position+4]
			position += 4
			id3Size = sizeByte[0] << 21 | sizeByte[1] << 14 | sizeByte[2] << 7 | sizeByte[3]
			position = id3Size + 10
			break
		position += 3

	if position == 1500000:
		position = 0

	# md5 hash value of first block of song
	data = fs[position:position+163840]
	md5val = hashlib.md5()
	md5val.update(data)

	header = {'Content-Type':'application/soap+xml'}
	# Dummy data
	encData = '4e06a8c06f189e54e0f22e7f645f172bc6ba2702618c445c2973848e004d4709d745cad80f1fc63654bae492019e771af038de6822b1123687d6598f0064cae237c4e1ac873f4d3aa267a6c27197878a0638cf29b571f049d50add1f4303b8d46c05020516d5ca8000d05a10371829da7a90aad4f4c68a62c0c6083ede28f247'

	# Dummy MAC address, IP address
	reqstr = '<?xml version="1.0" encoding="UTF-8"?>' +\
		'<SOAP-ENV:Envelope ' +\
		'xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" ' +\
		'xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" ' +\
		'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' +\
		'xmlns:xsd="http://www.w3.org/2001/XMLSchema" ' +\
		'xmlns:ns2="ALSongWebServer/Service1Soap" ' +\
		'xmlns:ns1="ALSongWebServer" ' +\
		'xmlns:ns3="ALSongWebServer/Service1Soap12">' +\
		'<SOAP-ENV:Body>' +\
		'<ns1:GetLyric7>' +\
		'<ns1:encData>' + encData + '</ns1:encData>' +\
		'<ns1:stQuery>' +\
		'<ns1:strChecksum>' + str(md5val.hexdigest()) + '</ns1:strChecksum>' +\
		'<ns1:strVersion>3.4</ns1:strVersion>' +\
		'<ns1:strMACAddress>00000000</ns1:strMACAddress>' +\
		'<ns1:strIPAddress>255.255.255.0</ns1:strIPAddress>' +\
		'</ns1:stQuery>' +\
		'</ns1:GetLyric7>' +\
		'</SOAP-ENV:Body>' +\
		'</SOAP-ENV:Envelope>'
		
	url = "http://lyrics.alsong.co.kr/alsongwebservice/service1.asmx"
	r = requests.post(url, data=reqstr, headers=header)
	#print(r)
	#print(r.status_code)

	text = r.text
	return text

text = extractLyric("Bad apple.mp3")
p = re.compile("[\[]\d{2}[:]\d{2}[.]\d{2}[\]](.*?)[;]")
m = p.findall(text)
lyric = []
for line in m:
	lyric.append(line.split('&lt')[0]);

for l in lyric:
	print(l)