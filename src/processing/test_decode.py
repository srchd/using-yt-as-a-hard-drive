from pathlib import Path
import numpy as np



def get_binary_string(filename):
	with open(filename, 'r', encoding='ISO-8859-1') as f:
		data = f.read()

	data = [format(ord(c), '08b') for c in data]
	data = list(''.join(data))

	return data


input_file_name = '08.pdf'
output_file_name = '08_reconstructed.pdf'
path = Path(__file__).parent.parent.parent
input_file_path = path / input_file_name
output_file_path = path / output_file_name


# with open(input_file_path, 'r', encoding='ISO-8859-1') as f:
# 	data = f.read()

with open(input_file_path, 'rb') as f:
	data = f.read()

# bin_str_list = [format(ord(c), '08b') for c in data]
# bin_str_list = list(''.join(bin_str_list))

bin_str_list = list(''.join([format(i, '08b') for i in data]))

bin_seq = np.asarray([int(bit) for bit in bin_str_list])

reconstr_data = []
for bit_array in bin_seq.reshape(-1,8):
	byte_str = ''.join([str(bit) for bit in  bit_array])
	i = int(byte_str,2)
	reconstr_data.append(i)
	

# reconstr_data = ''.join([chr(int(''.join(list(byte)),2)) for byte in bin_seq.reshape(-1,8)])

# print(data == reconstr_data)

# with open(path / '08_original.pdf', 'wb') as f:
# 	f.write(data)

with open(output_file_path, 'wb') as f:
	f.write(bytes(reconstr_data))