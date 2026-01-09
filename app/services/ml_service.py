"""ML Service wrapper for claims prediction API integration"""
import io
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd

from app.ml.claims_predictor import (
    engineer_features,
    load_data,
    predict_pending,
    prepare_training_data,
    train_model,
)


def predict_claims_from_bytes(csv_bytes: bytes) -> Dict:
    """
    Run ML prediction pipeline on CSV bytes (from FastAPI UploadFile).
    
    Args:
        csv_bytes: CSV file content as bytes
        
    Returns:
        Dictionary with:
        - predictions: List of prediction results
        - model_metrics: Model performance metrics
        - summary: Summary statistics
    """
    # Save bytes to temporary file
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as tmp_file:
        tmp_file.write(csv_bytes)
        tmp_path = Path(tmp_file.name)
    
    try:
        # Load data
        df = load_data(tmp_path)
        
        # Engineer features
        df, le_type, le_amount_cat = engineer_features(df)
        
        # Prepare training data
        X, y, df_train, df_pending, feature_cols = prepare_training_data(df)
        
        # Check if we have enough data to train
        if len(df_train) < 2:
            raise ValueError(
                "Insufficient training data. Need at least 2 claims with Paid/Denied status."
            )
        
        # Train model
        model = train_model(X, y)
        
        # Predict pending claims
        predictions_df = predict_pending(model, df_pending, feature_cols)
        
        # Prepare response
        result = {
            "total_claims": len(df),
            "training_claims": len(df_train),
            "pending_claims": len(df_pending),
            "predictions": [],
            "model_metrics": {
                "accuracy": None,  # Would need to extract from train_model
                "feature_importance": {}
            },
            "summary": {
                "paid_count": len(df_train[df_train['Status'] == 'Paid']),
                "denied_count": len(df_train[df_train['Status'] == 'Denied']),
                "pending_count": len(df_pending),
            }
        }
        
        # Convert predictions to list of dicts
        if predictions_df is not None and len(predictions_df) > 0:
            result["predictions"] = predictions_df.to_dict('records')
            # Convert numpy types to native Python types for JSON serialization
            for pred in result["predictions"]:
                for key, value in pred.items():
                    if pd.isna(value):
                        pred[key] = None
                    elif hasattr(value, 'item'):  # numpy scalar
                        pred[key] = value.item()
                    elif isinstance(value, (pd.Timestamp, pd.Timedelta)):
                        pred[key] = str(value)
        
        return result
        
    finally:
        # Clean up temporary file
        if tmp_path.exists():
            tmp_path.unlink()
