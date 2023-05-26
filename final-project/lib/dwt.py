import numpy as np

# Filter coefficients
lp_analysis = np.array([-1, 2, 6, 2, -1]) / 8
hp_analysis = np.array([-1, 2, -1]) / 2
lp_synthesis = np.array([1, 2, 1]) / 2
hp_synthesis = np.array([-1, -2, 6, -2, -1]) / 8


def pad_and_convolve_line(array, filter):
    # padding
    array = np.pad(array, (len(filter) // 2, len(filter) // 2), 'reflect')
    # convolution
    output = np.convolve(array, filter, mode='valid')
    return output

def pad_and_convolve_img(input_img, filter):
    input_conv_img = np.zeros(input_img.shape)
    width = input_img.shape[1]
    height = input_img.shape[0]
    for i in range(height):
        input_conv_img[i] = pad_and_convolve_line(input_img[i], filter)
    return input_conv_img

def decomposition(input_img):
    input_decomposition_img = np.zeros(input_img.shape)
    # decomposition
    hf = pad_and_convolve_img(input_img, hp_analysis)
    lf = pad_and_convolve_img(input_img, lp_analysis)
    input_decomposition_img[:,0:input_img.shape[1]//2] = lf[:,1::2]
    input_decomposition_img[:,input_img.shape[1]//2:input_img.shape[1]] = hf[:,::2]
    return input_decomposition_img

def reconstruction(input_img):
    # reconstruction
    hf = input_img[:,input_img.shape[1]//2:input_img.shape[1]]
    lf = input_img[:,0:input_img.shape[1]//2]
    hf_recon = np.zeros((input_img.shape[0], input_img.shape[1]))
    hf_recon[:,::2] = hf
    lf_recon = np.zeros((input_img.shape[0], input_img.shape[1]))
    lf_recon[:,1::2] = lf
    hf_recon = pad_and_convolve_img(hf_recon, hp_synthesis)
    lf_recon = pad_and_convolve_img(lf_recon, lp_synthesis)
    recon_img = hf_recon + lf_recon
    return recon_img

def decomposition_to_4(input_img):
    # decomposition
    L1 = decomposition(input_img)
    L2 = decomposition(L1.T).T
    return L2

def reconstruction_from_4(input_img):
    # reconstruction
    L1 = reconstruction(input_img.T).T
    L2 = reconstruction(L1)
    return L2

def decomposition_to_specify_level(input_img, level):
    input_img = input_img.astype(np.float64)
    L = input_img.astype(np.float64)
    height = input_img.shape[0]
    width = input_img.shape[1]
    for i in range(1,level+1):
        # print(width//i, height//i)
        L[0:height//i,0:width//i] = decomposition_to_4(L[0:height//i,0:width//i])
    return L

def reconstruction_from_specify_level(input_img, level):
    input_img = input_img.astype(np.float64)
    L = input_img.astype(np.float64)
    height = input_img.shape[0]
    width = input_img.shape[1]
    for i in range(level):
        # print(width//(level-i), height//(level-i))
        L[0:height//(level-i),0:width//(level-i)] = reconstruction_from_4(L[0:height//(level-i),0:width//(level-i)])
    return L