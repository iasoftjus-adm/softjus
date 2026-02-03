from datetime import datetime

def format_date(date_string, input_format="%Y%m%d", output_format="%d/%m/%Y"):
    """Format date string"""
    try:
        dt = datetime.strptime(date_string[:8], input_format)
        return dt.strftime(output_format)
    except:
        return date_string

def format_datetime(datetime_string):
    """Format datetime string"""
    try:
        dt = datetime.fromisoformat(datetime_string.replace('Z', '+00:00'))
        return dt.strftime('%d/%m/%Y %H:%M')
    except:
        return datetime_string

def truncate_text(text, max_length=100):
    """Truncate text to max length"""
    if len(text) > max_length:
        return text[:max_length-3] + "..."
    return text

def format_process_number(process_number):
    """Format process number for display"""
    if len(process_number) == 20:
        return f"{process_number[:7]}-{process_number[7:9]}.{process_number[9:13]}.{process_number[13]}.{process_number[14:16]}.{process_number[16:]}"
    return process_number