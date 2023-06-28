pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                // Execute build steps here
                sh 'echo "Building the project in Dev branch"'
            }
        }
        
        stage('Test') {
            steps {
                // Execute test steps here
                sh 'echo "Running tests in Dev branch"'
            }
        }
        
        stage('Deploy') {
            steps {
                // Execute deployment steps here
                sh 'echo "Deploying the project in Dev branch"'
            }
        }
    }
}
