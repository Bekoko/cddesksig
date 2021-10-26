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

COIN = [
    ('Select', ('Select')),
    ('BTC',('Bitcoin (BTC)')),
    ('ETH',('Ethereum (ETH)')),
]

OPERATION = [
    ('message',('Sign Message')),
    ('transaction',('Sign Transaction')),
]


class StartForm(forms.Form):
    """
    """           
    attr = {
    "name":"data_to_sign"
    }
    data_to_sign = forms.CharField(
        required=True,
        max_length=100000,
        label="Data to sign",
        widget=forms.TextInput(attrs=attr),
    )     

    coin = forms.ChoiceField(
        choices=COIN,
        required=True,
        label="Coin",
    )

    operation = forms.ChoiceField(
        choices=OPERATION,
        required=True,
        label="Operation",
    )   


# Create your views here.
def scan(request,*args,**kwargs):

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
                        print("barcodeData",barcodeData)
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
            
        data_to_sign = form.cleaned_data.get('data_to_sign')
        print("len(data_to_sign)",data_to_sign,len(data_to_sign))
        # add blank space after "message." using r'\1<space>'
        data_to_sign = re.sub(r'(sign this message\.)', r'\1 ', data_to_sign)
        # print("len(data_to_sign)",data_to_sign,len(data_to_sign))
        
        coin = form.cleaned_data.get('coin')
        operation = form.cleaned_data.get('operation')

        if coin == "BTC":

            try:   

                if operation == "message":

                    # sign message
                    signature = ecdsa_sign(data_to_sign,barcodeData,coin)

                    # verify
                    print("privtoaddr",Bitcoin().privtoaddr(barcodeData))
                    print("ecdsa_recover",ecdsa_recover(data_to_sign, signature))
                    pub=ecdsa_recover(data_to_sign, signature)
                    print("ecdsa_verify",ecdsa_verify(data_to_sign,signature,pub))

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

                    print("len(message)",len(data_to_sign))
                    print("len(signature)",len(signature))

                    r = Account.recover_message(message,signature=signature)
                    print("r",r)

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


    context = {
        'form':form,
        'operation':operation,
        'signature': signature,
    }
    return render(request, 'scan/scan.html', context)


