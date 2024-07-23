# BEIR with Fess

This project provides a simple and straightforward example of how to evaluate retrieval models from the BEIR benchmark using Fess.

## Introduction

This repository contains a Jupyter Notebook for evaluating retrieval models using the BEIR (Benchmark for Evaluation of Information Retrieval) framework and Fess search engine. BEIR is a comprehensive benchmark designed for zero-shot evaluation of information retrieval models across diverse tasks and datasets.

## What is BEIR?

[BEIR](https://github.com/beir-cellar/beir) (Benchmark for Evaluation of Information Retrieval) is a heterogeneous benchmark designed for zero-shot evaluation of information retrieval models. BEIR contains diverse retrieval tasks and different datasets, allowing for comprehensive evaluation of state-of-the-art retrieval models in a zero-shot setup.

## Setup

### Prerequisites

- Docker
- Python 3.10 or higher
- Jupyter Notebook

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/codelibs/beir-fess.git
    cd beir-fess
    ```

2. **Install the required Python packages**:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Open the Jupyter Notebook**:
    ```sh
    jupyter notebook
    ```

2. **Configure environment variables**:
    - Set the `BEIR_DATASET` environment variable to the dataset you want to evaluate (e.g., `scifact`).
    - Set the `FESS_DIR` environment variable to the directory where Fess is located (default is `fess`).

3. **Run the Notebook**:
    - Follow the steps in the Jupyter Notebook to download the dataset, start the Fess instance, and evaluate the retrieval model.

## Evaluating Retrieval Models

The notebook includes the following steps:

1. **Download the BEIR dataset**:
    - The dataset is downloaded and unzipped to the `datasets` directory.

2. **Start Fess**:
    - Fess is started using Docker Compose within the notebook.
    - The notebook waits for Fess to be ready before proceeding.

3. **Index the dataset in Fess**:
    - The dataset is indexed in Fess for retrieval.

4. **Retrieve and Evaluate**:
    - Use Fess to retrieve results for the queries.
    - Evaluate the retrieval using metrics such as NDCG, MAP, Recall, and Precision.

5. **Save and View Results**:
    - The evaluation results are saved as a CSV file in the `results` directory.
    - The results are printed in Markdown format for easy viewing.

## Results

The results are saved as CSV files in the `results` directory with the format `<dataset>-<fess_dir>.csv`. The results include the following metrics:

- NDCG (Normalized Discounted Cumulative Gain)
- MAP (Mean Average Precision)
- Recall
- Precision

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

