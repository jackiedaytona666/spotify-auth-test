// Build the Spotify OAuth authorization URL with required parameters
const params = new URLSearchParams({
  client_id: "801cfb401a964dfd89360c06f2c7303a",
  response_type: "token",
  redirect_uri: "https://jackiedaytona666.github.io/spotify-auth-test/callback.html",
  scope: "user-top-read"
});

// Assign the generated URL to the auth button's href
link.href = `https://accounts.spotify.com/authorize?${params.toString()}`;
