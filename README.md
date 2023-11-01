# Text-To-Speech App

A basic text to speech translation project.

### Goal
1. Convert image to text (numbers).
2. Translate numbers to speech in a given languages.

## Installation

Make sure you have Minikube and Docker installed in your machine. Follow the steps to get apps up and running.

#### Step 1
```bash
minikube start
```
#### Step 2
```bash
# Make the deploy file executable
chmod +x deploy-projects.sh
```
#### Step 3
```bash
./deploy-projects.sh
```

## Using the App

**Frontend:** http://localhost:3000/

**image-to-number-api:** http://localhost:3001/

**word-to-speech-api:** http://localhost:3002/

**number-to-word-api:** http://localhost:3003/

**backend-api:** http://localhost:3004/