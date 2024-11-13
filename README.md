# Statistical Analysis Tool

This project is a Domain-Specific Language (DSL) Compiler designed to parse and execute commands written in a custom DSL for data processing and machine learning tasks. The compiler is built using Bison for parsing and Flex for lexical analysis, with the backend written in C and integrated with Python for executing specific machine learning functions.

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
   git clone https://github.com/YourUsername/your-repository.git](https://github.com/Ashwinth04/Statistical-Analysis-Tool
   cd your-repository
   source venv/bin/activate
   ./build.sh
   ./statpiler < <program_name>.txt
