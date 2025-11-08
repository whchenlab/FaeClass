# FaeClass:  Faecalibacterium Species Distinguish

FaeClass, a core gene-based classifier, enables robust discrimination among closely related Faecalibacterium species, including *F. prausnitzii*, *F. duncaniae*, *F. longum*, and other *Faecalibacterium* species.

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

* **Sample Output**

  * **[Sample]_hmm_results.txt**

    · Complete sequence alignment results from HMM search, containing global alignment statistics for each target sequence against HMM models.

    |         Column        |       Description       |
    | :-------------------: | :---------------------: |
    |      target name      |   Target sequence name  |
    |       query name      |      HMM model name     |
    |        E-value        |  Full sequence E-value  |
    |         score         | Full sequence bit score |
    | description of target |  Functional description |

  ```markup
  #                                                               --- full sequence ---- --- best 1 domain ---- --- domain number estimation ---- # target name        accession  query name           accession    E-value  score  bias   E-value  score  bias   exp reg clu  ov env dom rep inc description of target #------------------- ---------- -------------------- ---------- --------- ------ ----- --------- ------ -----   --- --- --- --- --- --- --- --- --------------------- LNFJIAEA_00122       -          aas_Fp_alignment     -            1.5e-35  118.5   1.8   2.6e-35  117.8   1.8   1.4   1   0   0   1   1   1   1 Bifunctional protein Aas LNFJIAEA_02213       -          accA_Fp_alignment    -            3.8e-22   75.7   1.7   2.4e-21   73.1   2.3   2.1   2   0   0   2   2   2   1 Acetyl-coenzyme A carboxylase carboxyl transferase subunit alpha LNFJIAEA_02214       -          accD_Fp_alignment    -            3.2e-36  120.5   1.2   6.3e-36  119.5   1.2   1.5   1   0   0   1   1   1   1 Acetyl-coenzyme A carboxylase carboxyl transferase subunit beta LNFJIAEA_00012       -          ackA_Fp_alignment    -            8.8e-46  151.0   0.8   2.3e-45  149.7   0.8   1.8   1   0   0   1   1   1   1 Acetate kinase 
  ```

  * **[Sample]_hmm_results_dom.txt**

    · Domain-level alignment results from HMM search, providing detailed alignment information for each individual domain.

    |       Column      |          Description         |
    | :---------------: | :--------------------------: |
    |      c-Evalue     |      Conditional E-value     |
    |      i-Evalue     |      Independent E-value     |
    | hmm coord from/to |      HMM model positions     |
    | ali coord from/to | Alignment sequence positions |

  ```markup
  #                                                                            --- full sequence --- -------------- this domain -------------   hmm coord   ali coord   env coord
  # target name        accession   tlen query name           accession   qlen   E-value  score  bias   #  of  c-Evalue  i-Evalue  score  bias  from    to  from    to  from    to  acc description of target
  #------------------- ---------- ----- -------------------- ---------- ----- --------- ------ ----- --- --- --------- --------- ------ ----- ----- ----- ----- ----- ----- ----- ---- ---------------------
  LNFJIAEA_00122       -            203 aas_Fp_alignment     -             60   1.5e-35  118.5   1.8   1   1   8.9e-39   2.6e-35  117.8   1.8     1    60     1    61     1    61 0.99 Bifunctional protein Aas
  LNFJIAEA_02213       -            317 accA_Fp_alignment    -             60   3.8e-22   75.7   1.7   1   2   8.4e-25   2.4e-21   73.1   2.3     1    60     1    58     1    58 0.98 Acetyl-coenzyme A carboxylase carboxyl transferase subunit alpha
  LNFJIAEA_02213       -            317 accA_Fp_alignment    -             60   3.8e-22   75.7   1.7   2   2      0.63   1.8e+03   -3.4   0.0    12    22    70    80    69    82 0.82 Acetyl-coenzyme A carboxylase carboxyl transferase subunit alpha
  LNFJIAEA_02214       -            290 accD_Fp_alignment    -             60   3.2e-36  120.5   1.2   1   1   2.2e-39   6.3e-36  119.5   1.2     1    60     1    60     1    60 1.00 Acetyl-coenzyme A carboxylase carboxyl transferase subunit beta
  ...
  ```

  * **[Sample].classification.txt**

    · Classification statistics file, summarizing gene matches and total scores for each taxonomic unit.

    **Type**: Taxonomic unit type. Fp → F. prausnitzii, Fd → F. duncaniae, Fl → F. longum, Other → Other Faecalibacterium species

    **matches**: Number of successfully matched genes

    **total_score**: Sum of bit scores for all matched genes

    **Summary**: Final classification result

  ```markup
  Type Fp: matches=490, total_score=63276.00
  Type Fd: matches=487, total_score=73982.40
  Type Fl: matches=487, total_score=64263.30
  Type Other: matches=464, total_score=61032.70

  Summary: The highest score type is Fd with a total score of 73982.40.
  ```

  * **summary.txt**

    · Summary table of classification results for all samples, including final species identification and score information.

    |   Column  |                Description                |
    | :-------: | :---------------------------------------: |
    |   Genome  |             Genome sample name            |
    |    Type   |        Final classification result        |
    | Max_Score | Total score of the highest taxonomic unit |

  ```markup
  Genome	Type	Max_Score
  GCA_002549855	Fd	73982.40
  GCA_002549985	Fd	73855.60
  GCA_020687245	Fl	73097.80
  GCA_020687265	Fl	72946.80
  GCA_000166035	Other	65640.30
  GCA_001406355	Other	66909.40
  GCA_000154385	Fp	73014.60
  GCA_000209855	Fp	72453.80
  CLAAAH117.combined	Outgroup	12326.80
  CLAAAH118.combined	Outgroup	11977.30
  ```

  ## Citation

  If you use FaeClass, please cite:

  Li et al. [期刊]. Pan-genomic reclassification of Faecalibacterium prausnitzii sensu lato reveals F. longum as a dominant, functionally distinct, and health-associated gut anaerobe. Reference click here

