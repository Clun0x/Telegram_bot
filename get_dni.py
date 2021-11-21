#!/usr/bin/python3

from pwn import *
import re
import pdb

#Ctrl+C
def exit(sig, frame):
	print("\n[!] Saliendo...")
	sys.exit(1)

signal.signal(signal.SIGINT, exit)

#Variables Globales
dni_url = "https://eldni.com"
get_dni_url = "https://eldni.com/pe/buscar-por-nombres"

def get_dni(name, apell_p, apell_m):

	api_token = "b91f0473b50add6095381ffd2966e116cacbbe0736af83a998c02e45235051b8"
	s = requests.Session()

	header = {
		'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"
	}

	r =	s.get(dni_url, headers=header)

	token_value = re.findall(r'value=".*?"', r.text)[0]
	token = re.findall(r'".*?"', token_value)[0]

	form_data = {
		'_token': token.strip('"'),
		'nombres': name,
		'apellido_p': apell_p,
		'apellido_m': apell_m
	}

	dni_get = s.post(get_dni_url, headers=header, data=form_data)
	dni_extract = re.findall(r'<th>.*?</th>', dni_get.text)[4]
	dni = dni_extract.strip("</th>")

	api_url = ("https://apiperu.dev/api/dni/%s?api_token=%s" % (dni,api_token))

	datos = requests.get(api_url)

	print(datos.json())

if __name__ == '__main__':

	name = input("Cual es su nombre? : ").strip('\n')
	apell_p = input("Cual es su apellido paterno? : ").strip('\n')
	apell_m = input("Cual es su apellido materno? : ").strip('\n')
	get_dni(name, apell_p, apell_m)
