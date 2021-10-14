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
from bitcoin import *
# from django import forms
from django import forms
# verify
from eth_account import Account
from cryptoaddress import BitcoinAddress, EthereumAddress
# sign message
from eth_account.messages import encode_defunct

COIN = [
    ('Select', ('Select')),
    ('BTC',('Bitcoin (BTC)')),
    ('ETH',('Ethereum (ETH)')),
]


class StartForm(forms.Form):
    """
    """           
    attr = {
    "name":"message_to_sign"
    }
    message_to_sign = forms.CharField(
        required=True,
        max_length=100000,
        label="Message to sign",
        widget=forms.TextInput(attrs=attr),
    )     

    coin = forms.ChoiceField(
        choices=COIN,
        required=True,
        label="Coin",
    )   

# Create your views here.
def scan(request,*args,**kwargs):

    # params
    coin = None
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
            
        # for eth
        # barcodeData = '8da4ef21b864d2cc526dbdb2a120bd2874c36c9d0a1fb7f8c63d7f7a8b41de8f'
        # for btc
        # barcodeData = '57c617d9b4e1f7af6ec97ca2ff57e94a28279a7eedd4d12a99fa11170e94f5a4'


        message_to_sign = form.cleaned_data.get('message_to_sign')
        coin = form.cleaned_data.get('coin')

        if coin == "BTC":
            try:    
                # sign message
                signature = ecdsa_sign(message_to_sign,barcodeData)

            except:

                messages.warning(request, (
                    "Signature provided not valid. \n"
                    "Please try again with new signature."
                    )
                )               
                return redirect(request.get_full_path())  

        elif coin == "ETH":
            try:

                # sign message
                message = encode_defunct(text=message_to_sign)
                signed_message = Account.sign_message(message, private_key=barcodeData)
                sig = signed_message.signature
                signature = sig.hex()

            except:
                messages.warning(request, (
                    "Signature provided not valid. \n"
                    "Please try again with new signature."
                    )
                )               
                return redirect(request.get_full_path())


    context = {
        'form':form,
        'signature': signature,
    }
    return render(request, 'scan/scan.html', context)


