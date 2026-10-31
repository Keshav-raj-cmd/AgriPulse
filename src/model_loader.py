"""
Model loader module (re-exported from src.data_loader for backward compatibility).
"""
from src.data_loader import (
    load_linear_model,
    load_random_forest_model,
    load_xgboost_model,
    load_catboost_model
)

__all__ = [
    "load_linear_model",
    "load_random_forest_model",
    "load_xgboost_model",
    "load_catboost_model"
]

