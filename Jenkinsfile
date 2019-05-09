node('master'){

  stage('SCM Checkout'){
    git branch: '${gitTag}', url: 'https://github.com/bcgov/kirk'
  }
  stage('SonarQube analysis') {
    def scannerHome = tool 'sonarscanner'
    withSonarQubeEnv('CODEQA') {
      sh "${scannerHome}/bin/sonar-scanner -Dsonar.sources="." -Dsonar.projectKey="kirk" -Dsonar.login="${sonarToken}"
    }
  }


  stage ('OCP build'){
    sh '''echo "It will take 2 minutes for OpenShift rolling new install to runtime"'''
    def response = httpRequest contentType: 'APPLICATION_JSON_UTF8', httpMode: 'POST', requestBody: "{}", url: "${ocpBH}"
    ocpTask = readJSON text: response.content
    echo ocpTask.toString()
    return "Success".equals(ocpTask["status"])
  }
 }
