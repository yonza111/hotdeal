export const CLIENT_ID = '1219148050354802749';
export const REDIRECT_URI = 'http://127.0.0.1:3000/';
export const SCOPE = 'identify email';
export const DISCORD_AUTH_URL = `https://discord.com/api/oauth2/authorize?client_id=${CLIENT_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}&response_type=code&scope=${SCOPE}`