# Claims Predictor Script Analysis

## 📋 Overview

This script implements a **binary classification model** to predict whether pending insurance claims will be **Paid** or **Denied** based on historical data patterns.

## 🎯 Purpose & Workflow

1. **Load Data**: Reads CSV file with claims data
2. **Feature Engineering**: Extracts time-based and categorical features
3. **Train Model**: Uses Random Forest to learn patterns from Paid/Denied claims
4. **Predict**: Applies model to pending claims to forecast outcomes

## ✅ Strengths

### 1. **Well-Structured Pipeline**
- Clear separation of concerns (6 distinct functions)
- Logical flow from data loading → feature engineering → training → prediction
- Good use of function composition

### 2. **Feature Engineering**
- **Time-based features**: DayOfWeek, Month, DayOfMonth (captures temporal patterns)
- **Amount categorization**: Bins claims into Low/Medium/High (handles non-linear relationships)
- **Categorical encoding**: Properly encodes Type and AmountCategory

### 3. **Model Choice**
- **Random Forest**: Good for this use case (handles non-linear relationships, feature interactions)
- **Class balancing**: Uses `class_weight='balanced'` to handle imbalanced data
- **Stratified split**: Ensures balanced train/test distribution

### 4. **Evaluation Metrics**
- Accuracy, Classification Report, Confusion Matrix
- Feature importance analysis
- Probability outputs (not just binary predictions)

### 5. **Output Quality**
- Returns prediction probabilities (risk scores)
- Includes confidence levels
- Clear, readable results

## ⚠️ Issues & Concerns

### 1. **Critical: LabelEncoder State Not Persisted**
```python
# Problem: LabelEncoders are created but not saved
le_type, le_amount_cat = engineer_features(df)
# These encoders are lost after function returns!
```
**Impact**: Cannot use model for new predictions without retraining encoders
**Fix**: Save encoders (pickle/joblib) or use consistent encoding strategy

### 2. **Model Not Persisted**
```python
model = train_model(X, y)
# Model is lost after script ends!
```
**Impact**: Must retrain model every time (inefficient, inconsistent)
**Fix**: Save model using `joblib` or `pickle`

### 3. **Path Issues**
```python
def main(filepath='claims_export_2025.txt'):  # Relative path
    # ...
    main('./sample_data/claims_export_2025.txt')  # Hardcoded path
```
**Issues**:
- Default path won't work from different directories
- Hardcoded path in `__main__` block
- No path validation

### 4. **Missing Error Handling**
- No validation that required columns exist
- No handling for missing/null values
- No check for empty datasets
- No validation that AmountCategory bins work for all data ranges

### 5. **Data Quality Issues**
```python
df['AmountCategory'] = pd.cut(df['Amount'], 
                              bins=[0, 150, 400, 2000], 
                              labels=['Low', 'Medium', 'High'])
```
**Problems**:
- Hardcoded bins may not fit all datasets
- Values > 2000 will be NaN
- No handling for negative amounts (if they exist)

### 6. **Feature Engineering Issues**
- `AmountCategory_Encoded` is redundant (already have `AmountCategory`)
- Encoding `AmountCategory` loses the ordinal relationship (Low < Medium < High)
- Should use ordinal encoding instead of label encoding for categories

### 7. **No Data Validation**
```python
def load_data(filepath):
    df = pd.read_csv(filepath)  # No validation!
    return df
```
**Missing**:
- Column existence checks
- Data type validation
- Required values (Status must be Paid/Denied/Pending)
- Date format validation

### 8. **Small Dataset Problem**
- With only 15 claims in sample data, model will have very poor performance
- Need much more data for reliable predictions
- No warning about insufficient data

### 9. **Integration Gap**
- Script is standalone, not integrated with FastAPI
- No API endpoint to trigger predictions
- No way to save predictions to database

### 10. **Missing Dependencies**
- `sklearn` not in `requirements.txt`
- Script won't run without installing scikit-learn

## 🔧 Recommended Improvements

### 1. **Add Model Persistence**
```python
import joblib
from pathlib import Path

def save_model(model, encoders, filepath='models/claims_model.pkl'):
    Path(filepath).parent.mkdir(exist_ok=True)
    joblib.dump({
        'model': model,
        'le_type': encoders['le_type'],
        'le_amount_cat': encoders['le_amount_cat']
    }, filepath)

def load_model(filepath='models/claims_model.pkl'):
    return joblib.load(filepath)
```

### 2. **Fix Path Handling**
```python
from pathlib import Path

def main(filepath=None):
    if filepath is None:
        # Use project root relative path
        filepath = Path(__file__).parent.parent.parent / 'sample_data' / 'claims_export_2025.txt'
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    # ...
```

### 3. **Add Data Validation**
```python
def validate_data(df):
    required_cols = ['ClaimID', 'Status', 'Amount', 'Date', 'Type']
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    
    valid_statuses = {'Paid', 'Denied', 'Pending'}
    invalid = set(df['Status'].unique()) - valid_statuses
    if invalid:
        raise ValueError(f"Invalid status values: {invalid}")
    
    if df['Amount'].isna().any():
        raise ValueError("Amount column contains NaN values")
    # ...
```

### 4. **Improve Feature Engineering**
```python
from sklearn.preprocessing import OrdinalEncoder

# Use ordinal encoding for AmountCategory (preserves order)
ordinal_encoder = OrdinalEncoder(categories=[['Low', 'Medium', 'High']])
df['AmountCategory_Encoded'] = ordinal_encoder.fit_transform(df[['AmountCategory']])
```

### 5. **Dynamic Binning**
```python
def create_amount_bins(df, n_bins=3):
    """Create bins based on data distribution"""
    quantiles = np.linspace(0, 1, n_bins + 1)
    bin_edges = df['Amount'].quantile(quantiles).values
    return pd.cut(df['Amount'], bins=bin_edges, labels=['Low', 'Medium', 'High'])
```

### 6. **Add Error Handling**
```python
def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except pd.errors.EmptyDataError:
        raise ValueError("File is empty")
    
    if len(df) == 0:
        raise ValueError("No data in file")
    
    return df
```

### 7. **Add Integration with FastAPI**
```python
# In app/api/reports.py
from app.ml.claims_predictor import predict_pending_claims

@router.post("/reports/predict")
async def predict_claims(file: UploadFile = File(...)):
    # Load model, make predictions, return results
    pass
```

### 8. **Add Requirements**
```python
# Add to requirements.txt
scikit-learn==1.3.2
joblib==1.3.2
```

## 📊 Model Performance Considerations

### Current Limitations:
1. **Small dataset**: 15 claims is insufficient for reliable ML
2. **Class imbalance**: May have very few Denied claims
3. **Overfitting risk**: With small data, model may memorize rather than generalize
4. **Feature selection**: Only 6 features may not capture all patterns

### Recommendations:
- **Minimum data**: Need 100+ claims for basic model, 1000+ for reliable predictions
- **Cross-validation**: Use k-fold CV instead of single train/test split
- **Hyperparameter tuning**: Use GridSearchCV to optimize parameters
- **Feature selection**: Consider adding more features (claim age, processing time, etc.)

## 🔗 Integration with FastAPI

### Current State:
- Script is standalone, not integrated
- No API endpoint for predictions
- No database storage for predictions

### Recommended Integration:
1. **Create ML service module**: `app/services/ml_service.py`
2. **Add prediction endpoint**: `POST /reports/predict`
3. **Store predictions**: Add `Prediction` model to database
4. **Background processing**: Use Celery/BackgroundTasks for async predictions

## 📝 Summary

**Overall Assessment**: ⭐⭐⭐ (3/5)

**Strengths**: Well-structured, good feature engineering, appropriate model choice
**Weaknesses**: No persistence, path issues, missing error handling, not integrated

**Recommendation**: Fix critical issues (model persistence, error handling) before production use. Add integration with FastAPI for full functionality.
