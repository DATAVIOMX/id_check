#!/usr/bin/env python3
"""
Client command line utility for id_check
"""


import argparse
import requests
import cv2
import json


URL_TXT = "http://localhost:5000/api/v1/id-check/text"  # Falta la base de la URL
URL_IMG = "http://localhost:5000/api/v1/id-check/images"

def prep_req_img(args):
    """
    Converts image to numpy array string
    """
    end_f = args.frente[-4:]
    end_b = args.reverso[-4:]
    # Necesitamos la forma del array tambien
    arr_f = cv2.imread(args.frente)
    arr_b = cv2.imread(args.reverso)
    str_f = json.dumps(arr_f.tolist())
    str_b = json.dumps(arr_b.tolist())
    adict = {"front": str_f, "back": str_b, "api_key": args.key,
             "shape_f":list(arr_f.shape), "shape_b": list(arr_b.shape)}
    print(adict["shape_f"], adict["shape_b"]) 
    return adict

def prep_req_txt(args):
    """
    Prepares a dictionary from args fields
    """
    adict = {}
    if args.tipo in ['a', 'b', 'c']:
        adict['cve-elector'] = args.cve
        adict['emision'] = args.emision
        adict['ocr'] = args.ocr
        adict['api_key'] = args.key
        adict['tipo'] = args.tipo
    if args.tipo in ['d', 'e']:
        adict['api_key'] = args.key
        adict['cic'] = args.cic
        adict['ocr'] = args.ocr
        adict['tipo'] = args.tipo
    return adict

def create_parser():
    """
    Create a parser instance and add arguments to it
    ADD SUBPARSERS FOR TEXT AND IMAGE
    https://stackoverflow.com/questions/9505898/
    conditional-command-line-arguments-in-python-using-argparse
    id_check-client -m t -t <tipo-credencial> -v <clave-elector>
        -e <emision> -o <ocr> -c <cic> -s <salida>
    id_check-client -m i -f <frente> -b <reverso> -s <salida>
    """
    parser = argparse.ArgumentParser(description="""CLI client for id_check it
    uses either a text mode validation or image mode validation""")
    parser.add_argument('-s', '--salida', help='output file', required=True)
    parser.add_argument('-k', '--key', help='API key', required=True)
    subparsers = parser.add_subparsers(dest='subcommand', help='options are text or image')
    subparsers.required = True
    parser_text = subparsers.add_parser('text')
    parser_text.add_argument('-t', '--tipo', choices=['a', 'b', 'c', 'd', 'e'],
                             required=True, help='id version ')
    parser_text.add_argument('-v', '--cve', help='clave elector')
    parser_text.add_argument('-e', '--emision', help='emision')
    parser_text.add_argument('-o', '--ocr', help='texto ocr')
    parser_text.add_argument('-c', '--cic', help='CIC')
    parser_image = subparsers.add_parser('image')
    parser_image.add_argument('-f', '--frente', required=True, help='imagen de frente')
    parser_image.add_argument('-b', '--reverso', required=True, help='imagen del reverso')
    return parser

def main():
    """
    Main function of the client, creates a parser, prepares requests and
    receives the response, writes raw HTML to a file, and prints the valid_yn or
    error to screen
    """
    parser = create_parser()
    args = parser.parse_args()
    if args.subcommand == 'text':
        # prepare request
        req = prep_req_txt(args)
        # send request
        response = requests.post(URL_TXT, data=req)
    if args.subcommand == 'image':
        # prepare request
        req = prep_req_img(args)
        # send request
        response = requests.post(URL_IMG, data=req)
    # Receive request
    print(response)
    full_resp = response.json()
    print(full_resp)
    # Check for errors
    if "content" in full_resp.keys():
        # write to file the raw HTML response
        outfile = open(args.salida, "w+")
        outfile.write(full_resp["content"])
        outfile.close()
        # print to STDOUT the valid_yn
        print(full_resp["valid_yn"])
    elif "Error" in full_resp.keys():
        print(full_resp["Error"])
    else:
        print({"Error": "response is None"})

if __name__ == "__main__":
    main()
