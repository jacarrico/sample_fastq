#!/usr/bin/env python3

import argparse




def main():
    print("blop")
    def msg(name=None):
        return '''sample_fastq.py '''


    parser = argparse.ArgumentParser(description="This script uses seqtk to sample a file down to target depth", usage=msg())
    parser.add_argument('-gs', nargs='?', type=int, help='genome size', required=True)
    parser.add_argument('-tdep', nargs='?', type=int, help="Target desired depth", required=True)
    args = parser.parse_args()

if __name__ == "__main__":
        main()