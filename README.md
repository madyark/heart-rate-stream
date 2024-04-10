# Heart Rate Sream ELT Pipeline: Generating Synthetic Data, Sinking to S3, and Loading into a Data Warehouse

<p align="center">
    <img src="docs/img/hr-gif.gif" alt="animated" />
</p>

## Overview

This project implements a data pipeline for historical analysis of heart rate data, primarily catering to medical and research specialists studying cardiovascular health. The pipeline begins with the generation of synthetic heart rate data, which is streamed to a Kafka topic for real-time processing and sinked to a cloud data lake for persistant storage. The data is then incrementally ingested into a data warehouse where it is transformed and stored in a final state tailored for efficient querying and analysis.

### Key Components:

- Synthetic Data Generation: Synthetic heart rate data is generated to simulate real-world scenarios, such as Apple Watch .

- Streaming to Kafka: The generated data is streamed to a Kafka topic, ensuring real-time availability and accessibility for further processing.

- ELT Pipeline: A robust Extract, Load, Tranform (ELT) pipeline is employed to process the data from Kafka. This involves transforming the data into a format suitable for historical analysis.

Data Warehousing: Processed data is stored in a Kimball-style data warehouse, adopting a star schema design. This schema enables efficient querying and analysis, enhancing specialists' ability to derive meaningful insights from the data.

The following research questions could be answered with :