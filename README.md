# 🍷 Wine Quality Prediction - MLOps Pipeline

📋 **Overview**

This repository contains an end-to-end machine learning project with a comprehensive MLOps pipeline. The project demonstrates a complete workflow from data ingestion to model deployment with proper validation, transformation, training, and evaluation stages.

## 🚀 ML Pipeline Workflow

1. **Data Ingestion** - Download and extract data from source
2. **Data Validation** - Validate data schema and integrity  
3. **Data Transformation** - Feature engineering and preprocessing
4. **Model Training** - Train and save machine learning model
5. **Model Evaluation** - Evaluate model performance and track with MLflow/DagsHub

## 📊 Project Structure

```
machinelearningproject/
│
├── .github/workflows/     # CI/CD workflows
├── artifacts/             # Generated artifacts during pipeline execution
├── config/                # Configuration files
│   └── config.yaml        # Main configuration
├── research/              # Jupyter notebooks for experimentation
│   ├── 1_data_ingestion.ipynb
│   ├── 2_data_validation.ipynb
│   ├── 3_data_transformation.ipynb
│   ├── 4_model_trainer.ipynb
│   └── 5_model_evaluation.ipynb
├── src/datascience/       # Source code
│   ├── components/        # Pipeline components
│   ├── config/            # Configuration management
│   ├── constants/         # Constants and paths
│   ├── entity/            # Data classes
│   ├── pipeline/          # Pipeline orchestration
│   └── utils/             # Utility functions
├── static/                # Static files for web interface
│   ├── css/               # Stylesheets
│   └── js/                # JavaScript files
├── templates/             # HTML templates
├── app.py                 # Web application
├── main.py                # Pipeline execution entry point
├── params.yaml            # Model parameters
├── schema.yaml            # Data schema definition
├── setup.py               # Package setup
└── Dockerfile             # Container definition
```

## 💻 Technologies Used

- **Python** - Primary programming language
- **Jupyter Notebooks** - Research and experimentation
- **MLflow** - Model tracking and versioning
- **DagsHub** - MLOps platform integration
- **Web Interface** - Interactive model interface with HTML/CSS/JavaScript

## 🛠️ Implementation Workflow

1. Update `config.yaml` with project configuration
2. Update `schema.yaml` with data schema definitions
3. Update `params.yaml` with model parameters
4. Update entity classes in `src/datascience/entity/`
5. Update configuration manager in `src/datascience/config/`
6. Implement components in `src/datascience/components/`
7. Create pipelines in `src/datascience/pipeline/`
8. Execute workflow through `main.py`

## 🌐 Web Application

The project includes a web interface for easy interaction with the trained model. The interface features:

- Input validation
- Sample data population
- Interactive prediction
- Responsive design

## 📈 MLflow Integration

The model is tracked using MLflow and integrated with DagsHub for experiment tracking and version control. Model metrics and artifacts are automatically uploaded to the DagsHub repository.

## 🚦 Getting Started

1. **Clone the repository**

```bash
git clone https://github.com/danialasim/machinelearningproject.git
cd machinelearningproject
```

2. **Install dependencies**

```bash
pip install -e .
```

3. **Run the pipeline**

```bash
python main.py
```

4. **Launch the web application**

```bash
python app.py
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- [MLflow Dashboard](https://dagshub.com/danialasimbashir/machinelearningproject.mlflow)
- [DagsHub Repository](https://dagshub.com/danialasimbashir/machinelearningproject)

---

**Created by Muhammad Danial - © 2025**