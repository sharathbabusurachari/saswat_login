pipeline{
    agent any

    /*environment {
            NEXUS_VERSION = "nexus3"
            NEXUS_PROTOCOL = "http"
            NEXUS_URL = "172.31.40.209:8081"
            NEXUS_REPOSITORY = "vprofile-release"
    	    NEXUS_REPO_ID    = "vprofile-release"
            NEXUS_CREDENTIAL_ID = "nexuslogin"
            ARTVERSION = "${env.BUILD_ID}"
        }*/
    stages {
    
        stage('Setup Python Virtual ENV for dependencies'){
       
      steps  {
            sh '''
            sudo apt-get install python3.8-venv
            cd $WORKSPACE/scripts
            chmod +x envsetup.sh
            ./envsetup.sh
            '''}
        }
        stage('Setup Gunicorn Setup'){
            steps {
                sh '''
                cd $WORKSPACE/scripts
                chmod +x gunicorn.sh
                ./gunicorn.sh
                '''
            }
        }
        stage('setup NGINX and host application'){
            steps {
                sh '''
                cd $WORKSPACE/scripts
                chmod +x nginx.sh
                ./nginx.sh
                '''
            }
        }

        stage('CODE ANALYSIS with SONARQUBE') {

        		  environment {
                     scannerHome = tool 'SonarScanner'
                  }

                  steps {
                    withSonarQubeEnv('SonarQubeServer') {
                       sh '''${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=saswat_login_project \
                           -Dsonar.projectName=saswat_login_project-repo \
                           -Dsonar.projectVersion=1.0 \
                           -Dsonar.sources=$WORKSPACE/saswat_cust_app/ \
                           -Dsonar.java.binaries=target/test-classes/com/visualpathit/account/controllerTest/ \
                           -Dsonar.junit.reportsPath=target/surefire-reports/ \
                           -Dsonar.jacoco.reportsPath=target/jacoco.exec \
                           -Dsonar.java.checkstyle.reportPaths=target/checkstyle-result.xml'''
                    }

                    timeout(time: 5, unit: 'MINUTES') {
                       waitForQualityGate abortPipeline: true
                    }
                  }
                }

        stage('Publish to JFrog Repository'){
                    steps {
                    sh '''
                    echo 'PlacheHolder for Pushing Artifacts'
                    '''
                    }
                }
    }

  }
