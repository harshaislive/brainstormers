# Deployment Troubleshooting

## Coolify Deployment Issues

### Issue 1: `pip: command not found`
**Solution:** Use Dockerfile build method in Coolify instead of nixpacks.

### Issue 2: `Could not find version crewai==0.165.1` + Python version conflicts

**Root cause:** CrewAI version conflicts with Python versions in deployment environment.

**Solutions (try in order):**

### 1. Use Simple Dockerfile (Recommended)
Replace your Dockerfile with `Dockerfile.simple` content - installs latest compatible versions without strict pinning.

### 2. Use Flexible Requirements  
Use `requirements-simple.txt` instead:
```bash
# In Coolify build settings:
pip install -r requirements-simple.txt
```

### 3. Updated Python Version
All configs now use Python 3.11 (CrewAI compatible).

### 4. Manual Docker build
```bash
docker build -f Dockerfile.simple -t brainstormers .
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