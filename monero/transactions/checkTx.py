from monero import base58 as cnBase58
from monero.base58 import _binToHex as bintohex
from monero import ed25519
from config import *
#var der = generate_key_derivation(pub, sec)
from generate_key_derivation import generate_key_derivation
from derive_public_key import derive_public_key

#var pubkey = derive_public_key(der, i, spk)
import re
dataHashTag=''
'''
dataHashTag = document.getElementById('dataHash');
if (dataHashTag !== null){
    hashUpdate(document.getElementById('theData').value);
}
function hashUpdate(data){
    dataHashTag.value = keccak_256(data);
}
'''
def validate_hex_color(color):
    pattern = r'^#?([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$'
    return bool(re.match(pattern, color))

def validHex(hex):
    #print('validHex',hex)
    pattern = r"[0-9A-Fa-f]"*len(hex)
    return bool(re.match(pattern, hex))
'''
function validHex(hex){
    var exp = new RegExp("[0-9a-fA-F]{" + hex.length + "}");
    return exp.test(hex);
}
'''

#pip install pycryptodome
from Crypto.Hash import keccak
def cn_fast_hash(str):
    k = keccak.new(digest_bits=256)
    k.update(bytearray.fromhex(str))
    return k.hexdigest()

'''
this.cn_fast_hash = function(input, inlen) {
    /*if (inlen === undefined || !inlen) {
        inlen = Math.floor(input.length / 2);
    }*/
    if (input.length % 2 !== 0 || !this.valid_hex(input)) {
        throw "Input invalid";
    }
    //update to use new keccak impl (approx 45x faster)
    //var state = this.keccak(input, inlen, HASH_STATE_BYTES);
    //return state.substr(0, HASH_SIZE * 2);
    return keccak_256(hextobin(input));
};
'''
def sec_key_to_pub(sec):
    return ed25519.public_from_secret_hex(sec)
'''
private view key -> public view key
this.sec_key_to_pub = function(sec) {
    var input = hextobin(sec);
    if (input.length !== 32) {
        throw "Invalid input length";
    }
    var input_mem = Module._malloc(KEY_SIZE);
    Module.HEAPU8.set(input, input_mem);
    var ge_p3 = Module._malloc(STRUCT_SIZES.GE_P3);
    var out_mem = Module._malloc(KEY_SIZE);
    Module.ccall('ge_scalarmult_base', 'void', ['number', 'number'], [ge_p3, input_mem]);
    Module.ccall('ge_p3_tobytes', 'void', ['number', 'number'], [out_mem, ge_p3]);
    var output = Module.HEAPU8.subarray(out_mem, out_mem + KEY_SIZE);
    Module._free(ge_p3);
    Module._free(input_mem);
    Module._free(out_mem);
    return bintohex(output);
};
'''
api = "http://moneroblocks.info/api/"
'''
var api = "http://moneroblocks.info/api/";
'''
'''
function bintohex(bin) {
    var out = [];
    for (var i = 0; i < bin.length; ++i) {
        out.push(("0" + bin[i].toString(16)).slice(-2));
    }
    return out.join("");
}
'''
'''
from monero.transaction.extra import ExtraParser
print(test_res['transaction_data']['extra'])
e = ExtraParser(test_res['transaction_data']['extra'])
print(e.parse()['pubkeys'][0].hex())
'''

def parseExtra(bin):
    extra = {
        'pub': False,
        'paymentId': False
    }
    if bin[0] == 1: #pubkey is tag 1
        extra['pub'] = bintohex(bin[1: 33]) #pubkey is 32 bytes
        #print(bin,len(bin))
        if len(bin)>33 and (bin[33] == 2 and bin[35] == 0 or bin[35] == 1):
            extra['paymentId'] = bintohex(bin[36:36 + bin[34] - 1])
    elif bin[0] == 2:
        if bin[2] == 0 or bin[2] == 1:
            extra['paymentId'] = bintohex(bin[3: 3 + bin[1] - 1])
        #second byte of nonce is nonce payload length; payload length + nonce tag byte + payload length byte should be the location of the pubkey tag
        if bin[2 + bin[1]] == 1:
            offset = 2 + bin[1]
            extra['pub'] = bintohex(bin[offset + 1: offset + 1 + 32])
    return extra
'''
function parseExtra(bin){
    var extra = {
        pub: false,
        paymentId: false
    };
    if (bin[0] === 1){ //pubkey is tag 1
        extra.pub = bintohex(bin.slice(1, 33)); //pubkey is 32 bytes
        if (bin[33] === 2 && bin[35] === 0 || bin[35] === 1){
            extra.paymentId = bintohex(bin.slice(36, 36 + bin[34] - 1));
        }
    } else if (bin[0] === 2){
        if (bin[2] === 0 || bin[2] === 1){
            extra.paymentId = bintohex(bin.slice(3, 3 + bin[1] - 1));
        }
        //second byte of nonce is nonce payload length; payload length + nonce tag byte + payload length byte should be the location of the pubkey tag
        if (bin[2 + bin[1]] === 1){
            var offset = 2 + bin[1];
            extra.pub = bintohex(bin.slice(offset + 1, offset + 1 + 32));
        }
    }
    return extra;
}
'''

def checkTx(isFundingTx, debug=True):
    sec = test_private_view_key
    addr = test_public_address;
    typeTag = type[0]
    hash = txHash

    resultsTag = ''
    err = 0
    if (len(sec) != 64 or validHex(sec) != True):
        resultsTag += "Your private key is invalid. Please check it and try again.\n"
        err = 1
    if addr == "":
        resultsTag += "Address is required. Please enter your/the recipient's address and try again.\n"
        err = 2
    if err != 2 and len(addr) != 95 and len(addr) != 104:
        resultsTag += "Your address is the wrong length! Please check it and try again.\n"
        err = 2
    else:
        addrHex = cnBase58.decode(addr);
        if debug:
            print(f'public address: {addr}\naddrHex:        {addrHex}')
            if addr == test_public_address:
                print('test:          ',test_addrHex)
        if err != 2 and addrHex[-8:] != cn_fast_hash(addrHex[:-8])[0:8]: #checksum validation
            if debug:
                print('checksum validation')
                print('\tif err != 2 and addrHex[-8:] != cn_fast_hash(addrHex[:-8])[0:8]:')
                print('\terr:',err,'\n\taddrHex[-8:]:',addrHex[-8:],'\n\tcn_fast_hash(addrHex[:-8])',cn_fast_hash(addrHex[:-8]))
            resultsTag += "Address validation failed! Please check it and try again.\n"
            err = 2
    if err == 0 and typeTag == "Private Viewkey":
        if addrHex[66:130] != sec_key_to_pub(sec):
            if debug:
                print('typeTag == "Private Viewkey"')
                print('\taddrHex[66:130] != sec_key_to_pub(sec)')
                print('\taddrHex[66:130]:    ',addrHex[66:130],'\n\tsec_key_to_pub(sec):',sec_key_to_pub(sec))
            resultsTag += "Your View Key doesn't match your address. Please check it and try again.\n"
            err = 1
    if len(hash) != 64 or not validHex(hash):
        resultsTag += "Your transaction hash is missing or invalid. Please check it and try again.\n"
        err = 3
    if err != 0:
        print("One or more things are wrong with your inputs!")
        return
    spk = addrHex[2:66];

    res = test_res
    #print(res)
    if res['statusText'] != "OK":
        resultsTag = "Failed to get transaction data! Perhaps MoneroBlocks is down?"
        print("Failed to get transaction data!")
        return
    if typeTag == "Private Viewkey":
        if debug: print('extra:         ',res['transaction_data']['extra'])
        extra = parseExtra(res['transaction_data']['extra'])
        pub = extra['pub'];
        if not pub:
            resultsTag = "Unrecognized tx_extra format! Please let luigi1111 know what tx hash you were using."
            print("Unrecognized extra format") #definitely doesn't cover all possible extra formats, but others are quite uncommon
            return
    else:
        pub = addrHex[66,130]
    if debug: print('pub:           ',pub)
    outputNum = len(res['transaction_data']['vout'])
    der = generate_key_derivation(pub, sec)
    tot = 0
    for i in range(outputNum):
        pubkey = derive_public_key(der, i, spk)
        amount = res['transaction_data']['vout'][i]['amount']
        if pubkey == res['transaction_data']['vout'][i]['target']['key']:
            tot += amount
            print(f"You own output {i} with pubkey: " + pubkey + " for amount: " + str(amount / 1000000000000));
            resultsTag += f"This address owns output {i} with pubkey: " + pubkey + " for amount: " + str(amount / 1000000000000) + "\n" #amount / 10^12
        else:
            print(f"You don't own output {i} with pubkey: " + res['transaction_data']['vout'][i]['target']['key'] + " for amount: " + str(amount / 1000000000000))
            resultsTag += f"This address doesn't own output {i} with pubkey: " + res['transaction_data']['vout'][i]['target']['key'] + " for amount: " + str(amount / 1000000000000) + "\n" #amount / 10^12
    resultsTag += "\nTotal received: " + str(tot / 1000000000000) #10^12
    if isFundingTx and extra['paymentId'] != False:
        resultsTag += "\nPayment ID found: " + extra['paymentId'] + " Matches computed hash?: " + (extra['paymentId'] == dataHashTag)
    elif isFundingTx:
        resultsTag += "\nPayment ID not found! Funding data not logged in blockchain!"
    print("End of TX...");

'''
function checkTx(isFundingTx){
    resultsTag.innerHTML = "";
    var err = 0;
    var sec = private.value;
    if (sec.length !== 64 || validHex(sec) !== true){
        resultsTag.innerHTML += "<span class='validNo'>Your private key is invalid. Please check it and try again.</span><br>"
        err = 1;
    }
    var addr = addrTag.value;
    if (addr == ""){
    	resultsTag.innerHTML += "<span class='validNo'>Address is required. Please enter your/the recipient's address and try again.</span><br>";
        err = 2;
    }
    if (err !== 2 && addr.length !== 95 && addr.length !== 104){
    	resultsTag.innerHTML += "<span class='validNo'>Your address is the wrong length! Please check it and try again.</span><br>";
        err = 2;
    } else {
        var addrHex = cnBase58.decode(addr);
        if (err !== 2 && addrHex.slice(-8) !== cn_fast_hash(addrHex.slice(0,-8)).slice(0,8)){ //checksum validation
            resultsTag.innerHTML += "<span class='validNo'>Address validation failed! Please check it and try again.</span><br>";
            err = 2;
        }
    }
    if (err === 0 && typeTag.value === "Private Viewkey"){
        if (addrHex.slice(66,130) !== sec_key_to_pub(sec)){
            resultsTag.innerHTML += "<span class='validNo'>Your View Key doesn't match your address. Please check it and try again.</span><br>"
            err = 1;
        }
    }
    var hash = txHash.value;
    if (hash.length !== 64 || !validHex(hash)){
        resultsTag.innerHTML += "<span class='validNo'>Your transaction hash is missing or invalid. Please check it and try again.</span><br>";
        err = 3;
    }
    if (err !== 0){throw "One or more things are wrong with your inputs!";}
    var spk = addrHex.slice(2,66);
    var fullapi = api + "get_transaction_data/";
    var res = $.ajax({url: fullapi + hash, type: 'GET', async: false});
    if (res.statusText !== "OK"){
    	resultsTag.innerHTML = "<span class='validNo'>Failed to get transaction data! Perhaps MoneroBlocks is down?</span>";
        throw "Failed to get transaction data!";
    }
    res = JSON.parse(res.responseText);
    if (res.status !== "OK"){
    	resultsTag.innerHTML = "<span class='validNo'>Failed to get transaction data! Your Tx Hash probably doesn't exist.</span>";
        throw "Failed to get transaction data!";
    }
    if (typeTag.value === "Private Viewkey"){
        var extra = parseExtra(res.transaction_data.extra);
        var pub = extra.pub;
        if (!pub){
            resultsTag.innerHTML = "<span class='validNo'>Unrecognized tx_extra format! Please let luigi1111 know what tx hash you were using.</span>"
            throw "Unrecognized extra format"; //definitely doesn't cover all possible extra formats, but others are quite uncommon
        }
    } else {
        var pub = addrHex.slice(66,130);
    }
    var outputNum = res.transaction_data.vout.length;
    var der = generate_key_derivation(pub, sec);
    var tot = 0;
    for (i = 0; i < outputNum; i++){
        var pubkey = derive_public_key(der, i, spk);
        if (pubkey === res.transaction_data.vout[i].target.key){
            tot += res.transaction_data.vout[i].amount;
            console.log("You own output " + i + " with pubkey: " + pubkey + " for amount: " + res.transaction_data.vout[i].amount / 1000000000000);
            resultsTag.innerHTML += "<span class='validYes'>This address owns output&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + i + " with pubkey: " + pubkey + " for amount: " + res.transaction_data.vout[i].amount / 1000000000000 + "</span>" + "<br>"; //amount / 10^12
        } else {
            console.log("You don't own output " + i + " with pubkey: " + res.transaction_data.vout[i].target.key + " for amount: " + res.transaction_data.vout[i].amount / 1000000000000);
            resultsTag.innerHTML += "<span class='validNo'>This address doesn't own output " + i + " with pubkey: " + res.transaction_data.vout[i].target.key + " for amount: " + res.transaction_data.vout[i].amount / 1000000000000 + "</span>" + "<br>"; //amount / 10^12
        }
    }
    resultsTag.innerHTML += "<br>" + "Total received: " + tot / 1000000000000; //10^12
    if (isFundingTx && extra.paymentId !== false){
        resultsTag.innerHTML += "<br>" + "Payment ID found: " + extra.paymentId + " Matches computed hash?: " + (extra.paymentId === dataHashTag.value);
    } else if (isFundingTx){
        resultsTag.innerHTML += "<br>" + "Payment ID not found! Funding data not logged in blockchain!";
    }
    console.log("End of TX...");
}
'''
if __name__ == '__main__':
    print(__file__)
    #print(validHex(txHash))
    #checkTx(False)
