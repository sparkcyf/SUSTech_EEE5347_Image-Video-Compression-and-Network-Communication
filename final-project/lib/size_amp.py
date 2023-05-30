import numpy as np

def convert_to_bin(num, bin_len):
    if num >= 0:
        return bin(num)[2:].zfill(bin_len)
    else:
        return "0" + bin(abs(num))[3:].zfill(bin_len-1)

def convert_from_bin(num):
    if num[0] == "1": # positive
        return int(num, 2)
    else:
        return -int("1" + num[1:], 2)

   
def size_amplitude_single_list(input_list):
    input_list = input_list.copy()
    result_size = [] #len of amp, 0, T
    result_amplitude = []
    for num_to_enc in input_list: # avoid pop
        if num_to_enc == "T":
            result_size.append("T")
        elif num_to_enc == 0:
            result_size.append("Z")
        else:
            bin_len = num_to_enc.bit_length()
            result_size.append(bin_len)
            result_amplitude.append(convert_to_bin(num_to_enc, bin_len))
    result_size.append("E") #EOB
    return result_size, result_amplitude

def size_amplitude_to_2D_list(result_size, result_amplitude):
    result_size = result_size.copy()
    result_amplitude_index = 0
    recon_dpr_list = [[[] for _ in range(16)] for _ in range(16)]
    dpr_list_index = 0
    while result_size:
        size = result_size.pop(0)
        if size == "T": #ZTR
            recon_dpr_list[dpr_list_index//16][dpr_list_index%16].append("T")
        elif size == "Z": #ZERO
            recon_dpr_list[dpr_list_index//16][dpr_list_index%16].append(0)
        elif size == "E": #EOB
            dpr_list_index += 1
        else:
            size = int(size)
            amplitude = result_amplitude[result_amplitude_index:result_amplitude_index+size]
            recon_dpr_list[dpr_list_index//16][dpr_list_index%16].append(convert_from_bin(amplitude))
            result_amplitude_index += size
    return recon_dpr_list

def size_amplitude_to_2D_list_optimized(result_size, result_amplitude):
    # Avoids the need for pop(0), which is an O(n) operation.
    result_size = [(int(x), 'N') if x.isdigit() else (x, 'C') for x in result_size]

    result_amplitude_index = 0
    recon_dpr_list = [[[] for _ in range(16)] for _ in range(16)]
    dpr_list_index = 0

    # Use enumerate for faster access
    for size, type_ in result_size:
        dpr_list_index_div, dpr_list_index_mod = divmod(dpr_list_index, 16)
        if type_ == 'C':
            if size == "T":
                recon_dpr_list[dpr_list_index_div][dpr_list_index_mod].append("T")
            elif size == "Z":
                recon_dpr_list[dpr_list_index_div][dpr_list_index_mod].append(0)
            elif size == "E":
                dpr_list_index += 1
        else:
            amplitude = result_amplitude[result_amplitude_index:result_amplitude_index+size]
            recon_dpr_list[dpr_list_index_div][dpr_list_index_mod].append(convert_from_bin(''.join(str(x) for x in amplitude)))
            result_amplitude_index += size

    return recon_dpr_list
