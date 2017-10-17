import io
import hashlib
import requests
import re
import difflib

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
	print(r.status_code)

	text = r.text
	return text

text = extractLyric("C:\Bad apple.mp3")
p = re.compile("[\[]\d{2}[:]\d{2}[.]\d{2}[\]](.*?)[;]")
m = p.findall(text)
lyric = []
for line in m:
	lyric.append(line.split('&lt')[0]);

hiragana = {'あ':'아', 'い':'이', 'う':'우', 'え':'에', 'お':'오', \
			'か':'카', 'き':'키', 'く':'쿠', 'け':'케', 'こ':'코', \
			'が':'가', 'ぎ':'기', 'ぐ':'구', 'げ':'게', 'ご':'고', \
			'さ':'사', 'し':'시', 'す':'스', 'せ':'세', 'そ':'소', \
			'ざ':'자', 'じ':'지', 'ず':'즈', 'ぜ':'제', 'ぞ':'조', \
			'た':'타', 'ち':'치', 'つ':'츠', 'て':'테', 'と':'토', \
			'だ':'다',					  'で':'데', 'ど':'도', \
			'な':'나', 'に':'니', 'ぬ':'누', 'ね':'네', 'の':'노', \
			'は':'하', 'ひ':'히', 'ふ':'후', 'へ':'헤', 'ほ':'호', \
			'ば':'바', 'び':'비', 'ぶ':'부', 'べ':'베', 'ぼ':'보', \
			'ぱ':'파', 'ぴ':'피', 'ぷ':'푸', 'ぺ':'페', 'ぽ':'포', \
			'ま':'마', 'み':'미', 'む':'무', 'め':'메', 'も':'모', \
			'や':'야',			'ゆ':'유',			'よ':'요', \
			'ら':'라', 'り':'리', 'る':'루', 'れ':'레', 'ろ':'로', \
			'わ':'와', 								'を':'오'}

katagana = {'ア':'아', 'イ':'이', 'ウ':'우', 'エ':'에', 'オ':'오', \
			'カ':'카', 'キ':'키', 'ク':'쿠', 'ケ':'케', 'コ':'코', \
			'ガ':'가', 'ギ':'기', 'グ':'구', 'ゲ':'게', 'ゴ':'고', \
			'サ':'사', 'シ':'시', 'ス':'스', 'セ':'세', 'ソ':'소', \
			'ザ':'자', 'ジ':'지', 'ズ':'즈', 'ゼ':'제', 'ゾ':'조', \
			'タ':'타', 'チ':'치', 'ツ':'츠', 'テ':'테', 'ト':'토', \
			'ダ':'다',					  'デ':'데', 'ド':'도', \
			'ナ':'나', 'ニ':'니', 'ヌ':'누', 'ネ':'네', 'ノ':'노', \
			'ハ':'하', 'ヒ':'히', 'フ':'후', 'ヘ':'헤', 'ホ':'호', \
			'バ':'바', 'ビ':'비', 'ブ':'부', 'ベ':'베', 'ボ':'보', \
			'パ':'파', 'ピ':'피', 'プ':'푸', 'ペ':'페', 'ポ':'포', \
			'マ':'마', 'ミ':'미', 'ム':'무', 'メ':'메', 'モ':'모', \
			'ヤ':'야',			'ユ':'유',			'ヨ':'요', \
			'ラ':'라', 'リ':'리', 'ル':'루', 'レ':'레', 'ロ':'로', \
			'ワ':'와', 								'ヲ':'오'}

sp = {'ぁ', 'ぃ', 'ぅ', 'ぇ', 'ぉ', 'ょ', 'ゅ', 'っ', 'ん' \
	  'ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ョ', 'ュ', 'ッ', 'ン'}

iterlyric = iter(lyric)
for l in iterlyric:
	if any(key in l for key in hiragana.keys()) or any(key in l for key in katagana.keys()):
		# 요음 처리 부분. 예외 발생시 이 부분에 추가.
		if any(key2 in l for key2 in sp):
			print('yoon')

		l2 = l
		p = next(iterlyric)
		k = next(iterlyric)
		for ch in hiragana.keys():
			l2 = l2.replace(ch, hiragana[ch])
		for ch in katagana.keys():
			l2 = l2.replace(ch, katagana[ch])
		
		diff = difflib.ndiff(l2, p)

		pos = 0
		punc = ''
		try:
			for d in diff:
				if d[0] == ' ' and punc != '':
					l = l[:pos+1] + '(' + punc + ')' + l[pos+1:]
					pos += (len(punc)+2)
					punc = ''
				elif d[2] == ' ':
					pass
				elif d[0] == '-':
					pos += l[pos:].find(d[2])
				elif d[0] == '+':
					temp = ''
					for key in hiragana:
						if hiragana[key] == d[2]:
							punc += key
			if punc != '':
				l = l[:pos+1] + '(' + punc + ')' + l[pos+1:]
				pos += (len(punc)+2)
				punc = ''
			
		except TypeError:
			pass
		
		print(l)
		print(k)
		print()
		
