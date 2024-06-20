from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

# The list of scopes that you need access to
SCOPES = ['https://www.googleapis.com/auth/userinfo.email',
          'https://www.googleapis.com/auth/userinfo.profile']

def authenticate():
    creds = None
    
    # The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
    token_path = 'token.json'
    
    # Check if the token file already exists
    if os.path.exists(token_path):
        # Try to load credentials from the token file
        creds = Credentials.from_authorized_user_file(token_path)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh expired credentials
            creds.refresh(Request())
        else:
            # Start the OAuth 2.0 flow for the user to authenticate
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return creds

def main():
    # Authenticate the user
    credentials = authenticate()
    
    # Use the credentials to access protected resources
    # For example, you can make API requests using the credentials
    
    # Print user info
    print("Authenticated user:")
    print("Name:", credentials.id_token['name'])
    print("Email:", credentials.id_token['email'])

if __name__ == '__main__':
    main()
