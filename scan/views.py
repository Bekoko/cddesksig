from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import time 
# cv
import cv2
import imutils
from pyzbar import pyzbar
from imutils.video import VideoStream
# import ecdsa
from .cryptos import *
# from django import forms
from django import forms
# verify
from eth_account import Account
# sign message
from eth_account.messages import encode_defunct
# randome gen
import secrets
# eval
import ast
# regex to add space
import re
# from bitcoin import *
from .utils import *


COIN = [
    ('Select', ('Select')),
    ('BTC',('Bitcoin (BTC)')),
    ('ETH',('Ethereum (ETH)')),
]

OPERATION = [
    ('Select', ('Select')),
    ('address', ('Crypto Address')),    
    ('message',('Sign Message')),
    ('transaction',('Sign Transaction')),
]


class StartForm(forms.Form):
    """
    """           
    def __init__(self, *args, **kwargs):
        super(StartForm, self).__init__(*args, **kwargs)

        self.fields['data_to_sign'].strip = False
        # self.fields['data_to_sign'].empty_value = True

    attr = { 
        "name":"data_to_sign",
    }

    data_to_sign = forms.CharField(
        required=False,
        max_length=100000,
        label="Data to sign",
        widget=forms.Textarea(attrs=attr),

    )     

    coin = forms.ChoiceField(
        choices=COIN,
        required=False,
        label="Coin",
    )

    operation = forms.ChoiceField(
        choices=OPERATION,
        required=True,
        label="Operation",
)


# Create your views here.
def scan(request,*args,**kwargs):
    """
    to wif priv key = https://github.com/crcarlo/btcwif/blob/master/btcwif.py#L63
    """
    # params
    coin = None
    operation = None
    barcodeData = None
    signature = None    

    form = StartForm(request.POST or None)
    if form.is_valid():

        # video capture
        vs = VideoStream(src=0).start()
        time.sleep(2.0)

        while True:

            frame = vs.read()
            frame = imutils.resize(frame, width=600)
            barcodes = pyzbar.decode(frame)

            try:
                for barcode in barcodes:
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    barcodeData = barcode.data.decode("utf-8")
                    barcodeType = barcode.type
                    text = "{} ({})".format(barcodeData, barcodeType)
                    cv2.putText(frame, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    if barcodeData:
                        print("barcodeData cam",barcodeData)
                        raise barcodeData
            except:
                if barcodeData:
                    break

            exit_key = ("Press any key to stop video")
            cv2.putText(frame, str(exit_key),(10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (138, 107, 0), 2)                                    # color code order is inversed
            # yield(b'--frame\r\n'
            #       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            cv2.imshow("Barcode Scanner", frame)
            key = cv2.waitKey(1) & 0xFF
            if key != 255:                                                                          # verify if it changes
                break

        cv2.destroyAllWindows()
        vs.stop()   
          
        coin = form.cleaned_data.get('coin')
        operation = form.cleaned_data.get('operation')
        data_to_sign = form.cleaned_data.get('data_to_sign')

        # remove \r from text
        data_to_sign = data_to_sign.replace('\r', '')

        # priv for tests
        # barcodeData = "F34F5F802635A4402ABB6B1A2FC1371DBDC0AE9BD067E72E6AFA4AFCFEAA38CF"

        if operation == "address":

            signature = barcodeData

            context = {
                'form':form,
                'operation':operation,
                'signature': signature,
            }
            return render(request, 'scan/scan.html', context)


        if coin == "BTC":

            try:   

                if operation == "message":
     
                    # wif = privToWif(barcodeData)
                    signature = ecdsa_sign(data_to_sign,barcodeData)

                    # signature = chr(ord(signature[0]) + 1) + signature[1:]

                    # # verify
                    pub=ecdsa_recover(data_to_sign, signature)
                    assert ecdsa_verify(data_to_sign,signature,pub) is True

                else:

                    c = Bitcoin()                                    
                    data_to_sign_dict=ast.literal_eval(data_to_sign)
                    sig = c.sign(data_to_sign_dict,0,barcodeData)  
                    signature = str(sig)                                  

            except:

                messages.warning(request, (
                    "BTC Signature provided not valid. \n"
                    "Please try again with new signature."
                    )
                )               
                return redirect(request.get_full_path())  

        elif coin == "ETH":

            try:

                if operation == "message":                

                    # sign message
                    message = encode_defunct(text=data_to_sign)
                    signed_message = Account.sign_message(message, private_key=barcodeData)
                    sig = signed_message.signature
                    signature = sig.hex()

                    # print("len(message)",len(data_to_sign))
                    # print("len(signature)",len(signature))

                    r = Account.recover_message(message,signature=signature)
                    # print("r",r)

                else:

                    # convert string to dict
                    data_to_sign_dict =ast.literal_eval(data_to_sign)                    

                    signed_transaction = Account.sign_transaction(data_to_sign_dict, barcodeData)
                    signature_hex = signed_transaction.rawTransaction

                    # convert HexBytes to string
                    signature = str(signature_hex)

            except:
                messages.warning(request, (
                    "ETH Signature provided not valid. \n"
                    "Please try again with new signature."
                    )
                )               
                return redirect(request.get_full_path())

        # attribut new value to memory place having read private keys
        barcodeData = 0

    context = {
        'form':form,
        'operation':operation,
        'signature': signature,
    }
    return render(request, 'scan/scan.html', context)





















