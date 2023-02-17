import pytest
from src.utils.custom_validations import custom_validations

payload = {
    "reference":{
        "location": ["test/data/HapMap_r23a_CEP_C1_AllSNPs.txt"],
        "header": False,
        "delimiter": "\t",
    },
    "lab":{
        "location": ["test/data/genotype_inf.txt"],
        "header": True,
        "delimiter": ";",
    },
    "results":{
        "location": ["test/data/results/output/"],
        "name": "output",
        "type": "txt",
    },
}

def test_custom_validations():
    obj = custom_validations(payload)
    assert True == obj.validations()
    
def test_custom_validations_bad_payload():
    payload['reference']['header'] = True
    payload['reference']['location'] = ["test/data/reference"]
    with pytest.raises(Exception):
        obj = custom_validations(payload)
        assert False == obj.validations()