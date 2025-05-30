# music-box-py

Save your [top listened to artists](https://www.last.fm/user/bernardolm/library/artists) 👩‍🎤 on [last.fm](https://www.last.fm/user/bernardolm) to a [gist](https://gist.github.com/bernardolm/9132eb72fc69193d357cd87a68058cd2) and pin 📌 it to your [profile](https://github.com/bernardolm) 🎵.

This code was heavily inspired by [@jacc](https://github.com/jacc) repo [github.com/jacc/music-box](https://github.com/jacc/music-box) 🙏.

## env config

You need to create some project action secrets and variables before runnig the action.

You can create a local _.env_ file to help debug with these same envs.

| env name | required | env type | default value |
| :--- | :---: | :---: | :--- |
| `GH_GIST_ID` | **yes** | variable | |
| `GH_TOKEN` | **yes** | secret | |
| `LASTFM_API_KEY` | **yes** | secret | |
| `LASTFM_USERNAME` | **yes** | variable | |
| `BAR_EMPTY_SYMBOL` | no | variable | ⣀ |
| `BAR_FILLED_SYMBOL` | no | variable | ⣿ |
| `BAR_WIDTH` | no | variable | 20 |
| `DEBUG` | no | variable | False |
| `HEADER_DECORATION` | no | variable | - |
| `LASTFM_API_URL` | no | variable | http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&format=json |
| `LASTFM_LIMIT` | no | variable | 10 |
| `LASTFM_PERIOD` | no | variable | 7day |
| `LINES_WIDTH` | no | variable | 51 |
| `PLAYS_PREFIX` | no | variable | |
| `PLAYS_SUFIX` | no | variable | |
| `PLAYS_WIDTH` | no | variable | 4 |
| `SPACES_WIDTH` | no | variable | 1 |
