# DevOps CA2,  Matteo Coletti X00201548

## Overview
This project is to demonstrate the implementation of Continuous Integration practices around a small application. The application that I used was a simple calculator application built in python to show the following: 
- Proper version control practices.
- Build automation setup.
- CI pipeline implementation.
- Branch protection and policies.
- Automated testing integration.

This documentation will show the processes and steps taken to successfully achieve the tasks ruled out in the CA 2 document in a easy to replicate format. 

## Technologies Used
  - Python 3. For the programming language
  - Pytest. For the testing frameworks
  - PyTest-Cov. For the code coverage 
  - Pylint. For Static code analysis
  
  - Azure DevOps Pipelines. For the automated CL pipeline
  - YAML. For the pipeline configuration
  - Coberura. For the coverage report published to Azure Devops
  - Git. For version control
  - GitHub. To host the repository


## Local Development Setup and Application Features

For the local development setup, I had a project folder that had the following: 
  - An app folder with the calc.py (Calculator application)
  - A tests folder with the test_calc.py file that had my tests.

Below is the code for the two .py files:

Calc.py

```
  def add(a, b):
      return a + b
  
  def multiply(a, b):
      return a * b
  
  def subtract(a, b):
      return a - b
  
  def divide(a, b):
      return a / b
```
test_calc.py

```
from app import calc


def test_add():
    assert calc.add(2, 3) == 5
    assert calc.add(6, 3) == 9


def test_multiply():
    assert calc.multiply(2, 4) == 8
    assert calc.multiply(6, 2) == 12

def test_subtract():
    assert calc.subtract(5, 3) == 2
    assert calc.subtract(7, 1) == 6

def test_divide():
    assert calc.divide(10, 2) == 5
    assert calc.divide(6, 2) == 3
```
So, the calculator had 4 features addition, multiply, subtraction and divide. For the test_calc file I have 4 tests that assert values for a and b and would test that the results are true. 

In the terminal I used the following commands:

```
pip install pytest

pip install pytest-cov
```

These commands installed pytest and pytest coverage. This allowed me to then do some testing locally. I did that by entering the following commands:

```
python -m pytest 

python -m pytest --cov=app
```

Below is the output of the two pytest commands:

<img width="751" height="473" alt="image" src="https://github.com/user-attachments/assets/e7a2be78-d7cc-46d3-866c-0be6c9cf0d2d" />

As you can see from the screenshot above the test_calc.py passed the 4 tests with 100% coverage. 

After I set everything up locally, I pushed the project file up to my GitHub repository to the development branch using the following commands: 

```
git checkout -b development
git add .
git status
git commit -m "Initial setup"
git push -u origin development
```

## CI Pipeline Implementation

I then created an Azure DevOps project and in pipelines connected it to my GitHub repo. 
I then chose an existant yaml file and used the azure-pipelines.yml file below that I pushed into my GitHub repository in the development branch. 


```
trigger:
  branches:
    include:
      - main
      - development

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.x'

  - script: |
      python -m pip install --upgrade pip
      pip install -r requirements.txt
    displayName: 'Install Dependencies'

  - script: pylint app/*.py
    displayName: 'Static Analysis with Pylint'

  - script: |
      pytest -q --cov=app --cov-report=xml --cov-fail-under=80 --junitxml=junit.xml
    displayName: 'Run Tests with Coverage (fail <80%)'


  - task: PublishCodeCoverageResults@2
    inputs:
      codeCoverageTool: Cobertura
      summaryFileLocation: 'coverage.xml'
      reportDirectory: '.'
    displayName: 'Publish Coverage'

```
After this file was set up it automatically ran after every push and pull request to the main and development branch. 

This section of the .yml file below triggers the pipeline for every push and pull to the main or development branch: 
```
trigger:
  branches:
    include:
      - main
      - development

```
This section of the .yml file below installs python and project dependencies using pip:

```

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.x'


  - script: |
      python -m pip install --upgrade pip
      pip install -r requirements.txt
    displayName: 'Install Dependencies'
```

From the snippet of the .yml file above you can see the dependencies are in the requiremnets.txt file.
Below is the contents requirments.txt file: 

```
pytest
pytest-cov
pylint

```

This installs pytest, pytest-cov and pylint into the pipeline.

This section of the .yml file below starts a static code analysis using pylint: 

```
  - script: pylint app/*.py
    displayName: 'Static Analysis with Pylint'

```
The last section of the .yml file below created an xml file, and fails if coverage of the test coverage is under 80% and uploads the coverage results to Azure Devops:

```
  - script: |
      pytest -q --cov=app --cov-report=xml --cov-fail-under=80 --junitxml=junit.xml
    displayName: 'Run Tests with Coverage (fail <80%)'


  - task: PublishCodeCoverageResults@2
    inputs:
      codeCoverageTool: Cobertura
      summaryFileLocation: 'coverage.xml'
      reportDirectory: '.'
    displayName: 'Publish Coverage'
```

After everything in the CI implementation is working you can view the automated testing in full effect every time you trigger a pull or push request on the main and development branches as shown in the job below: 

<img width="3235" height="1538" alt="image" src="https://github.com/user-attachments/assets/76f7951e-b296-461d-95a0-73bd34933a3f" />

## Branch Policies and Protection

In github I configured the main branch with the following:
<img width="2863" height="1342" alt="image" src="https://github.com/user-attachments/assets/4651ef80-e0b5-448b-bfe7-cbc139074f90" />
The two branch protection rules that I enabled for the main branch where "Require a pull request before merging" and "Require status checks to pass before merging" this ensures that you cannot directly push changes into main you would need to perform a pull request from the development branch to the main and it also ensures that the pipeline tests have completed before it can be passed to merge.


## Troubleshooting Guide
The only real issue I faced was an error with the application after some code changes and I accidently left some blank lines at the end of the file so the pipeline job failed at the static analysis of the application code as shown below:
<img width="3167" height="1601" alt="pylint error" src="https://github.com/user-attachments/assets/e9548a9b-29e8-4e45-8218-664d225af898" />
The fix: remove the blank space at the end of the python file for the application save the file and push up to the development branch. It should then pass.


