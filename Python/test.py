import NFCDriver as nfc

cancel = False
NFC = 0
while NFC == 0 and not cancel : 
    NFC = ''.join([hex(i)[-2:] for i in nfc.ReadCard()])
print(NFC)