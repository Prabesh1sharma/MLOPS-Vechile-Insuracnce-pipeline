# MLOPS-Vechile-Insuracnce-pipeline


## 🚀 Overview
This project is an end-to-end MLOps pipeline that streamlines the process of building, deploying, and maintaining machine learning models efficiently. The project integrates data ingestion, validation, transformation, model training, evaluation, and deployment with cloud services like AWS and MongoDB. The goal is to impress recruiters and showcase expertise in MLOps principles, best practices, and cutting-edge tools.

## 📌 Key Features
- **Automated Project Setup**: Generate a structured project template effortlessly.
- **Environment Management**: Virtual environment setup and dependency management.
- **MongoDB Integration**: Data storage and retrieval from MongoDB Atlas.
- **Logging & Exception Handling**: Robust logging and error tracking.
- **Data Ingestion & Transformation**: Seamless data fetching, validation, and transformation.
- **Model Training & Evaluation**: Advanced model training and performance tracking.
- **AWS Cloud Deployment**: Model storage and deployment with S3, EC2, and ECR.
- **CI/CD Pipeline**: Automated build, test, and deployment workflows with GitHub Actions.

---

## 🛠 Tech Stack
- **Programming Language**: Python 3.12
- **Frameworks & Libraries**: Pandas, NumPy, Scikit-learn, TensorFlow/PyTorch
- **Database**: MongoDB Atlas
- **Cloud Services**: AWS S3, EC2, ECR, IAM
- **Containerization & Orchestration**: Docker
- **CI/CD**: GitHub Actions
- **Logging & Monitoring**: Python Logging Module

---

## 📂 Project Structure
```
mlops_project/
│── src/                       # Source Code
│   ├── components/            # Core Modules (Data Ingestion, Model Training, etc.)
│   ├── configuration/          # Configuration files for DB & Cloud
│   ├── entity/                 # Entities and Data Classes
│   ├── utils/                  # Helper Functions
│   ├── aws_storage/            # AWS S3 Integration
│── notebook/                   # Jupyter Notebooks for EDA & Experimentation
│── artifacts/                   # Model Artifacts & Logs
│── .github/workflows/           # CI/CD Workflows
│── Dockerfile                   # Containerization
│── pyproject.toml               # Package Configuration
│── setup.py                     # Package Setup
│── requirements.txt             # Dependencies
│── README.md                    # Project Documentation
```

---

## 📌 Installation & Setup

### 1️⃣ Create & Activate Virtual Environment
```sh
conda create -n envmlop python=3.12 -y
conda activate envmlop
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Verify Package Installation
```sh
pip list
```

---

## 🗄️ MongoDB Setup
### 1️⃣ Sign Up & Create Cluster
- Sign up at [MongoDB Atlas](https://www.mongodb.com/atlas)
- Create a new project and cluster (M0 tier)

### 2️⃣ Configure Database User
- Create a new database user with access credentials.
- Set Network Access to **0.0.0.0/0** to allow connections from any IP.

### 3️⃣ Obtain Connection String
- Navigate to *Database > Get Connection String*.
- Select **Python Driver (3.6 or later)** and copy the connection URL.

### 4️⃣ Load Data into MongoDB
```python
from pymongo import MongoClient
client = MongoClient("your_mongo_connection_string")
db = client["your_database"]
collection = db["your_collection"]
# Insert your data here
```

---

## ⚙️ Logging & Exception Handling
- Implemented **logging** for better debugging.
- Custom **exception handling** framework.

---

## 📊 Data Pipeline Implementation

### 🔹 Data Ingestion
- Fetch raw data from MongoDB.
- Convert into structured **Pandas DataFrame**.
- Store processed data in artifacts directory.

### 🔹 Data Validation
- Define schema in `config.schema.yaml`.
- Validate data against schema constraints.

### 🔹 Data Transformation
- Feature Engineering & Scaling.
- Handle missing values & outliers.

### 🔹 Model Training
- Train models using **Scikit-learn, TensorFlow, or PyTorch**.
- Save trained models to **artifacts directory**.

### 🔹 Model Evaluation
- Compare model performance.
- Implement **threshold-based validation** before deployment.

### 🔹 Model Deployment
- Upload trained models to **AWS S3**.
- Deploy model on **EC2 instance**.

---

## ☁️ AWS Integration
### 1️⃣ Configure AWS Credentials
```sh
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
```

### 2️⃣ Create & Configure S3 Bucket
```sh
aws s3 mb s3://my-model-mlopsproj
```

### 3️⃣ Push Model to S3
```sh
aws s3 cp model.pkl s3://my-model-mlopsproj/model-registry/
```

---

## 🛠️ CI/CD Pipeline
### 1️⃣ Setup GitHub Secrets
Navigate to *GitHub Project > Settings > Secrets and Variables > Actions* and add:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`
- `ECR_REPO`

### 2️⃣ Configure Self-Hosted Runner on EC2
```sh
./run.sh
```

### 3️⃣ Enable CI/CD Workflow
- Push code to GitHub repository.
- GitHub Actions triggers CI/CD pipeline.

---

## 🚢 Docker & EC2 Deployment
### 1️⃣ Build & Push Docker Image
```sh
docker build -t mlops-app .
docker tag mlops-app:latest <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/vehicleproj:latest
docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/vehicleproj:latest
```

### 2️⃣ Deploy on EC2 & Expose API
```sh
docker run -p 5080:5000 mlops-app
```

### 3️⃣ Access Deployed Application
Open a browser and visit:
```
http://<EC2_PUBLIC_IP>:5080
```

---

## 📈 Model Training & Prediction
### Train Model
```sh
curl -X POST http://<EC2_PUBLIC_IP>:5080/training
```

### Predict
```sh
curl -X POST http://<EC2_PUBLIC_IP>:5080/predict -H "Content-Type: application/json" -d '{ "input_data": [...] }'
```

---

## 🎯 Conclusion
This MLOps project demonstrates a complete pipeline from **data ingestion to model deployment** in a production-ready environment. By leveraging **MongoDB, AWS, Docker, and CI/CD**, this project ensures **scalability, reproducibility, and automation**.

---

