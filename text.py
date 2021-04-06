from Crypto.Cipher import AES
import base64
import msgpack
import re
import os

def decrypt(encrypted):
    mode = AES.MODE_CBC
    ss2 = base64.b64decode(encrypted)
    vi = b'ha4nBYA2APUD6Uv1'
    key = ss2[-32:]
    ss2 = ss2[:-32]
    cryptor=AES.new(key,mode, vi)
    plain_text  = cryptor.decrypt(ss2)
    try:
        return msgpack.unpackb(plain_text)
    except msgpack.ExtraData as err:
        return err.unpacked
    except:
        return {"data_headers" : {}, "data" : {}}

def decrypt_req(ss2):
    mode = AES.MODE_CBC
    vi = b'ha4nBYA2APUD6Uv1'
    key = ss2[-32:]
    ss2 = ss2[:-32]
    cryptor=AES.new(key,mode, vi)
    plain_text  = cryptor.decrypt(ss2)
    try:
        return msgpack.unpackb(plain_text)
    except msgpack.ExtraData as err:
        return err.unpacked
    except:
        return {"data_headers" : {}, "data" : {}}

def text_trans(inpath, outpath):
    filein = ''.join(open(inpath,'r').readlines())
    cdata = re.findall(r'CDATA\[.+\]', filein)
    line0 = cdata[0][6:-2]
    data_req = base64.b64decode(bytes(cdata[3][6:-2], encoding='utf-8'))
    line1 = str(decrypt_req(re.split(b'\r\n\r\n',data_req)[-1]))
    data_res = base64.b64decode(bytes(cdata[4][6:-2], encoding='utf-8'))
    line2 = str(decrypt(re.split(b'\r\n\r\n',data_res)[-1]))
    f = open(outpath,'w').write(line0 + '\n' + line1 + '\n' + line2 + '\n\n')

def text_pcr():
    rootDir = 'listen'
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            inpath = os.path.join(root ,file)
            outpath = os.path.join('unpack', file[:-3]+'json')
            text_trans(inpath, outpath)

if __name__ == "__main__":
    text_pcr()
    # inpath = 'listen\\logv4.xml'
    # outpath = 'unpack\\logv4.json'
    # text_trans(inpath, outpath)