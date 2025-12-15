## README FILE

Project name : Snake Project / Automatised analyser of SAM file

## Autors and academic context

**Developers** : Marie-Charlotte PARIENTE & Théo MORLEVAT  
**Academic framework** : System project Bio-Info - 2025-2026 - HAI724I  
**Establishment** : Faculté des Sciences - Université de Montpellier  
**Specialization** : Paired-end sequencing data analysis

## Contacts :
- theo.morlevat@etu.umontpellier.fr
- marie-charlotte.pariente@etu.umontpellier.fr

---

## Global view :

The Snake project aims to facilitate sequence alignment file analysis and generate a summary of the results usable in the laboratory. It was designed to allow the processing of long-range **SAM (Sequence Alignment/Map)** files, thus offering the possibility of separating computer tools from biological data and to ensure that no scripts pollute the experimental files. These scripts were designed to remain accessible and understandable to biologists, without requiring advanced programming skills.

### Features
- **Complete analysis** : Overall statistics, alignment quality, reading pair analysis.
- **Robust parsing** : Decoding of CIGAR and FLAG fields in accordance with official SAM specifications.
- **Sequence extraction** : Automatic generation of files in FASTA format (separation of mapped, unmapped and partially aligned reads).
- **Modular architecture** : Strict separation between source code and experimental data.
- **User interaction** : Interactive options suitable for biologists without advanced computer skills.

**Note** : The authors chose to comment their code extensively in French to make it accessible to French-speaking biologists. In addition, the scripts use explicit variable names and docstrings (Python) in English, thus facilitating understanding and use by the international scientific community.

---

## System architecture

The system relies on two scripts, a bash script and a python script, located in a **centralized folder** :

| Component            | Type     | Role                                                                                 |
|----------------------|----------|--------------------------------------------------------------------------------------|
| `analyse_sam.py`     | Python 3 | Analysis engine: statistical calculations, CIGAR/FLAG parsing, report generation |
| `launcher_bioinfo.sh` | Bash     | User interface: interaction, permission management, secure execution    |

### Arborescent type
```
/root/
├── bio-info/                      # Script folder (Admin)
│   ├── analyse_sam.py
│   ├── launcher_bioinfo.sh
│   ├── LISEZ-MOI.md
│   └── README.md
│
└── home/user/data/                # Biologist's folder (User)
    ├── experiment_1.sam
    └── (Output files generated here)
```
**Fundamental principle** : The scripts remain in `bio-info/` and are never permanently copied to the data folders. During execution, a temporary copy of the Python script is created in the same directory as the SAM file to be analyzed. The commands are then executed in this directory, ensuring that the script acts directly on the local data. Once execution is complete, the temporary copy of the script is automatically deleted.

---

## Technical specifications

### System prerequisites

| Component | Minimum | Recommended |
|-----------|---------|------------|
| Python    | 3.0     | 3.6+       |
| Bash      | 4.0     | 5.1+       |

### Python Dependencies

```
# Standard libraries only
- re (regular expressions)
- sys (system arguments)
- math (mathematical functions)
```

**Advantage** : No external library installation required. Works with a standard Python installation.

### Known limitations

- **File size** : Optimized for SAM < 2 GB (adaptation recommended for larger files)
- **Encoding** : Assumes UTF-8 encoding of SAM files
- **Format** : Expect a standard SAM format (with @HD and @SQ headers recommended, no blank lines)

---

## Installation

### Downloading scripts
Download the Python file analyse_sam.py and the file launcher_bioinfo.sh from git.

```
https://github.com/theo-morlevat/projet-snake.git
```

It is recommended to place these scripts in a folder (example: bio-info) whose path you know.

#### Make the Bash script executable

```bash
chmod +x launcher_bioinfo.sh
```

**Note** : The Python script does not need to be executable; it is called via `python3` by the Bash script.

---

## 
User Guide

### Syntax

```bash
/chemin/vers/bio-info/launcher_bioinfo.sh <DATA_FOLDER> <SAM_FILE>
```
### Arguments

| Argument            | Type           | Description                                                               |
|---------------------|----------------|---------------------------------------------------------------------------|
| `<DATA_FOLDER>`     | Path           | Directory containing your data files (absolute or relative path)          |
| `<SAM_FILE>`        | File name      | Name of the `.sam` file to analyze (must be located in `DATA_FOLDER`)     |

### Concrete examples

- Assuming you are in your session ~

```bash
~/bio-info/launcher_bioinfo.sh ~/my_experiments/exp_1 my_alignement.sam
```
- Once you know the paths to the scripts and the sam file to analyze, you can run this command anywhere.
- The results will be generated in ~/my_experiences/exp_1

### Parameters in argument of launcher_bioinfo.sh

```
-h ou –-help : parameter explaining how to use the script and the possible parameters.

-i ou –-input : parameter specifying what input data to enter and an example.

-o ou --output : parameter specifying the expected output at the end of the script.
```

 ---

## Interactive menu

Once the script is launched, you will be prompted to choose the type of analysis :

### Options available

**1. COMPLETE Analysis**
- Complete summary report (`summary.txt`)
- Calculation of the overall GC percentage
- Read pair analysis (R1/R2), FLAG, CIGAR, chromosome distribution, and MAPQ
- Generating `.fasta` file(s) according to user requirements
- **Duration** : Moderate

**2. CIGAR Analysis**
- CIGAR chain extraction and decoding
- Direct display of results in the terminal (no output file)
- **Duration** : Fast

**3. Analyse MAPPING**
- Alignment quality (MAPQ), %GC content, and chromosome coverage
- Direct display of results in the terminal (no output file)
- **Duration** : Fast

**4. FASTA Extraction**
- Generating `.fasta` file(s) according to user requirements
- 'unmapped' : Unmapped reads (FLAG = 4)
- 'partiallyMapped' : Reads partially mapped (with indels or clipping)
- 'mapped' : Reads perfectly mapped
- 'all' : Generation of the 3 files mentioned above
- **Duration** : Fast to Moderate

**Note** : Execution times are proportional to the size of the input file

### Interaction example

```
Verifications completed
This script could work on all data or on specifics needs. You want to work on : 'full', 'cigar', 'mapping', 'fasta'
full (data entered in the console)
You want to work on : 'mapped', 'partiallyMapped', 'unmapped', 'all'?
all (data entered in the console)
Analysis in progress...
--- Analysis begins (Mode: full) ---
Reading SAM file...
Analyzing CIGAR...
Mapping Analysis (Quality, GC content, Chromosomes)...
FASTA file generation for : ['all'] ...
Writing the complete report...
Success! Check 'summary.txt'
ദി(˵•̀ᴗ-˵)✧
Analysis successfully completed
```
 ---
All results are generated **directly in the data folder** provided as an argument.
This script can create 4 different files.

| File                    | Type  | Generated by                        | Description                                                                  |
|-------------------------|-------|-------------------------------------|------------------------------------------------------------------------------|
| `summary.txt`           | Texte | COMPLETE Analysis                   | Summary report containing: overall statistics, alignment quality, pair analysis, distribution by chromosome, GC content.|
| `unmapped.fasta`        | FASTA | COMPLETE Analysis, FASTA Extraction | DNA sequences of reads that could not be aligned (FLAG 4)                    |
| `partiallyMapped.fasta` | FASTA | COMPLETE Analysis, FASTA Extraction | Sequences are aligned but exhibit indels, clipping, or complex cigar-shaped distortion    |
| `mapped.fasta`          | FASTA | COMPLETE Analysis, FASTA Extraction | Perfectly aligned sequences (without apparent mutations)                     |

### File format `summary.txt`

```
=== SAM ANALYSIS REPORT ===

Total reads analyzed: 2256936
Global GC Content: 22.43%

--- Paired-End Analysis ---
Pairs with 1 Full Mapped & 1 Unmapped: 9
Pairs with 1 Full Mapped & 1 Partial:  156
Pairs fully mapped (Both Perfect):     439

--- Reads per category ---
Number of reads mapped : 119220 (5.28%)
Number of reads partiallyMapped : 87494 (3.88%)
Number of reads unmapped : 2137716 (94.72%)

--- FLAG statistics ---
Number of reads per FLAG value:
FLAG 65 : 166 reads (0.01%)
FLAG 69 : 154 reads (0.01%)
FLAG 73 : 3098 reads (0.14%)
FLAG 77 : 1066875 reads (47.27%)
...

--- Global CIGAR operations ---
Match (M): 37.91%
Insertion (I): 0.0%
Deletion (D): 0.0%
Skipped region (N): 0.0%
Soft clipping (S): 41.22%
Hard clipping (H): 20.85%
Padding (P): 0.0%
Sequence match (=): 0.0%
Sequence mismatch (X): 0.0%

--- Chromosome Distribution ---
Chromosome NC_045512.2 : 119220 reads

--- Position statistics per chromosome ---
Chromosome NC_045512.2 : positions min=7 max=29885 mean=16409.33 sd=9881.18

--- Mapping Quality (MAPQ) ---
Average MAPQ score: 3.14
Distribution:
  0 (Ambiguous/Unmapped): 2138292 (94.74%)
  1-29 (Low Confidence): 389 (0.02%)
  30+ (High Confidence): 118255 (5.24%)
```
---

## How the script works

### Bash script execution flow

To ensure a strict separation between source code and data, the Bash script follows this logic :

1. **Argument verification** : Checking for the presence of 2 arguments
2. **File Validation** : Verification of the existence of the folder and SAM file
3. **Secure travel** : Changing the current directory to the data folder (`cd`)
4. **Temporary copy** : Copying the Python script into the data folder
5. **Execution** : Launching the Python script with the chosen parameters
6. **Cleaning** : Immediate removal of the copy of the Python script
7. **Report** : Display of the final status and generated files

### Python script architecture

- **read_sam** : Analyzes the SAM file and organizes the reads by their query name (QNAME).
- **flag_decoding** : Decodes the FLAGs bit by bit into a dictionary of booleans
- **analyze_cigar** : Analyzes the CIGARs, tallies the databases by type of operation and produces overall statistics on all aligned readings
- **categorize_reads** : Classify the reads into categories (aligned, unaligned, partially aligned)
- **FASTA Generation** : Extraction of the QNAME and sequences based on the selected options
- **analyze_mapping** : Analyzes the distribution of reads mapped onto reference chromosomes
- **analyze_mapq** : Classify the readings into three categories and evaluate the quality scores of the reading mapping.
- **analyze_pairs** : Analyze the "paired-end" reads to identify specific mapping configurations
- **calculate_GC** : Calculate the overall percentage of GC content across all sequences read
- **write_summary** : Write a complete analysis report in a text file

---

## License

This project is distributed under a **copyleft-free** license. You are authorized to :

- Use the code for academic and research purposes
- Modify the code to suit your needs
- Redistribute the modified code, provided that the modifications are mentioned

**Obligations** : Any redistribution must include this license notice and the name(s) of the original author(s).

---

**Last update** : Décember 2025  
**README Version** : 1.0
