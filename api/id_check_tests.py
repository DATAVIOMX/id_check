#!/usr/bin/env python3
"""
Simple test suite for the functions
"""
import cv2
import id_check

def t001():
    """
    Test get_qr
    Condition: if img is None return None 
    """
    img = None
    result = id_check.get_qr(img)
    if result is None:
        return "OK"

def t002():
    """
    Test get_qr
    Condition: image exists but has no QR, return None
    """
    img = cv2.imread('lena.png')
    result = id_check.get_qr(img)
    if result is None:
        return "OK"

def t003():
    """
    Test get_qr
    Condition: image exists and has QR, return url
    """
    url = "http://www.motoko-research.com"
    img = cv2.imread('frame.png')
    result = id_check.get_qr(img)
    if result == url:
        return "OK"
    else:
        return "ERROR", result, url

def t004():
    """
    Test query_qr
    Condition: url is None, returns None
    """
    url = None
    result = id_check.query_qr(url)
    if result == None:
        return "OK"
    else:
        return "ERROR not None response with None URL"

def t005():
    """
    Test query_qr
    Condition: url is not valid, returns None
    """
    url = "perro"
    result = id_check.query_qr(url)
    if result == None:
        return "OK"
    else:
        return "ERROR not None response with invalid URL"

def t006():
    """
    Test query_qr
    Condition: url is None, returns None
    """
    url = "http://www.google.com"
    result = id_check.query_qr(url)
    if result is not None:
        return "OK", result[:50]
    else:
        return "ERROR not None response with invalid URL"

def t007():
    """
    Test clean_qr_response
    Condition: Response is None; returns None
    """
    inp = None
    result = id_check.clean_qr_response(inp)
    if result == None:
        return "OK"
    else:
        return "ERROR not None result"

def t008():
    """
    Test clean_qr_response
    Condition: Response is invalid; returns None
    """
    inp = "www.google.com"
    result = id_check.clean_qr_response(inp)
    if result == None:
        return "OK"
    else:
        return "ERROR no valid_yn"


def t009():
    """
    Test clean_qr_response
    Condition: Response is valid; returns response and validyn
    """
    inp = ""  # some HTML
    result = id_check.clean_qr_response(inp)
    if result['valid_yn'] == "valido":
        return "OK"
    else:
        return "ERROR no valid_yn"

def t010():
    """
    Test prep_img
    Condition: image is None; returns None
    """
    inp = None
    result = id_check.prep_img(inp)
    if result is None:
        return "OK"
    else:
        return "ERROR Invalid output for None input"

def t011():
    """
    Test prep_img
    Condition: image is valid; returns array of processed images
    """
    img = cv2.imread('lena.jpg')
    result = id_check.prep_img(img)
    for r in result:
        cv2.imshow("image", r)
        cv2.waitKey(0)
    return "OK"

def t012():
    """
    Test ocr_img
    Condition: image is None; returns None
    """
    
    

def t014():
    """
    Test ocr_img
    Condition: image is not None returns text
    """
    pass

# def t016():
    # pass

# def t017():
    # pass

# def t018():
    # pass

# def t019():
    # pass

# def t020():
    # pass

# def t021():
    # pass

# def t022():
    # pass

# def t023():
    # pass

# def t024():
    # pass

# def t025():
    # pass

# def t026():
    # pass

# def t027():
    # pass

# def t028():
    # pass

# def t029():
    # pass

# def t030():
    # pass

# def t031():
    # pass

# def t032():
    # pass

# def t033():
    # pass


# def t034():
    # pass

# def t035():
    # pass

# def t036():
    # pass


if __name__=='__main__':
    print("T001", t001())
    print("T002", t002())
    print("T003", t003())
    print("T004", t004())
    print("T005", t005())
    print("T006", t006())
    print("T007", t007())
    print("T008", t008())
    # print("T009", t009())
    print("T010", t010())
    # print("T011", t011())
    print("T012", t012())
    print("T013", t013())
    # print("T014", t014())
    # print("T015", t015())
    # print("T016", t016())
    # print("T017", t017())
    # print("T018", t018())
    # print("T019", t019())
    # print("T020", t020())
    # print("T021", t021())
    # print("T022", t022())
    # print("T023", t023())
    # print("T024", t024())
    # print("T025", t025())
    # print("T026", t026())
    # print("T027", t027())
    # print("T028", t028())
    # print("T029", t029())
    # print("T030", t030())
    # print("T031", t031())
    # print("T032", t032())
    # print("T033", t033())
    # print("T034", t034())
