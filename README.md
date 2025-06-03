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
