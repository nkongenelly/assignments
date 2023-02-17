import pytest
from mock import patch
from pyspark.sql import SparkSession
from src.main import Main
import pandas as pd
from data.test_payload import payload as payload

@pytest.fixture(scope="session")
def spark_session():
    return SparkSession.builder.getOrCreate()


def test_process_data(spark_session):
    # with patch('src.main.Main.process_data', return_value='100'):
    with patch('src.utils.error_handling.ErrorHandling.send_slack_notification', return_value=200):
        main_obj = Main(payload)

        result = main_obj.process_data()
        assert result == 605
        assert type(result) == int
        
def test_process_data_with_folder(spark_session):
    payload['reference']['folder'] = True
    payload['reference']['location'] = ["test/data/reference/"]
    with patch('src.utils.error_handling.ErrorHandling.send_slack_notification', return_value=200):
        main_obj = Main(payload)

        result = main_obj.process_data()
        print(result)
        assert result == 605
        assert type(result) == int
        
    
    