
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
<p align="center"> Introducing DocVerifyRAG, a cutting-edge solution revolutionizing document verification processes across various sectors. Our app goes beyond mere document classification; it focuses on ensuring metadata accuracy by cross-referencing against a vast vector database of exemplary cases. Inspired by the necessity for precise data management, DocVerifyRAG leverages AI to scrutinize document metadata, instantly flagging anomalies and offering suggested corrections.

Powered by Vectara vector store technology and supported by the innovative capabilities of together.ai API, our app employs advanced anomaly detection algorithms to scrutinize metadata, ensuring compliance with regulatory standards and enhancing data integrity. With DocVerifyRAG, users can effortlessly verify document metadata accuracy, minimizing errors and streamlining operational efficiency.</p>

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


![ttthh](https://github.com/eliawaefler/DocVerifyRAG/assets/19821445/331845d7-a360-4315-92ef-d4bb50021eaa)

## Technology Stack

| Technology | Description                 |
| ---------- | --------------------------- |
| AI/ML      | Artificial Intelligence and Machine Learning |
| Python     | Programming Language        |
| Flask      | Web Framework               |
| Docker     | Containerization            |
| Tech Name    | Short description                    |

### Features

1. **Metadata Verification:**
- Cross-references document metadata against a comprehensive vector database of exemplary cases.
- Instantly identifies anomalies and discrepancies, ensuring metadata accuracy and compliance.

2. **Automated Metadata Correction:**
- Offers suggested metadata corrections based on processed PDF files, facilitating swift and accurate adjustments.
- Potential for automated inspection of numerous metadata rows for seamless large-scale data verification.

3. **Question Answering Retriever:**
- Utilizes Vectara vector store technology for efficient retrieval of relevant information.
- Employs Hugging Face embeddings E5 multilingual model for precise analysis of multilingual data.
- Identifies anomalies in names, descriptions, and disciplines, providing actionable insights for data accuracy.

4. **User-Friendly Interface:**
- Intuitive web interface for effortless document upload, metadata verification, and correction.
- Simplifies document management processes, reducing manual effort and enhancing operational efficiency.

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

Access the web interface and follow the prompts to upload documents, classify them, and verify metadata. The AI-powered anomaly detection system will automatically flag any discrepancies or errors in the document metadata, providing accurate and reliable document management solutions.
## Authors

| Name           | Link                                      |
| -------------- | ----------------------------------------- |
| Sandra Ashipala | [GitHub](https://github.com/sandramsc) |
| Elia Wäfler | [GitHub](https://github.com/eliawaefler) |
| Carlos Salgado | [GitHub](https://github.com/salgadev) |
| Abdul Qadeer | [GitHub](https://github.com/AbdulQadeer-55) |


## License

[![GitLicense](https://img.shields.io/badge/License-MIT-lime.svg)](https://github.com/eliawaefler/DocVerifyRAG/blob/main/LICENSE)
