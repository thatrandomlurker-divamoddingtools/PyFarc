# ulsr, stands for Undefined Length String Reader
# standard usage would simply be ulsr.reader('opened file name here'), it should read at the current offset)

bytes = []
strings = []
int_cancel = int(0)

def reader(MMF):
    while True:
        byte = MMF.read(1)
        if byte == b'\x00':
            if len(bytes) == 0:
                break
            string = b''.join(bytes).decode('utf-8')
            bytes.clear()
            return string
        else:
            bytes.append(byte)
            
def Str_Read_At_Offset(Offset, File):
    curr_pos = int(File.tell())
    File.seek(Offset)
    while True:
        byte = File.read(1)
        if byte == b'\x00':
            if len(bytes) == 0:
                break
            string = b''.join(bytes).decode('utf-8')
            bytes.clear()
            strings.append(string)
            break
        else:
            bytes.append(byte)
        
    File.seek(curr_pos)
    return string



