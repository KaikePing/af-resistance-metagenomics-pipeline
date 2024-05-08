import os, subprocess, argparse
from collections import defaultdict

def build_kraken2_db(db_name, ref_dir):
    if not os.path.isdir(db_name):
        os.mkdir(db_name)

    if not os.path.isfile(os.path.join(db_name, "hash.k2d")):
        subprocess.run(["kraken2-build", "--download-taxonomy", "--db", db_name])
        for file in os.listdir(ref_dir):
            if file.endswith(".fna"):
                subprocess.run(["kraken2-build", "--add-to-library", os.path.join(ref_dir, file), "--db", db_name])
        subprocess.run(["kraken2-build", "--build", "--db", db_name])

def run_kraken2(db_name, output_dir, report_dir, fastq_dir, paired):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    if not os.path.isdir(report_dir):
        os.mkdir(report_dir)

    fastq_files = defaultdict(list)
    for file in os.listdir(fastq_dir):
        if file.endswith(".fastq"):
            prefix = file.rsplit('_', 1)[0]
            fastq_files[prefix].append(os.path.join(fastq_dir, file))

    for prefix, files in fastq_files.items():
        output_file = os.path.join(output_dir, f"{prefix}_output.txt")
        report_file = os.path.join(report_dir, f"{prefix}_report.txt")

        command = ["kraken2", "--db", db_name, "--output", output_file, "--report", report_file]
        if paired:
            command.append("--paired")
        command.extend(files)
        subprocess.run(command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build Kraken2 database and run Kraken2.')
    parser.add_argument('db_name', help='The name of the database.')
    parser.add_argument('ref_dir', help='The directory containing the reference sequences.')
    parser.add_argument('fastq_dir', help='The directory containing the FASTQ files.')
    parser.add_argument('--output-dir', default='.', help='The directory to store the output file.')
    parser.add_argument('--report-dir', default='.', help='The directory to store the report file.')
    parser.add_argument('--paired', action='store_true', help='Indicate that the input file is a paired FASTQ file.')
    args = parser.parse_args()

    build_kraken2_db(args.db_name, args.ref_dir)
    run_kraken2(args.db_name, args.output_dir, args.report_dir, args.fastq_dir, args.paired)
    