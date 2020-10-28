# PyFarc
import struct
import os

class FarcHeader(object):
  def FarcHeader(self):
    self.F
    self.A
    self.r
    self.c
    self.Alignment

class FileMD(object):
  def FarcHeader(self):
    self.FileSize
    self.CompressedSize
    self.Offset
    self.Name

def WriteFarc(outfarc):
  path = input("> ")
  infolderlist = os.listdir(path)
  offsets_positions = []
  with open(outfarc, 'r+b') as farc:
    farc.write(b'FArc')
    farc.write(struct.pack("I", 1))
    for file in infolderlist:
      with open(path + "/" + file, 'rb') as d:
        data = d.read()
        MD = FileMD()
        MD.FileSize = len(data)
        MD.CompressedSize = len(data)
        MD.Offset = 0
        MD.Name = file.encode("UTF-8")
        farc.write(struct.pack("I", MD.FileSize))
        farc.write(struct.pack("I", MD.CompressedSize))
        pos = farc.tell()
        farc.write(struct.pack("I", MD.Offset))
        farc.write(MD.Name)



WriteFarc('f.farc')
