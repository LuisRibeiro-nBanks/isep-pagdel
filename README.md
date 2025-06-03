# PAGDEL

Final Project for the Post-Graduation "Big Data &amp; Decision Making" from ISEP. 
Let's go team!
<br>

### 1. How to run the project

This chapter defines how you are able to run the project.

##### 1.1. Requirements
✅ *Docker Desktop*
✅ *8GB* (or more) of memory alocated to *Docker*

##### 1.2. Steps

>**⚠️ Warning:** To execute the project you should, firstly, ensure that *Docker  Desktop* is currently running on your desktop/server, if not, the following steps won't work as expected.

<br>

To execute the project the following steps should be performed:

1. Access the Project Directory (if not already in there):
```
cd PATH_TO_DIRECTORY
```

2. Ensure the Docker Image is restored:
```
docker-compose down -v
```

3. Ensure there is no Volume Dangling:
```
docker volume prune
```

4. Run the Docker Image:
```
docker-compose up -d  
```

<br>

If you want to run the Docker Image with a single CMD command, you can run the following line:
```
clear; docker-compose down -v; clear; echo "Docker Image is Down"; sleep 2; clear; docker volume prune -f; echo "Pruned all the Volumes!"; sleep 2; clear; docker-compose up -d; clear; echo "PAGDEL Project Initialized Successfully!"; sleep 2
``` 

<br>

##### 1.3. Credentials
**Superset:**
- User: `admin`
- Password: `admin`



### 2. Update Result Dataset

>**⚠️ Warning:** If you find any issue related to the *Google Services*, contact the project infrastructure team to ensure that the Google Drive link is still valid and accessible, or if your *Google* account is able to connect to the projet.

To update the result dataset you should run the `test_drive.py` script.
This script will download the latest dataset from the Google Drive link and update the result dataset in the project.

This script will also update the `result_dataset.csv` file in the project directory, if such action is requested through the `--mode upload` argument.

The arguments that can be passed to the script are:
- `--mode`: The mode of the script. It can be `download` or `upload`.
- `--file`: The path to the file to be uploaded/downloaded.

To run the script, you can use the following command:
```
python test_drive.py --mode MODE --file FILE_PATH
```




### 3. Packages

This chapter defines the packages used in the project.
The following packages are used in the project and should be installed in your environment to run the project successfully:

- `numpy`
- `pyspark`
- `json`
- `time`
- `os`
- `pandas`
- `requests`
- `gdown`
- `google-api-python-client` 
- `google-auth-httplib2` 
- `google-auth-oauthlib`
- `argparse`

To install the packages, you can run the following command:
```
pip install -r requirements.txt
```