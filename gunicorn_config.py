import os
import sys

# Debug: Print the PORT value
port = os.environ.get('PORT', '8080')
print(f"DEBUG: Using PORT={port}", file=sys.stderr)

bind = f"0.0.0.0:{port}"
workers = 2
threads = 4
timeout = 120
accesslog = '-'
errorlog = '-'
