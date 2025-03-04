import pandas as pd

# Function to save extracted text to an Excel file
def save_to_excel(data, file_name="business_card_data.xlsx"):
    df = pd.DataFrame(data, columns=["Extracted Text"])
    df.to_excel(file_name, index=False)
    print(f"Data saved to {file_name}")

# Save results
save_to_excel(text_data)
