import os
import json
import glob

def getInputFiles(path, in_basename):
	if(path is not '' and path[-1]!='/'):
		path = path+"/"
	return(sorted(glob.glob(path+in_basename+'*.json')))

def getFileSize(file):
    return os.stat(file).st_size

def getFileData(file, data):
	with open(file, 'r') as f:
		temp_data= json.load(f)
	for key in temp_data:
		if(key in data):
			for val in temp_data[key]:
				data[key].append(val)
		else:
			data[key] = temp_data[key]
	return data

def SplitData(data, key, out_basename, cnt, max_size):
	temp_dict = {}
	size = len(str(key))+5
	val_str_len = 0
	temp_dict[key] = []
	for val in data[key]:
		val_str_len += len(str(val))
		if(val_str_len + size < max_size):
			temp_dict[key].append(val)
			continue

		_, cnt, val_str_len = DumpData(temp_dict, out_basename, cnt)
		temp_dict[key] = []
		temp_dict[key].append(val)
		val_str_len += len(str(val))

	if(bool(temp_dict)):
		_, _, _ = DumpData(temp_dict, out_basename, cnt)
	return cnt+1

def DumpToDiffFiles(data, out_basename, max_size):
	cnt = 1
	temp_dict = {}	
	_size = 0
	
	for key in data:
		if(len(str(data[key]))+len(key)+3 > max_size):
			if(bool(temp_dict)):
				temp_dict, cnt, _size = DumpData(temp_dict, out_basename, cnt)
			cnt = SplitData(data, key, out_basename, cnt, max_size)
			continue

		_size += len(str(data[key]))+len(key)+3
		temp_dict[key] = data[key]
		if(_size >= max_size):
			temp_dict, cnt, _size = DumpData(temp_dict, out_basename, cnt)

	if(bool(temp_dict)):
		_, _, _ = DumpData(temp_dict, out_basename, cnt)	

def DumpData(data, out_basename="Merge", cnt):
	out_file = out_basename+str(cnt)+'.json' 
	with open(out_file, 'w') as f:
		json.dump(data,f)

	print(f'{out_file} file of size {getFileSize(out_file)} bytes was generated.')
	return({},cnt+1,0)

if __name__ == "__main__":
	path = input("Folder Path[ignore if current dir]: ")
	in_basename = input("Input file BaseName: ")
	out_basename = input("Output file BaseName: ")
	max_size = int(input("File Maximum size[INT]: "))
	
	input_files = getInputFiles(path, in_basename)

	data = {}
	for file in input_files:
		# print(f'{input_files.index(file)+1} - {file}')
		data = getFileData(file, data)

	if(bool(data)):
		DumpToDiffFiles(data, out_basename, max_size-3)
	else:
		print(f"[Info] No file found with Prefix '{in_basename}'")