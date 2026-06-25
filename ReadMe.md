Kompanion.ai

AI-Powered Productivity Companion with Optional AWS Integration

Kompanion.ai is a productivity platform that helps users plan tasks more effectively, assess their likelihood of completion, and receive guidance when goals are not achieved. Unlike conventional task managers, it combines task tracking, workload assessment, and AI-driven coaching to support better decision-making and consistency.

The application is designed with a dual-mode architecture, allowing users to operate either in a standalone local environment or with AWS-powered cloud capabilities.

Overview

Users can create tasks by specifying:

* Priority level
* Estimated completion time
* Current fatigue level

Based on these inputs, Kompanion.ai calculates a task viability score and provides a structured view of workload and productivity. When a task is marked as failed, the system generates actionable recommendations to help the user recover and continue progressing.


Key Features

* Task creation and management
* Priority-based workload planning
* Fatigue-aware task evaluation
* Task completion probability analysis
* AI-generated recovery recommendations
* Real-time productivity dashboard
* Cloud-based task persistence (AWS mode)

AWS Integration

Amazon Bedrock

Amazon Bedrock is used to generate personalized productivity coaching. When a task is not completed, the application sends task context to Claude 3.5 Sonnet through Bedrock and returns actionable feedback, alternative approaches, and next-step recommendations.

Amazon DynamoDB

Amazon DynamoDB is used for persistent storage of task data. In AWS mode, tasks and status updates are automatically synchronized, enabling users to restore and continue their progress across sessions.


Dual-Mode Architecture

Local Mode (Non-AWS Users)

Users can access the platform without an AWS account.

Available capabilities:

* Task management
* Productivity scoring
* Dashboard analytics
* Simulated AI coaching

This mode provides a complete standalone experience without requiring cloud resources.

Cloud Mode (AWS Users)

Users can connect their AWS account to enable cloud services.

Available capabilities:

* AI coaching through Amazon Bedrock
* Persistent task storage with DynamoDB
* Cloud synchronization
* Historical task recovery

This approach ensures accessibility for all users while providing enhanced functionality through AWS services.


Technology Stack

Frontend

* Streamlit
* HTML/CSS
* SVG-based Custom UI Components

Backend

* Python

Cloud Services

* Amazon Bedrock
* Amazon DynamoDB

SDK

* Boto3 (AWS SDK for Python)

Foundation Model

* Claude 3.5 Sonnet via Amazon Bedrock

---------------------------------------------------------------------------------

Purpose

Kompanion.ai was built to address a common productivity challenge: users often know what they need to do but struggle with realistic planning, consistency, and recovery after setbacks. By combining workload analysis, task tracking, and AI-powered coaching, the platform helps users make informed decisions and maintain progress toward their goals.
