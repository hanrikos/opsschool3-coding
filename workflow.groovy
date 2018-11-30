node ('ami-0e04fcf3327b27349'){

    stage('Checkout'){
        dir('/home/ubuntu/workspace/new_pipeline'){
            git url: 'https://github.com/hanrikos/opsschool3-coding.git'
        }
    }
    stage('RunScript'){
      sh '''#!/bin/bash
      cd home-assignments/session2
      python3 cli.py --city dublin --forecast TODAY+3 -
      '''
    }
}