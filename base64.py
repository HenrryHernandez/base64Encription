import math
#------------------------------------------ESTA PARTE SE USA PARA AMBAS COSAS, ENCRIPTAR Y DESENCRIPTAR


#TABLA QUE CONTIENE LOS CARACTERES EN BASE64
tabla = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/', '=']


def toBits(numero, howManyBits): #AQUI SIMPLEMENTE CONVERTIMOS A BITS LOS ASCIIS NUMERICOS DE LOS CARACTERES
	bits = ""
	potencia = howManyBits - 1
	while potencia > -1:
		if numero - math.pow(2, potencia) < 0:
			bits += "0"
			potencia -= 1
		else:
			bits += "1"
			numero -= math.pow(2, potencia)
			potencia -= 1
	return bits


def getAsciiBits(asciis, howManyBits): #AQUI QUEREMOS PASAR LOS ASCII NUMERICOS PERO A BITS, USAREMOS PARA ELLO LA FUNCION QUE CONVIERTE A BITS
									#EL "howManyBits" SIGNIFICA DE CUANTO ES LA AGRUPACION DE BITS, POR EJEMPLO, PARA ENCRIPTAR ES DE 8, PARA DESENCRIPTAR ES DE 6
	bits = ""
	for i in asciis:
		bits += toBits(i, howManyBits)
	return bits




#--------------------------------------------------ESTA PARTE ES LO USADO PARA ENCRIPTAR-----------------------------------------------------


def getWordAscii(palabra): #ESTE METODO NOS SIRVE PARA OBTENER EL ASCII NUMERICO DE TODOS LOS CARACTERES DE LA PALABRA A ENCRIPTAR
	palabraEnAscii = []
	for i in palabra:
		palabraEnAscii.append(ord(i))
	return palabraEnAscii


def difineGroupsInBytesOf3(bytesArr): #ESTA FUNCION NOS AYUDA A SEPARA LOS GRUPOS DE 3 BYTES EN 6 BITS ADEMAS DE EVALUAR EL CASO EN DONDE NO HAYAN GRUPOS DE
									#BYTES QUE SEAN MULTIPLO DE 3
	bytesEnTres = []
	seises = len(bytesArr[len(bytesArr) - 1]) // 6
	if seises != 4:
		if len(bytesArr[len(bytesArr) - 1]) - 6 * seises != 0:
			for i in range(len(bytesArr[len(bytesArr) - 1]), 6 * (seises + 1)):
				bytesArr[len(bytesArr) - 1].append("0")
		seises = len(bytesArr[len(bytesArr) - 1])

	for i in range(seises, 24): #en caso de que no haya multiplos de 3 exactos en la cantidad de los grupos de bytes, usaremos el '@' de comodin, lo usaremos
								#por que su ascii es base64 el caracter 65 ('=') nos ayuda cuando no son multiplos de 3 la cantidad de grupos de 3 bytes
		bytesArr[len(bytesArr) - 1].append("@")

	for i in range(len(bytesArr)):
		bytesEnTres.append([])

		for j in range(4):
			bytesEnTres[i].append("")
			for k in range(6):
				bytesEnTres[i][j] += bytesArr[i][j * 6 + k]

	return bytesEnTres



def difineBytes(bits): #UNO DE LOS PASOS PARA ENCRIPTAR ES SEPARAR LOS BITS QUE COMPONEN UNA PALABRA EN GRUPOS DE 3 BYTES O 24 BITS, EN ESTA FUNCION LO HACEMOS,
						#PERO AUN NO SEPARAMOS EN 6 BITS LOS GRUPOS 24 BITS (3 BYTES) Y TAMPOCO HEMOS EVALUADO LA POSIBILIDAD EN DONDE NO SE CUMPLA QUE LA CANTIDAD
						#DE GRUPOS DE 3 BYTES QUE HAYA SEA MULTIPLO DE 3
	veinticuatros = len(bits) // 24
	sobrantes = len(bits) - 24 * veinticuatros
	bytess = []

	for i in range(veinticuatros):
		bytess.append([])
		for j in range(24):
			bytess[i].append(bits[i * 24 + j])

	
	bytess.append([])
	for i in range(veinticuatros * 24, len(bits)):
		bytess[veinticuatros].append(bits[i])

	if len(bytess[veinticuatros]) == 0:
		del bytess[veinticuatros]

	bytess = difineGroupsInBytesOf3(bytess) #EL LLAMADO A ESTA FUNCION NOS AYUDARA CON EL PROBLEMA ANTERIOR MENCIONADO
	return bytess


def getBitsAsciis(bytess): #AQUI, UNA VEZ YA OBTENIDOS LOS BITS DE LA PALABRA CIFRADA, DEBEMOS CONVERTIR DICHOS BITS EN ASCIIS DE NUEVO
	asciis = []
	for i in range(len(bytess)):
		for j in range(4):
			palabraNumero = 0
			potencia = 0
			asciis.append(0)
			for k in range(5, - 1, -1):
				if bytess[i][j][k] == '1': #esta parte nos ayudara para ir sumando los bits que esten en la palabra de bits
					asciis[(len(asciis) - 1)] += int(math.pow(2, potencia))
					potencia += 1
					continue
				elif bytess[i][j][k] == '@': #si la posision a evaluar contiene un @ significa que su ascii sera 65 y el caracter sera '=', esto es cuando no
											#se cumple el caso de que haya cantidad de grupos de 3 bytes multiplos de 3
					asciis[(len(asciis) - 1)] += ord(bytess[i][j][k])
					break
				potencia += 1
	return asciis



def changeToWordAgainWithTable(tabla, bytesDefinidos): #ESTA FUNCION NOS AYUDA A, UNA VEZ OBTENIDO EL ASCII DE LA SUMA DE LOS BITS, CONVERTIR DICHOS BITS EN CARACTERES
	bytesDefinidos = getBitsAsciis(bytesDefinidos) #PARA PODER HACER LO ANTERIOR MENCIONAD, USAREMOS LA AYUDA DE ESTE METODO
	palabraEnciptada = ""
	for i in bytesDefinidos:
		palabraEnciptada += tabla[i]
	
	return palabraEnciptada


def encode(palabra): #ESTE METODO HARA LAS LLAMADAS NECESARIAS A LOS OTRS METODOS PARA HACER LA ENCRIPTACION, ESTO PARA NOSOTROS HACER UNA SOLA LLAMADA A UN
						#METODO CUANDO QUERAMOS ENCRIPTAR, EL CUAL SERA A ESTE
	palabraBits = getAsciiBits(getWordAscii(palabra), 8)
	bytesDefinidos = difineBytes(palabraBits)
	palabraEnciptada = changeToWordAgainWithTable(tabla, bytesDefinidos)
	return palabraEnciptada













#--------------------------------------------------ESTA PARTE ES LO USADO PARA DESENCRIPTAR-----------------------------------------------------


def wordToAscii(word):  #ESTE METODO NOS SIRVE PARA OBTENER EL ASCII NUMERICO DE TODOS LOS CARACTERES DE LA PALABRA A ENCRIPTAR, PERO EN REALIDAD NO EL ASCII
						#COMO TAL, SINO SU VALOR EN LA TABLA, PERO LE DIGO ASCII NOMAS PORQUE NO SE COMO DECIRLE
	asciis = []
	for i in word:
		if i == "=":
			continue
		elif i == tabla[ord(i) - 65]: #checamos si es Mayuscula
			asciis.append(ord(i) - 65)
		elif i == tabla[ord(i) - 97 + 26]: #checamos si es Minuscula
			asciis.append(ord(i) - 97 + 26)
		elif i == tabla[ord(i) - 48 + 52]: #checamos si es Numero
			asciis.append(ord(i) - 48 + 52)
		elif i == "+":
			asciis.append(62)
		elif i == "/":
			asciis.append(63)

	return asciis


def groupBitsInCompleteBytes(bits): #AQUI AGRUPAMOS LOS BITS DE BYTE EN BYTE, O SEA DE 8 EN 8 BITS, AQUI YA NO ES NECESARIO ESO DE QUE TIENE QUE HABER GRUPOS
									#DE BYTES MULTIPLES DE 3
	numBytes = len(bits) // 8
	bytesArr = []

	for i in range(numBytes):
		bytesArr.append("")
		for j in range(8):
			bytesArr[i] += bits[i * 8 + j]
	return bytesArr


def getAsciis(bytesArr): #SE CONVIERTE DE BITS A ASCII
	asciis = []
	for i in range(len(bytesArr)):
		asciis.append(0)
		potencia = 0
		for j in range(7, -1, -1):
			if bytesArr[i][j] == "1":
				asciis[i] += int(math.pow(2, potencia))
				potencia += 1
				continue
			potencia += 1

	return asciis


def changeToWordAgainWithAscii(asciis): #SE CONVIERTE DE ASCII A CARACTERES Y SE RETORNA LA PALABRA DESENCRIPTADA
	word = ""
	for i in asciis:
		word += chr(i)
	return word


def decode(palabra):#ESTE METODO HARA LAS LLAMADAS NECESARIAS A LOS OTRS METODOS PARA HACER LA DESENCRIPTACION, ESTO PARA NOSOTROS HACER UNA SOLA LLAMADA A UN
					#METODO CUANDO QUERAMOS ENCRIPTAR, EL CUAL SERA A ESTE
	palabraAAscii = wordToAscii(palabra)
	bitsDeAscii = getAsciiBits(palabraAAscii, 6)
	numBytes = groupBitsInCompleteBytes(bitsDeAscii)
	asciis = getAsciis(numBytes)
	palabraDesencriptada = changeToWordAgainWithAscii(asciis)
	return palabraDesencriptada








#--------------------------------PRUEBAS------------------------------------------------------


#LLAMADAS DE PRUEBA PARA PROBAR LA ENCRIPTACION
palabra = "hauoo n lmd "
print(encode(palabra))



#LLAMADAS DE PRUEBA PARA PROBAR LA DESENCRIPTACION
#palabra = "hauoo n lmd "
#print(decode(palabra))
