# Stock Analysis
**A Financial Statement Visualization Tool**

![](example.webp)

## Overview
This Python application provides a graphical interface to visualize key financial metrics from income statements, cash flows, balance sheets, and computed metrics of publicly traded companies, using data sourced from Yahoo Finance. The application uses PyQt5 for the GUI and Matplotlib for plotting, enabling dynamic selection of ticker symbols and interactive viewing of financial data.

## Features
- **Dynamic Ticker Input**: Enter any ticker symbol of a publicly traded company listed on Yahoo Finance to fetch and display its financial statements.
- **Interactive GUI**: Select the type of financial statement and specific metrics to plot via a dropdown menu. Financial data is displayed in a table that allows for multi-selection of metrics for plotting.
- **Enhanced Data Display**: Financial data is displayed in a user-friendly format in the QTableWidget, with values appropriately scaled to thousands or shown as percentages where applicable. Negative values are indicated with brackets.
- **Bar Plot Visualization**: Visualize selected financial metrics over time with dynamically adjustable bar plots.
- **User-Friendly Navigation**: Easily navigate through financial data using a clean and intuitive interface.

## Installation

### Prerequisites
Ensure you have Python 3.x installed along with the following Python packages: PyQt5, numpy, matplotlib, and yfinance.

Install all required packages using pip:

```bash
pip install PyQt5 numpy matplotlib yfinance
```

### Running the Application
To run the application, execute the following command in the terminal:

```bash
python path_to_script.py
```

Replace `path_to_script.py` with the actual path to the Python script file.

## Usage
1. Start the application using the command above. The GUI will prompt you to input a ticker symbol.
2. Enter the ticker symbol for the company whose financial data you want to analyze.
3. Click 'Fetch Data' to load the financial statements associated with the entered ticker symbol.
4. Use the dropdown menu to select the type of financial statement.
5. The financial data will appear in a table. Select the rows (metrics) you wish to visualize.
6. Click the 'Update Chart' button to generate a bar plot of the selected metrics.

## Data Display
- **Values Formatting**: Monetary values are shown in thousands with negative numbers displayed in brackets. Percentages and ratios retain their formatting to ensure clarity and accuracy.
- **Table Interaction**: The table allows for selection of multiple rows for data plotting, with each row representing a financial metric.

## Customization
This tool is designed to be versatile, allowing analysis of financial data for any publicly traded company by simply entering a ticker symbol in the GUI.

## Limitations
- Data retrieval is dependent on the availability and responsiveness of the Yahoo Finance API.
- The GUI layout is optimized for simplicity but may not handle an exceptionally large number of financial metrics efficiently.

## License
This project is open source and available under the MIT License.

## Contributing
Contributions to the project are welcome. To contribute, please fork the repository, make your changes, and submit a pull request.
