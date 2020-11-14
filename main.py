import sys
import farclib

def main():
    if len(sys.argv) < 3:
        dcmpdump_flag = False
    else:
        dcmpdump_flag = True
    farclib.Unpack(sys.argv[1], dcmpdump_flag)
        
if __name__ == "__main__":
    main()
        