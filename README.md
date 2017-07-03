# AutoSignin

SMZDM 签到

## Run as docker ##
```bash
docker run -d --name asi --restart=always -e SMZDM_USER_NAME='username1,username2' -e SMZDM_USER_PASSWD='password1,password2' uuaing/autosignin
```
