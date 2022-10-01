from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.views import APIView
from django.views import View
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate,login,logout
import datetime
from web3 import Web3

# Create your views here.


# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(17, GPIO.OUT)

# define public keys as user address of metamask
# define private keys of wallet of metamask
# public_key="""0xEaEd195caFDB768FB4864DE5089eF7abc881dF5e""",
private_key="0xb3067b0799888af49e37d3e6f2472f21c5aace1a5324f3b9f6a4f3a8508af070"

# infura url
# ropsten = 'https://api.sc.testnet.shimmer.network/chain/rms1prr4r7az8e46qhagz5atugjm6x0xrg27d84677e3lurg0s6s76jr59dw4ls/evm/jsonrpc'
ropsten = "https://goerli.infura.io/v3/4bbdcd3c6c064ae6a518e86f85076ca6"
# connect to ropsten infura url
web3 = Web3(Web3.HTTPProvider(ropsten))

# deployed contract address 

address = Web3.toChecksumAddress("0xA872f46f1250F6ed412f347E8985D1f0C92398fb")

# contract ABI 
abi="""[
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "uint8",
				"name": "_pin",
				"type": "uint8"
			},
			{
				"internalType": "bool",
				"name": "_isActive",
				"type": "bool"
			}
		],
		"name": "controlPin",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint8",
				"name": "",
				"type": "uint8"
			}
		],
		"name": "pinStatus",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
"""

contract_instance = web3.eth.contract(abi=abi, address=address)

class Toggle(View):
    def get(self,request):
        return render(request, 'pages/toggle.html')

    def post(self, request):
        # print("is working")

        check = True if request.POST.get('checked') == "on" else False
        nonce=web3.eth.getTransactionCount("0xEaEd195caFDB768FB4864DE5089eF7abc881dF5e")
        print(" status form HTML ",check)
        tx = contract_instance.functions.controlPin(15, check).build_transaction({
            'chainId': 5,
            'gas': 300000,
            'gasPrice': web3.toWei('40', 'gwei'),
            'nonce': nonce
        })
        
        singed_tx=web3.eth.account.signTransaction(tx, private_key)
        tx_hash=web3.eth.sendRawTransaction(singed_tx.rawTransaction)
        tx_ricept=web3.eth.wait_for_transaction_receipt(tx_hash)
        print("tx_ricept",tx_ricept)
        print("Trans hash:", tx_ricept['transactionHash'].hex())
        print("###############################################################################")
        pin_status=format(contract_instance.functions.pinStatus(15).call())
        print("pin_status",pin_status)
        return render(request, 'pages/toggle.html',{"state":pin_status})


def blockchain_integration(check):
    nonce=web3.eth.getTransactionCount("0xEaEd195caFDB768FB4864DE5089eF7abc881dF5e")
    print(" status form HTML ",check)
    tx = contract_instance.functions.controlPin(15, check).build_transaction({
        'chainId': 5,
        'gas': 300000,
        'gasPrice': web3.toWei('40', 'gwei'),
        'nonce': nonce
    })
    
    singed_tx=web3.eth.account.signTransaction(tx, private_key)
    tx_hash=web3.eth.sendRawTransaction(singed_tx.rawTransaction)
    tx_ricept=web3.eth.wait_for_transaction_receipt(tx_hash)
    print("tx_ricept",tx_ricept)
    print("Trans hash:", tx_ricept['transactionHash'].hex())
    print("###############################################################################")
    pin_status=format(contract_instance.functions.pinStatus(15).call())
    print("pin_status",pin_status)
    
    return pin_status


class LoginView(View):
    def get(self, request):
        print(datetime.datetime.now())
        return render(request, "login.html")
    
    def post(self, request):
        params = request.POST
        user = authenticate(email=params["email"], password=params["password"])
        if user is not None and user.user_type == "Admin":
            login(request,user)
            return HttpResponseRedirect("index/")
        else:
            return redirect("/")




class HomeView(View):  
    def get(self,request):
        context = {"user_data": MyUser.objects.all()}
        return render(request, 'pages/index.html',context)
    
    
class DetailView(View):
    def get(self, request, id):
        return render(request, 'pages/detailview.html', {"selected_user": MyUser.objects.get(id=id)})

   
# class blockchainApiView(APIView):
#     def post(self, request):
#         serializer = BlockchainSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'Status': '200.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeviceAPi(APIView):
    def post(self,request):
        data=request.data
        print(data)
        # pin_status = blockchain_integration(data['status'])
        pin_status = data['status']
        try:
            obj = MyUser.objects.get(device=data['device_id'])
            obj.device_type = data["device_type"]
        except:
            return Response({"status": status.HTTP_404_NOT_FOUND, "message": "device id not exist in our db."}, status=status.HTTP_404_NOT_FOUND)
        if pin_status == True:
            InDateTime(user=obj, in_date_time=datetime.datetime.now()).save()
            created_at = InDateTime.objects.last()
            return Response({"status": status.HTTP_200_OK, "created_at": created_at.id}, status=status.HTTP_200_OK)
        return Response({"status": status.HTTP_404_NOT_FOUND}, status. HTTP_404_NOT_FOUND)


class DeviceOutAPI(APIView):
    def post(self, request):
        data=request.data
        print(data)
        # pin_status = blockchain_integration(data['status'])
        pin_status = data['status']
        try:
            created_obj = InDateTime.objects.get(id=data["created_at"])
            if pin_status == False:
                OutDateTime(indate=created_obj, out_date_time=datetime.datetime.now()).save()
            return Response({"status": status.HTTP_200_OK, "message": "data updated successfully."})
        except Exception as e:
            print(e)
            return Response({"status": status.HTTP_404_NOT_FOUND, "message": "something went wrong."}, status.HTTP_404_NOT_FOUND)
