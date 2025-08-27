# Deployment Troubleshooting

## Coolify Deployment Issues

### Issue: `pip: command not found`

**Solutions (try in order):**

### 1. Use Dockerfile instead of nixpacks
In Coolify, change build method to "Dockerfile" instead of nixpacks.

### 2. Update nixpacks configuration
Use the updated `nixpacks.toml` that includes pip package explicitly.

### 3. Use Python buildpack
Set these environment variables in Coolify:
```
NIXPACKS_BUILD_CMD=python -m pip install -r requirements.txt
NIXPACKS_START_CMD=python app.py
```

### 4. Manual Docker build
```bash
docker build -t brainstormers .
docker run -p 8000:8000 brainstormers
```

## Required Environment Variables

Set these in Coolify:
```
AZURE_OPENAI_API_KEY=your_key_here
AZURE_API_BASE=https://your-resource.cognitiveservices.azure.com/
AZURE_API_VERSION=2024-08-01-preview  
AZURE_MODEL_NAME=gpt-5-chat
```

## Alternative: Railway/Render
If Coolify continues having issues, try:
- Railway.app (better nixpacks support)
- Render.com (excellent Python support)
- Vercel (for simpler deployments)