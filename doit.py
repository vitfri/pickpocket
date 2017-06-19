#!/usr/bin/python

import os, sys, string, json
from pprint import pprint

from keys import decode_keystore_json #keys.py from pyethereum, we only want the decode_keystore_json function
import itertools
import traceback
from joblib import Parallel, delayed
import multiprocessing

def get_indices(passwd, alphabet):
    # Get indices of a password; for testing use
    return [alphabet.index(i) for i in passwd]

def generate_all(passwd_len, alphabet, slice_start, slice_end):
    indices = [slice_start] + [0]*(passwd_len-1)
    # Uncomment and replace password to prove with test file
    # indices = get_indices('59mn9wD%39sd!GYn', alphabet)
    alphabet_len = len(alphabet) # Hopefully shave off microseconds

    while True:
        yield ''.join([alphabet[i] for i in indices])
        # Increment password
        for i in range(passwd_len-1,-1,-1):
            if indices[i]+1 < (alphabet_len if i>0 else slice_end):
                indices[i] += 1
                break # Done incrementing
            if i==0:
                print "Reached final password"
                raise StopIteration()
            # Reset to first element in alphabet
            indices[i] = 0

class PasswordFoundException(Exception):
    pass

def attempt(w, pw):
    # print(pw)
    # sys.stdout.write("\r")

    # sys.stdout.write("\rAttempt #%d: %s" % (counter.value, pw)) #prints simple progress with # in list that is tested and the pw string
    sys.stdout.write("Attempt #%d: %s\n" % (counter.value, pw)) #prints simple progress with # in list that is tested and the pw string
    sys.stdout.flush()
    #print(counter.value)
    counter.increment()

    if len(pw) < 10:
        return ""
    try:
        o = decode_keystore_json(w,pw)
        # print(o)
        # print (pw)q
        print "Password is:  '%s'" % pw
        # raise PasswordFoundException(
        #     """\n\nYour password is:\n%s""" % o)
        raise PasswordFoundException(
            """\n\nYour password is:\n'%s'""" % pw)
    except ValueError as e:
        # print(e)
        return ""

class Counter(object):
    def __init__(self):
        self.val = multiprocessing.Value('i', 0)

    def increment(self, n=1):
        with self.val.get_lock():
            self.val.value += n

    @property
    def value(self):
        return self.val.value

def __main__():
    alphabet = string.printable[:-5]
    passwd_len = int(os.getenv("PASSWD_LEN",12))
    slice_start = int(os.getenv("SLICE_START",0))
    slice_end = int(os.getenv("SLICE_END",len(alphabet)))

    print "Working on passwd:  length %d, initial character range '%s'" % (
        passwd_len, alphabet[slice_start:slice_end])

    try:
        fname = os.getenv("WALLET_FILE",None) or sys.argv[1]
    except:
        print "Unable to determine wallet file name; please set WALLET_FILE env var"
        sys.exit(1)
    try:
        with open(fname,'r') as f:
            w = json.loads(f.readline())
    except Exception as e:
        print "Unable to read wallet file: %s" % e
        sys.exit(1)

    print "Read wallet contents:"
    pprint(w)

    global counter
    counter = Counter()
    pwds = generate_all(passwd_len, alphabet, slice_start, slice_end)

    # n_pws = len(list(pwds))
    # print 'Number of passwords to test: %d' % (n_pws)

    try:
        Parallel(n_jobs=-1)(delayed(attempt)(w, pw)
                            for pw in generate_all(
                                    passwd_len, alphabet, slice_start, slice_end))
        # print("\n")
    except Exception, e:
        traceback.print_exc()


if __name__ == '__main__':
    __main__()
