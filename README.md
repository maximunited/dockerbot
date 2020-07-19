# DockerBot

DockerBot is a [Telepot](https://telepot.readthedocs.io/en/latest/) powered, easy to use Telegram bot written in python that runs as Docker Container.
With DockerBot you can:
- List existing containers (and get status).
- Start, Stop and Restart containers.
- Run SpeedTest.
- Get memory Status (Used, Free, etc.)
- Get disk usage
- Get server time
- Get server public (External) IP
- Get server uptime


#### Credits:
=======

- [Tomer Klein](https://github.com/t0mer)
- [Adam Russak](https://github.com/AdamRussak)


## Usage
### Run from hub

#### docker-compose from hub
```yaml
version: "3.7"

services:
  dockerbot:
    image: techblog/dockerbot
    container_name: dockerbot
    security_opt:
      - no-new-privileges
    restart: always
    environment:
      - API_KEY=  #Required
      - ALLOWED_IDS= #Required
    volumes:
       - /var/run/docker.sock:/var/run/docker.sock
```
Alternatively to using API_KEY and ALLOWED_IDS, one can supply API_KEY_FILE and ALLOWED_IDS_FILE for easier usage using [Docker secrets](https://docs.docker.com/engine/swarm/secrets/)
#### docker-compose using secrets
```yaml
version: "3.7"

services:
  dockerbot:
    image: techblog/dockerbot
    container_name: dockerbot
    security_opt:
      - no-new-privileges
    restart: always
    environment:
      - API_KEY_FILE=/run/secrets/dockerbot_api_key
      - ALLOWED_IDS_FILE=/run/secrets/dockerbot_allowed_ids
    secrets:
      - dockerbot_allowed_ids
      - dockerbot_api_key
    volumes:
       - /var/run/docker.sock:/var/run/docker.sock
secrets:
  dockerbot_allowed_ids:
    file: ${SECRETSDIR}/dockerbot_allowed_ids
  dockerbot_api_key:
    file: ${SECRETSDIR}/dockerbot_api_key
```

Replace API_KEY with your bot token. One can create a token
using the instruction in Step 2 in the following article:
[TelePi – Control your pi with Telegram Bot](https://en.techblog.co.il/2018/08/11/telepi-control-your-pi-with-telegram-bot/) 

In order to secure the bot and block unwanted calls from Unauthorized users add your allowd ID's with comma separated values into ALLOWED_IDS
environmet. In order to get your id use [@myidbot](https://t.me/myidbot) in telegram and send the /getid command. The answer is your ID:

[![Get your ID](https://github.com/t0mer/dockerbot/raw/master/screenshots/Idbot.PNG "Get your ID")](https://github.com/t0mer/dockerbot/raw/master/screenshots/Idbot.PNG "Get your ID")

# Screenshots

[![Get Containers List](https://github.com/t0mer/dockerbot/raw/master/screenshots/dockerbot_get_containers_list.PNG "Device Listing")](https://github.com/t0mer/dockerbot/raw/master/screenshots/dockerbot_get_containers_list.PNG "Device Listing")

[![Show Disk Info](https://github.com/t0mer/dockerbot/raw/master/screenshots/dockerbot_get_disk_info.PNG "Show Disk Info")](https://github.com/t0mer/dockerbot/raw/master/screenshots/dockerbot_get_disk_info.PNG "Show Disk Info")

[![Run Speed Test](https://github.com/t0mer/dockerbot/raw/master/screenshots/dockerbot_speedtest.PNG "Run Speed Test")](https://github.com/t0mer/dockerbot/raw/master/screenshots/dockerbot_speedtest.PNG "Run Speed Test")
