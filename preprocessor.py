import re
import pandas as pd

def preprocess(data):
    # Regular expression to match date patterns
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]  # Skip the first split as it may be empty
    dates = re.findall(pattern, data)
    
    # Check if the lengths match
    if len(messages) != len(dates):
        raise ValueError("Mismatch between number of messages and dates.")
    
    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    
    # Function to handle multiple date formats
    def parse_date(date_str):
        formats = ['%m/%d/%y, %H:%M - ', '%d/%m/%y, %H:%M - ']
        for fmt in formats:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except ValueError:
                continue
        return pd.NaT

    df['message_date'] = df['message_date'].apply(parse_date)
    df.rename(columns={'message_date': 'date'}, inplace=True)
    
    users = []
    messages = []
    
    # Iterate through each message in the 'user_message' column
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if len(entry) > 1:
            # Split user and message
            users.append(entry[1].strip())  # User name
            messages.append(" ".join(entry[2:]).strip())  # The actual message
        else:
            # Handle system messages (e.g., group notifications)
            users.append('group_notification')
            messages.append(message.strip())
    
    df['user'] = users
    df['message'] = messages
    
    # Extract additional date/time information
    df['year'] = df['date'].dt.year
    df['only_date'] = df['date'].dt.date
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    
    
    
    
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
    
    
