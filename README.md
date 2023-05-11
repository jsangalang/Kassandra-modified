# Modified Kassandra model
This is a modified version of the Kassandra deconvolution model, based initially by the paper by Zaitsev et al., 2022:

Zaitsev A, Chelushkin M, Dyikanov D, Cheremushkin I, Shpak B, Nomie K, Zyrin V, Nuzhdina E, Lozinsky Y, Zotova A, Degryse S, Kotlov N, Baisangurov A, Shatsky V, Afenteva D, Kuznetsov A, Paul SR, Davies DL, Reeves PM, Lanuti M, Goldberg MF, Tazearslan C, Chasse M, Wang I, Abdou M, Aslanian SM, Andrewes S, Hsieh JJ, Ramachandran A, Lyu Y, Galkin I, Svekolkin V, Cerchietti L, Poznansky MC, Ataullakhanov R, Fowler N, Bagaev A. Precise reconstruction of the TME using bulk RNA-seq and a machine learning algorithm trained on artificial transcriptomes. Cancer Cell. 2022 Aug 8;40(8):879-894.e16. doi: 10.1016/j.ccell.2022.07.006. PMID: 35944503.

The initial command line implementation in BostonGene/Kassandra repository was missing some information. Therefore, I tried my modified version of their code.

All original code is written by BostonGene, the authors and their collaborators. This is only a mere modification to their code, since no one has been updating/replying to issues in their Github since 2021.

The issues namely in their code were:
| No.  | Issue | Fix |
| -----|--------------|-------------|
| 1    | `cell_types.yaml` includes `Dendritic_cells` and `Granulocytes`, however they are not included in the training datasets. | Updated `cell_types.yaml` to remove these cell types. **However**, because of this, they are no longer included in the deconvolution. |
| 2    | The Python code does not separate the training data into cancer and normal cells, causing errors when running the code | Added some lines of script in the Python code to separate cancer and normal cells. |
| 3    | Some errors in the `change_subtype_proportions` function of `core/mixer.py` | Changed `specified_subtypes = set(self.proportions.dropna().index).intersection(cell_subtypes)` to `specified_subtypes = list(set(self.proportions.dropna().index).intersection(cell_subtypes))` |

**NOTE:** I've only used this for the tumor model, so I don't know how this would work for the full blood model. 

## Instructions:
1. Create conda environment using the environment.yaml: `conda env create -f environment.yaml`
2. Download training data from BostonGene's website (https://science.bostongene.com/kassandra/downloads). The training data for Kassandra are both *Collection of 9056 bulk RNA-seq samples from 505 datasets of sorted cells, cancer cells and cell lines* and *348 bulk RNA-seq samples of sorted cell populations (including 343 samples of cells from the blood)* >> i.e., 4 files in total.
   I placed these in a directory called "training_data" 
3. Modify the "kassandra_model_training_example.py" to change the **location + name of your input data**, and the **location + name of the resulting output data**. *Note*: The input data **MUST** be the transcript TPM results from running kallisto.
4. Modify the "kassandra_model_training_example.sh" to change parameters to run on your HPC, such as changing SBATCH parameters and location of your conda bin.
5. Run the "kassandra_model_training_example.sh". If using sbatch, I run it with `sbatch kassandra_model_training_example.sh`
