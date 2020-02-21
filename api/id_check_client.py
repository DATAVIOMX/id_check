#!/usr/bin/env python3
"""
Client command line utility for id_check
"""


import argparse
import requests
import cv2


def prep_req_img(args):
    """
    Converts image to numpy array string
    """
    end_f = args.front[-4:]
    end_b = args.back[-4:]
    str_f = cv2.imencode(end_f, args.front)[1].tostring()
    str_b = cv2.imencode(end_b, args.back)[1].tostring()
    adict = {"front": str_f, "back": str_b, "api-key": args.key}
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
        response = requests.post('http://', data=req)
    if args.subcommand == 'image':
        # prepare request
        req = prep_req_img(args)
        # send request
        response = requests.post('http://', data=req)
    # Receive request
    full_resp = response.json()
    # Check for errors
    if full_resp["Error"]:
        print(full_resp["Error"])
        return -1
    if all(["", "valid_yn"]) in full_resp.keys:
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
