from dotenv import dotenv_values


class Environment:
    def __init__(self):
        environments = dotenv_values(".env") 
        self.api_url = environments.get("API_URL")
        self.api_key = environments.get("API_KEY")
        self.email_supabase = environments.get("EMAIL_SUPABASE")
        self.password_supabase = environments.get("PASSWORD_SUPABASE")