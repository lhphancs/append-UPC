'''
Program will take file, parse it, and spit out same
file with all possible digit(s) appended to upc.
User can append number to upc with the following choices:

1) Both left end AND right end
2) ONLY left end
3) ONLY right end
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
    write_stream = open(WRITE_FILE_NAME, 'a')

    write_header_to_file(write_stream)
    parse_and_write_file(read_stream, write_stream)


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
            

def parse_and_write_file(read_stream, write_stream)->None:
    no_upc_count = 0
    for line in read_stream:
        if re.search('[a-zA-Z0-9]', line): #Only parse if line contains something(num/letters)
            product_info = get_info_from_line(line)
            if product_info != None: #If upc grabbed successfully...continue as normal
                print(product_info)
                ################
            else: #Skip
                no_upc_count = no_upc_count + 1
                continue

def get_info_from_line(line:str)->list:
    word_list = line.split()
    product_num = get_and_delete_number(word_list)
    upc = get_and_delete_upc(word_list)
    if upc == '':
        return None
    description = get_and_delete_description(word_list)
    price = get_and_delete_price(word_list)
    cs = get_and_delete_cs(word_list)

    return ProductInfo(product_num = product_num, upc = upc,
                       description = description, price = price, cs = cs)
    
def get_and_delete_number(word_list:list)->str:
    return word_list.pop(0)

def get_and_delete_upc(word_list:list)->str:
    upc = ''
    current_word = ''
    while(True):
        current_word = word_list[0]
        if current_word.isdigit():
            upc = upc + current_word
            del word_list[0]
        else:
            break
    if upc == '':
        return ''

def get_and_delete_description(word_list:list)->str:
    description = ''
    while(True):
        current_word = word_list[0]
        try:
            float(current_word)
            return description
        except ValueError:
            description = description + current_word
            del word_list[0]

def get_and_delete_price(word_list:list)->str:
    return word_list.pop(0)

def get_and_delete_cs(word_list:list)->str:
    return word_list.pop(0)

            
if __name__ == '__main__':
    run_program_interface()
    
