# azole-resistance-metagenomics-pipeline

A computational pipeline for identifying antifungal-resistant Aspergillus fumigatus strains in metagenomic data.

# TOC

- [azole-resistance-metagenomics-pipeline](#azole-resistance-metagenomics-pipeline)
- [TOC](#toc)
  - [Requirement](#requirement)
  - [1. Data Retrieval](#1-data-retrieval)
    - [sra\_downloader.py](#sra_downloaderpy)
      - [Usage](#usage)
      - [Example](#example)
  - [2. Kraken2 Building and Classification](#2-kraken2-building-and-classification)
    - [kraken2_workflow.py](#kraken2_workflowpy)
      - [Usage](#usage-1)


## Requirement

- SRA Toolkit (>=3.1.0)
- Kraken2

## 1. Data Retrieval

### sra_downloader.py

This script is used to download and extract `fasta` or `fastq` files from the Sequence Read Archive (SRA). It can take either a single SRA ID or a file containing multiple SRA IDs (one per line) as input.

#### Usage

```bash
python sra_downloader.py <input>
```

Where `<input>` is either a single SRA ID or a file containing multiple SRA IDs (one per line).

#### Example

```bash
python sra_downloader.py SRR123456
```

This command will download the .sra file for SRA ID SRR123456 and extract the `fastq` files.

```bash
python sra_downloader.py sra_ids.txt
```

This command will read the file `sra_ids.txt` (each line containing a single SRA ID) and download and extract the `fastq` files for each SRA ID. 

We provide an example file `example_metagenomics_list.txt` containing a list of SRA IDs from the paper *"Etienne K A, Berkow E L, Gade L, et al. Genomic diversity of azole-resistant Aspergillus fumigatus in the United States[J]. MBio, 2021, 12(4): 10.1128/mbio. 01803-21."*

## 2. Kraken2 Building and Classification

### kraken2_workflow.py

The script automates the process of building a Kraken2 database and running Kraken2 for metagenomic sequence classification. 

It takes as input the name of the database, the directory containing the reference sequences, and the directory containing the FASTQ files. It also accepts optional arguments for the output directory, the report directory, and a flag indicating whether the FASTQ files are paired. 

The script groups FASTQ files based on their prefixes, runs Kraken2 for each group, and generates output and report files named after the corresponding FASTQ file prefix.

#### Usage

```bash
Usage: python kraken2_workflow.py <db_name> <ref_dir> <fastq_dir> [--output-dir OUTPUT_DIR] [--report-dir REPORT_DIR] [--paired]

Arguments:
  db_name: The name of the Kraken2 database to be built.
  ref_dir: The directory containing the reference sequences (.fna files).
  fastq_dir: The directory containing the FASTQ files.

Options:
  --output-dir OUTPUT_DIR: The directory to store the output files. Default is the current directory.
  --report-dir REPORT_DIR: The directory to store the report files. Default is the current directory.
  --paired: Indicate that the FASTQ files are paired. If this flag is set, the script will treat files with the same prefix (before the last underscore) as a pair.

Example:
  python kraken2_workflow.py my_db /path/to/reference /path/to/fastq --output-dir /path/to/output --report-dir /path/to/report --paired
```

This command will build a Kraken2 database named `my_db` using the reference sequences in `/path/to/reference`, then run Kraken2 on the FASTQ files in `/path/to/fastq`. The output and report files will be stored in `/path/to/output` and `/path/to/report`, respectively. The `--paired` flag indicates that the FASTQ files are paired.
