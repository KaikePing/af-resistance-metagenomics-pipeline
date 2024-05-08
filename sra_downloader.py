from tqdm import tqdm
import os, argparse

# Read the metadata file
def read_sra_numbers(input):
    if os.path.isfile(input):
        with open(input) as f:
            return f.read().splitlines()
    else:
        return [input]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and extract fastq files from SRA")
    parser.add_argument('input', help='SRA number or file containing SRA numbers (one per line)')

    args = parser.parse_args()
    
    sra_numbers = read_sra_numbers(args.input)

    # this will download the .sra files to data/ (will create directory if not present)
    for sra_id in tqdm(sra_numbers):
        print ("Currently downloading: " + sra_id)
        prefetch_command = 'prefetch -O ./data ' + sra_id
        print ("The command used was: " + prefetch_command)
        os.system(prefetch_command)

    # this will extract the .sra files from above into a folder named 'fastq'
    for sra_id in tqdm(sra_numbers):
        print ("Generating fastq for: " + sra_id)
        fastq_dump_command = 'fasterq-dump --outdir ./fastq --gzip --skip-technical --readids --read-filter pass --dumpbase --split-3 --clip ./data/' + sra_id + '/' + sra_id + '.sra'
        # print ("Generating fasta for: " + sra_id)
        # fastq_dump_command = 'fasterq-dump --fasta --outdir ./fastq --gzip --skip-technical --readids --read-filter pass --dumpbase --split-3 --clip ./data/' + sra_id + '/' + sra_id + '.sra'
        print ("The command used was: " + fastq_dump_command)
        os.system(fastq_dump_command)

    print ("All done!")
