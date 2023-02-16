import pytest
from utils.payload_validation_schema import payload_config_schema
from jsonschema import validate, ValidationError
from pyspark.sql.types import *

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

def test_validation_schema_good():
    result = validate(payload, payload_config_schema)
    
    assert result == None
    
def test_validation_schema_bad():
    payload['reference']['header'] = "False"
    with pytest.raises(Exception):
        validate(payload, payload_config_schema)
    
    