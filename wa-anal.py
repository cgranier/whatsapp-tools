import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns
from datetime import datetime
import argparse
import os

def analyze_account_activity(df, output_prefix):
    print("\nAccount Activity Analysis:")
    
    post_counts = df['Sender'].value_counts()
    median_posts = post_counts.median()
    print(f"Median number of posts: {median_posts:.2f}")
    
    active_accounts = post_counts[post_counts > median_posts]
    inactive_accounts = post_counts[post_counts <= median_posts]
    
    print(f"Total unique accounts: {len(post_counts)}")
    print(f"Number of active accounts: {len(active_accounts)}")
    print(f"Number of inactive accounts: {len(inactive_accounts)}")
    
    print("\nPosting frequency statistics:")
    print(post_counts.describe())
    
    plt.figure(figsize=(12, 6))
    sns.histplot(post_counts, kde=True, bins=30)
    plt.title('Distribution of Posting Frequency')
    plt.xlabel('Number of Posts')
    plt.ylabel('Number of Accounts')
    plt.axvline(median_posts, color='r', linestyle='--', label='Median')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_posting_frequency_distribution.png')
    plt.close()
    
    print(f"\nPosting frequency distribution plot saved as '{output_prefix}_posting_frequency_distribution.png'")

def additional_analysis(df, output_prefix):
    print("\nAdditional Analysis:")
    
    total_accounts = df['Sender'].nunique()
    active_accounts = df['Sender'].value_counts().count()
    pct_active = (active_accounts / total_accounts) * 100
    
    print(f"1. Unique posters:")
    print(f"   Absolute: {active_accounts}")
    print(f"   Percentage of total: {pct_active:.2f}%")
    
    inactive_accounts = total_accounts - active_accounts
    print(f"\n2. Posting activity:")
    print(f"   Accounts that post: {active_accounts}")
    print(f"   Accounts that don't post: {inactive_accounts}")
    
    total_messages = len(df)
    avg_messages_total = total_messages / total_accounts
    avg_messages_active = total_messages / active_accounts
    
    print(f"\n3. Average messages:")
    print(f"   Per total accounts: {avg_messages_total:.2f}")
    print(f"   Per active accounts: {avg_messages_active:.2f}")
    
    message_counts = df['Sender'].value_counts()
    print("\n4. Distribution of message counts:")
    print(message_counts.describe())
    
    plt.figure(figsize=(12, 6))
    sns.histplot(message_counts, kde=True)
    plt.title('Distribution of Message Counts per Sender')
    plt.xlabel('Number of Messages')
    plt.ylabel('Number of Senders')
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_message_count_distribution.png')
    plt.close()
    
    print(f"\nMessage count distribution plot saved as '{output_prefix}_message_count_distribution.png'")

def main(input_file):
    output_prefix = os.path.splitext(os.path.basename(input_file))[0]
    
    df = pd.read_csv(input_file)
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%m/%d/%y %H:%M')

    print("WhatsApp Group Chat Analysis")
    print("===========================")

    print("\n1. Basic Statistics:")
    print(f"Total messages: {len(df)}")
    print(f"Date range: {df['DateTime'].min().date()} to {df['DateTime'].max().date()}")
    print(f"Number of unique senders: {df['Sender'].nunique()}")

    print("\n2. Top 20 Most Active Senders:")
    top_senders = df['Sender'].value_counts().head(20)
    print(top_senders)

    plt.figure(figsize=(12, 6))
    top_senders.plot(kind='bar')
    plt.title('Top 20 Most Active Senders')
    plt.xlabel('Sender')
    plt.ylabel('Number of Messages')
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_top_senders.png')
    plt.close()

    print("\n3. Activity by Day of Week:")
    df['DayOfWeek'] = df['DateTime'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    activity_by_day = df['DayOfWeek'].value_counts().reindex(day_order)
    print(activity_by_day)

    plt.figure(figsize=(10, 6))
    activity_by_day.plot(kind='bar')
    plt.title('Activity by Day of Week')
    plt.xlabel('Day of Week')
    plt.ylabel('Number of Messages')
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_activity_by_day.png')
    plt.close()

    print("\n4. Activity by Hour:")
    df['Hour'] = df['DateTime'].dt.hour
    activity_by_hour = df['Hour'].value_counts().sort_index()
    print(activity_by_hour)

    plt.figure(figsize=(12, 6))
    activity_by_hour.plot(kind='line')
    plt.title('Activity by Hour of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Messages')
    plt.xticks(range(0, 24))
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_activity_by_hour.png')
    plt.close()

    print("\n5. Most Common Words:")
    df['Message'] = df['Message'].fillna('').astype(str)
    words = ' '.join(df['Message']).lower().split()
    word_freq = Counter(words)
    common_words = word_freq.most_common(20)
    print(common_words)

    plt.figure(figsize=(12, 6))
    word_df = pd.DataFrame(common_words, columns=['Word', 'Frequency'])
    sns.barplot(x='Frequency', y='Word', data=word_df)
    plt.title('20 Most Common Words')
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_common_words.png')
    plt.close()

    print("\n6. Average Message Length by Sender:")
    df['MessageLength'] = df['Message'].str.len()
    avg_length = df.groupby('Sender')['MessageLength'].mean().sort_values(ascending=False).head(10)
    print(avg_length)

    plt.figure(figsize=(12, 6))
    avg_length.plot(kind='bar')
    plt.title('Average Message Length by Top 10 Senders')
    plt.xlabel('Sender')
    plt.ylabel('Average Message Length')
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_avg_message_length.png')
    plt.close()

    additional_analysis(df, output_prefix)
    analyze_account_activity(df, output_prefix)

    print("\nAnalysis complete. Visualizations saved as PNG files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze WhatsApp chat data from a CSV file.")
    parser.add_argument("input_file", help="Path to the input CSV file containing WhatsApp chat data")
    args = parser.parse_args()

    main(args.input_file)