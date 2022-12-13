pipeline {
  agent {
    kubernetes {
      yaml '''
apiVersion: v1 
kind: Pod 
metadata: 
    name: dind 
spec: 
    containers: 
      - name: docker-cmds 
        image: docker:1.12.6 
        command: ['docker', 'run', '-p', '80:80', 'httpd:latest'] 
        resources: 
            requests: 
                cpu: 10m 
                memory: 256Mi 
        env: 
          - name: DOCKER_HOST 
            value: tcp://localhost:2375 
      - name: dind-daemon 
        image: docker:1.12.6-dind 
        resources: 
            requests: 
                cpu: 20m 
                memory: 512Mi 
        securityContext: 
            privileged: true 
        volumeMounts: 
          - name: docker-graph-storage 
            mountPath: /var/lib/docker 
    volumes: 
      - name: docker-graph-storage 
        emptyDir: {}
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
