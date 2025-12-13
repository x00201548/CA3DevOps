# DevOps CA3,  Matteo Coletti X00201548

## Overview
This project is to demonstrate the implementation of a complete CI/CD Pipeline, extending the CI implementation of CA2.


## Technologies Used
- Python 3. For the programming language
- Pytest. For the testing frameworks
- PyTest-Cov. For the code coverage 
- Pylint. For Static code analysis
- Slenium. For UAT testing.
- Locust for performance testing.
- Azure Devops for CI/CD pipeline.
- SonarCloud for security testing.

## Local Setup
- I first cloned my CA2 Repo and created a new CA3 folder.
- I then set up a new repo and pushed the CA3 folder into the development branch.
- I then set up a new project in Azure Devops and connected the github repository.

## Application Features
For the application it is a basic calculator application. I tried to create a web viesrion of the calculator but failed to deploy it when triggering the pipleine so I kept the application the same as CA2 and added new features and used the calculator.net app as the application I will be testing for selenium and other web based testing as I was having issues with my own applictaion.

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

  def square(a):
      """Return the square of a."""
      return a * a
  
  def cube(a):
      """Return the cube of a."""
      return a * a * a

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

def square(a):
    """Return the square of a."""
    return a * a

def cube(a):
    """Return the cube of a."""
    return a * a * a

``` 

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

 

After I set everything up locally, I pushed the project file up to my GitHub repository to the development branch using the following commands: 

```
git checkout -b development
git add .
git status
git commit -m "Initial setup"
git push -u origin development
```

## Pipeline Implementation

I then created a new Azure DevOps project and in pipelines connected it to my GitHub repo. 
I then chose an existant yaml file and used the azure-pipelines.yml file below that I pushed into my GitHub repository in the development branch. 

Below is my previous CA2 .yaml file

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
Below is the added yaml  steps and stages for CA3 integration:


```

    steps:

      - task: SonarCloudPrepare@4
        inputs:
          SonarCloud: 'Devops'
          organization: 'x00201548'
          scannerMode: 'CLI'
          configMode: 'manual'
          cliProjectKey: 'x00201548_CA3DevOps'
          cliProjectName: 'CA3DevOps'
          cliSources: 'app'
          extraProperties: |
            sonar.python.coverage.reportPaths=coverage.xml
            sonar.python.xunit.reportPath=junit.xml
        displayName: 'SonarCloud'

          - task: SonarCloudAnalyze@4
        displayName: 'Analyze'
      - task: PublishCodeCoverageResults@2
        inputs:
          codeCoverageTool: Cobertura
          summaryFileLocation: 'coverage.xml'
          reportDirectory: '.'
        displayName: 'Publish Coverage'



```
The SonarCloudPrepare@4 Task above prepares the pipline to send code results to Sonar cloud. It connects to my sonar cloud project and scans the app folder. The Task SonarCloudAnalyze@4 scans the code for security vulribilities and publishes the results.
```
      - script: |
          pytest tests/test_calc_selenium.py -v 
        displayName: 'Selenium UAT Tests'

```
The Above script runs the selenium tests in my test/ folder.
```
      - script: |
          pip install locust
          echo "from locust import HttpUser, task
          class WebsiteUser(HttpUser):
              @task
              def test_homepage(self):
                  self.client.get('/')
          " > locustfile.py
          locust --headless -u 5 -r 1 -t 10s --host=https://www.calculator.net 
        displayName: 'Performance Testing with Locust'

```
The above script runs performance testing on the calculator.net website. The test uses 5 users to identify the website performance under load.

```

      - task: CopyFiles@2
        inputs:
          contents: |
            app/**
            requirements.txt
            *.py
          targetFolder: '$(Build.ArtifactStagingDirectory)'
        displayName: 'Copy Application Files'

```
The Above task copies all contents of the app folder requirments and all .py files into the artifact staging directory.
```
      - task: PublishBuildArtifacts@1
        inputs:
          pathToPublish: '$(Build.ArtifactStagingDirectory)'
          artifactName: 'drop'
```
The above task then publishes the artifacts.
```
- stage: DelpoyTest
  displayName: "Delpoy to Test"
  dependsOn: Build
  condition: succeeded()
  jobs:
  - deployment: DeployTest
    environment: 'Test'
    pool:
      vmImage: 'ubuntu-latest'
    strategy:
      runOnce:
        deploy:
          steps:
          - download: current
            artifact: drop
          - script: echo "Deploying to Test environment"
            displayName: 'Deploy to Test'
```
The above stage deploys the test stage. The test stage only deploys if the build stage succeeds. If build stage succeeds the Test enviroment can deploy after a manual approval has been made in Azure Devops.
```
- stage: DeployProduction
  displayName: "Deploy To Production"
  dependsOn: DeployDev
  condition: succeeded()
  jobs:
  - deployment: DeployProduction
    environment: 'Production'
    pool:
      vmImage: 'ubuntu-latest'
    strategy:
      runOnce:
        deploy:
          steps:
          - download: current
            artifact: drop
          - script: echo "Deploying to Production environment"
            displayName: 'Deploy to Production'
```
The above stage is the Production stage that Runs after the Test stage is successful. It targets the test enviroment after a manual approval has been made in Azure DevOps if all other stages pass.


## BranchPolicies and Protection
- The main brach requires a pull request before merging.
- Requires approvals and status check of the production stage to pass before merging.
- The Development Branch requires status check of the test stage to pass before merging.

## Testing Strategy
- Unit tests with pytest + coverage.
- Static Analysys with pylint code quality checks.
- Security testing with Sonar Cloud analysis.
- Performance testing with Locust load testing.
- UAT testing with Selenium for autmated browser testing.

## Environment Setup and Configuration
- Test Enviroment with automatic deployment after build is successfull and manual approval check.
- Production Enviroment with automatic deployment after build is successsful and manual approval check is completed.
## Deployment Process
- Commits automatically trigger the pipleline.
- Build stage executes.
- If the build stage is successfull manual approval is required for the Test Enviroment stage to deploy.
- If the Test Enviroment is succsesfull the Production stage requires.








