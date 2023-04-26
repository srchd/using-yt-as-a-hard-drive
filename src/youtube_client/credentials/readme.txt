1. Go to https://console.cloud.google.com/
2. Create a new project (selector in top left corner, then click New project)
3. Give it a name and Create
4. Go to https://console.cloud.google.com/apis/credentials and make sure your project is selected in the top left
5. Click Configure consent screen
6. User Type: External
7. Create
8. Give an app a name and your email address as a support email and as the developer contact information
9. Save and continue
10. Click Add or remove scopes
11. Add the following urls to the "Manually add scopes" section:
    https://www.googleapis.com/auth/youtube
    https://www.googleapis.com/auth/youtube.channel-memberships.creator
    https://www.googleapis.com/auth/youtube.force-ssl
    https://www.googleapis.com/auth/youtube.readonly
    https://www.googleapis.com/auth/youtube.upload
    https://www.googleapis.com/auth/youtubepartner
    https://www.googleapis.com/auth/youtubepartner-channel-audit
12. Click update
13. Click Save and continue
14. Click Add Users
15. Enter your email address and press Add
16. Click Save and continue
17. Go back to https://console.cloud.google.com/apis/credentials
18. Click Create credentials
19. OAuth client ID
20. Application type: Desktop app, give it a name and press Create
21. Download JSON
22. Put this JSON file into the credentials folder and name it "credentials.json"