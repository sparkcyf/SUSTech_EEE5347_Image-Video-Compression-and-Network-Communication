import json

# encode

def pad_encoded_data(data):
    # Calculate the number of bits we need to pad
    pad_size = 8 - (len(data) % 8)
    
    # Pad with zeros
    data += '0' * pad_size

    # Also add the size of the padding to the start of the string
    pad_info = "{0:08b}".format(pad_size)
    data = pad_info + data

    return data

def convert_code_table_to_binary(code_table):
    # Convert the code table to a JSON string
    code_table_str = json.dumps(code_table)

    # Convert the JSON string to binary
    code_table_binary = ''.join(format(ord(i), '08b') for i in code_table_str)
    
    return code_table_binary

def write_to_binary_file(data, filename):
    with open(filename, 'wb') as file:
        for i in range(0, len(data), 8):
            chunk = data[i:i+8]
            byte = int(chunk, 2).to_bytes(1, 'big')
            file.write(byte)

# decode
def read_from_binary_file(filename):
    with open(filename, 'rb') as file:
        data_bytes = file.read()

    return ''.join(format(byte, '08b') for byte in data_bytes)

def split_data(data, separator):
    return data.split(separator)

def convert_binary_to_code_table(binary_str):
    json_str = ''.join(chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8))
    return json.loads(json_str)

def decode_data(data, code_table):
    reversed_code_table = {v: k for k, v in code_table.items()}

    # Extract the padding size from the start of the data
    pad_size = int(data[:8], 2)
    data = data[8:]

    # Decode the data
    decoded_data = []
    buffer = ''
    for bit in data:
        buffer += bit
        if buffer in reversed_code_table:
            decoded_data.append(reversed_code_table[buffer])
            buffer = ''
    
    # Remove the padding from the end of the decoded data
    decoded_data = decoded_data[:-pad_size] if pad_size != 0 else decoded_data

    return decoded_data