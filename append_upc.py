'''
7-1-17
Program will take a file called "in_file.txt", and will write to "out_file.txt".
"in_file.txt" will be parsed and will write the same file
with all possible digit(s) appended to upc.

User can append number to upc with the following choices:
1) Both left end AND right end
2) ONLY left end
3) ONLY right end

Example of appending to ONLY left:
    BEFORE: abc123 001 002 0303 description number 1.11 0
    AFTER:  abc123 00010020303 description number 1.11 0
            abc123 10010020303 description number 1.11 0
            .
            .
            .
            abc123 90010020303 description number 1.11 0

NOTE: header is hardcoded, and the parsed "in_file.txt"
        must be in the specific format seen above in "BEFORE"
'''

import re
import collections

READ_FILE_NAME = 'in_file.txt'
READ_HEADER_LIST = ['product_num', 'upc', 'description', 'price', 'cs']
WRITE_FILE_NAME = 'out_file.txt'
WRITE_DELIMITER = '\t'

ProductInfo = collections.namedtuple('ProductInfo', 'product_num upc description price cs')

def run_program_interface()->None:
    user_input_int = get_user_input_mode()
    read_stream = open(READ_FILE_NAME, 'r')
    write_stream = open(WRITE_FILE_NAME, 'w')
    write_header_to_file(write_stream)
    write_stream.close()
    write_stream = open(WRITE_FILE_NAME, 'a')


    parse_and_write_file(read_stream, write_stream, user_input_int)


    read_stream.close()
    write_stream.close()

def get_user_input_mode()->int:
    while(True):
        print('SELECT MODE...')
        print('Add nubmers to...')
        print('1) Both Left AND right end')
        print('2) ONLY left end')
        print('3) ONLY right end')
        user_input = input('').strip()
        if not is_valid_input(user_input):
            print('')
            continue
        else:
            return int(user_input)

def is_valid_input(user_input:str)->bool:
        try:
            user_input_int = int(user_input)
        except(ValueError):
            print('Non-number entered. Try again...')
            return False
        if(user_input_int >= 1 and user_input_int <= 3):
            return True
        else:
            print('Invalid number. Must enter a number "1-3". Try again...')
            return False
    

def write_header_to_file(write_stream):
    global READ_HEADER_LIST
    
    header_len = len(READ_HEADER_LIST)
    last_index = header_len - 1
    for i in range(header_len):
        write_stream.write(READ_HEADER_LIST[i])
        if(i < last_index):
            write_stream.write(WRITE_DELIMITER)
        else:
            write_stream.write('\n')
            

def parse_and_write_file(read_stream:'read_stream',
                         write_stream:'write_stream', user_input_int:int)->None:
    no_upc_count = 0
    for line in read_stream:
        if re.search('[a-zA-Z0-9]', line): #Only parse if line contains something(num/letters)
            product_info = get_info_from_line(line)
            if product_info != None: #If upc grabbed successfully...continue as normal
                write_appended_upc(write_stream, product_info, user_input_int)
            else: #Skip
                no_upc_count = no_upc_count + 1
                continue

def write_appended_upc(write_stream:'write_stream',
                       product_info:ProductInfo, user_input_int:int)->None:
    if user_input_int == 1:
        write_left_and_right_upc(write_stream, product_info)
    elif user_input_int == 2:
        write_left_upc(write_stream, product_info)
    else:
        write_right_upc(write_stream, product_info)

def write_left_and_right_upc(write_stream:'write_stream', product_info:ProductInfo)->None:
    for i in range(10):
        for j in range(10):
            new_upc = str(i) + product_info.upc + str(j)
            write_line = '{0}\t{1}\t{2}\t{3}\t{4}\n'.format(product_info.product_num,
                                         new_upc, product_info.description,
                                         product_info.price, product_info.cs)
            write_stream.write(write_line)

def write_left_upc(write_stream:'write_stream', product_info:ProductInfo)->None:

    for i in range(10):
        new_upc = str(i) + product_info.upc
        write_line = '{0}\t{1}\t{2}\t{3}\t{4}\n'.format(product_info.product_num,
                                                        new_upc, product_info.description,
                                                        product_info.price, product_info.cs)
        write_stream.write(write_line)

def write_right_upc(write_stream:'write_stream', product_info:ProductInfo)->None:
    for i in range(10):
        new_upc = product_info.upc + str(i)
        write_line = '{0}\t{1}\t{2}\t{3}\t{4}\n'.format(product_info.product_num,
                                                        new_upc, product_info.description,
                                                        product_info.price, product_info.cs)
        write_stream.write(write_line)

def get_info_from_line(line:str)->ProductInfo:
    word_list = line.split()
    product_num = get_and_delete_product_num(word_list)
    upc = get_and_delete_upc(word_list)
    if upc == '':
        return None
    description = get_and_delete_description(word_list)
    price = get_and_delete_price(word_list)
    cs = get_and_delete_cs(word_list)

    return ProductInfo(product_num = product_num, upc = upc,
                       description = description, price = price, cs = cs)
    
def get_and_delete_product_num(word_list:list)->str:
    return word_list.pop(0)

def get_and_delete_upc(word_list:list)->str:
    upc = ''
    while(True):
        current_word = word_list[0]
        if current_word.isdigit():
            upc = upc + current_word
            del word_list[0]
        else:
            break
    return upc

def get_and_delete_description(word_list:list)->str:
    description = ''
    while(True):
        current_word = word_list[0]
        try:
            float(current_word)
            description = description.strip()
            return description
        except ValueError:
            description = description + ' ' + current_word
            del word_list[0]

def get_and_delete_price(word_list:list)->str:
    return word_list.pop(0)

def get_and_delete_cs(word_list:list)->str:
    return word_list.pop(0)

            
if __name__ == '__main__':
    run_program_interface()