# FaeClass:  Faecalibacterium Species Distinguish

FaeClass, a Core-gene-based Classifier, enables robust discrimination among closely related Faecalibacterium species, including *F. prausnitzii*, *F. duncaniae*, *F. longum*, and other *Faecalibacterium* species.

## Table of Contents

* FaeClass: Faecalibacterium Species Distinguish

  * Table of Contents

  * Software requirement

  * Installation

  * Usage

  * Expected Output

  * Citation

## Software requirement

* Python 3.6+

* HMMER 3.1+

## Installation

To install FaeClass, download the model directory (hmm_classifier) and the execution script (classifier.py) from the GitHub repository.

* **hmm_classifier/**

  * **Fp, Fd, Fl, Other**: Species-specific directories.

    * ***.aln**: Core gene alignment files for each species group.

    * ***.hmm**: Individual single-gene HMM models for each species group.

  * ***_models.hmm**: Single-species HMM databases.

  * ***_models.hmm.h3***: Compressed index files for each single-species HMM database.

  * **merged.hmm**: Complete HMM database combining all species groups.

  * **merged.hmm.h3***: Compressed index files for the complete merged database.

* **classifier.py**: Main script implementing the classification functionality.

## Usage

* **Basic Usage**

  python3 classifier.py /path/to/genome_dir

* **Advanced Usage with Custom Parameters**

  python3 classifier.py /path/to/genome_dir --hmm-dir my_hmms --output-dir my_results

* **Parameter Description**

  * /path/to/genome_dir: Input directory containing sequence files for classification.

  * --hmm-dir: (Optional) Custom directory containing HMM database files.

  * --output-dir: (Optional) Custom directory for storing classification results.

* **Input Requirements**

  * Files should be standard protein sequence (FASTA format) with the ".faa" file extension, either from public databases or derived from de novo genome annotation pipelines.

## Expected Output

All results will be saved in the hmm_results directory (customizable via the --output-dir parameter).

* **Directory Structure**

  hmm_results/&#x20;

  ├── details/                           # Detailed Results Directory&#x20;

  │   ├── [Sample1]_hmm_results.txt      # Raw HMM Search Results&#x20;

  │   ├── [Sample1]_hmm_results_dom.txt  # HMM Domain-Level Details&#x20;

  │   ├── [Sample2]_hmm_results.txt&#x20;

  │   └── ...&#x20;

  ├── [Sample1].classification.txt       # Individual Sample Classification Results&#x20;

  ├── [Sample2].classification.txt&#x20;

  ├── ...

  └── summary.txt                       # Final Summary File

* **Classification Key**

  * Fp → *F. prausnitzii*

  * Fd → *F. duncaniae*

  * Fl → *F. longum*

  * Other → Other *Faecalibacterium* species

  * Outgroup → Non-*Faecalibacterium* species (organisms outside the *Faecalibacterium* genus)

## Citation

If you use FaeClass, please cite:

Li et al. []. Pan-genomic reclassification of *Faecalibacterium* prausnitzii sensu lato reveals *F. longum* as a dominant, functionally distinct, and health-associated gut anaerobe. Reference click here
github: https://github.com/MinWLi/FaeClass



