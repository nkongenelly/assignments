import pandas as pd
import pyspark
from pyspark.sql import SparkSession
from pyspark.context import SparkContext
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import  date, timedelta, datetime
import time
from utils.combine_df import combine_df
import json 
from utils.error_handling import ErrorHandling 

class Main:
    def __init__(self, payload):
        self.payload = payload 
        # Initializing SparkSession
        self.spark= SparkSession.builder.master("local[1]").appName("Uppsala_assignment").getOrCreate()
        self.hadoop_conf = self.spark.sparkContext._jsc.hadoopConfiguration()
        
        self.schema = StructType(self.payload['schema']) if 'schema' in self.payload else None
        self.default_tolerance = 100

        self.reference_location = self.payload.get('reference').get('location')
        self.reference_header = self.payload.get('reference').get('header')
        self.reference_delimiter = self.payload.get('reference').get('delimiter')
        
        self.lab_location = self.payload.get('lab').get('location')
        self.lab_header = self.payload.get('lab').get('header')
        self.lab_delimiter = self.payload.get('lab').get('delimiter')

    def process_data(self):
        
        # create dataframe for combined lab files
        df_lab = combine_df(file_location=self.lab_location, table_name="table_lab", header=self.lab_header, delimiter=self.lab_delimiter, schema=self.schema, spark=self.spark)
        
        # assuming lab files will always hav ehe headers, assume lab files schema if schema is not provided in payload
        schema = self.schema if self.schema != None else df_lab.schema
        
        # create dataframe for combined reference files
        df_reference = combine_df(file_location=self.reference_location, table_name="table_reference", header=self.reference_header, delimiter=self.reference_delimiter, schema=schema, spark=self.spark)
        

        # return count
        query_count = "SELECT COUNT(t_lab.allele_result) FROM table_lab t_lab WHERE t_lab.allele_result NOT IN (SELECT t_ref.allele_result FROM table_reference t_ref)"

        # return marker
        query_markers = "SELECT DISTINCT(t_lab.marker) FROM table_lab t_lab WHERE t_lab.allele_result NOT IN (SELECT t_ref.allele_result FROM table_reference t_ref)"

        query_count_labs = "SELECT COUNT(*) FROM table_lab"
        
        df_count = self.spark.sql(query_count)
        df_markers = self.spark.sql(query_markers)
        df_count_labs = self.spark.sql(query_count_labs)

        faulty_result_count = self.assess_tolerance(df_count, df_count_labs)
        
        
        return faulty_result_count
    
    def assess_tolerance(self, df_count, df_count_labs):
        # getting list of rows using collect()
        count_labs_rows, count_faulty  = self.get_counts_of_failed_and_total_for_lab_files(df_count, df_count_labs)
        
        success_percent = (count_faulty/ count_labs_rows) * 100 
        print(f'type....{type(success_percent)}')       
        tolerance = self.payload.get('tolerance_score', self.default_tolerance)

        
        if success_percent < tolerance:
            error_obj = ErrorHandling('TOLERANCE TOO LOW', 'NOTICE')
            
            payload = {"text": f"The files success is {success_percent}% which is lower than the given {tolerance}%"}
            error_obj.send_slack_notification(payload)
            
        return count_faulty
        
        
    def get_counts_of_failed_and_total_for_lab_files(self, df_count, df_count_labs):
        row_list_count = df_count.collect()
        row_list_count_labs = df_count_labs.collect()
                
        count_faulty = row_list_count[0].__getitem__('count(allele_result)')    
        count_labs_rows = row_list_count_labs[0].__getitem__('count(1)')
        
        return {count_faulty, count_labs_rows}
        

