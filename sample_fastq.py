#!/usr/bin/env python3

import argparse
import sys
import os
import subprocess

def main():
    def msg(name=None):
        return '''sample_fastq.py -P1 [R1.fastq.gz] -P2 [R2.fastq.gz] -gs [Genome size (MB)] -tdep [Target Depth]'''


    parser = argparse.ArgumentParser(description="This script uses seqtk to sample a file down to target depth", usage=msg())
    parser.add_argument('-P1', nargs='?', type=str, help='Paired End fastq.gz 1', required=True)
    parser.add_argument('-P2', nargs='?', type=str, help='Paired End fastq.gz 2', required=True)
    parser.add_argument('-gs', nargs='?', type=float, help='genome size (MB)', required=True)
    parser.add_argument('-tdep', nargs='?', type=int, help="Target desired depth", required=True)
    args = parser.parse_args()

    GenomeSize = args.gs
    TargetDepth = args.tdep
    P1 = args.P1
    P2 = args.P2

    R1_fqchk = subprocess.Popen(['seqtk', 'fqchk', P1], stdout=subprocess.PIPE)
    R1_stdout, R1_stderr = R1_fqchk.communicate()
    B_P1=int(R1_stdout.splitlines()[2].split()[1])
    print("Bases P1:"+str(B_P1))

    R2_fqchk = subprocess.Popen(['seqtk', 'fqchk', P2], stdout=subprocess.PIPE)
    R2_stdout, R2_stderr = R2_fqchk.communicate()
    B_P2= int(R2_stdout.splitlines()[2].split()[1])
    print("Bases P2:"+str(B_P2))
    print("")

    EstCov = (B_P1 + B_P2)/ (GenomeSize * 1E6)
    print ("Estimated coverage: "+str(EstCov))
    Ratio = TargetDepth/EstCov

    print(Ratio)
    if Ratio < 1:
        ps = subprocess.Popen(('seqtk', 'sample', P1, str(Ratio)), stdout=subprocess.PIPE)
        with open('R1.fq.gz','w') as outfile:
            output = subprocess.Popen(('pigz', '--fast', '-c'), stdin=ps.stdout, stdout=outfile )
        ps.wait()

       ps = subprocess.Popen(('seqtk', 'sample', '-s 100', P2, str(Ratio)), stdout=subprocess.PIPE)
        with open('R2.fq.gz','w') as outfile:
            output = subprocess.Popen(('pigz', '--fast', '-c'), stdin=ps.stdout, stdout=outfile )
        ps.wait()



if __name__ == "__main__":
        main()