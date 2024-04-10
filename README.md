# Heart Rate Stream ELT Pipeline: Generating Synthetic Data, Sinking to S3, and Loading into a Data Warehouse

<p align="center">
    <img src="docs/img/hr-gif.gif" alt="animated" />
</p>

## Overview

This project implements a data pipeline for historical analysis of heart rate data, primarily catering to medical and research specialists studying cardiovascular health. 

The pipeline begins with the generation of synthetic heart rate data, which is streamed to a Kafka topic for real-time processing and sinked to a cloud data lake for persistant storage. 

The data is then incrementally ingested into a data warehouse where it is transformed and stored in a final state tailored for efficient querying and analysis.

The following research questions could be answered with the warehoused data:

- How does heart rate vary across different activities for users of different genders?

- Are there discernible trends in heart rate variability among users of different blood types across various regions?

- Can historical heart rate data provide insights into the impact of seasonal variations on heart rate patterns among different user demographics?

- Can historical heart rate data be used to predict the likelihood of specific activities occurring at certain times of the day within different regions?

- Can historical heart rate data be used to forecast potential changes in heart rate patterns as users age or undergo changes in weight or height?

## Project Components:

- Synthetic Data Generation: Synthetic heart rate data is generated to simulate real-world scenarios, such as heart rate data measured by an Apple Watch device. Additionally, synthetic operational data is generated (i.e. users data, activities data) that is stored in a mock operational OLTP database (running on PostgreSQL) hosted on an RDS instance.  

- Stream Data 

- Streaming to Kafka: The generated data is streamed to a Kafka topic, where real-time processing is applied before it is eventually written to a data lake for persitent storage.

- Sinking to S3: The S3 bucket partitions and stores the streamed data by its event time (YYYY/MM/DD/HH directory format). This approach enables reusability of the data for subsequent workflows, such as machine learning pipelines operating on raw data. 

- Data Ingestion with Airbyte: Airbyte is used to ingest the static operational RDS data and the unbounded S3 stream data into the data warehouse hosted on Snowflake.

- Transformation with dbt: Data transformation tasks are performed using dbt (Data Build Tool). The transformation tasks are broken down into different stages (staging, serving) and the data is broken into different models adopting a Kimball-style star schema design.

- Star Schema Modeling: This design optimizes query performance and facilitates intuitive analysis by organizing data into fact and dimension tables. Fact tables contain measurable data (heart rate measurements), while dimension tables provide context (user information, timestamp details). Certain dimension tables are implemented as Type 2 Slowly Changing Dimension (SCD) enabling historical tracking of dimensional data (e.g. difference in heart rate for when a user has recorded a change in weight). 

