import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import warnings
warnings.filterwarnings('ignore')

# Step 1: Load and prepare data
def load_data(filepath):
    """Load claims data from CSV file"""
    # Convert to Path object if string
    filepath = Path(filepath)
    
    # Check if file exists
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    # Check if file is readable
    if not filepath.is_file():
        raise ValueError(f"Path is not a file: {filepath}")
    
    try:
        df = pd.read_csv(filepath)
    except pd.errors.EmptyDataError:
        raise ValueError(f"File is empty: {filepath}")
    except Exception as e:
        raise ValueError(f"Error reading file {filepath}: {str(e)}")
    
    if len(df) == 0:
        raise ValueError(f"No data in file: {filepath}")
    
    print(f"Data loaded successfully from: {filepath}")
    print(f"Total records: {len(df)}\n")
    return df

# Step 2: Feature engineering
def engineer_features(df):
    """Create meaningful features from raw data"""
    df = df.copy()
    
    # Convert date to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Extract time-based features
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['Month'] = df['Date'].dt.month
    df['DayOfMonth'] = df['Date'].dt.day
    
    # Amount-based features
    df['AmountCategory'] = pd.cut(df['Amount'], 
                                    bins=[0, 150, 400, 2000], 
                                    labels=['Low', 'Medium', 'High'])
    
    # Encode categorical variables
    le_type = LabelEncoder()
    df['Type_Encoded'] = le_type.fit_transform(df['Type'])
    
    le_amount_cat = LabelEncoder()
    df['AmountCategory_Encoded'] = le_amount_cat.fit_transform(df['AmountCategory'])
    
    print("Features engineered:")
    print(df[['ClaimID', 'Status', 'Amount', 'Type', 'AmountCategory']].head())
    print()
    
    return df, le_type, le_amount_cat

# Step 3: Prepare training data
def prepare_training_data(df):
    """Split data into features and target, handle pending claims"""
    # Filter out pending claims for training
    df_train = df[df['Status'] != 'Pending'].copy()
    df_pending = df[df['Status'] == 'Pending'].copy()
    
    # Create binary target: 1 = Denied, 0 = Paid
    df_train['Target'] = (df_train['Status'] == 'Denied').astype(int)
    
    # Select features for model
    feature_cols = ['Amount', 'Type_Encoded', 'DayOfWeek', 
                    'Month', 'DayOfMonth', 'AmountCategory_Encoded']
    
    X = df_train[feature_cols]
    y = df_train['Target']
    
    print(f"Training data: {len(df_train)} claims")
    print(f"Denied claims: {y.sum()}, Paid claims: {len(y) - y.sum()}")
    print(f"Pending claims to predict: {len(df_pending)}\n")
    
    return X, y, df_train, df_pending, feature_cols

# Step 4: Train the model
def train_model(X, y):
    """Train Random Forest classifier"""
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    # Train Random Forest
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42,
        class_weight='balanced'  # Handle class imbalance
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    
    print("=" * 50)
    print("MODEL PERFORMANCE")
    print("=" * 50)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2%}\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, 
                                target_names=['Paid', 'Denied']))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print()
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print("Feature Importance:")
    print(feature_importance)
    print()
    
    return model

# Step 5: Predict pending claims
def predict_pending(model, df_pending, feature_cols):
    """Predict outcomes for pending claims"""
    if len(df_pending) == 0:
        print("No pending claims to predict.")
        return None
    
    X_pending = df_pending[feature_cols]
    
    # Get predictions and probabilities
    predictions = model.predict(X_pending)
    probabilities = model.predict_proba(X_pending)
    
    results = df_pending[['ClaimID', 'Amount', 'Type', 'Date']].copy()
    results['Predicted_Status'] = ['Denied' if p == 1 else 'Paid' for p in predictions]
    results['Denial_Probability'] = probabilities[:, 1]
    results['Confidence'] = probabilities.max(axis=1)
    
    print("=" * 50)
    print("PENDING CLAIMS PREDICTIONS")
    print("=" * 50)
    print(results.to_string(index=False))
    print()
    
    return results

# Step 6: Main execution function
def main(filepath=None):
    """
    Run the complete ML pipeline
    
    Args:
        filepath: Path to CSV file. If None, uses default sample data path
                  relative to project root: sample_data/claims_export_2025.txt
    """
    # If no filepath provided, use default relative to project root
    if filepath is None:
        # Get project root (2 levels up from app/ML/claims_predictor.py)
        script_dir = Path(__file__).parent  # app/ML/
        project_root = script_dir.parent.parent  # project root
        filepath = project_root / 'sample_data' / 'claims_export_2025.txt'
    
    # Convert to Path object if string
    filepath = Path(filepath)
    
    # Resolve relative paths
    if not filepath.is_absolute():
        filepath = filepath.resolve()
    
    print("=" * 50)
    print("CLAIMS REJECTION PREDICTION MODEL")
    print("=" * 50)
    print(f"Input file: {filepath}\n")
    
    # Load data
    df = load_data(filepath)
    
    # Engineer features
    df, le_type, le_amount_cat = engineer_features(df)
    
    # Prepare training data
    X, y, df_train, df_pending, feature_cols = prepare_training_data(df)
    
    # Train model
    model = train_model(X, y)
    
    # Predict pending claims
    predictions = predict_pending(model, df_pending, feature_cols)
    
    print("=" * 50)
    print("KEY INSIGHTS")
    print("=" * 50)
    print("1. Model trained on historical Paid/Denied claims")
    print("2. Pending claims predicted based on learned patterns")
    print("3. Higher denial probability = higher rejection risk")
    print("4. Consider reviewing high-risk pending claims manually")
    
    return model, predictions

# Run the model
if __name__ == "__main__":
    # Use default path (will resolve to project_root/sample_data/claims_export_2025.txt)
    model, predictions = main()