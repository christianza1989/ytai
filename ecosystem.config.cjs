module.exports = {
  apps: [
    {
      name: 'music-generator',
      script: 'python3',
      args: 'admin_app.py',
      env: {
        FLASK_ENV: 'development',
        PORT: 5000
      },
      watch: false,
      instances: 1,
      exec_mode: 'fork',
      autorestart: true,
      max_restarts: 5,
      min_uptime: '10s'
    }
  ]
}