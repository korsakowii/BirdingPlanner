# API Keys Configuration Guide

This guide explains how to securely configure API keys for BirdingPlanner.

## 🔐 eBird API Key

### 1. Get Your API Key
1. Visit [eBird API Key Generator](https://ebird.org/api/keygen)
2. Sign in with your eBird account
3. Generate a new API key
4. Copy the key (it will look like: `4t69mf94tb37`)

### 2. Configure the API Key

#### Option A: Environment Variable (Recommended)
```bash
# Set for current session
export EBIRD_API_KEY=your_api_key_here

# Set permanently (add to ~/.zshrc or ~/.bashrc)
echo 'export EBIRD_API_KEY=your_api_key_here' >> ~/.zshrc
source ~/.zshrc
```

#### Option B: .env File (Development)
1. Create a `.env` file in the project root:
```bash
# .env
EBIRD_API_KEY=your_api_key_here
```

2. Install python-dotenv (if not already installed):
```bash
pip install python-dotenv
```

3. Update `src/config/settings.py` to load from .env:
```python
from dotenv import load_dotenv
load_dotenv()
```

#### Option C: Direct Configuration
```python
from src.config.settings import update_settings

update_settings(ebird_api_key="your_api_key_here")
```

### 3. Verify Configuration
```bash
# Test the configuration
python test_ebird_integration.py
```

## 🔒 Security Best Practices

### ✅ Do's
- Use environment variables for production
- Keep API keys out of version control
- Use different keys for development and production
- Regularly rotate API keys
- Use `.env` files only for development

### ❌ Don'ts
- Never commit API keys to Git
- Don't hardcode keys in source code
- Don't share API keys publicly
- Don't use the same key across multiple environments

## 🚀 Production Deployment

### Docker
```bash
# Pass environment variable to container
docker run -e EBIRD_API_KEY=your_key birdingplanner
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  birdingplanner:
    build: .
    environment:
      - EBIRD_API_KEY=${EBIRD_API_KEY}
```

### Cloud Platforms
- **Heroku**: Set via dashboard or CLI
- **AWS**: Use AWS Secrets Manager
- **Google Cloud**: Use Secret Manager
- **Azure**: Use Key Vault

## 🔧 Troubleshooting

### Common Issues

1. **"No eBird API key found"**
   - Check if environment variable is set: `echo $EBIRD_API_KEY`
   - Verify the variable name is correct: `EBIRD_API_KEY`

2. **API requests failing**
   - Verify the API key is valid
   - Check eBird API status: https://status.ebird.org/
   - Ensure you're not exceeding rate limits

3. **Permission denied**
   - Make sure the API key has the necessary permissions
   - Check if the key is active in your eBird account

### Testing Your Setup
```bash
# Run the integration test
python test_ebird_integration.py

# Run the demo
python demo_ebird_integration.py
```

## 📝 Example Configuration Files

### .env.example
```bash
# Copy this to .env and fill in your actual keys
EBIRD_API_KEY=your_ebird_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
```

### .env (your actual file)
```bash
EBIRD_API_KEY=4t69mf94tb37
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
```

## 🔄 Updating API Keys

If you need to update your API key:

1. Generate a new key from eBird
2. Update your environment variable or .env file
3. Restart your application
4. Test with the integration script

## 📞 Support

If you encounter issues with API key configuration:

1. Check the troubleshooting section above
2. Verify your eBird account status
3. Contact eBird support for API issues
4. Check the project's GitHub issues for known problems 