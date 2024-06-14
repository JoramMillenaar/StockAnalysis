# Stock Analysis
A Financial Statement Visualization Tool
![](example.png)

## Overview
This Python application provides a graphical interface to visualize key financial metrics from income statements, cash flows, and balance sheets of publicly traded companies, using data sourced from Yahoo Finance. The application utilizes PyQt5 for the GUI and Matplotlib for plotting the data, allowing users to select and view financial data interactively.

## Features
- Fetch and display financial statements (Income Statement, Cash Flow, Balance Sheet) for any publicly traded company listed on Yahoo Finance.
- Interactive GUI to select the type of financial statement and specific metrics to plot.
- Bar plot visualization of selected financial metrics over time.
- Easy navigation through financial data using a dropdown menu and a multi-select list.

## Installation

### Prerequisites
- Python 3.x
- PyQt5
- numpy
- matplotlib
- yfinance

You can install all required packages using pip:

```bash
pip install PyQt5 numpy matplotlib yfinance
```

### Running the Application
To run the application, use the following command in the terminal:

```bash
python path_to_script.py
```

Ensure you replace `path_to_script.py` with the actual path to the script file.

## Usage
1. Start the application using the command above. The main window will appear.
2. From the dropdown menu at the top, select the type of financial statement you want to view.
3. From the list below the dropdown, select one or more metrics to visualize.
4. Click the 'Update Chart' button to view the bar plot of the selected metrics.

The bar plot will display the selected financial metrics over time, based on the available data for the selected company (default is AAPL).

## Customization
To analyze a different company's financial data, change the `ticker` variable in the `main()` function from 'AAPL' to the desired company's stock ticker symbol.

## Limitations
- The application currently defaults to displaying data for Apple Inc. (AAPL). Users need to modify the source code to visualize data for other companies.
- The GUI is basic and may not handle exceptionally large datasets or a wide variety of financial metrics elegantly.

## License
This project is open source and available under the MIT License.

## Contributing
Contributions to the project are welcome. Please fork the repository, make your changes, and submit a pull request.
