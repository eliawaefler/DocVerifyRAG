
---
title: DocVerifyRAG
emoji: 🐠
colorFrom: pink
colorTo: green
sdk: streamlit
sdk_version: 1.27.0
app_file: app.py
pinned: false
---

<!-- PROJECT TITLE -->
  <h1 align="center">DocVerifyRAG: Document Verification and Anomaly Detection</h1>
 <div id="header" align="center">
</div>
<h2 align="center">
 Description
</h2>
<p align="center"> DocVerifyRAG is a revolutionary tool designed to streamline document verification processes in hospitals. It utilizes AI to classify documents and identify mistakes in metadata, ensuring accurate and efficient document management. Inspired by the need for improved data accuracy in healthcare, DocVerifyRAG provides automated anomaly detection to identify misclassifications and errors in document metadata, enhancing data integrity and compliance with regulatory standards. </p>

## Table of Contents

<details>
<summary>DocVerifyRAG</summary>
  
- [Application Description](#application-description)
- [Table of Contents](#table-of-contents)
- [Local installation](#install-locally)
- [Install using Docker](#install-using-docker)
- [Usage](#usage)
- [Contributing](#contributing)
- [Authors](#authors)
- [License](#license)

</details>

## TRY the prototype
[DocVerifyRAG](https://docverify-rag.vercel.app)

## Screenshots

![Screenshot 2024-04-19 130438](https://github.com/sandramsc/DocVerifyRAG/assets/19821445/a5628346-994d-4ba3-9717-6b06ca419144)


## Technology Stack

| Technology | Description                 |
| ---------- | --------------------------- |
| AI/ML      | Artificial Intelligence and Machine Learning |
| Python     | Programming Language        |
| Flask      | Web Framework               |
| Docker     | Containerization            |
| Tech Name    | Short description                    |

### Features

1. **Document Classification:**
    - Utilizes AI/ML algorithms to classify documents based on content and metadata.
    - Provides accurate and efficient document categorization for improved data management.

2. **Anomaly Detection:**
    - Identifies mistakes and misclassifications in document metadata through automated anomaly detection.
    - Enhances data integrity and accuracy by flagging discrepancies in document metadata.

3. **User-Friendly Interface:**
    - Offers a user-friendly web interface for easy document upload, classification, and verification.
    - Simplifies the document management process for hospital staff, reducing manual effort and errors.

### Install locally

#### Step 1 - Frontend

1. Clone the repository:
    ```bash
    $ git clone https://github.com/eliawaefler/DocVerifyRAG.git
    ```

2. Navigate to the frontend directory:
    ```bash
    $ cd DocVerifyRAG/frontend
    ```

3. Install dependencies:
    ```bash
    $ npm install
    ```
4. Run project:
    ```bash
    $ npm run dev
    ```

#### Step 2 - Backend

1. Navigate to the backend directory:
    ```bash
    $ cd DocVerifyRAG/backend
    ```

2. Install dependencies:
    ```bash
    $ pip install -r requirements.txt
    ```

### Install using Docker

To deploy DocVerifyRAG using Docker, follow these steps:

1. Pull the Docker image from Docker Hub:

    ```bash
    $ docker pull sandra/docverifyrag:latest
    ```

2. Run the Docker container:

    ```bash
    $ docker run -d -p 5000:5000 sandramsc/docverifyrag:latest
    ```

### Usage

Access the web interface and follow the prompts to upload documents, classify them, and verify metadata. The AI-powered anomaly detection system will automatically flag any discrepancies or errors in the document metadata, providing accurate and reliable document management solutions for hospitals.
## Authors

| Name           | Link                                      |
| -------------- | ----------------------------------------- |
| Sandra Ashipala | [GitHub](https://github.com/sandramsc) |
| Elia Wäfler | [GitHub](https://github.com/eliawaefler) |
| Carlos Salgado | [GitHub](https://github.com/salgadev) |
| Abdul Qadeer | [GitHub](https://github.com/AbdulQadeer-55) |


## License

[![GitLicense](https://img.shields.io/badge/License-MIT-lime.svg)](https://github.com/eliawaefler/DocVerifyRAG/blob/main/LICENSE)
