#!/usr/bin/env python3

import argparse
import subprocess

def main():
    def msg(name=None):
        return '''sample_fastq.py -P1 [R1.fastq.gz] -P2 [R2.fastq.gz] -gs [Genome size (MB)] -tdep [Target Depth]'''


    parser = argparse.ArgumentParser(description="This script uses seqtk to sample a file down to target depth", usage=msg())
    parser.add_argument('-P1', nargs='?', type=str, help='Paired End fastq.gz 1', required=True)
    parser.add_argument('-P2', nargs='?', type=str, help='Paired End fastq.gz 2', required=True)
    parser.add_argument('-gs', nargs='?', type=float, help='genome size (MB)', required=True)
    parser.add_argument('-tdep', nargs='?', type=int, help="Target desired depth", required=True)
    parser.add_argument('--compSoft', choices=['pigz', 'gzip'], type=str, metavar='pigz', default='pigz',
                        help='Compression software for subsampled reads compression (available options: %(choices)s)',
                        required=False)
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

    print("Subsample target ratio:"+str(Ratio))
    if Ratio < 1:
        print ("Writing read_1.fq.gz")
        ps = subprocess.Popen(('seqtk', 'sample','-s100', P1, str(Ratio)), stdout=subprocess.PIPE)
        with open('read_1.fq.gz','w') as outfile:
            output = subprocess.Popen((args.compSoft, '--fast', '-c'), stdin=ps.stdout, stdout=outfile )
        ps.wait()

        print ("Writing read_2.fq.gz")
        ps = subprocess.Popen(('seqtk', 'sample', '-s100', P2, str(Ratio)), stdout=subprocess.PIPE)
        with open('read_2.fq.gz','w') as outfile:
            output = subprocess.Popen((args.compSoft, '--fast', '-c'), stdin=ps.stdout, stdout=outfile )
        ps.wait()
        print("All done. Have a nice day!")
    else:
        print("WARNING: Original depth lower than target depth: Exiting")

if __name__ == "__main__":
        main()
