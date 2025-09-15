module.exports = {
  apps: [
    {
      name: 'webapp',
      script: 'python3',
      args: 'admin_app.py',
      env: {
        FLASK_ENV: 'development',
        PORT: 3000,
        // API keys loaded from .env file for security
        GEMINI_MODEL: 'gemini-2.5-flash',
        IDEOGRAM_RENDERING_SPEED: 'STANDARD',
        IDEOGRAM_STYLE_TYPE: 'GENERAL'
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