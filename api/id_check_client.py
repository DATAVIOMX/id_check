#!/usr/bin/env python3
"""
Client command line utility for id_check
"""


import argparse
import requests
import cv2


URL_TXT = "/api/v1/id-check/text"  # Falta la base de la URL
URL_IMG = "/api/v1/id-check/images"

def prep_req_img(args):
    """
    Converts image to numpy array string
    """
    end_f = args.front[-4:]
    end_b = args.back[-4:]
    # Necesitamos la forma del array tambien
    
    arr_f = cv2.imread(args["front"])
    arr_b = cv2.imread(args["front"])
    shape_f = list(arr_f.shape)
    shape_b = list(arr_b.shape)
    str_f = arr_f.tostring()
    str_b = arr_b.tostring()
    
    adict = {"front": str_f, "back": str_b, "api-key": args.key,
             "shape_f":shape_f, "shape_b": shape_b}
    return adict

def prep_req_txt(args):
    """
    Prepares a dictionary from args fields
    """
    adict = {}
    if args.tipo in ['a', 'b', 'c']:
        adict['cve-elector'] = args.cve
        adict['emision'] = args.emision
        adict['ocr-v'] = args.ocr
        adict['api-key'] = args.key
    if args.tipo in ['d', 'e']:
        adict['api-key'] = args.key
        adict['cic'] = args.cic
        adict['ocr-h'] = args.ocr
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
    parser.add_argument('-s', '--salida', help='archivo de salida')
    parser.add_argument('-k', '--key', help='API key')
    subparsers = parser.add_subparsers(dest='subcommand')
    parser_text = subparsers.add_parser('text')
    parser_text.add_argument('-t', '--tipo', choices=['a', 'b', 'c', 'd', 'e'],
                             required=True, help='id version')
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
    print(args.subcommand)
    print(args)
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
    full_resp = response.json()
    # Check for errors
    if full_resp["Error"]:
        print(full_resp["Error"])
        return -1
    if all(["content", "valid_yn"]) in full_resp.keys:
        # write to file the raw HTML response
        outfile = open(args.salida, "w")
        outfile.write(full_resp["content"])
        outfile.close()
        # print to STDOUT the valid_yn
        print(response["valid_yn"])
        return 0
    return -1
if __name__ == "__main__":
    main()
