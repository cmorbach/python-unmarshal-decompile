# (C) cmorbach

import marshal
import sys
import codecs
import re
if sys.version_info < (3, 0):
	import cStringIO
else:
	from typing import TextIO
	from io import BufferedWriter
	from io import BytesIO
	from io import TextIOWrapper
if sys.version_info < (3, 7):
	from uncompyle6.main import decompile #pip install uncompyle6
else:
	from decompyle3.main import decompile #pip install decompyle3


def marshaledCodeFromFile(inFileName):
	print("open file " + inFileName)

	# open marshaled Python script
	try:
		with open(inFileName,"r") as f:
			fileContent = f.read()
	except Exception as E:
		print("cannot open " + inFileName)
		raise(E)

	# extract marshaled code
	try:
		match = re.search(r"marshal.loads\(b?'([^']+)'\)", fileContent)
		marshaledCode = match.group(1)
	except Exception as E:
		print("file has no marshaled code of unknown format")
		raise(E)

	# test string for debugging
	# marshaledCode = marshal.dumps(compile("def test(): return 0\nprint(test())", "<source>", "exec")).__repr__()[2:-1]
	# print(marshaledCode)

	# convert marshaled code to 8 bits ASCII
	try:
		if sys.version_info >= (3, 0):	# Python 3 needs byte array (Python 2 not)
			marshaledCode = marshaledCode.encode('latin-1')
		marshaledCodeAscii8 = marshaledCode.decode('unicode_escape').encode('latin-1')

	except Exception as E:
		print("cannot de-escape and convert code to ASCII")
		raise(E)

	return marshaledCodeAscii8


def deMarshal(marshaledCode, inFileVersion):
	global compiledStr

	sysVersionStr = "%s.%s" % (sys.version_info.major, sys.version_info.minor)
	inFileVersionStr = "%s.%s" % (inFileVersion[0], inFileVersion[1])
	print("decompile Python " + inFileVersionStr + " code with Python " + sysVersionStr)

	if sys.version_info < (3, 0):
		version = inFileVersionStr
		stringBuffer = cStringIO.StringIO()
	else:
		version = inFileVersion
		stringBuffer = BytesIO()
	
	codecinfo = codecs.lookup("utf8")
	buffer = codecs.StreamReaderWriter(stringBuffer, codecinfo.streamreader, codecinfo.streamwriter)
	
	try:
		byteCode = marshal.loads(marshaledCode)
		decompile(bytecode_version=version, co=byteCode, out=buffer)
	except Exception as E:
		print("unable to decompile marshaledCode")
		print(E)
		raise E

	buffer.seek(0)
	pythonCode = buffer.read()

	return pythonCode


def writeDecompiledCodeToFile(pythonCode, originalFileName):
	match = re.search(r"(.*)(\.[^\.]+)$", originalFileName)

	if match and len(match.groups()) == 2:
		filenameWithoutExtension = match.group(1)
		filenameExtension = match.group(2)
		newFileName = filenameWithoutExtension + "_decompiled" + filenameExtension
	else:
		newFileName = originalFileName + "_decompiled" + ".py"

	print("write decompiled code to " + newFileName)

	try:
		with open(newFileName,"w") as f:
			f.write(pythonCode)
	except Exception as E:
		print("error writing file")
		raise E


if __name__ == '__main__':
	print("unmarshal/decompile Python")

	if len(sys.argv) == 3 and len(sys.argv[2]) == 2:
		inFileName = sys.argv[1]
		inFileVersion = (int(sys.argv[2][0]), int(sys.argv[2][1]))
	else:
		print("usage: " + sys.argv[0] + " <file to decompile> <2-letter-version-string>")
		print("   example: " + sys.argv[0] + " marshaledFile.py 27")
		print("   for Python 2.7")

	#decompile
	try:
		marshaledCode = marshaledCodeFromFile(inFileName=inFileName)
		pythonCode = deMarshal(marshaledCode=marshaledCode, inFileVersion=inFileVersion)
		writeDecompiledCodeToFile(pythonCode=pythonCode, originalFileName=inFileName)
	except:
		exit()
