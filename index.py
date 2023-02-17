from src.main import Main
from pyspark.sql.types import *
from src.utils.payload_validation_schema import payload_config_schema
from jsonschema import validate, ValidationError
from src.utils.error_handling import ErrorHandling
from src.utils.custom_validations import custom_validations

# "location": ["data/HapMap_r23a_CEP_C1_AllSNPs.txt","data/HapMap_r23a_CEP_C2_AllSNPs.txt","data/HapMap_r23a_CEP_C13_AllSNPs.txt","data/HapMap_r23a_CEP_C14_AllSNPs.txt","data/HapMap_r23a_CEP_C15_AllSNPs.txt","data/HapMap_r23a_CEP_C16_AllSNPs.txt"],
payload = {
    "reference":{
        "folder" : True,
        "location": ["data/reference/"],
        "header": False,
        "delimiter": "\t",
        "type": "txt"
    },
    "lab":{
        "location": ["data/genotype_inf.txt"],
        "header": True,
        "delimiter": ";",
    },
    "results":{
        "location": ["data/results/output/"],
        "name": "output",
        "type": "txt",
    },
    "schema": [\
        StructField("individual", StringType(), True),\
        StructField("marker", StringType(), True),\
        StructField("allele_result", StringType(), True)],
    "error_margin": 0
}

try:
    # validate the payload
    validate(payload, payload_config_schema)
    
    # more custom validations
    custom_validations_result_obj = custom_validations(payload)
    custom_validations_result = custom_validations_result_obj.validations()

    if custom_validations_result:
        obj = Main(payload)
        res = obj.process_data()
        print(f'No. of faulty alleles = {res}')
except ValidationError as e:
    error_obj = ErrorHandling('PAYLOAD_CONFIG', 'NOTICE')
    error_obj.print_error(e.message)
    
