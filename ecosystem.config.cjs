module.exports = {
  apps: [
    {
      name: 'music-generator',
      script: 'python3',
      args: 'admin_app.py',
      env: {
        FLASK_ENV: 'development',
        PORT: 5000,
        // API keys should be set in .env file or environment variables
        // SUNO_API_KEY: 'your-suno-api-key-here',
        // GEMINI_API_KEY: 'your-gemini-api-key-here',
        GEMINI_MODEL: 'gemini-2.5-flash',
        // YOUTUBE_API_KEY: 'your-youtube-api-key-here',
        // YOUTUBE_CLIENT_ID: 'your-youtube-client-id-here',
        // YOUTUBE_CLIENT_SECRET: 'your-youtube-client-secret-here',
        // YOUTUBE_CHANNEL_ID: 'your-youtube-channel-id-here'
      },
      env_file: '.env',
      watch: false,
      instances: 1,
      exec_mode: 'fork',
      autorestart: true,
      max_restarts: 5,
      min_uptime: '10s'
    }
  ]
}