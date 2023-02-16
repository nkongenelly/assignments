from src.main import Main
from pyspark.sql.types import *
from utils.payload_validation_schema import payload_config_schema
from jsonschema import validate, ValidationError
from utils.error_handling import ErrorHandling

payload = {
    "reference":{
        "location": ["data/HapMap_r23a_CEP_C1_AllSNPs.txt","data/HapMap_r23a_CEP_C2_AllSNPs.txt","data/HapMap_r23a_CEP_C13_AllSNPs.txt","data/HapMap_r23a_CEP_C14_AllSNPs.txt","data/HapMap_r23a_CEP_C15_AllSNPs.txt","data/HapMap_r23a_CEP_C16_AllSNPs.txt"],
        "header": False,
        "delimiter": "\t",
        "skip_row": False,
    },
    "lab":{
        "location": ["data/genotype_inf.txt"],
        "header": True,
        "delimiter": ";",
        "skip_row": True,
        "skip_row_num": 1
    },
    "schema": [\
        StructField("individual", StringType(), True),\
        StructField("marker", StringType(), True),\
        StructField("allele_result", StringType(), True)],
    "tolerance_score": 100
}


# validate the payload
try:
    validate(payload, payload_config_schema)

    obj = Main(payload)
    obj.process_data()
except ValidationError as e:
    error_obj = ErrorHandling('PAYLOAD_CONFIG', 'NOTICE')
    error_obj.print_error(e.message)