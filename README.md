# af-resistance-metagenomics-pipeline

A computational pipeline for identifying antifungal-resistant Aspergillus fumigatus strains in metagenomic data.

## Requirement

- SRA Toolkit
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
