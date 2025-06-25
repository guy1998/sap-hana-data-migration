# sap-hana-data-migration
This is a simple solution that handles migration of data between tables in two different SAP-hana databases. The migration is performed in batches which makes it ideal even for large amounts of data You can run it on your own machine as a simple python script or as a deployment in kubernetes. Both are explained below.

# Running as a python script
To run this code as a python script all you have to do is specify the `.env` file (please check the section below on that). Then run the following command to install all libraries and dependencies (python 3.10 or newer required):
```bash 
pip install -r requirements.txt
```
Then you can simply start the script by executing the following command or in your preferred IDE (e.g PyCharm)
```bash
python main.py
```
Now you can relax and wait for the migration to finish.

# Running it as a deployment in kubernetes
To run it as a Kubernetes deployment you can use the following `.yaml` template. Feel free to change the name of the deployment and of course do not forget to update your .env variables. In here I will specify my own docker image but you can of course create another one by forking this repo.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hana-migrator
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hana-migrator
  template:
    metadata:
      labels:
        app: hana-migrator
    spec:
      containers:
        - name: hana-migrator
          image: your-dockerhub-username/hana-migrator:latest
          imagePullPolicy: Always
          env:
            - name: SOURCE_ADDRESS
              value: "your.source.db.address"
            - name: SOURCE_PORT
              value: "30015"
            - name: SOURCE_USER
              value: "admin"
            - name: SOURCE_PASSWORD
              value: "admin_pass"
            - name: TARGET_ADDRESS
              value: "your.target.db.address"
            - name: TARGET_PORT
              value: "30015"
            - name: TARGET_USER
              value: "admin"
            - name: TARGET_PASS_WORD
              value: "admin_pass"
            - name: SOURCE_TABLE
              value: "MY_SCHEMA.SOURCE_TABLE"
            - name: TARGET_TABLE
              value: "MY_SCHEMA.TARGET_TABLE"
            - name: BATCH_SIZE
              value: "1000"
            - name: ORDER_BY
              value: "ID"
            - name: FILENAME
              value: "logfile.txt"
```
# Environment variables
This application uses the following environment variables to configure the source and target SAP HANA database connections, table names, batching behavior, and logging.
### Hana source configuration
| Variable          | Description                          | Example              |
| ----------------- | ------------------------------------ | -------------------- |
| `SOURCE_ADDRESS`  | Hostname or IP of the source HANA DB | `source.hana.local`  |
| `SOURCE_PORT`     | Port for source HANA DB              | `30015`              |
| `SOURCE_USER`     | Username for source HANA DB          | `admin`              |
| `SOURCE_PASSWORD` | Password for source HANA DB          | `my_secret_password` |
### Hana target configuration
| Variable           | Description                          | Example              |
| ------------------ | ------------------------------------ | -------------------- |
| `TARGET_ADDRESS`   | Hostname or IP of the target HANA DB | `target.hana.local`  |
| `TARGET_PORT`      | Port for target HANA DB              | `30015`              |
| `TARGET_USER`      | Username for target HANA DB          | `admin`              |
| `TARGET_PASSWORD` | Password for target HANA DB          | `my_secret_password` |
### Batch and table configuration
| Variable       | Description                              | Example                 |
| -------------- | ---------------------------------------- | ----------------------- |
| `SOURCE_TABLE` | Full name of the source table            | `MY_SCHEMA.SOURCE_DATA` |
| `TARGET_TABLE` | Full name of the target table            | `MY_SCHEMA.TARGET_DATA` |
| `BATCH_SIZE`   | Number of rows per batch migration       | `1000`                  |
| `ORDER_BY`     | Column name to order rows during reading | `ID`                    |
### Logging
| Variable   | Description                         | Example       |
| ---------- | ----------------------------------- | ------------- |
| `FILENAME` | Path or filename for the log output | `logfile.txt` |

