#! /bin/python3
from pyperclip import copy
from getpass import getpass
from Crypto.Hash import SHA512
from Base94 import Base94
from Contains import contains
from StringSum import strSum
from Alias import alias
from Crypto.Cipher import Blowfish
import os
import pickle


def inputR(output, default=None, f=None, hide=False):
    newInput = getpass if hide else input
    while True:
        if not default:
            temp = newInput(output + ':')
        elif default:
            temp = newInput(output + '(default(' + default + ')):')
            if temp == '':
                temp = default
        if not f or f(temp):
            return temp

mode = inputR('Hash or Cipher mode?(h/c)', default='h', f=lambda x: x in {'h','c'})
if mode == 'h':
    t = inputR('Enter type(id(i)password(p)name(n))',default='p', f=lambda x: x in {'i','p','n'})
    k = inputR('Enter keyword', default=None, f=None)
    f = inputR('Enter flag(Enter an integer not less than 0', default='0', f=lambda x: x.isdecimal() and int(x) >= 0)
    if f == '0':
        f = ''
    if t == 'n':
        m = k + t + f
    else:
        d = inputR('Do not ban starting with a digit?(y/n)', default='y', f=lambda x: x in {'y','n'})
        swd = False if d == 'n' else True
        l = int(inputR('Enter length(between 6 and 256)', default='16', f=lambda x: int(x) in range(6, 257)))
        if t == 'p':
            w = inputR('With punctuations(y/n)', default='y', f=lambda x: x in {'y','n'})
            wp = False if w == 'n' else True
            s = inputR('Enter seed',default=None,f=strSum, hide=True)
            m = k + t + s + f
        elif t == 'i':
            w = inputR('With punctuations(y/n)', default='n', f=lambda x: x in {'y','n'})
            wp = False if w == 'n' else True
            v = inputR('Old version?(y/n)', default='n', f=lambda x: x in {'y','n'})
            m = k + 'i' + f if v == 'n' else k + 'u' + f
            

    h = SHA512.new()
    h.update(m.encode())

    if t == 'i' or t == 'p':
        b = h.digest()
        string = Base94(b, wp).decode()
        for i in range(513 - l):
            res = string[i: l + i]
            if contains(res, withPunctuation=wp, startWithDigit=swd):
                break
    elif t == 'n':
        res = alias(int(h.hexdigest(),16))
    copy(res)
    print('Already copy it to clipboard.')
elif mode == 'c':
    if not os.path.exists('upgen.bin'):
        print("First time to use mode cipher, new upgen.bin is established")
        with open('upgen.bin', 'wb') as fp:
            pass

    eord = inputR('Which do you want(e for encry, d for decry)',default = None, f = lambda x: x in {'e','d'})
    k = inputR('Enter keyword', default=None, f=None)
    f = inputR('Enter flag(Enter an integer not less than 0', default='0', f=lambda x: x.isdecimal() and int(x) >= 0)
    if f == '0':
        f = ''
    h = SHA512.new()
    h.update((k + f).encode())
    kf = h.hexdigest()

    if eord == 'e':
        with open('upgen.bin','rb') as fp:
            dic = pickle.load(fp) if os.path.getsize('upgen.bin') > 0 else dict()
            if kf in dic:
                exit("The keyword and flag have already been used. Run me again to make a new one")


        s = inputR('Enter seed',default=None,f=strSum, hide=True)
        key = k + f + s
        m = 8 * inputR('Enter message', default=None,f=lambda x: len(x) > 0)

        kk = Blowfish.new(key.encode(), Blowfish.MODE_CBC)
        cc = kk.encrypt(m.encode())
        dic[kf] = cc

        with open('upgen.bin','wb') as fp:
            pickle.dump(dic, fp)
            print('Your message has been encrypted to file upgen.bin')
    elif eord == 'd':
        with open('upgen.bin','rb') as fp:
            dic = pickle.load(fp) if os.path.getsize('upgen.bin') > 0 else dict()
            if kf not in dic:
                exit('The keyword and flag are not in the upgen.bin')
            else:
                s = inputR('Enter seed',default=None,f=strSum, hide=True)
                key = k + f + s

                kk = Blowfish.new(key.encode(), Blowfish.MODE_CBC)
                cc = dic[kf]
                p = kk.decrypt(cc).decode()
                copy(p[0:len(p) // 8])
                print('Already copy it to clipboard.')
