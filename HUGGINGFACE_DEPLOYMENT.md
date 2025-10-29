# Hugging Face Spaces Deployment Guide

This guide will help you deploy the AI Multi-Agent Supply Chain Optimizer to Hugging Face Spaces.

## Prerequisites

1. A Hugging Face account (sign up at https://huggingface.co)
2. Git installed on your machine
3. Required API keys:
   - OpenRouter API key (required for AI agents)
   - OpenWeather API key (optional, for weather data)
   - OpenRouteService API key (optional, for route optimization)

## Step 1: Create a New Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in the details:
   - **Space name**: `ai-supply-chain-optimizer` (or your preferred name)
   - **License**: MIT
   - **SDK**: Docker
   - **Visibility**: Public (or Private if you prefer)
4. Click "Create Space"

## Step 2: Clone Your New Space

```bash
# Clone the empty space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME
```

## Step 3: Copy Your Project Files

Copy all files from this project to your cloned space directory:

```bash
# From your AI-Multi-Agent-Supply-Chain-Optimizer directory
cp -r * /path/to/YOUR_SPACE_NAME/
cp -r .dockerignore /path/to/YOUR_SPACE_NAME/
```

Or manually copy these essential files:
- `Dockerfile`
- `.dockerignore`
- `frontend/` directory
- `backend/` directory
- `README_HUGGINGFACE.md` (rename to `README.md`)

## Step 4: Rename README

```bash
cd /path/to/YOUR_SPACE_NAME
mv README_HUGGINGFACE.md README.md
```

## Step 5: Configure Environment Variables

1. Go to your Space on Hugging Face
2. Click on "Settings" (gear icon)
3. Navigate to "Variables and secrets"
4. Add the following secrets:

### Required:
- **Name**: `OPENROUTER_API_KEY`
  - **Value**: Your OpenRouter API key
  - Type: Secret

### Optional (for enhanced features):
- **Name**: `OPENWEATHER_API_KEY`
  - **Value**: Your OpenWeather API key
  - Type: Secret

- **Name**: `OPENROUTESERVICE_API_KEY`
  - **Value**: Your OpenRouteService API key
  - Type: Secret

## Step 6: Push to Hugging Face

```bash
# Initialize git if needed
git add .
git commit -m "Initial deployment of AI Supply Chain Optimizer"

# Push to Hugging Face
git push
```

## Step 7: Wait for Build

1. Go to your Space page
2. You'll see "Building..." status
3. The build process takes about 10-15 minutes
4. Once complete, you'll see "Running" status
5. Your app will be accessible at: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`

## Step 8: Verify Deployment

1. Visit your Space URL
2. Try running an analysis:
   - Select origin: Mumbai
   - Select destination: Delhi
   - Choose scenario: Normal Operations
   - Click "Run Analysis"

## Troubleshooting

### Build Fails

1. Check the build logs in your Space
2. Common issues:
   - Missing dependencies: Update `backend/requirements.txt` or `frontend/package.json`
   - Docker timeout: The build might be too large; optimize `.dockerignore`

### App Doesn't Load

1. Check if the Space is running (should show "Running" status)
2. Check the logs for errors
3. Verify environment variables are set correctly

### API Errors

1. Verify your API keys are correctly set in Secrets
2. Check the backend logs for detailed error messages
3. Ensure API keys have proper permissions

### CORS Errors

- The CORS configuration has been updated to allow Hugging Face Spaces domains
- If you still see CORS errors, check the browser console for specific issues

## Updating Your Space

To update your deployed app:

```bash
# Make changes to your code
git add .
git commit -m "Description of changes"
git push
```

Hugging Face will automatically rebuild and redeploy your Space.

## Performance Tips

1. **API Keys**: Make sure all API keys are valid to get full functionality
2. **Cold Starts**: First load might be slow; subsequent loads will be faster
3. **Resource Limits**: Free Spaces have resource limits; consider upgrading for heavy usage

## Cost Considerations

- Hugging Face Spaces: Free tier available with limitations
- OpenRouter API: Pay per use (required for AI agents)
- OpenWeather API: Free tier available (up to 60 calls/min)
- OpenRouteService API: Free tier available (up to 2000 requests/day)

## Support

If you encounter issues:

1. Check Hugging Face Spaces documentation: https://huggingface.co/docs/hub/spaces
2. Review your Space's logs
3. Open an issue on your project repository

## Next Steps

After successful deployment:

1. Share your Space URL with others
2. Add a demo video/gif to your README
3. Consider adding example scenarios
4. Monitor usage and performance
5. Gather feedback and iterate

Enjoy your deployed AI Supply Chain Optimizer on Hugging Face Spaces!
