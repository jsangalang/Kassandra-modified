# Import libraries

import pandas as pd
import matplotlib.pyplot as plt

from IPython.display import Image
from core.mixer import Mixer
from core.cell_types import CellTypes
from core.model import DeconvolutionModel
from core.plotting import print_cell_matras, cells_p, print_all_cells_in_one
from core.utils import *

##############################

# Import training data
dataset_all_anno = pd.read_csv('training_data/all_models_annot.tsv', sep=',', index_col=0)
dataset_all_expr = pd.read_csv('training_data/all_models_expr.tsv', sep=',', index_col=0)

# Laboratory dataset
lab_dataset_anno = pd.read_csv('training_data/laboratory_data_annotation.tsv', sep='\t', index_col = 0)
lab_dataset_expr = pd.read_csv('training_data/laboratory_data_expressions.tsv', sep='\t', index_col=0)

##############################

# Separate into cancer and normal cells

# Cancer
cancer_cells_rows_anno = dataset_all_anno[~dataset_all_anno['Tumor_model_annot'].isna()]
cancer_cells_rows_anno = cancer_cells_rows_anno[cancer_cells_rows_anno['Tumor_model_annot']=='cancer_cells']
cancer_cells_rows_anno = cancer_cells_rows_anno[['Tumor_model_annot', 'Dataset']]
cancer_cells_rows_anno.rename(columns = {'Tumor_model_annot':'Cell_type'}, inplace = True)
cancer_cells_rows_anno['Sample'] = list(cancer_cells_rows_anno.index)
cancer_cells_rows_expr = dataset_all_expr[cancer_cells_rows_anno.index]

# Normal
normal_cells_rows_anno = dataset_all_anno[~dataset_all_anno['Tumor_model_annot'].isna()]
normal_cells_rows_anno = normal_cells_rows_anno[normal_cells_rows_anno['Tumor_model_annot']!='cancer_cells']
normal_cells_rows_anno = normal_cells_rows_anno[['Tumor_model_annot', 'Dataset']]
normal_cells_rows_anno.rename(columns = {'Tumor_model_annot':'Cell_type'}, inplace = True)
normal_cells_rows_anno['Sample'] = list(normal_cells_rows_anno.index)
normal_cells_rows_expr = dataset_all_expr[normal_cells_rows_anno.index]

##############################

# Pseudobulk generation (for artificial datasets)
cell_types = CellTypes.load('configs/cell_types.yaml')
mixer = Mixer(cell_types=cell_types,
              cells_expr=normal_cells_rows_expr, cells_annot=normal_cells_rows_anno,
              tumor_expr=cancer_cells_rows_expr, tumor_annot=cancer_cells_rows_anno,
              num_av = 3, num_points = 30)
expr, values = mixer.generate('Immune_general')

# Model training
mixer = Mixer(cell_types=cell_types,
              cells_expr=normal_cells_rows_expr, cells_annot=normal_cells_rows_anno,
              tumor_expr=cancer_cells_rows_expr, tumor_annot=cancer_cells_rows_anno,
              num_av = 3, num_points = 300000)

model = DeconvolutionModel(cell_types,
                           boosting_params_first_step='configs/boosting_params/lgb_parameters_first_step.tsv',
                           boosting_params_second_step='configs/boosting_params/lgb_parameters_second_step.tsv')
model.fit(mixer)

##############################

# Model prediction with datasets

# First, we have to convert transcripts to genes
expr = pd.read_csv('LOCATION/OF/KALLISTO/TPM/TRANSCRIPTS/COUNTS.tsv', sep='\t', index_col=0)
expr = tr_to_genes(expr, tr_ids_path='data/tumor_model_transcripts.txt')
expr = renorm_expressions(expr, 'data/genes_in_expression.txt')

# Then run the model on this trained model
preds = model.predict(expr) * 100
preds.loc['Lymphocytes'] = preds.loc[['B_cells', 'T_cells', 'NK_cells']].sum()
preds.loc['Stromal'] = preds.loc[['Endothelium', 'Fibroblasts']].sum()
preds_df = pd.DataFrame(preds)

# Save results
preds_df.to_csv('LOCATION/TO/SAVE/DECONVOLUTION/PERCENTAGES.tsv', sep = '\t', header = True, index = True)