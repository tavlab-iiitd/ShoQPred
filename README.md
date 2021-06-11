# ShoQPred - AI for Shock Prediction in ICU Validated across Continents

## Predicting Hemodynamic shock using physiological vitals time-series data
ShoQPred is Deployable Human Centric Software Suite for hemodynamic shock prediction which leverages AI and ML methods on physiological vitals time-series data to predict hemodynamic shock prediction upto 3 to 12 hours before the event.

## Requirements
1. Python 3.6+ / Django
2. Tsfresh
3. Sklearn
(extended requirements in requirements.txt)

or Docker for Docker deployment

## Deployment
### Docker 
Readily available installation, user can pull the docker image from docker hub, here are the instruction to use it.

Create DockerHub Account and login on docker command line using ```docker login```. Pull and run app.

```bash
docker pull raptor4/shoqpredxgb:latest
docker run --name shoqpred-app -p 5005:5005 raptor4/shoqpredxgb:latest
```
App will run on localhost:5005

### Native Python
Native System Deployment Reqirements

System must have:-
1. Python 3.6+
2. Tsfresh

Clone the repository, install requirements and run app.

```bash
git clone https://github.com/SAFE-ICU/ShoQPred
pip3 install -r requirements.txt
python3 manage.py runserver
```


Sample input files are available in sample data.