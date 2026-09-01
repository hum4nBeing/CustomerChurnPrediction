# 📊 Customer Churn Prediction

A full-stack machine learning application for predicting customer churn in a telecommunications company, featuring an interactive data exploration dashboard and real-time predictions.

## 📋 Table of Contents
- [Overview](#-overview)
- [Project Architecture](#%EF%B8%8F-project-architecture)
- [Directory Structure](#-directory-structure)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Machine Learning Details](#-machine-learning-details)
- [Setup and Installation](#-setup-and-installation)
- [API Documentation](#-api-documentation)
- [License](#-license)

## 🔭 Overview

This project provides a comprehensive solution for telecommunications customer churn analysis and prediction. It demonstrates an end-to-end data science workflow: from data loading and preprocessing to model training, evaluation, deployment, and visualization through an interactive Streamlit dashboard.

The solution helps businesses answer critical questions like:
- Which customers are likely to churn?
- What are the primary drivers of customer churn?
- How can we develop targeted retention strategies based on customer segments?

## 🏗️ Project Architecture

The project follows a modern microservices architecture with three main components:

1. **Frontend Application (Streamlit)**:
   - Provides an interactive dashboard for data exploration.
   - Visualizes churn patterns, segment analysis, and insights.
   - Offers a user interface for making predictions in real-time.

2. **Backend Service (FastAPI)**: 
   - Serves ML model predictions via a RESTful API.
   - Handles model training and evaluation (`train_model.py`).
   - Generates model performance reports and threshold optimization.

3. **Database (PostgreSQL)**:
   - Stores customer data loaded from CSV.
   - Enables SQL-based data querying for the backend training pipelines.

All services can be containerized using Docker and orchestrated with Docker Compose for seamless deployment.

## 📁 Directory Structure

```text
CustomerChurnPrediction/
├── backend/
│   ├── api/
│   │   ├── main.py             # FastAPI prediction service
│   │   ├── train_model.py      # ML training & evaluation script
│   │   └── requirements.txt    # Backend dependencies
│   ├── reports/                # Generated model reports (ROC, CM, etc.)
│   └── Dockerfile              # Backend container configuration
├── frontend/
│   ├── components/             # Streamlit UI components
│   ├── app.py                  # Streamlit dashboard entrypoint
│   ├── requirements.txt        # Frontend dependencies
│   └── Dockerfile              # Frontend container configuration
├── data/
│   ├── Telco-Customer-Churn.csv # Source dataset
│   └── load_data.py            # Script to load CSV into PostgreSQL
├── postgres/
│   └── create_schema.sql       # Database schema initialization
├── docker-compose.yml          # Docker Compose configuration
└── README.md                   # Project documentation
```

## 🌟 Key Features

- **Interactive Dashboard**: Comprehensive Streamlit-based visualization dashboard with multiple views (Overview, Insights, Prediction, About).
- **Category-Based Analysis**: Deep dive into demographics, service usage, payment patterns, and clustering.
- **Real-time Predictions**: FastAPI backend for quick churn predictions via REST API.
- **Data Persistence**: PostgreSQL database integration for storing and retrieving customer data.
- **End-to-end ML Pipeline**: Full pipeline with feature engineering, preprocessing, and hyperparameter tuning using scikit-learn's GradientBoostingClassifier.
- **Model Reporting**: Comprehensive reports including ROC curves, confusion matrices, and optimal threshold selection based on F1 score.

## 💻 Technology Stack

- **Frontend**: Streamlit, Plotly
- **Backend**: FastAPI, Uvicorn, scikit-learn, SQLAlchemy
- **Data processing & ML**: pandas, numpy, scikit-learn, matplotlib
- **Database**: PostgreSQL
- **DevOps**: Docker, Docker Compose

## 🧠 Machine Learning Details

### Feature Engineering
- Derived features such as `avg_charge_per_month`
- Count of active services (`services_count`)
- Tenure categorization into meaningful buckets

### Preprocessing Pipeline
- Separate pipelines for numeric and categorical features.
- Missing value imputation (Median for numeric, Most Frequent for categorical).
- Feature scaling using `StandardScaler`.
- One-hot encoding for categorical variables.

### Model Selection & Tuning
- Algorithm: **Gradient Boosting Classifier** (via scikit-learn).
- Hyperparameter space explored via `RandomizedSearchCV` with 5-fold Stratified Cross-Validation.
- Optimization metric: **ROC AUC**.

### Threshold Optimization
- Custom threshold selection to balance precision and recall.
- Optimizes the F1 score for the final classification threshold.

## 🚀 Setup and Installation

### Prerequisites
- Docker and Docker Compose
- Alternatively: Python 3.9+, PostgreSQL

### Quick Start (Docker)

1. Clone the repository:
   ```bash
   git clone https://github.com/hum4nBeing/CustomerChurnPrediction.git
   cd CustomerChurnPrediction
   ```

2. Start the application stack:
   ```bash
   docker-compose up -d
   ```

3. Access the components:
   - **Streamlit Dashboard**: http://localhost:8501
   - **FastAPI Documentation**: http://localhost:8000/docs

### Manual Setup (Without Docker)

1. **Setup PostgreSQL database**:
   ```bash
   psql -U postgres -c "CREATE DATABASE churn_db;"
   psql -U postgres -d churn_db -f postgres/create_schema.sql
   ```

2. **Load Data**:
   ```bash
   python data/load_data.py
   ```

3. **Backend Setup**:
   ```bash
   cd backend
   pip install -r api/requirements.txt
   python api/train_model.py      # Trains model and generates model.pkl
   uvicorn api.main:app --reload  # Starts API on port 8000
   ```

4. **Frontend Setup**:
   ```bash
   cd ../frontend
   pip install -r requirements.txt
   streamlit run app.py           # Starts UI on port 8501
   ```

## 📚 API Documentation

The FastAPI backend exposes the following prediction endpoint.

### Prediction Endpoint
```http
POST /predict
```

**Sample Request:**
```json
{
  "tenure": 12,
  "monthly_charges": 70.0,
  "total_charges": 840.0,
  "contract": "Month-to-month",
  "gender": "Female",
  "senior_citizen": 0,
  "partner": "No",
  "dependents": "No",
  "internet_service": "Fiber optic",
  "multiple_lines": "No",
  "online_security": "No",
  "online_backup": "No",
  "device_protection": "No",
  "tech_support": "No",
  "streaming_tv": "No",
  "streaming_movies": "No",
  "paperless_billing": "Yes",
  "payment_method": "Electronic check"
}
```

**Sample Response:**
```json
{
  "prediction": "Yes",
  "probability": 0.72
}
```

## 📄 License

This project is licensed under the MIT License.
