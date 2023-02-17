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
    },
    "lab":{
        "location": ["data/genotype_inf.txt"],
        "header": True,
        "delimiter": ";",
    },
    "schema": [\
        StructField("individual", StringType(), True),\
        StructField("marker", StringType(), True),\
        StructField("allele_result", StringType(), True)],
    "tolerance_score": 100
}

try:
    # validate the payload
    validate(payload, payload_config_schema)

    obj = Main(payload)
    res = obj.process_data()
    print(f'No. of faulty alleles = {res}')
except ValidationError as e:
    error_obj = ErrorHandling('PAYLOAD_CONFIG', 'NOTICE')
    error_obj.print_error(e.message)
