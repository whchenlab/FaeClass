# FaeClass:  a core gene-based classifier to accurately distinguish Faecalibacterium species

FaeClass, a core gene-based classifier, enables robust discrimination among closely related Faecalibacterium species, including *F. prausnitzii*, *F. duncaniae*, *F. longum*, and other *Faecalibacterium* species.

## Table of Contents

* FaeClass: Faecalibacterium Species Distinguish

  * Table of Contents

  * Software requirement

  * Installation

  * Usage

  * Output Explanation

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

## Output Explanation

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

* **Running Example**

  ```markup
  cd FaeClass/exmaple
  python3 classifier.py test --hmm-dir FaeClass/hmm_classifier --output-dir my_results
  ```

  * **[Sample]_hmm_results.txt**

    · Complete sequence alignment results from HMM search, containing global alignment statistics for each target sequence against HMM models.

    |         Column        |       Description       |
    | :-------------------: | :---------------------: |
    |      target name      |   Target sequence name  |
    |       query name      |      HMM model name     |
    |        E-value        |  Full sequence E-value  |
    |         score         | Full sequence bit score |
    | description of target |  Functional description |

  ![](README_md_files/68dc7200-bcb7-11f0-9a45-433d18e6f797.jpeg?v=1&type=image)

  * **[Sample]_hmm_results_dom.txt**

    · Domain-level alignment results from HMM search, providing detailed alignment information for each individual domain.

    |       Column      |          Description         |
    | :---------------: | :--------------------------: |
    |      c-Evalue     |      Conditional E-value     |
    |      i-Evalue     |      Independent E-value     |
    | hmm coord from/to |      HMM model positions     |
    | ali coord from/to | Alignment sequence positions |

  ![](README_md_files/b079e160-bcb7-11f0-9a45-433d18e6f797.jpeg?v=1&type=image)

  * **[Sample].classification.txt**

    · Classification statistics file, summarizing gene matches and total scores for each taxonomic unit.

    **Type**: Taxonomic unit type. Fp → F. prausnitzii, Fd → F. duncaniae, Fl → F. longum, Other → Other Faecalibacterium species

    **matches**: Number of successfully matched genes

    **total_score**: Sum of bit scores for all matched genes

    **Summary**: Final classification result

  ![](README_md_files/113fe5d0-bcb8-11f0-9a45-433d18e6f797.jpeg?v=1&type=image)

  * **summary.txt**

    · Summary table of classification results for all samples, including final species identification and score information.

    |   Column  |                Description                |
    | :-------: | :---------------------------------------: |
    |   Genome  |             Genome sample name            |
    |    Type   |        Final classification result        |
    | Max_Score | Total score of the highest taxonomic unit |

  ![](README_md_files/35b7fce0-bcb8-11f0-9a45-433d18e6f797.jpeg?v=1&type=image)

  ## Citation

  If you use FaeClass, please cite:

  Li et al. [期刊]. Pan-genomic reclassification of Faecalibacterium prausnitzii sensu lato reveals F. longum as a dominant, functionally distinct, and health-associated gut anaerobe. Reference click here

