This project requires Python 2.7, with boto3 and scikit learn.

experiments.py was used to conduct accuracy experiments.

The main class for the deployed service is service.py, but this requires access to the database.
Deployment of this project to the cloud requires building all of the dependencies for scikit-learn and pymysql,
then including them with the source code in a zip file uploaded to AWS lambda. (Not recommended without assistance from the team)









