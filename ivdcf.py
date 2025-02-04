import tkinter as tk
from tkinter import filedialog, messagebox
import yfinance as yf

class DCFCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Discounted Cash Flow Calculator 🧮")
        self.configure(bg="#2C2C2C")  # Dark background
        self.geometry("600x500")
        self.create_widgets()
        
    def create_widgets(self):
        # Define fonts for a consistent look
        label_font = ("Helvetica", 12)
        entry_font = ("Helvetica", 12)
        
        # Input Frame
        input_frame = tk.Frame(self, bg="#2C2C2C")
        input_frame.pack(pady=10, padx=10, fill="x")
        
        # Stock Ticker Input
        tk.Label(input_frame, text="Stock Ticker:", bg="#2C2C2C", fg="white", font=label_font).grid(row=0, column=0, sticky="w")
        self.ticker_entry = tk.Entry(input_frame, font=entry_font, bg="#3C3F41", fg="white", insertbackground="white")
        self.ticker_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        input_frame.columnconfigure(1, weight=1)
        
        # Discount Rate Input
        tk.Label(input_frame, text="Discount Rate (e.g., 0.10):", bg="#2C2C2C", fg="white", font=label_font).grid(row=1, column=0, sticky="w")
        self.discount_rate_entry = tk.Entry(input_frame, font=entry_font, bg="#3C3F41", fg="white", insertbackground="white")
        self.discount_rate_entry.insert(0, "0.10")
        self.discount_rate_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        # Growth Rate Input
        tk.Label(input_frame, text="Growth Rate (e.g., 0.05):", bg="#2C2C2C", fg="white", font=label_font).grid(row=2, column=0, sticky="w")
        self.growth_rate_entry = tk.Entry(input_frame, font=entry_font, bg="#3C3F41", fg="white", insertbackground="white")
        self.growth_rate_entry.insert(0, "0.05")
        self.growth_rate_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        # Terminal Growth Rate Input
        tk.Label(input_frame, text="Terminal Growth Rate (e.g., 0.02):", bg="#2C2C2C", fg="white", font=label_font).grid(row=3, column=0, sticky="w")
        self.terminal_growth_rate_entry = tk.Entry(input_frame, font=entry_font, bg="#3C3F41", fg="white", insertbackground="white")
        self.terminal_growth_rate_entry.insert(0, "0.02")
        self.terminal_growth_rate_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        
        # Forecast Period Input
        tk.Label(input_frame, text="Forecast Period (years):", bg="#2C2C2C", fg="white", font=label_font).grid(row=4, column=0, sticky="w")
        self.forecast_years_entry = tk.Entry(input_frame, font=entry_font, bg="#3C3F41", fg="white", insertbackground="white")
        self.forecast_years_entry.insert(0, "5")
        self.forecast_years_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        
        # Calculate Button
        self.calc_button = tk.Button(self, text="Calculate Intrinsic Value", command=self.calculate, bg="#7FDBFF", fg="black", font=label_font)
        self.calc_button.pack(pady=10)
        
        # Text Widget for Result Display
        self.result_text = tk.Text(self, height=10, bg="#3C3F41", fg="white", font=("Courier", 12))
        self.result_text.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Export Button
        self.export_button = tk.Button(self, text="Export Data 📄", command=self.export_data, bg="#7FDBFF", fg="black", font=label_font)
        self.export_button.pack(pady=10)
        
    def calculate(self):
        """Fetches financial data using yfinance, performs DCF calculations, and displays the results."""
        # Clear previous results
        self.result_text.delete("1.0", tk.END)
        
        # Retrieve user inputs
        ticker_symbol = self.ticker_entry.get().strip().upper()
        try:
            discount_rate = float(self.discount_rate_entry.get().strip())
            growth_rate = float(self.growth_rate_entry.get().strip())
            terminal_growth_rate = float(self.terminal_growth_rate_entry.get().strip())
            forecast_years = int(self.forecast_years_entry.get().strip())
        except ValueError:
            messagebox.showerror("Input Error", "Please check your inputs. Ensure numeric values are entered where required.")
            return
        
        if not ticker_symbol:
            messagebox.showerror("Input Error", "Please enter a valid stock ticker symbol.")
            return
        
        self.result_text.insert(tk.END, f"Fetching data for {ticker_symbol}...\n")
        self.update()  # Refresh the UI
        
        try:
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info
        except Exception as e:
            messagebox.showerror("Data Fetch Error", f"Error fetching data for {ticker_symbol}: {str(e)}")
            return
        
        # Retrieve Free Cash Flow (FCF)
        fcf = None
        if "freeCashflow" in info and info["freeCashflow"] is not None:
            fcf = info["freeCashflow"]
        else:
            # Attempt to compute FCF from cash flow data: Operating CF + Capital Expenditures (capex is typically negative)
            try:
                cashflow = ticker.cashflow
                if 'Total Cash From Operating Activities' in cashflow.index and 'Capital Expenditures' in cashflow.index:
                    most_recent = cashflow.columns[0]
                    operating_cf = cashflow.loc['Total Cash From Operating Activities', most_recent]
                    capex = cashflow.loc['Capital Expenditures', most_recent]
                    fcf = operating_cf + capex
                else:
                    raise Exception("Necessary cash flow data not found.")
            except Exception as e:
                messagebox.showerror("Data Error", f"Could not retrieve Free Cash Flow data for {ticker_symbol}. {str(e)}")
                return
        
        self.result_text.insert(tk.END, f"Most recent Free Cash Flow: {fcf:,.2f}\n\n")
        
        # DCF Calculation: Project FCF for each forecast year and discount them
        fcf_forecasts = []
        discounted_fcf = []
        current_fcf = fcf
        for year in range(1, forecast_years + 1):
            current_fcf *= (1 + growth_rate)
            fcf_forecasts.append(current_fcf)
            discounted_value = current_fcf / ((1 + discount_rate) ** year)
            discounted_fcf.append(discounted_value)
            self.result_text.insert(tk.END, f"Year {year}: Projected FCF = {current_fcf:,.2f}, Discounted Value = {discounted_value:,.2f}\n")
        
        # Terminal Value Calculation (using the Gordon Growth Model)
        terminal_value = fcf_forecasts[-1] * (1 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)
        discounted_terminal_value = terminal_value / ((1 + discount_rate) ** forecast_years)
        self.result_text.insert(tk.END, f"\nTerminal Value: {terminal_value:,.2f}, Discounted Terminal Value = {discounted_terminal_value:,.2f}\n")
        
        enterprise_value = sum(discounted_fcf) + discounted_terminal_value
        self.result_text.insert(tk.END, f"\nEnterprise Value (Intrinsic Value): {enterprise_value:,.2f}\n")
        
        # Calculate per-share value if shares outstanding data is available
        if "sharesOutstanding" in info and info["sharesOutstanding"]:
            per_share_value = enterprise_value / info["sharesOutstanding"]
            self.result_text.insert(tk.END, f"Intrinsic Value per Share: {per_share_value:,.2f}\n")
        else:
            per_share_value = None
            self.result_text.insert(tk.END, "Shares outstanding data not available for per-share valuation.\n")
        
        # Store results and company info for export
        self.calculation_result = {
            "ticker": ticker_symbol,
            "free_cash_flow": fcf,
            "fcf_forecasts": fcf_forecasts,
            "discounted_fcf": discounted_fcf,
            "terminal_value": terminal_value,
            "discounted_terminal_value": discounted_terminal_value,
            "enterprise_value": enterprise_value,
            "per_share_value": per_share_value,
            "discount_rate": discount_rate,
            "growth_rate": growth_rate,
            "terminal_growth_rate": terminal_growth_rate,
            "forecast_years": forecast_years,
            "company_info": info
        }
        
    def export_data(self):
        """Exports the calculation details and company data to a text file at a user-specified location."""
        if not hasattr(self, "calculation_result"):
            messagebox.showerror("Export Error", "No calculation data available. Please perform a calculation first.")
            return
        
        # Let the user choose where to save the report
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
                                                 title="Save Report As")
        if not file_path:
            return
        
        try:
            with open(file_path, "w") as f:
                result = self.calculation_result
                f.write(f"DCF Intrinsic Value Report for {result['ticker']}\n")
                f.write("=" * 50 + "\n")
                f.write(f"Free Cash Flow (Most Recent): {result['free_cash_flow']:,.2f}\n")
                f.write(f"Discount Rate: {result['discount_rate']}\n")
                f.write(f"Growth Rate: {result['growth_rate']}\n")
                f.write(f"Terminal Growth Rate: {result['terminal_growth_rate']}\n")
                f.write(f"Forecast Period: {result['forecast_years']} years\n\n")
                
                f.write("Yearly Projections:\n")
                for i, (proj, disc) in enumerate(zip(result["fcf_forecasts"], result["discounted_fcf"]), start=1):
                    f.write(f"Year {i}: Projected FCF = {proj:,.2f}, Discounted Value = {disc:,.2f}\n")
                    
                f.write("\n")
                f.write(f"Terminal Value: {result['terminal_value']:,.2f}\n")
                f.write(f"Discounted Terminal Value: {result['discounted_terminal_value']:,.2f}\n\n")
                f.write(f"Enterprise Value (Intrinsic Value): {result['enterprise_value']:,.2f}\n")
                if result["per_share_value"] is not None:
                    f.write(f"Intrinsic Value per Share: {result['per_share_value']:,.2f}\n")
                else:
                    f.write("Intrinsic Value per Share: N/A (shares outstanding not available)\n")
                f.write("\n")
                f.write("Company Info (Partial):\n")
                # Include a few key company details
                keys = ["longName", "sector", "industry", "country", "website"]
                for key in keys:
                    if key in result["company_info"]:
                        f.write(f"{key}: {result['company_info'][key]}\n")
            messagebox.showinfo("Export Successful", f"Report exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting data: {str(e)}")

if __name__ == "__main__":
    app = DCFCalculator()
    app.mainloop()
