# AI Model Preprocessing and Backend Integration

This project provides a backend C implementation for running various machine learning models (e.g., Linear Regression, K-Nearest Neighbors, Support Vector Machines) and performing tasks such as data preprocessing, dimensionality reduction, and model evaluation. The backend integrates Python for executing the Linear Regression model and utilizes Lex/Flex and Yacc/Bison for processing input.

## Features
- **Linear Regression**: Integrates Python for performing linear regression on data.
- **KNN and SVM**: Placeholder functions for running K-Nearest Neighbors and Support Vector Machines algorithms.
- **Preprocessing**: Provides preprocessing utilities such as setting target variables, dimensionality reduction, and data scaling.
- **Export and Evaluation**: Supports data export and model evaluation tasks.
- **Model Automation**: Placeholder for automatically selecting and training models based on data.

## Technologies Used
- **C**: Core backend logic, utilizing Lex/Flex for scanning and Yacc/Bison for parsing.
- **Python**: Integrated for running the Linear Regression model using the `preprocess.py` script.
- **Lex/Flex**: Used to generate a scanner for input parsing.
- **Yacc/Bison**: Used to generate a parser for the input format.

## Setup

### Prerequisites
1. **Python 3.x**: Required for running the Python-based Linear Regression model.
2. **Flex**: Required to generate the scanner from the `scanner.l` file.
3. **Bison**: Required to generate the parser from the `parser.y` file.
4. **GCC**: Compiler for C files.

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/YourUsername/your-repository.git
   cd your-repository
