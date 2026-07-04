# 🚗 European Car Recommendation System Using AWS Cloud

A cloud-based car recommendation web application built with **Python**, **Streamlit**, **Pandas**, **Amazon EC2**, and **Amazon RDS MySQL**.

This project helps users find suitable European cars based on preferences such as brand, model, price range, fuel type, transmission, performance, and other vehicle details.

---

## 📌 Project Overview

The European Car Recommendation System is a web application that allows users to search and filter car options from a cloud-hosted database.

The application was first developed locally using **Visual Studio Code** and later deployed on an **AWS EC2 Ubuntu server**. The car dataset was stored in an **Amazon RDS MySQL database**, and the Streamlit application retrieves the data from RDS to display recommendations.

---

## 🎯 Project Objective

The main objective of this project is to build and deploy a cloud-based recommendation system that:

- Allows users to search cars by model or brand
- Filters cars based on user preferences
- Displays matching car recommendations
- Uses a managed cloud database
- Runs continuously on a cloud server
- Demonstrates real-world cloud deployment using AWS

---

## 🛠️ Technologies Used

### Frontend
- Streamlit
- HTML/CSS styling inside Streamlit

### Backend
- Python
- Pandas
- SQLAlchemy
- PyMySQL

### Cloud Services
- Amazon EC2
- Amazon RDS MySQL
- AWS Security Groups
- Public IPv4 access

### Database
- Amazon RDS MySQL
- MySQL 8.4.8
- RDS instance class: `db.t3.micro`
- Storage: 50 GiB gp2

### Version Control
- Git
- GitHub

---

## ☁️ AWS Architecture

```text
User Browser
     |
     | HTTP Request
     | Port 8501
     v
AWS EC2 Instance
Ubuntu Server
Streamlit Application
Python app.py
     |
     | MySQL Connection
     | Port 3306
     v
Amazon RDS MySQL Database
car-database
db.t3.micro
MySQL 8.4.8
