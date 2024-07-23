# Data Engineering Practical Case

## Description

This project involves developing a data pipeline that extracts information from public APIs (Banxico and INEGI), cleans it, and stores it in a MongoDB database. Subsequently, this information is queried and visualized in Power BI.

## Project Structure

```
practical_case_engineering/
├── etl/
│   ├── src/
│   │   ├── __pycache__/
│   │   ├── clean_and_store_data.py
│   │   ├── constants.py
│   │   ├── get_apis_data.py
│   │   ├── update_data.py
│   │   ├── test_banxico.py
│   │   ├── test_inegi.py
│   │   ├── test_powerbi_mongo.py
│   │   ├── test_verify_banxico_data.py
│   │   ├── test_verify_mongo_data.py
│   │   └── .env
├── README.md
└── requirements.txt
```

## Environment Setup

### Installing Dependencies

Run the following command to install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### .env File

Create a `.env` file with the following variables:

```
INEGI_TOKEN=<your_inegi_token>
BANXICO_TOKEN=<your_banxico_token>
MONGO_URI=<your_mongo_uri>
```

## Scripts and Functionality

### 1. constants.py

Defines constants and URLs for INEGI and Banxico APIs.

### 2. clean_and_store_data.py

This script cleans and stores the data in MongoDB.

### 3. get_apis_data.py

Extracts data from INEGI and Banxico APIs, cleans it, and stores it in MongoDB.

### 4. update_data.py

Scheduled script to update INEGI and Banxico data in MongoDB.

### Running the Scripts

### Extracting and Storing Data

Run the following command to extract data from INEGI and Banxico APIs, clean it, and store it in MongoDB:

```bash
python etl/src/get_apis_data.py
```

### Updating Data

To update the data periodically, run the following script:

```bash
python etl/src/update_data.py
```

### Verifying Data

To verify that data has been correctly stored in MongoDB:

```bash
python etl/src/test_verify_mongo_data.py
```

### Connecting to Power BI

#### ODBC Connection

1. **Download and Install ODBC Driver**

   Download the MongoDB ODBC driver from the [MongoDB website](https://www.mongodb.com/try/download/odbc-driver).

2. **Configure DSN**

   - Open the ODBC Data Source Administrator on your system.
   - Add a new DSN and configure it using the MongoDB ODBC driver.
   - Enter your connection details, including MongoDB URI, username, and password.

3. **Connect Power BI to MongoDB**

   - Open Power BI Desktop.
   - Go to "Get Data" and select "ODBC".
   - Select the DSN you configured and enter your credentials if prompted.
   - Choose the database and collections you want to import.
   - Load the data into Power BI.

## Example MongoDB URI

Replace `<username>`, `<password>`, and `<database>` with your actual MongoDB Atlas credentials and database name.

```plaintext
mongodb+srv://<username>:<password>@cluster0.mongodb.net/<database>?retryWrites=true&w=majority
```

### Logging and Error Handling

Logs are written to `update_data.log` to keep track of the data extraction and storage process, including any errors encountered.

## Areas of Opportunity

1. **Containerization**
   - Implement the entire project within Docker containers. This would ensure consistency across different environments and simplify the deployment process. By containerizing the application, you can manage dependencies more effectively and scale the solution more easily.

2. **Cloud Integration for Scheduling and Updates**
   - Currently, the update script is scheduled to run on a local machine using Windows Task Scheduler. For a Linux environment, a cron job could be used to achieve the same functionality.
   - To further enhance this, migrating the scheduling to a cloud service like AWS Glue could automate the updates at specific intervals without manual intervention. AWS Glue jobs can be scheduled to run at specific times, ensuring the data is always up-to-date. Similarly, Azure Data Factory or Google Cloud Composer can be used for scheduling and orchestrating ETL workflows.

3. **Automated Power BI Refresh**
   - Power BI reports can be configured to refresh periodically. By setting up a data refresh schedule, you can ensure that the reports always display the most recent data. This can be managed directly within the Power BI service.

4. **Enhanced Logging and Monitoring**
   - Implement more comprehensive logging and monitoring for the ETL processes. Using a centralized logging service like AWS CloudWatch can provide better insights into the performance and any issues that arise.

5. **Scalability and Performance Optimization**
   - The use of distributed databases or data warehouses might be necessary for handling larger datasets.

6. **Security Enhancements**
   - Ensure that all sensitive data is encrypted both in transit and at rest. Implement role-based access control (RBAC) to restrict access to the data and ETL processes.

7. **Documentation and Code Quality**
   - Improve documentation to include more detailed explanations of each component and its purpose. Additionally, ensure that the code adheres to best practices for readability and maintainability, possibly incorporating automated linting and testing frameworks.
   
## Conclusion

By following the steps outlined above, you can successfully extract data from public APIs, clean and store it in MongoDB, and visualize it in Power BI. This documentation provides a comprehensive guide to setting up and running the data pipeline effectively.
