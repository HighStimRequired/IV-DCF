# IV-DCF

**IV-DCF** is a Python desktop application that calculates a stock’s intrinsic value using the **Discounted Cash Flow (DCF)** method. It leverages real-time financial data from [yfinance](https://pypi.org/project/yfinance/) to project future cash flows, apply discount rates, and estimate an intrinsic value per share. The app sports a dark, cozy theme with light blue accents, and it provides an option to export the calculated data to a user-specified file.

## Features

- **DCF Calculation** – Automatically calculates projected Free Cash Flows, discounts them, and computes a Terminal Value using the Gordon Growth Model.
- **Real-Time Data** – Fetches real-time financial metrics (e.g., free cash flow, shares outstanding) via yfinance.
- **Customizable Inputs** – Lets you modify discount rate, growth rate, terminal growth rate, and forecast period.
- **Dark UI Theme** – Aesthetic dark background with light-blue accents for a cozy, readable interface.
- **Export to File** – Exports the entire calculation and company data to a user-selected text file.

## Requirements

- **Python 3.7+**  
- **yfinance** (for financial data retrieval)  
- **tkinter** (bundled with most Python installations)

## Installation

1. **Clone or Download** the repository:
   ```bash
   git clone https://github.com/yourusername/IV-DCF.git
   cd IV-DCF
   ```
2. **Install Dependencies**:
   ```bash
   pip install PyQt5 Pillow reportlab pdfkit markdown cairosvg
   ```

3. **Run the Application**:
   ```bash
   python iv_dcf_app.py
   ```

## Usage

1. **Launch** the `iv_dcf_app.py` script.  
2. **Enter** your desired stock ticker (e.g., `AAPL`), discount rate, growth rate, terminal growth rate, and forecast period.  
3. **Click** the **"Calculate Intrinsic Value"** button to perform the DCF analysis.  
4. **View** the results, including projected free cash flows, discounted values, terminal value, and overall intrinsic value.  
5. **Export** the detailed calculation and company data by clicking **"Export Data"**, choosing your preferred export location.

## Project Structure

- **iv_dcf_app.py** – Main Python script containing the Tkinter GUI and DCF calculation logic.  
- **README.md** – Project documentation (this file).  
- **requirements.txt** – Dependencies for easy installation.

## Contributing

1. **Fork** the project.  
2. **Create** a new branch for your feature or bugfix.  
3. **Commit** your changes and **open** a pull request.

## License

This project is available under the **MIT License**. See the [LICENSE](LICENSE) file for more information.
