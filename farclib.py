import struct
import ulsr
import os
import gzip

class FarcHead(object):
    def FarcHead(self):
        self.Format
        self.Header_Size
        self.Alignment  # Internal use only, doesn't matter for reading/writing, best to just use alignment 1
        
class FarcEntry(object):
    def FarcEntry(self):
        self.FileName
        self.FileOffset
        self.FileSizeCompressed
        self.FileSizeDecompressed
        
def PrintFileMeta(file):
    with open(file, 'rb') as f:
        Is_Encrypted = False
        Is_Compressed = False
        Head = FarcHead()
        Head.Format = f.read(4).decode('UTF-8')
        Head.Header_Size = struct.unpack(">I", f.read(4))[0]
        Head.Alignment = struct.unpack(">I", f.read(4))[0]
        if Head.Format[2] == 'R':
            Is_Encrypted = True
        if Head.Format[3] == 'C':
            Is_Compressed = True
        print(Head.Format)
        print(f"Farc Details: Is_Encrypted = {Is_Encrypted}, Is_Compressed = {Is_Compressed}, Header Length (Bytes) = {Head.Header_Size}, File Alignment: {Head.Alignment}.")
        while True:
            if f.tell() >= Head.Header_Size:
                break
            ENT = FarcEntry()
            ENT.FileName = ulsr.reader(f)
            ENT.FileOffset = struct.unpack(">I", f.read(4))[0]
            ENT.FileSizeCompressed = struct.unpack(">I", f.read(4))[0]
            ENT.FileSizeDecompressed = struct.unpack(">I", f.read(4))[0]
        
            print(f"Entry Details: File Name = {ENT.FileName}, Offset = {ENT.FileOffset}, Compressed Size = {ENT.FileSizeCompressed}, Decompressed size = {ENT.FileSizeDecompressed}")

def Unpack(file, dumpCompressedData):
    EntryList = []
    with open(file, 'rb') as f:
        s_path = file.split('.')
        if not os.path.exists(s_path[0]):
            os.mkdir(s_path[0])
        if dumpCompressedData == True:
            if not os.path.exists(f'{s_path[0]}_cmp'):
                os.mkdir(f'{s_path[0]}_cmp')
        Is_Encrypted = False
        Is_Compressed = False
        Head = FarcHead()
        Head.Format = f.read(4).decode('UTF-8')
        Head.Header_Size = struct.unpack(">I", f.read(4))[0]
        Head.Alignment = struct.unpack(">I", f.read(4))[0]
        if Head.Format[2] == 'R':
            Is_Encrypted = True
        if Head.Format[3] == 'C':
            Is_Compressed = True
        while True:
            if f.tell() >= Head.Header_Size:
                break
            
            ENT = FarcEntry()
            ENT.FileName = ulsr.reader(f)
            ENT.FileOffset = struct.unpack(">I", f.read(4))[0]
            ENT.FileSizeCompressed = struct.unpack(">I", f.read(4))[0]
            ENT.FileSizeDecompressed = struct.unpack(">I", f.read(4))[0]
            
            EntryList.append(ENT)
        for entry in EntryList:
            f.seek(entry.FileOffset)
            cmpData = f.read(entry.FileSizeCompressed)
            if dumpCompressedData == True:
                with open(f'{s_path[0]}_cmp//{entry.FileName}', 'wb') as cmpOut:
                    cmpOut.write(cmpData)
            dcmpData = gzip.decompress(cmpData)
            with open(f'{s_path[0]}//{entry.FileName}', 'wb') as dcmpOut:
                dcmpOut.write(dcmpData)
            
        