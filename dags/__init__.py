# File: /home/gr00stl/Nextcloud/Projects/reviews-sentiment/user_feedback_analysis/dags/__init__.py

"""
This module initializes the dags package and provides easy access to DAG objects.
"""

from .load_data_dag import dag as load_data_dag

# You can add more DAG imports here as you create them
# from .another_dag import dag as another_dag

# List of all DAGs in this package
__all__ = ['load_data_dag']