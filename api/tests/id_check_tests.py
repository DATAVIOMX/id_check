#!/usr/bin/env python3
"""
Simple test suite for the functions
"""
import numpy as np
import cv2
from bs4 import BeautifulSoup
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
    inp = """

<script language="JavaScript">
if (top.location != self.location){top.location = self.location;}
</script>

<head><meta http-equiv=X-Frame-Options content=deny></head><head><meta http-equiv=X-Frame-Options content=deny></head><!DOCTYPE html>
<html lang="es">
<head>
    <meta http-equiv="X-Frame-Options" content="deny">
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Servicios de Informacion</title>
    <!-- Bootstrap -->
    <link href="media-queries.css" rel="stylesheet">

<!-- GOOGLE ANALITICS-->
	<script>
	  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
	  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
	  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
	  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
	
	  ga('create', 'UA-39814429-4', 'ife.org.mx');
	  ga('send', 'pageview');
	</script>
<!--PARA FACEBOK-->
<div id="fb-root"></div>
<script>(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/es_LA/sdk.js#xfbml=1&version=v2.3";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));</script>
<script language="JavaScript">
<!--// evito que se cargue en otro frame
if (top.location != self.location){top.location = self.location;}
//-->
</script>
	
</head>

<body alink="#ffffff" class="container" onLoad="setTimeout('enviar()', 00000)" > <!-- es en milesimas de segundo 5000 = 5 segundos -->
<script>
  if (self == top) {
    var theBody = document.getElementsByTagName('body')[0]
    theBody.style.display = "block"
  } else {
    top.location = self.location
  }
</script>

<script>
function soloNumeros(e){
        var key = window.Event ? e.which : e.keyCode
        return (key >= 48 && key <= 57)
}

</script>

<div id="pagewrap">

                <div id="header">
                                <div  id="headerizq" >
                                        <a href="http://www.ine.mx/es/web/portal/inicio" target="_blank"><img src="images/logoINE.png"  width="97%" ></a>
                                </div>
                                <div id="headerder">
                                        <span class="text_cabecera"><input type="image" src="images/banner.png" width=100%></span>
                                </div>
                </div>
                <div id="nensaje_rapido" >
<table border=0 >
<tr>
<td width=30%>
                                	<div id="ima_msj"><input type="image" src="images/SII.png" width=100%></div>
</td>
<td width=70%>
					<div id="menje" ><p>Est&aacute; vigente como medio de identificaci&oacute;n, y puedes votar.</p></div>
</td>
</tr>
</table>
                                                        </div>
                <div id="content" >

       <div id="elemento1">

        <form enctype="multipart/form-data" action="https://listanominal.ine.mx/scpln/src/" method="post" target="_self">
        <input type="hidden" name="boton" value="8" pattern="[8]{1}"  maxlength="1"                             onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="e" value="9" pattern="[0-9]{1,2}"  maxlength="2"          onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="s" value="3779" pattern="[0-9]{1,4}"  maxlength="4"        onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="modulo" value="999999"     onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="CIC" value="121254481" pattern="[0-9]{1,9}"  maxlength="9"            onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="salto" value="1" pattern="[1]{1}"   maxlength="1" onKeyPress="return soloNumeros(event)">
        <input type="hidden" value="SI" name="con_cic"  pattern="[SI]{1,2}" >
        <input type="IMAGE"  name="buscar" value="" src="images/botonera2_01.png"   width="100%" />
        </form>
        </div>
       <div id="elemento1">

        <form enctype="multipart/form-data" action="https://ubicatucasilla.ine.mx" method="post" target="_self">
        <input type="hidden" name="boton" value="8" pattern="[8]{1}"  maxlength="1"                             onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="e" value="9" pattern="[0-9]{1,2}"  maxlength="2"          onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="s" value="3779" pattern="[0-9]{1,4}"  maxlength="4"        onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="modulo" value="999999"     onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="CIC" value="121254481" pattern="[0-9]{1,9}"  maxlength="9"            onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="salto" value="1" pattern="[1]{1}"   maxlength="1" onKeyPress="return soloNumeros(event)">
        <input type="hidden" value="SI" name="con_cic"  pattern="[SI]{1,2}" >
        <input type="IMAGE"  name="buscar" value="" src="images/botonera2_02.png"   width="100%" />
        </form>
        </div>
       <div id="elemento1">

        <form enctype="multipart/form-data" action="http://ubicatumodulo.ife.org.mx/" method="post" target="_self">
        <input type="hidden" name="boton" value="8" pattern="[8]{1}"  maxlength="1"                             onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="e" value="9" pattern="[0-9]{1,2}"  maxlength="2"          onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="s" value="3779" pattern="[0-9]{1,4}"  maxlength="4"        onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="modulo" value="999999"     onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="CIC" value="121254481" pattern="[0-9]{1,9}"  maxlength="9"            onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="salto" value="1" pattern="[1]{1}"   maxlength="1" onKeyPress="return soloNumeros(event)">
        <input type="hidden" value="SI" name="con_cic"  pattern="[SI]{1,2}" >
        <input type="IMAGE"  name="buscar" value="" src="images/botonera2_03.png"   width="100%" />
        </form>
        </div>
       <div id="elemento1">

        <form enctype="multipart/form-data" action="https://app-inter.ife.org.mx/siac2011/citas_initCapturaCitas.siac" method="post" target="_self">
        <input type="hidden" name="boton" value="8" pattern="[8]{1}"  maxlength="1"                             onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="e" value="9" pattern="[0-9]{1,2}"  maxlength="2"          onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="s" value="3779" pattern="[0-9]{1,4}"  maxlength="4"        onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="modulo" value="999999"     onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="CIC" value="121254481" pattern="[0-9]{1,9}"  maxlength="9"            onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="salto" value="1" pattern="[1]{1}"   maxlength="1" onKeyPress="return soloNumeros(event)">
        <input type="hidden" value="SI" name="con_cic"  pattern="[SI]{1,2}" >
        <input type="IMAGE"  name="buscar" value="" src="images/botonera2_04.png"   width="100%" />
        </form>
        </div>
       <div id="elemento1">

        <form enctype="multipart/form-data" action="http://www.ine.mx/archivos2/portal/credencial/tramite/" method="post" target="_self">
        <input type="hidden" name="boton" value="8" pattern="[8]{1}"  maxlength="1"                             onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="e" value="9" pattern="[0-9]{1,2}"  maxlength="2"          onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="s" value="3779" pattern="[0-9]{1,4}"  maxlength="4"        onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="modulo" value="999999"     onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="CIC" value="121254481" pattern="[0-9]{1,9}"  maxlength="9"            onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="salto" value="1" pattern="[1]{1}"   maxlength="1" onKeyPress="return soloNumeros(event)">
        <input type="hidden" value="SI" name="con_cic"  pattern="[SI]{1,2}" >
        <input type="IMAGE"  name="buscar" value="" src="images/botonera2_05.png"   width="100%" />
        </form>
        </div>
       <div id="elemento1">

        <form enctype="multipart/form-data" action="http://www.ine.mx/archivos2/previo/credencial/tramite" method="post" target="_self">
        <input type="hidden" name="boton" value="8" pattern="[8]{1}"  maxlength="1"                             onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="e" value="9" pattern="[0-9]{1,2}"  maxlength="2"          onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="s" value="3779" pattern="[0-9]{1,4}"  maxlength="4"        onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="modulo" value="999999"     onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="CIC" value="121254481" pattern="[0-9]{1,9}"  maxlength="9"            onKeyPress="return soloNumeros(event)">
        <input type="hidden" name="salto" value="1" pattern="[1]{1}"   maxlength="1" onKeyPress="return soloNumeros(event)">
        <input type="hidden" value="SI" name="con_cic"  pattern="[SI]{1,2}" >
        <input type="IMAGE"  name="buscar" value="" src="images/botonera2_06.png"   width="100%" />
        </form>
        </div>

                </div>



                <div id="footer">
                        <span class="text_gris2">
                                Si tienes dudas llama a
                        </span>
                        <span class="subtitulo">
                                INETEL
                        </span>
                        <span class="text_gris2">
                                al
                        </span>
                        <span class="subtitulo">
                                01 800 433 2000.
                        </span>
                        <span class="text_gris2"><br>
                                La llamada no tiene costo y puedes realizarla desde cualquier parte del pa&iacute;s.
                        </span>

                </div>

</div>

	

	
	<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>
</body>
</html>
"""  # some HTML
    result = id_check.clean_qr_response(inp)
    if result['valid_yn'] == "Y":
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
    img = cv2.imread('test22.jpg')
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
    inp = None
    result = id_check.ocr_img(inp)
    if result is None:
        return "OK"
    else:
        return "ERROR Invalid output for None input"
    

def t013():
    """
    Test ocr_img
    Condition: image is not None returns text
    """
    inp = [cv2.imread("esp.helvetica.exp1.png")]
    result = id_check.ocr_img(inp)
    if result is not None:
        return "OK", result
    else:
        return "ERROR, not returning anything"

def t014():
    """
    Test proc_text
    Condition: text is None; result is None
    """
    inp = None
    inp2 = None
    result = id_check.proc_text(inp, inp2)
    if result is None:
        return "OK"
    else:
        return "ERROR Invalid output for None input"

def t015():
    """
    Test proc_text
    Condition: text is not None but invalid; result is None
    """
    inp = """
    este era un perro que una vez
    dijo 3 palabras:
    Chinguen su madre
    """
    inp2 = "d"
    result = id_check.proc_text(inp, inp2)
    if result is None:
        return "OK"
    else:
        return "ERROR Invalid output for None input", result

def t016():
    """
    Test proc_text
    Condition: text is not None; result is dict
    """
    inp = """
    HHHROT84062109H500
    IDMEX1212544810<<3779071056199
    8406217H2412311MEX<01<<38062<4
    HAHN<HERRERA<<OTTO<<<<<<<<<<<<
    """
    inp2 = "d"
    result = id_check.proc_text(inp, inp2)
    print(result)
    if result is not None:
        return "OK", result
    else:
        return "ERROR None output for valid input"

def t017():
    """
    get_id_type
    Condition text is None; result None
    """
    inp = None
    result = id_check.get_id_type(inp)
    if result is None:
        return "OK"
    else:
        return "ERROR Invalid output for None input"

def t018():
    """
    get_id_type
    Condition text is not None but useless; result None
    """
    inp = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore 
    magna aliqua.
    """
    result = id_check.get_id_type(inp)
    if result is None:
        return "OK"
    else:
        return "ERROR Invalid output for invalid input"

def t019():
    """
    get_id_type
    Condition: Text is Valid; returns 'd'
    """
    inp = """
    MEXICO INSTITUTO NACIONAL ELECTORAL
    CREDENCIAL PARA VOTAR
    NOMBRE FECHA DE NACIMIENTO
    HAHN        21/06/1984
    HERRERA       SEXO H
    OTTO
    DOMICILIO
    AV INSURGENTES SUR 3493 E 1 203
    COL VILLA OLIMPICA 14020
    TLALPAN D.F.
    
    CLAVE DE ELECTOR HHHROT84062109H500
    CURP HAHO840621HDFHRT04 ANO DE REGISTRO   2005 01
    
    ESTADO 09 MUNICIPIO 012  SECCION 3779
    LOCALIDAD 0001    EMISION 2014  VIGENCIA 2024
    IDMEX1212544810<<3779071056199
    8406217H2412311MEX<01<<38062<4
    HAHN<HERRERA<<OTTO<<<<<<<<<<<<
    """
    result = id_check.get_id_type(inp)
    if result == "e":
        return "OK", result
    else:
        return "ERROR Invalid output for invalid input", result

def t020():
    """
    proc-ocr_text
    Condition: Text is None; returns None
    """
    inp = None
    result = id_check.proc_ocr_text(inp)
    if result is None:
        return "OK"
    else:
        return "ERROR Invalid output for None input"

def t021():
    """
    proc_ocr_text
    Condition: Text is not None but useless; returns None
    """
    inp = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore 
    magna aliqua.
    """
    result = id_check.proc_ocr_text(inp)
    if result is None:
        return "OK"
    else:
        return "ERROR Invalid output for invalid input"

def t022():
    """
    proc_ocr_text
    Condition: Text is not None, useful; returns dict
    """
    inp = """
    MEXICO INSTITUTO NACIONAL ELECTORAL
    CREDENCIAL PARA VOTAR
    NOMBRE FECHA DE NACIMIENTO
    HAHN        21/06/1984
    HERRERA       SEXO H
    OTTO
    DOMICILIO
    AV INSURGENTES SUR 3493 E 1 203
    COL VILLA OLIMPICA 14020
    TLALPAN D.F.
    
    CLAVE DE ELECTOR HHHROT84062109H500
    CURP HAHO840621HDFHRT04 ANO DE REGISTRO   2005 01
    
    ESTADO 09 MUNICIPIO 012  SECCION 3779
    LOCALIDAD 0001    EMISION 2014  VIGENCIA 2024
    IDMEX1212544810<<3779071056199
    8406217H2412311MEX<01<<38062<4
    HAHN<HERRERA<<OTTO<<<<<<<<<<<<
    """
    result = id_check.proc_ocr_text(inp)
    if result is not None:
        return "OK", result
    else:
        return "ERROR Invalid output for valid input"

def t023():
    """
    query_web
    Condition: data load is None; returns None
    """
    inp = None
    result = id_check.query_web(inp)
    if result is None:
        return "OK"
    else:
        return "ERROR Invalid output for invalid input"

def t024():
    """
    query_web
    Condition: data load is invalid; returns None
    """
    inp = {"data1":"data", "data2":"data"}
    result = id_check.query_web(inp)
    if result is None:
        return "OK"
    else:
        return "ERROR, invalid output for invalid input"

def t025():
    """
    query_web
    Condition: data load is valid; returns HTML and valid_yn
    """
    inp = {"tipo":"e", "cic":"121554481", "ocr_h":"071056199"}
    result = id_check.query_web(inp)
    if result:
        return "OK", result
    else:
        return "ERROR in response"

def t026():
    """
    proc_web_response
    Condition: response is None; returns None
    """
    inp = None
    result = id_check.proc_web_response(inp)
    if result is None:
        return "OK"
    else:
        return "ERROR in response"

def t027():
    """
    proc_web_response
    Condition: response is not None but invalid; returns None
    """
    inp = BeautifulSoup("<html>this is a  text</html>", "html.parser")
    out_dict = {}
    result = id_check.proc_web_response(inp)
    if result is None:
        return "OK"
    else:
        return "ERROR in response"

def t028():
    """
    proc_web_response
    Condition: content is valid; returns dict
    """
    inp = BeautifulSoup("""
    <html>
    <head>
        <title>
        A Simple HTML Document
        </title>
    </head>
    <body>
        <p>This is a very simple HTML document</p>
        <div class="col-md-7">
        <h4 style="color:#d50080;">Esta vigente como medio de identificación y puedes votar.</h4>
        </div>
        <p>It only has two paragraphs</p>
    </body>
    </html>
    """, "html.parser")
    result = id_check.proc_web_response(inp)
    if result:
        return "OK", result["valid_yn"]
    else:
        return "ERROR in response"

def t029():
    """
    check_id_text
    Condition: input is None; returns Error dictionary
    """
    inp = None
    result = id_check.check_id_text(inp)
    if result == {"Error": "Input is empty"}:
        return "OK"
    else:
        return "Error, bad processing"

def t030():
    """
    check_id_text
    Condition: input is invalid; returns Error dictionary
    """
    inp = {"something":"bad"}
    result = id_check.check_id_text(inp)
    if result["Error"] == "Invalid input":
        return "OK"
    else:
        return "Error, bad processing"

def t031():
    """
    check_id_text
    Condition: input is valid; returns dictionary with HTML and valid_yn
    """
    # "tipo", "cve_elec", "num_emis", "ocr_v"
    inp = {"tipo":"e", "cic": "121254481", "ocr_h": "3779071056199"}
    result = id_check.check_id_text(inp)
    if result:
        return "OK", result
    if result["Error"]:
        return result

def t032():
    """
    check_id_img
    Condition: input is None returns error dictionary
    """
    inp = None
    inp2 = None
    result = id_check.check_id_img(inp, inp2)
    if result["Error"] == "Input is empty":
        return "OK"
    else:
        return "Error, bad processing"

def t033():
    """
    check_id_img
    Condition: input is invalid; returns error dictionary
    """
    inp1 = cv2.imread("lena.jpg")
    inp2 = cv2.imread("lena.jpg")
    result = id_check.check_id_img(inp1, inp2)
    if result == {"Error": "invalid input"}:
        return "OK"
    else:
        return "Error, bad processing"

def t034():
    """
    check_img_id
    Condition images are valid; returns dictionary with HTML and valid_yn
    """
    inp1 = cv2.imread("test34_front.jpg")
    inp2 = cv2.imread("test22.jpg")
    result = id_check.check_id_img(inp1, inp2)
    if result["valid_yn"] == "Y":
        return "OK", result
    else:
        return "Error, bad processing"

if __name__=='__main__':
    #print("T001", t001())
    #print("T002", t002())
    print("T003", t003())
    #print("T004", t004())
    #print("T005", t005())
    #print("T006", t006())
    #print("T007", t007())
    #print("T008", t008())
    #print("T009", t009())
    #print("T010", t010())
    #print("T011", t011())
    #print("T012", t012())
    #print("T013", t013())
    #print("T014", t014())
    #print("T015", t015())
    #print("T016", t016())
    #print("T017", t017())
    #print("T018", t018())
    #print("T019", t019())
    #print("T020", t020())
    #print("T021", t021())
    #print("T022", t022())
    #print("T023", t023())
    #print("T024", t024())
    #print("T025", t025())
    #print("T026", t026())
    #print("T027", t027())
    #print("T028", t028())
    #print("T029", t029())
    #print("T030", t030())
    #print("T031", t031())
    #print("T032", t032())
    print("T033", t033())
    #print("T034", t034())
