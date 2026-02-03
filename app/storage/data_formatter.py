from datetime import datetime


class DataFormatter:
    @staticmethod
    def format_date(date_string, input_format="%Y%m%d", output_format="%d/%m/%Y"):
        """Format date string"""
        try:
            dt = datetime.strptime(date_string[:8], input_format)
            return dt.strftime(output_format)
        except:
            return date_string

    @staticmethod
    def format_datetime(datetime_string):
        """Format datetime string"""
        try:
            dt = datetime.fromisoformat(datetime_string.replace('Z', '+00:00'))
            return dt.strftime('%d/%m/%Y %H:%M')
        except:
            return datetime_string

    @staticmethod
    def extract_classe_info(classe_data):
        """Extract class information"""
        if isinstance(classe_data, dict):
            return f"{classe_data.get('codigo', '')} - {classe_data.get('nome', 'N/A')}"
        return str(classe_data)

    @staticmethod
    def extract_orgao_info(orgao_data):
        """Extract organ information"""
        if isinstance(orgao_data, dict):
            return f"{orgao_data.get('nome', 'N/A')} ({orgao_data.get('codigoMunicipioIBGE', '')})"
        return str(orgao_data)