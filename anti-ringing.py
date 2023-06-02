import numpy as np
import cv2
from numba import njit

@njit
def anti_ringing(lr_input, hr_input):
    shape = hr_input.shape
    output = np.empty(shape).astype('float64')

    for j in range(shape[0]):
        for i in range(shape[1]):
            j_lr = np.minimum(shape[0] / 2, np.maximum(np.floor(j / 2) - 1, 0))
            i_lr = np.minimum(shape[1] / 2, np.maximum(np.floor(i / 2) - 1, 0))
            for k in range(shape[2]):
                local_min = np.amin(lr_input[j_lr : j_lr + 4, i_lr : i_lr + 4, k])
                local_max = np.amax(lr_input[j_lr : j_lr + 4, i_lr : i_lr + 4, k])
                output[j, i, k] = np.minimum(local_max, np.maximum(hr_input[j, i, k], local_min))

    return output

hr_input = cv2.imread('./hr_input.png', cv2.IMREAD_COLOR)
hr_input = np.array(hr_input).astype(np.float64) / 255.0
hr_input = np.minimum(1, np.maximum(hr_input, 0))

lr_input = cv2.imread('./lr_input.png', cv2.IMREAD_COLOR)
lr_input = np.array(lr_input).astype(np.float64) / 255.0
lr_input = np.minimum(1, np.maximum(lr_input, 0))

output = anti_ringing(lr_input, hr_input)

output = np.clip(output, 0, 1)
output = np.squeeze((np.around(output * 255)).astype(np.uint8))
cv2.imwrite('output-test.png', output)
