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
    while input_list:
        num_to_enc = input_list.pop(0)
        if num_to_enc == "T":
            result_size.append("T")
        elif num_to_enc == 0:
            result_size.append("Z")
        else:
            bin_len = int(np.log2(np.abs(num_to_enc))) + 1
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