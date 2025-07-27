# 🚀 Menu2Img Web Deployment Guide

This guide will help you deploy your Menu2Img web application to various hosting platforms.

## 📋 Prerequisites

1. **OpenAI API Key**: You'll need an OpenAI API key for the AI features
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Environment Variables**: You'll need to set up environment variables on your hosting platform

## 🌐 Hosting Options

### Option 1: Render (Recommended - Free & Easy)

**Render** is perfect for Flask apps and offers a generous free tier.

#### Step-by-Step Deployment:

1. **Sign up for Render**
   - Go to [render.com](https://render.com)
   - Sign up with your GitHub account

2. **Create a New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `menu2img` repository

3. **Configure the Service**
   - **Name**: `menu2img-web` (or any name you prefer)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn src.web.app_production:app`
   - **Plan**: Free (or choose a paid plan for more resources)

4. **Set Environment Variables**
   - Go to "Environment" tab
   - Add the following variables:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     UPLOAD_FOLDER=uploads
     OUTPUT_FOLDER=dishes
     HISTORY_FILE=upload_history.json
     ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy your app
   - Your app will be available at: `https://your-app-name.onrender.com`

### Option 2: Railway

**Railway** is another excellent option with a free tier.

#### Step-by-Step Deployment:

1. **Sign up for Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up with your GitHub account

2. **Deploy from GitHub**
   - Click "Deploy from GitHub repo"
   - Select your `menu2img` repository

3. **Configure Environment Variables**
   - Go to "Variables" tab
   - Add the same environment variables as above

4. **Deploy**
   - Railway will automatically detect it's a Python app
   - Your app will be deployed and available at the provided URL

### Option 3: Heroku

**Heroku** is a classic choice (requires credit card for verification).

#### Step-by-Step Deployment:

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Or download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set OPENAI_API_KEY=your_openai_api_key_here
   heroku config:set UPLOAD_FOLDER=uploads
   heroku config:set OUTPUT_FOLDER=dishes
   heroku config:set HISTORY_FILE=upload_history.json
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Open the App**
   ```bash
   heroku open
   ```

### Option 4: Vercel

**Vercel** is great for static sites but requires some configuration for Flask.

#### Step-by-Step Deployment:

1. **Create vercel.json**
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "src/web/app_production.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "src/web/app_production.py"
       }
     ]
   }
   ```

2. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Vercel will automatically deploy

## 🔧 Environment Variables

All hosting platforms require these environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-...` |
| `UPLOAD_FOLDER` | Folder for uploaded images | `uploads` |
| `OUTPUT_FOLDER` | Folder for generated images | `dishes` |
| `HISTORY_FILE` | File to store upload history | `upload_history.json` |

## 📁 File Structure for Deployment

Your repository should have this structure for deployment:

```
menu2img/
├── requirements.txt          # Python dependencies
├── Procfile                  # For Render/Heroku
├── runtime.txt              # Python version
├── src/
│   └── web/
│       ├── app_production.py # Production Flask app
│       └── templates/
│           └── index.html    # Web interface
└── README.md
```

## 🚨 Important Notes

### File Storage
- **Free tiers** typically have ephemeral storage (files are lost on restart)
- For persistent storage, consider:
  - **AWS S3** for file storage
  - **Cloudinary** for image hosting
  - **Paid hosting plans** with persistent storage

### API Limits
- **OpenAI API** has rate limits and costs
- Monitor your usage to avoid unexpected charges
- Consider implementing caching to reduce API calls

### Security
- Never commit your API keys to Git
- Use environment variables for all sensitive data
- Consider adding authentication for production use

## 🔍 Troubleshooting

### Common Issues:

1. **Build Failures**
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version is compatible

2. **Environment Variables**
   - Verify all required variables are set
   - Check variable names match exactly

3. **File Permissions**
   - Some platforms require specific file permissions
   - Check platform documentation

4. **Port Configuration**
   - Most platforms use `PORT` environment variable
   - The production app automatically detects this

## 📞 Support

If you encounter issues:

1. Check the platform's documentation
2. Review the deployment logs
3. Ensure all files are committed to Git
4. Verify environment variables are set correctly

## 🎉 Success!

Once deployed, your Menu2Img app will be available online and accessible to anyone with the URL!

**Example URLs:**
- Render: `https://menu2img.onrender.com`
- Railway: `https://menu2img-production.up.railway.app`
- Heroku: `https://your-app-name.herokuapp.com`
- Vercel: `https://your-app-name.vercel.app` 