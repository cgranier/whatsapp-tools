import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import os

def analyze_top_senders(input_file):
    # Load the CSV file
    df = pd.read_csv(input_file)

    # Convert Date and Time to DateTime
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%m/%d/%y %H:%M')

    # Identify top 10 senders
    top_senders = df['Sender'].value_counts().nlargest(10).index.tolist()

    # Filter DataFrame to include only top 10 senders
    df_top_senders = df[df['Sender'].isin(top_senders)]

    # Group by date and sender, count messages
    daily_message_count = (df_top_senders
        .groupby([df_top_senders['DateTime'].dt.date, 'Sender'])
        .size()
        .unstack(fill_value=0)
    )

    # Prepare data for plotting
    daily_message_count = daily_message_count.reset_index()
    daily_message_count_melted = daily_message_count.melt(id_vars='DateTime',
                                                          var_name='Sender',
                                                          value_name='MessageCount')

    # Create the plot
    plt.figure(figsize=(15, 8))
    sns.lineplot(data=daily_message_count_melted, x='DateTime', y='MessageCount', hue='Sender', marker='o')

    # Customize the plot
    plt.title('Number of Messages Sent by Top 10 Senders Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Messages')
    plt.xticks(rotation=45)
    plt.legend(title='Sender', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()

    # Generate output filename based on input filename
    output_filename = os.path.splitext(os.path.basename(input_file))[0] + '_top_10_senders_daily_activity.png'

    # Save the plot
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Plot saved as '{output_filename}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze and plot top 10 senders' activity over time from a WhatsApp chat CSV file.")
    parser.add_argument("input_file", help="Path to the input CSV file containing WhatsApp chat data")
    args = parser.parse_args()

    analyze_top_senders(args.input_file)