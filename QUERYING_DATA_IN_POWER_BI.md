# Querying Data in Power BI

## Connecting MongoDB Atlas with Power BI

Here’s a detailed process I followed to connect MongoDB Atlas to Power BI and query the tables.

### Prerequisites

1. **MongoDB Atlas Account**: I ensured I had a MongoDB Atlas account with a cluster and database set up.
2. **Power BI Desktop**: I downloaded and installed Power BI Desktop from the [official website](https://powerbi.microsoft.com/desktop/).
3. **MongoDB ODBC Driver**: I downloaded and installed the MongoDB ODBC driver from the [MongoDB website](https://www.mongodb.com/try/download/odbc-driver).

### Step-by-Step Guide

#### 1. Configure MongoDB Atlas

1. **Create a Cluster**: I created a cluster in MongoDB Atlas.
2. **Set Up Network Access**: I ensured my IP address was whitelisted in MongoDB Atlas.
3. **Create Database and Collections**: I set up my database and collections. For this case, I created the following collections:
   - `consumer_confidence`
   - `inpc_base`
   - `unemployment_rate`
4. **Obtain Connection String**: I obtained my MongoDB connection string (URI) from the Atlas dashboard. It looks like this:
   ```plaintext
   mongodb+srv://<username>:<password>@cluster0.mongodb.net/<database>?retryWrites=true&w=majority
   ```

#### 2. Install and Configure the MongoDB ODBC Driver

1. **Download the Driver**: I downloaded the MongoDB ODBC driver from the [MongoDB website](https://www.mongodb.com/try/download/odbc-driver).
2. **Install the Driver**: I ran the installer and followed the installation instructions.

#### 3. Set Up DSN (Data Source Name)

1. **Open ODBC Data Source Administrator**: In Windows, I searched for "ODBC Data Source" in the start menu and opened it.
2. **Add a New DSN**:
   - I went to the "User DSN" or "System DSN" tab and clicked "Add".
   - I selected the MongoDB ODBC driver and clicked "Finish".
3. **Configure the DSN**:
   - I entered a name for my DSN (e.g., `MongoDB_BI`).
   - I provided the MongoDB URI I obtained earlier.
   - I tested the connection to ensure it worked.

#### 4. Connect Power BI to MongoDB

1. **Open Power BI Desktop**: I launched Power BI Desktop on my computer.
2. **Get Data**: I clicked on "Get Data" in the Home ribbon.
3. **Select ODBC**:
   - In the "Get Data" window, I selected "ODBC" and clicked "Connect".
   - I chose the DSN I configured (`MongoDB_BI`).
4. **Enter Credentials**:
   - If prompted, I entered my MongoDB Atlas username and password.
5. **Select Database and Collections**:
   - I navigated through the database and selected the collections I wanted to import.
   - I clicked "Load" to bring the data into Power BI.

#### 5. Querying and Visualizing Data

1. **Explore the Data**:
   - Once the data was loaded, I started exploring it using the fields pane in Power BI.
2. **Create Visualizations**:
   - I dragged and dropped fields to the canvas to create various visualizations such as tables, charts, and graphs.
3. **Build Reports**:
   - I combined multiple visualizations to build comprehensive reports.
4. **Set Up Data Refresh**:
   - In the Power BI service, I scheduled data refreshes to ensure my reports were always up-to-date with the latest data from MongoDB Atlas.

By following these steps, I was able to successfully connect MongoDB Atlas to Power BI and visualize my data. This documentation provides a comprehensive guide to setting up and querying data in Power BI effectively.