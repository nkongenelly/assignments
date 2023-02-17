from pyspark.sql.types import *
payload = {
    "reference":{
        "location": ["test/data/HapMap_r23a_CEP_C1_AllSNPs.txt"],
        "header": False,
        "delimiter": "\t",
        "skip_row": False,
    },
    "lab":{
        "location": ["test/data/genotype_inf.txt"],
        "header": True,
        "delimiter": ";",
        "skip_row": True,
        "skip_row_num": 1
    },
    "results":{
        "location": ["test/data/results/output/"],
        "name": "output",
        "type": "txt",
    },
    "schema": [\
        StructField("individual", StringType(), True),\
        StructField("marker", StringType(), True),\
        StructField("allele_result", StringType(), True)],
    "error_margin": 100
}