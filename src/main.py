import pandas as pd
import pyspark
import glob
from pyspark.sql import SparkSession
from pyspark.context import SparkContext
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import  date, timedelta, datetime
import time
from src.utils.combine_df import combine_df
import json 
from src.utils.error_handling import ErrorHandling 
import os

class Main:
    def __init__(self, payload):
        self.payload = payload 
        # Initializing SparkSession
        self.spark= SparkSession.builder.master("local[1]").appName("Uppsala_assignment").getOrCreate()
        self.hadoop_conf = self.spark.sparkContext._jsc.hadoopConfiguration()
        
        self.schema = StructType(self.payload['schema']) if 'schema' in self.payload else None
        self.default_error_margin = 100

        reference = self.payload.get('reference')
        self.reference_location = reference.get('location') if reference.get('folder', False) == False else glob.glob(f'{reference.get("location")[0]}*')
        self.reference_type = reference.get('type') if 'type' in reference else self.get_file_type('reference')
        self.reference_header = reference.get('header')
        self.reference_delimiter = reference.get('delimiter')
        
        lab = self.payload.get('lab')
        self.lab_location = lab.get('location') if lab.get('folder', False) == False else glob.glob(f'{lab.get("location")[0]}*')
        self.lab_type = lab.get('type') if 'type' in lab else self.get_file_type('lab')
        self.lab_header = lab.get('header')
        self.lab_delimiter = lab.get('delimiter')
        
        results = self.payload.get('results')
        self.results_location = results.get('location')[0]
        self.results_type = results.get('type')
        self.results_name = results.get('name')
            

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
        self.df_markers = self.spark.sql(query_markers)
        df_count_labs = self.spark.sql(query_count_labs)

        self.faulty_result_count = self.assess_error_margin(df_count, df_count_labs)
        
        # write results to output folder if given 
        self.write_results_to_file()
    
        return self.faulty_result_count
    
    def get_file_type(self, type):
        sample_file = self.reference_location[0]
        file_type = sample_file.split(".")[-1]
        return file_type
        
    def assess_error_margin(self, df_count, df_count_labs):
        # getting list of rows using collect()
        count_labs_rows, count_faulty  = self.get_counts_of_failed_and_total_for_lab_files(df_count, df_count_labs)
        
        error_percent = (count_faulty/ count_labs_rows) * 100     
        error_margin = self.payload.get('error_margin', self.default_error_margin)

        
        if error_percent > error_margin:
            error_obj = ErrorHandling('error_margin TOO HIGH', 'NOTICE')
            
            payload = {"text": f"The error_margin calculated is {error_percent}% which is higher than the given {error_margin}%"}
            error_obj.send_slack_notification(payload)
            
            
        return count_faulty
            
    def get_counts_of_failed_and_total_for_lab_files(self, df_count, df_count_labs):
        row_list_count = df_count.collect()
        row_list_count_labs = df_count_labs.collect()
                
        count_faulty = row_list_count[0].__getitem__('count(allele_result)')    
        count_labs_rows = row_list_count_labs[0].__getitem__('count(1)')
        
        return {count_faulty, count_labs_rows}
        
    def write_results_to_file(self):
        # add faulty allele_results in df
        count_of_allele = [
            [f'{self.faulty_result_count} faulty allele_results'],
            ['----------------------------------------'],
            ['markers'], 
            ['----------------------------------------']
        ]
        count_of_allele_df = self.spark.createDataFrame(count_of_allele)
        df_output =count_of_allele_df.union(self.df_markers)

        # write results to output folder if given
        df_output.coalesce(1).write.format("text").option("header", "true").option("encoding", "UTF-8").mode("overwrite").save(f'{self.results_location}')
        
        # rename partition file to given name if provided
        src_path = f'{self.results_location}*.{self.results_type}'
        dest_path = f'{self.results_location}{self.results_name}.{self.results_type}'
        os.rename((glob.glob(src_path))[0], dest_path) 