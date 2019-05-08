pipeline {

    stages {
        stage ('code checkout') {
            steps {
                git branch: '${gitTag}', url: "${gitRepo}"
            }
        }

        stage('SonarQube analysis') {
        environment {
        scannerHome = tool 'sonarscanner'
        }    
            steps {
                withSonarQubeEnv('CODEQA') {
                        sh 'sonar-scanner -Dsonar.sources="." -Dsonar.exclusions="node_modules/**/*" -Dsonar.projectKey="kirk" -Dsonar.projectVersion="${gitTag}" -Dsonar.login="${sonarToken}"'
				}
			}
	}
		
	stage ('OCP build') {
		steps {
			sh 'echo "It will take 2 minutes for OpenShift rolling new install to runtime"'
			def response = httpRequest contentType: 'APPLICATION_JSON_UTF8', httpMode: 'POST', requestBody: "{}", url: "${ocpBH}"
			ocpTask = readJSON text: response.content
			echo ocpTask.toString()
			return "Success".equals(ocpTask["status"])
			}
		}
	}
}
