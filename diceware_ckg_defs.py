import requests
import json
import math


def numberToBase(n, b, num_digits=0):
    # a nonzero num_digits will return the num_digits least significant digits
    # and will pad with zeros
    # num_digits == 0 will return the natural number of digits
    # numberToBase digits are little endian, the least shall be first
    if num_digits == 0:
        # num_digits = int(n/b) + 1
        num_digits = int(math.log(n, b)) + 1
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    for _ in range(num_digits - len(digits)):
        digits.append(0)
    digits = digits[::-1][len(digits)-num_digits:]
    return digits[::-1]


def Wordlist_dict(wordlist_url):
    # retrieve a diceware wordlist and put the words in a dictionary indexed no die roll
    # The EFF list is the one used by Doug Muth and much more pleasing to Reinhold's original
    #
    # The results from the GET look like
    # >>> wordlist.content
    # b'11111\tabacus\n11112\tabdomen\n11113\tabdominal\n11114\tabide\n11115\tabiding\n...
    #
    wordlist = requests.get(wordlist_url)
    words_dict = {}

    # the strings come in binary encoding, decode it to UTF-8
    # create the dictionary of words mappings
    # 11111 a     -> 11111: a
    # 11112 aa    -> 11112: aa
    # ...            ...
    # 12255 anita -> 12255: anita
    # ...
    #
    # >>> for content in wordlist.iter_lines():
    # ...   print(content)
    # ...
    # b'11111\tabacus'
    # b'11112\tabdomen'
    # b'11113\tabdominal'
    # b'11114\tabide'

    # construct a dictionary of words from text file
    # for convenient lookup later
    for line in wordlist.iter_lines():
        line = line.decode('UTF-8')
        # line should now be a string of form 'NNNN\tword'
        # check that line starts with 5 digits then split on the tab
        if line != "" and str(line)[0:5].isdigit():
            line_split = line.split("\t")
            # words_dict.update({line.split("\t")[0]:line.split("\t")[1]})
            words_dict.update({line_split[0]: line_split[1]})
    # print(words_dict)
    # XXX -- this should be a function to create the wordlist dictionary
    return words_dict


def getRands(number_of_rands=6):
    rand_type = "uint16"  # 0 - 65535 - 5 random numbers between 0 and 65535
    url = "https://api.quantumnumbers.anu.edu.au?length=" + str(number_of_rands) + "&type=" + rand_type
    # Construct the API key header
    # header_content = '{"x-api-key": "hPPHuwVZdf919sIdtumYd7pq2HqXz1dS2qeAgz1t"}'  # free api
    # header_content = '{"x-api-key": "QMIuR2VKZ18PllJOlaXES3QLuwSit0II64v0l0vx"}'  # pay $0.0005 / request
    # header_content = dict(json.loads(header_content))
    # why did I use json.loads??
    header_content = dict()
    # header_content['x-api-key'] = 'hPPHuwVZdf919sIdtumYd7pq2HqXz1dS2qeAgz1t'
    header_content['x-api-key'] = 'QMIuR2VKZ18PllJOlaXES3QLuwSit0II64v0l0vx'  # pay $0.0005 / request
    index_list = []
    response = requests.get(url, headers=header_content)
    if response.status_code == 200:
        data = json.loads(json.dumps(response.json()))['data']
    else:
        print("Error getting random numbers!")
        print("HTTP: " + str(response.status_code))
        exit(response.status_code)
    # number_of_dice = "5"
    # number_of_rands = number_of_dice * rolls
    return data


def Dieroll(rolls=6) :
    # Number of the dice to roll (get 5 random numbers,  The words dictionary has 11111-66666 words)
    number_of_dice = 5
    # should check that base of dice ** number of dice < size of random
    # to support future arbitrary size wordlists, die size, etc
    # for now we assume standard Diceware: 6^5 = 7776 < 65536
    # to economize API calls, we get a block of random numbers
    # number_of_rands = number_of_dice * rolls
    random_digits = getRands(rolls)
    # this_digit = 0
    result_list = []
    for roll in random_digits:
        digits = numberToBase(roll, 6, number_of_dice)
        this_roll = ""
        for digit in digits:
            this_roll = this_roll + str(digit + 1)
        result_list.append(this_roll)
    return result_list


'''
    while rolls > 0:
        i = 0
        index = 0
        # interested in the first digit for the returned numbers
        # other cool ways to get a digit would be to add the digits
        # until only one remains
        # e.g. 4 + 2 + 4 = 10; 1+0 = 1
        #      4 + 6 + 8 + 6 + 0 = 24; 2 + 4 = 6
        # "data": [424, 46860, 63139, 5946, 62605, 64827]
        for num in data:
            num_i = str(num)[0]
            # print(num_i)
            num_i = int(num_i)
            # if digit is larger than 6 then take modulus 6
            if num_i > 6:
                num_i = num_i % 6
            # build the index by adding the digit*(10^i)
            index = index + num_i * (10 ** i)
            i =+ 1
        index = str(index)
        index_list.append(index)
        rolls = rolls - 1
    return index_list
'''
