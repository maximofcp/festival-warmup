- Setup a local environment for python (3.12 compatible)
- Copy the .env.template to an .env file with command `cp .env.template .env`
- Run `make initial-setup` to setup everything. All dependencies and migrations will be installed from scratch
- Run `make tunnel` to start a new tunnel, so the local environment is temporarily open to the internet on port 8000.
  The tunnel must remain open to be able to authenticate the user, then it can be closed.
- Copy one of the hosts printed and also collect `CLIENT_ID` and `CLIENT_SECRET` from spotify webAPI. Paste those on
  the `.env` file, along with the tunnel host
- Run `make show-redirect-uri`, copy the URI and save it on spotify webAPI
- Run `make run` to start django server. Verify that admin login is possible with user `admin:admin`
- Run `make spotify-user` to sync your django user with spotify's user
- Run `make playlists` to create playlists!