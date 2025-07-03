#!/bin/bash

echo "🛠️ Setting up Gemini Analytics Integration"
echo "=========================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Create sample service account file if it doesn't exist
if [ ! -f "service-account.json" ]; then
    echo "📝 Creating sample service account configuration..."
    cat > service-account.json << 'EOF'
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
}
EOF
    echo "⚠️  Sample service-account.json created. Please replace with your actual Google Service Account credentials."
else
    echo "✅ service-account.json already exists"
fi

# Set environment variables
echo "🔧 Setting up environment variables..."
echo "export GOOGLE_SERVICE_ACCOUNT_FILE=service-account.json" >> .env
echo "export DOMAIN_ADMIN_EMAIL=admin@semrush.com" >> .env

echo ""
echo "🎉 Gemini Analytics setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Replace service-account.json with your actual Google Service Account credentials"
echo "2. Update DOMAIN_ADMIN_EMAIL in .env file with your actual admin email"
echo "3. Ensure your service account has domain-wide delegation enabled"
echo "4. Test the integration: python3 gemini_tracker.py"
echo ""
echo "🚀 Your dashboard will now show live Gemini usage data!"
