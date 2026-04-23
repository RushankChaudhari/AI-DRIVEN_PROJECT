# AI-Driven Healthcare System Monitoring using Hadoop and Spark

## Overview

This project focuses on monitoring healthcare system operations using Big Data technologies and Machine Learning. It analyzes operational data to detect anomalies, evaluate system performance, and provide meaningful insights for improving system reliability.

## Objectives

* Detect abnormal behavior in healthcare systems
* Evaluate system performance using key metrics
* Classify system health into defined categories
* Provide visual representation of system status
* Generate actionable recommendations for identified issues

## Technologies Used

Python, Hadoop (HDFS), Apache Spark, Scikit-learn, Pandas, NumPy, Matplotlib, Seaborn

## Working Methodology

### Data Generation

A synthetic dataset is created representing daily operations of multiple healthcare systems. The dataset includes metrics such as workload, response time, error count, and CPU usage.

### Data Processing

The dataset is stored in Hadoop Distributed File System and processed using Apache Spark for efficient handling and querying.

### Anomaly Detection

Isolation Forest algorithm is applied to identify abnormal patterns in system behavior. Each record is classified as normal or anomalous.

### Severity Classification

Based on system metrics, each record is categorized as Healthy, Warning, or Critical.

### System Health Evaluation

A health score is calculated for each system based on the proportion of normal and anomalous records. Systems are labeled as Stable, Warning, or Critical.

### Visualization

The system generates:

* A bar chart showing health score of each system
* A heatmap showing daily system severity

### AI-Based Diagnostic Report

The system identifies the type of issue (such as overload, performance degradation, or application failure) and provides corresponding recommendations for improvement.

## Output

* Anomaly detection summary
* System-wise health report with scores
* Visual charts for performance analysis
* Diagnostic report with recommended solutions

## Key Feature

The system not only detects anomalies but also explains possible causes and suggests practical solutions, making it useful for real-world monitoring and decision-making.
