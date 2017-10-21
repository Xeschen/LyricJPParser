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

text = extractLyric("C:\yoiyami.mp3")
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
			'は':'와', 'ひ':'히', 'ふ':'후', 'へ':'에', 'ほ':'호', \
			'ば':'바', 'び':'비', 'ぶ':'부', 'べ':'베', 'ぼ':'보', \
			'ぱ':'파', 'ぴ':'피', 'ぷ':'푸', 'ぺ':'페', 'ぽ':'포', \
			'ま':'마', 'み':'미', 'む':'무', 'め':'메', 'も':'모', \
			'や':'야',			'ゆ':'유',			'よ':'요', \
			'ら':'라', 'り':'리', 'る':'루', 'れ':'레', 'ろ':'로', \
			'わ':'와', 								'を':'오', \
			'、':',', '？':'?', '！':'!'}

hiratabl = {'아':'あ', '이':'い', '우':'う', '에':'え', '오':'お', \
			'카':'か', '키':'き', '쿠':'く', '케':'け', '코':'こ', \
			'가':'が', '기':'ぎ', '구':'ぐ', '게':'げ', '고':'ご', \
			'사':'さ', '시':'し', '스':'す', '세':'せ', '소':'そ', \
			'자':'ざ', '지':'じ', '즈':'ず', '제':'ぜ', '조':'ぞ', \
			'타':'た', '치':'ち', '츠':'つ', '테':'て', '토':'と', \
			'다':'だ',					  '데':'で', '도':'ど', \
			'나':'な', '니':'に', '누':'ぬ', '네':'ね', '노':'の', \
			'하':'は', '히':'ひ', '후':'ふ', '헤':'へ', '호':'ほ', \
			'바':'ば', '비':'び', '부':'ぶ', '베':'べ', '보':'ぼ', \
			'파':'ぱ', '피':'ぴ', '푸':'ぷ', '페':'ぺ', '포':'ぽ', \
			'마':'ま', '미':'み', '무':'む', '메':'め', '모':'も', \
			'야':'や',			'유':'ゆ',			'요':'よ', \
			'라':'ら', '리':'り', '루':'る', '레':'れ', '로':'ろ', \
			'와':'わ', 										}


katakana = {'ア':'아', 'イ':'이', 'ウ':'우', 'エ':'에', 'オ':'오', \
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

# Cast Hangul with three arguments
def cast(cho, jung, jong):
	return cho*588 + (jung-30)*28 + jong + 0xAC00

def decast(hangul):
	hangul = ord(hangul)
	cho = (hangul - 0xAC00) // 588
	jung = (((hangul - 0xAC00) % 588) // 28 + 30)
	jong = hangul - cho*588 - (jung-30)*28 - 0xAC00
	return cho, jung, jong

# Cast jaeum to choseong
def jaToCho(ja):
	# ㄱ, ㄲ, ㄴ, ㄷ, ㄸ, ㄹ, ㅁ, ㅂ, ㅃ, ㅅ, ㅆ, ㅇ, ㅈ, ㅉ, ㅊ, ㅋ, ㅌ, ㅍ, ㅎ
	dic = {0:0, 1:1, 3:2, 6:3, 7:4, 8:5, 16:6, 17:7, 18:8, 20:9, 21:10, 22:11, 23:12, 24:13, 25:14, 26:15, 27:16, 28:17, 29:18}
	return dic[ja]

# Cast choseong to jongseong
def choToJong(ja):
	# ㄱ, ㄲ, ㄳ, ㄴ, ㄵ, ㄶ, ㄷ, ㄹ, ㄺ, ㄻ, ㄼ, ㄽ, ㄾ, ㄿ, ㅀ, ㅁ, ㅂ, ㅄ, ㅅ, ㅆ, ㅇ, ㅈ, ㅊ, ㅋ, ㅌ, ㅍ, ㅎ
	# Index starts from 1.
	dic = {0:1, 1:2, 2:4, 3:7, 5:8, 6:16, 7:17, 9:19, 10:20, 11:21, 12:22, 14:23, 15:24, 16:25, 17:26, 18:27}
	return dic[ja]

# Cast choseong to jaeum
def choToJa(cho):
	choDic = {0:0, 1:1, 2:3, 3:6, 4:7, 5:8, 6:16, 7:17, 8:18, 9:20, 10:21, 11:22, 12:23, 13:24, 14:25, 15:26, 16:27, 17:28, 18:29}
	return choDic[cho]

# Cast jongseong to choseong
def jongToCho(jong):
	jongDic = {1:0, 2:1, 4:2, 7:3, 8:5, 16:6, 17:7, 19:9, 20:10, 21:11, 22:12, 23:14, 24:15, 25:16, 26:17, 27:18}
	return jongDic[jong]

'''
print(ord('왓'))
cho, jung, jong = decast('왓')
print(cho, jung, jong)
print("%c%c%c"%(cho+0x3131, jung+0x3131, jong+0x3131))
print("%c%c%c"%(choToJa(cho)+0x3131, jung+0x3131, choToJa(jongToCho(jong))+0x3131))
print("%c"%cast(cho, jung, jong))
'''

#lyric = ['戸惑う  言葉  与えられても', '토마도우 코토바 아타에라레테모', '뜻밖의 말을 듣더라도']
#lyric = ['こんな  時間に  私はいるの?', '콘나 지칸니 와타시와 이루노?', '이런 세상에 나는 왜 존재하는 걸까?']
#lyric = ['自分の  心  ただ上の  空', '지분노 코코로 타다 우와노 소라', '나의 마음 속에선 그저 흘러들을 뿐']
iterlyric = iter(lyric)
for l in iterlyric:
	if any(key in l for key in hiragana.keys()) or any(key in l for key in katakana.keys()):

		l2 = l
		p = next(iterlyric)
		k = next(iterlyric)
		for ch in hiragana.keys():
			l2 = l2.replace(ch, hiragana[ch])
		for ch in katakana.keys():
			l2 = l2.replace(ch, katakana[ch])
		length = len(l2)
		i = 0
		while i <length:
			if (l2[i] == 'ん' or l2[i] == 'ン') and i > 0:
				cho, jung, jong = decast(l2[i-1])
				word = chr(cast(cho, jung, 4))	# ㄴ 받침
				l2 = l2[:i-1] + word + l2[i+1:]
				length -= 1
				i -= 1
			elif (l2[i] == 'っ' or l2[i] == 'ッ') and i > 0:
				cho, jung, jong = decast(l2[i-1])
				word = chr(cast(cho, jung, 19))	# ㅅ 받침
				l2 = l2[:i-1] + word + l2[i+1:]
				length -= 1
				i -= 1
			elif (l2[i] == 'ぁ' or l2[i] == 'ァ') and i > 0:
				cho, jung, jong = decast(l2[i-1])
				if jung == 30:	# ex) さぁ
					word = '아'
					l2 = l2[:i] + word + l2[i+1:]
					length -= 1
					i -= 1
				elif jung == 48:	# ex) ふぁ
					word = chr(cast(cho, 32, 0))	# ㅡ 가 ㅏ로 변화
					l2 = l2[:i-1] + word + l2[i+1:]
					length -= 1
					i -= 1
			elif (l2[i] == 'ぃ' or l2[i] == 'ィ') and i > 0:
				cho, jung, jong = decast(l2[i-1])
				if jung == 43:	# ex) フイ
					word = chr(cast(cho, 46, 0))	# ㅡ가 ㅟ로 변화
					l2 = l2[:i-1] + word + l2[i+1:]
					length -= 1
					i -= 1
			elif (l2[i] == 'ぉ' or l2[i] == 'ォ') and i > 0:
				cho, jung, jong = decast(l2[i-1])
				if jung == 43:	# ex) フォ
					word = chr(cast(cho, 38, 0))	# ㅡ가 ㅟ로 변화
					l2 = l2[:i-1] + word + l2[i+1:]
					length -= 1
					i -= 1
			elif (l2[i] == 'ぅ' or l2[i] == 'ゥ') and i > 0:
				l2 = l2[:i] + l2[i+1:]
				length -= 1
				i -= 1
			elif (l2[i] == 'ぇ' or l2[i] == 'ェ') and i > 0:
				cho, jung, jong = decast(l2[i-1])
				if jung == 43:	# ex) フェ
					word = chr(cast(cho, 5, 0))	# ㅡ가 ㅔ로 변화
					l2 = l2[:i-1] + word + l2[i+1:]
					length -= 1
					i -= 1
			elif (l2[i] == 'ょ' or l2[i] == 'ョ') and i > 0:
				cho, jung, jong = decast(l2[i-1])
				if jung == 43:	# ex) フョ
					word = chr(cast(cho, 44, 0))	# ㅡ가 ㅛ로 변화
					l2 = l2[:i-1] + word + l2[i+1:]
					length -= 1
					i -= 1
				elif jung == 50:	# ex) ショ
					word = chr(cast(cho, 44, 0))	# ㅣ가 ㅛ로 변화
					l2 = l2[:i-1] + word + l2[i+1:]
					length -= 1
					i -= 1
			elif (l2[i] == 'ゅ' or l2[i] == 'ュ') and i > 0:
				cho, jung, jong = decast(l2[i-1])
				if jung == 50:	# ex) しゅ
					word = chr(cast(cho, 47, 0))	# ㅣ가 ㅠ로 변화
					l2 = l2[:i-1] + word + l2[i+1:]
					length -= 1
					i -= 1
			i += 1
		spacel2 = []
		for i in range(len(l2)):
			if l2[i] == ' ':
				spacel2.append(i)
		l2 = l2.replace(' ', '')
		spacep = []
		for i in range(len(p)):
			if p[i] == ' ':
				spacep.append(i)
		p = p.replace(' ', '')
		
		diff = difflib.ndiff(l2, p)

		'''
		if 'は' in l:	# Heuristic for wa and ha
			for i in range(len(l)):
				if l[i] == 'は':
					l3 = l[:i] + 'わ' + l[i+1:]
					for ch in hiragana.keys():
						l3 = l3.replace(ch, hiragana[ch])
					for ch in katakana.keys():
						l2 = l2.replace(ch, katakana[ch])
					length = len(l3)
					i = 0
					while i <length:
						if l3[i] == 'ん' and i > 0:
							cho, jung, jong = decast(l2[i-1])
							word = chr(cast(cho, jung, 4))
							l3 = l3[:i-1] + word + l3[i+1:]
							length -= 1
							i -= 1
						i += 1

					spacel3 = []
					for i in range(len(l3)):
						if l3[i] == ' ':
							spacel3.append(i)
					l3 = l3.replace(' ','')
					diff2 = difflib.ndiff(l3, p)
					cnt1 = 0
					cnt2 = 0
					for e in list(diff):
						if e[0] == ' ':
							pass
						cnt1 += 1
					for e in list(diff2):
						if e[0] == ' ':
							pass
						cnt2 += 1
					if cnt2 < cnt1:
						l2 = l3
						spacel2 = spacel3
						'''

#		for sploc in spacel2:
#			l2 = l2[:sploc] + ' ' + l2[sploc:]
#		for sploc in spacep:
#			p = p[:sploc] + ' ' + p[sploc:]
#		diff = difflib.ndiff(l2, p)

		pos = 0
		sign = 0	# 0 for none, 1 for -, 2 for +
		punck = ''
		puncj = ''
		listk = []
		listj = []
		
		try:
			for d in diff:
				if d[0] == ' ' or d[2] == ' ':
					sign = 0
					if punck != '':
						listk.append(punck)	# Dump former block
						punck = ''
					if puncj != '':
						listj.append(puncj)	# Dump former block
						puncj = ''
					pass
				elif d[0] == '-':
					if sign != 1:	# New - block begins
						if puncj != '':
							listj.append(puncj)	# Dump former block
							puncj = ''
					puncj += d[2]
					sign = 1
				elif d[0] == '+':
					if sign != 2:	# New + block begins
						if punck != '':
							listk.append(punck)	# Dump former block
							punck = ''
					sign = 2
					punck += d[2]
			if punck != '':
				listk.append(punck)	# Dump former block
				punck = ''
			if puncj != '':
				listj.append(puncj)	# Dump former block
				puncj = ''
			for punck, puncj in zip(listk, listj):
				pwrite = ''
				pos += (l[pos:].find(puncj[0]) + len(puncj) - 1)
				for word in punck:
					follower = False
					cho, jung, jong = decast(word)
					if jung == 32:	# ㅑ
						if cho != 11 or jong != 0:	# や가 아닌 경우
							word = chr(cast(cho, 50, jong))	# ㅣ+ゃ
							follower = True
					elif jung == 42:	# ㅛ
						if cho != 11 or jong != 0:	# よ가 아닌 경우
							word = chr(cast(cho, 50, jong))	# ㅣ+ょ
							follower = True
					if jong == 4:	# ㄴ 받침
						word = chr(cast(cho, jung, 0))
						follower = True
					elif jong == 19:	# ㅅ 받침
						word = chr(cast(cho, jung, 0))
					if word in hiratabl:
						pwrite += hiratabl[word]
					if follower == True:
						if jung == 32:	# ㅑ
							pwrite += 'ゃ'
						elif jung == 42:	# ㅛ
							pwrite += 'ょ'
						if jong == 4:	# ㄴ 받침
							pwrite += 'ん'
				l = l[:pos+1] + '(' + pwrite + ')' + l[pos+1:]
				pos += (len(pwrite)+2)
			
		except TypeError:
			pass
		
		print(l)
#		print(l2)
#		print(p)
		print(k)
		print()
		
