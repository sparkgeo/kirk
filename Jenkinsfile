 pipeline {
    agent any

    stages {
        stage ('code checkout') {
            steps {
                git branch: '${gitTag}', url: "https://github.com/bcgov/kirk"
            }
        }
      
        stage('SonarQube analysis') {
        environment {
        scannerHome = tool 'sonarscanner'
        }    
            steps {
                withSonarQubeEnv('CODEQA') {
                        sh '${scannerHome}/bin/sonar-scanner -Dsonar.sources="." -Dsonar.projectKey="kirk" -Dsonar.projectVersion="${gitTag}" -Dsonar.login="${sonarToken}"'
                    }
                }       
        }
	 
	stage("Quality Gate"){
  	timeout(time: 4, unit: 'MINUTES') {
    	def qg = waitForQualityGate()
    	if (qg.status != 'OK') {
      	error "Pipeline aborted due to quality gate failure: ${qg.status}"
              		}
     		}
	}

       stage ('OCP Build') {
            steps {
                script {
					sh '''echo "It will take 2 minutes for OpenShift rolling new install to runtime"'''
					def response = httpRequest contentType: 'APPLICATION_JSON_UTF8', httpMode: 'POST', requestBody: "{}", url: "${ocpBH}"
					ocpTask = readJSON text: response.content
					echo ocpTask.toString()
					return "Success".equals(ocpTask["status"])
            }
          }
        }
      }
    }
