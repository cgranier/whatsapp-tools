import pandas as pd
import re
import argparse
import os

def clean_phone_number(phone):
    cleaned = re.sub(r'\D', '', phone)
    if cleaned.startswith('1') and len(cleaned) > 10:
        cleaned = cleaned[1:]
    return cleaned

def parse_whatsapp_chat(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    pattern = r'(\d{1,2}/\d{1,2}/\d{2}, \d{2}:\d{2}) - ([^:]+): (.+?)(?=\n\d{1,2}/\d{1,2}/\d{2}, \d{2}:\d{2} - |$)'
    matches = re.findall(pattern, content, re.DOTALL)
    dates, times, senders, messages = [], [], [], []
    for match in matches:
        date_time, sender, message = match
        date, time = date_time.split(', ')
        dates.append(date)
        times.append(time)
        senders.append(sender.strip())
        messages.append(message.strip())
    return pd.DataFrame({'Date': dates, 'Time': times, 'Sender': senders, 'Message': messages})

def main():
    parser = argparse.ArgumentParser(description="Process WhatsApp chat export and convert to various formats.")
    parser.add_argument("input_file", help="Input text file containing WhatsApp chat export")
    parser.add_argument("-c", "--contacts", help="CSV file containing contact information")
    parser.add_argument("-o", "--output", help="Output file name (without extension)")
    args = parser.parse_args()

    # Parse the chat and create DataFrame
    df = parse_whatsapp_chat(args.input_file)

    # Process contacts if provided
    if args.contacts:
        phone_df = pd.read_csv(args.contacts, header=None, names=['Phone', 'Name'])
        phone_df['Phone'] = phone_df['Phone'].apply(clean_phone_number)
        phone_dict = dict(zip(phone_df['Phone'], phone_df['Name']))
        df['Sender'] = df['Sender'].apply(lambda x: phone_dict.get(clean_phone_number(x), x))

    # Convert Date and Time columns to datetime
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%m/%d/%y %H:%M')

    # Determine output file name
    if args.output:
        output_base = args.output
    else:
        output_base = os.path.splitext(args.input_file)[0]

    # Save to CSV
    csv_file = f"{output_base}.csv"
    df.to_csv(csv_file, index=False)
    print(f"CSV file saved as: {csv_file}")

    # Save to Excel
    excel_file = f"{output_base}.xlsx"
    df.to_excel(excel_file, index=False)
    print(f"Excel file saved as: {excel_file}")

    # Save to Parquet (requires pyarrow or fastparquet)
    parquet_file = f"{output_base}.parquet"
    try:
        df.to_parquet(parquet_file, index=False)
        print(f"Parquet file saved successfully as {parquet_file}")
    except ImportError:
        print("Parquet file could not be saved. Install pyarrow or fastparquet to enable Parquet support.")

    print("\nBasic Analysis:")
    print(f"Total messages: {len(df)}")
    print(f"Unique senders: {df['Sender'].nunique()}")
    print("\nTop 5 most active senders:")
    print(df['Sender'].value_counts().head())

if __name__ == "__main__":
    main()
