pipeline {
  agent {
    kubernetes {
      yaml '''
apiVersion: v1
        kind: Pod
        spec:
          containers:
          - name: docker
            image: docker:latest
            command:
            - cat
            tty: true
            volumeMounts:
             - mountPath: /var/run/docker.sock
               name: docker-sock
          volumes:
          - name: docker-sock
            hostPath:
              path: /var/run/docker.sock   
        '''
    }
  }
  environment {
    dockerimagename = "ayi-test"
    dockerImage = ""
  }
  stages {
    stage('Checkout Source') {
      steps {
        git 'https://github.com/shazforiot/nodeapp_test.git'
      }
    }

    stage('Build-Docker-Image') {
      steps {
        container('docker') {
          sh 'docker build -t ss69261/testing-image:latest .'
        }
      }
    }

    stage('Pushing Image') {
      environment {
               registryCredential = 'dockerhublogin'
           }
      steps{
        script {
          docker.withRegistry( 'https://registry.hub.docker.com', registryCredential ) {
            dockerImage.push("latest")
          }
        }
      }
    }

    stage('Deploying App to Kubernetes') {
      steps {
        script {
          kubernetesDeploy(configs: "cronjob.yaml", kubeconfigId: "kubernetes")
        }
      }
    }
  }
}
