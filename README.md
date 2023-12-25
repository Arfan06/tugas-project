## Environment
conda create --name dashboard python=3.11
conda activation --name dashboard python=3.11

## Library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

## Run Dashboard
streamlit run dashboard.py
