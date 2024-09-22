# **@flothers company**
my work as AI &amp; machine learning intern in @flothers company

## *1. URL Malware Recognizer:*

This project implements a URL malware detection system using machine learning techniques. The system classifies URLs as either benign or malicious based on various features extracted from the URL string. It utilizes the XGBoost classifier and is designed for easy deployment through a web interface created with Streamlit.

The URL Malware Recognizer project aims to identify potentially malicious URLs using a machine learning model. The model is trained on a dataset containing both benign and malicious URLs. The final system includes a web application that allows users to input a URL and receive a classification along with the probability of it being malicious or benign.

### Data Collection

The dataset used for training the model includes:

- Mixed data from Kaggle
- Malicious URL data from Phishtank and URLhaus
- Additional benign URLs from the top million URLs

### Feature Extraction

The following features are extracted from URLs for classification:

- URL length
- Domain length
- Path length
- Presence of IP addresses (IPv4 and IPv6)
- Number of subdomains
- Presence of hexadecimal characters
- Entropy of the URL
- Count of characters in the domain extension
- Presence of port numbers
- Count of digits, alphabets, and special characters
- Existence of specific substrings and patterns

### Model Training

The model is built using the XGBoost classifier with hyperparameter tuning through RandomizedSearchCV. The following parameters were optimized:

- `n_estimators`: Number of boosting rounds
- `learning_rate`: Step size shrinkage
- `max_depth`: Maximum depth of a tree
- `gamma`: Minimum loss reduction required to make a further partition

The best model achieved an accuracy of approximately 98% on the test set.

### Web Application

A web interface is provided using Streamlit, allowing users to input a URL and get predictions. The application uses the trained XGBoost model and standard scaler to make predictions and display probabilities.

### Streamlit Interface Features

- Input field for entering the URL
- Analyze button to get predictions
- Displays classification results and probabilities

### Installation

To set up the project locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/url-malware-recognizer.git
    cd url-malware-recognizer
    ```

2. **Install dependencies:**

    It is recommended to use a virtual environment. You can create one and install dependencies using pip:

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    pip install -r requirements.txt
    ```

    Make sure you have the required packages listed in `requirements.txt`. Here are some example dependencies:

    ```
    pandas
    scikit-learn
    xgboost
    streamlit
    joblib
    ```

3. **Download and place the model and scaler files:**

    Ensure that `scaler_v1.pkl` and `xgb_model_v1.ubj` are available in the `models` directory. If not, you need to train the model and save it as described in the code.

### Usage

1. **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

2. **Navigate to the web interface:**

    Open your web browser and go to `http://localhost:8501`.

3. **Use the application:**

    - Enter a URL into the input field.
    - Click "Analyze" to get predictions.
    - The result will show whether the URL is predicted to be malicious or benign, along with probabilities.
