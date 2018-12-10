import sys
import os
import numpy as np

def signed_to_hex(value, width):
    return hex(int(round((1 << width) + value)) % (1 << width))

def debug_format_line(line, fout):
    line = [*line, *([0] * (64 - len(line)))]
    ret = ''.join([format(v, '02x') + ('  ' if i % 8 == 7 else ('--' if i % 8 == 3 else '')) for v, i in
                   zip(line, range(len(line)))])
    fout.write('Address 0X00000000: ' + ret + '\n')


def split_chunks(L, n):
    for i in range(0, len(L), n):
        yield L[i:i + n]



def log_next_pow_of_2(value):
    ret = 0
    while value > 1 or value <= -1:
        value = value / 2
        ret = ret + 1

    return ret, value

def pow_next_log_of_2_no_round(value, bound_shift, shift_max_shift=4):
    mul, shift = np.frexp(np.abs(value))
    ret = bound_shift - 1 - shift
    mul = np.sign(value) * mul * np.power(2, bound_shift - 1)
    return ret, mul

def pow_next_log_of_2(value, bound_shift, shift_max_shift=4):
    ret = 0
    shift_max = 1 << shift_max_shift
    while value >= -(1 << (bound_shift - 2)) and value < (1 << (bound_shift - 2)) \
            and value != 0 and ret < (shift_max - 1):
        value = value * 2
        ret = ret + 1

    return ret, value


def min_max_to_scale_bias(minv, maxv):
    scale = (maxv - minv) / 255
    bias = minv
    return scale, bias

def import_from_path(module_path):
    module_dir = os.path.dirname(module_path)
    module_name = os.path.basename(module_path)

    if module_name.endswith('.py'):
        module_name = module_name[:-3]

    sys_path = sys.path
    sys.path = [os.path.abspath(module_dir)] if module_dir else ['.']
    loaded_module = __import__(module_name)
    sys.path = sys_path

    return loaded_module