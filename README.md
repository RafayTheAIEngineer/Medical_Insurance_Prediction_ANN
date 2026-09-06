
# 🏥 End-to-End Medical Insurance Cost Prediction

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.0%2B-orange.svg)
![Pandas](<https://img.shields.io/badge/Pandas-Data%20Wrangling-green.svg>)

## Live Demo
[My App](https://medical-insurance-estimator.streamlit.app/)

## 📌 Project Overview

This project applies **Machine Learning (Regression Analysis)** to predict the medical insurance costs of individuals based on their demographic information and health metrics. The goal is to build a robust predictive model that can help insurance companies dynamically estimate charges and help individuals understand the factors driving their healthcare costs.

## 📊 Dataset Description

The dataset contains information on primary beneficiaries.

* **Target Variable:** `charges` (Continuous - Individual medical costs billed by health insurance)
* **Features:**
  * `age`: Age of primary beneficiary
  * `sex`: Insurance contractor gender (female, male)
  * `bmi`: Body mass index (ideal range: 18.5 to 24.9)
  * `children`: Number of children covered by health insurance / Number of dependents
  * `smoker`: Smoking status (yes, no)
  * `region`: The beneficiary's residential area in the US (northeast, southeast, southwest, northwest)

## 🛠️ Tech Stack

* **Language:** Python
* **Data Preprocessing & EDA:** Pandas, NumPy, Matplotlib, Seaborn
* **Machine Learning:** Scikit-Learn (Linear Regression, Random Forest, XGBoost)
* **Hyperparameter Tuning:** GridSearchCV / RandomizedSearchCV

## 🚀 Project Workflow

### 1. Exploratory Data Analysis (EDA)

* Analyzed the distribution of the target variable (`charges`), which exhibited a right-skewed distribution.
* Conducted bivariate analysis to identify key cost drivers.
* **Key Insight:** `smoker` status combined with high `bmi` showed a massive correlation with peak insurance charges.

### 2. Data Preprocessing

* **Encoding:** Applied One-Hot Encoding for categorical variables (`sex`, `smoker`, `region`).
* **Scaling:** Utilized `StandardScaler` to normalize numerical features (`age`, `bmi`, `children`) to ensure stable model convergence.
* **Outlier Handling:** Capped extreme outliers in the `charges` and `bmi` columns using the IQR (Interquartile Range) method.

### 3. Model Training & Evaluation

We trained multiple regression models to find the best fit. The models were evaluated using **RMSE (Root Mean Squared Error)** and **R² (Coefficient of Determination)**.

| Model                             |   R² Score   | Performance Note                                         |
| :-------------------------------- | :------------: | :------------------------------------------------------- |
| **Linear Regression**       |      ~75%      | Baseline model; struggled with non-linear relationships. |
| **Random Forest Regressor** |      ~85%      | Captured non-linear patterns effectively.                |
| **XGBoost Regressor**       | **~87%** | Best performing model after hyperparameter tuning.       |

*(Note: The exact final metrics may vary slightly based on the random seed and data splitting).*

### 4. Key Takeaways

1. **Smoking is the strongest predictor:** Smokers face drastically higher medical costs compared to non-smokers.
2. **The BMI multiplier:** High BMI independently raises costs, but when combined with smoking, the charges increase exponentially.
3. **Age plays a steady role:** There is a linear and consistent increase in insurance charges as age increases.

## 💻 How to Run This Project

1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/medical-insurance-prediction.git](https://github.com/your-username/medical-insurance-prediction.git)
   ```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Jupyter Notebook to explore the EDA, model training, and advanced metric visualizations.


# 🤝 Let's Connect
If you found this project interesting or have any feedback, feel free to connect with me!
Let's connect on [LinkedIn](www.linkedin.com/in/abdulrafay-aiengineer).

GitHub: [GitHub Profile URL](https://github.com/RafayTheAIEngineer)