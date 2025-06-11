from dataclasses import dataclass

import httpx

from app.users.auth.schemas import GoogleUserData
from app.settings import Settings


@dataclass
class GoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient()

    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = self._get_access_token(code=code)
        async with self.async_client as client:
            user_info = await client.get(url="https://www.googleapis.com/oauth2/v1/userinfo",
                                         headers={"Authorization": f"Bearer {access_token}"})
            user_data = user_info.json()
        return GoogleUserData(**user_data, access_token=access_token)

    async def _get_access_token(self, code: str) -> str:
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_SECRET_KEY,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        async with self.async_client as client:
            response = await client.post(self.settings.GOOGLE_TOKEN_URL, data=data)
            print(response.json())
        return response.json()['access_token']



