from mangum import Mangum
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from main import app
    handler = Mangum(app, lifespan="off")
except Exception as e:
    print(f"Error importing app: {e}")
    # Fallback handler
    def handler(event, context):
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }
