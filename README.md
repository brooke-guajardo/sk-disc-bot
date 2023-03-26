Fun project of converting Space King's improv tabletop rule set into discord bot form. No affiliation, just a way to learn discord API. [License](misc/LICENSE)

TODO:
1. Add support for python slash commands
2. Add auto-complete support
3. Refactor SQL queries and updates - potentially move away from sqlite
4. Clean docker wipe

## Build the docker image
```
make build
```

Image must exist for the start command to work. Assumes you have docker daemon running with the image 'discord_bot'

Hint: this image name is whatever you put as ``` -t string ``` in the build section of the [Makefile](https://github.com/brooke-guajardo/sk-bot.py/blob/3a6bb36629c3038687ead40af6e13d729bf0cd0c/Makefile#L15)

## Running the bot with docker
```
make start
```

Need to copy (cp) the secret.json file that has your token like:
```
{
"token": "your-token-here"
}
```

docker cp command:
```
docker cp /local/path/to/secret.json discord-bot-discord-1:/usr/src/app/secret.json
```

Docker container has to exist for cp command to work. After the cp command is ran just rerun ```make start``` 

**Please remember to never include the token in any commits**

## Debug
Run this after reruning ```make start``` after the cp command. 
```
docker logs -t -n 20 discord-bot-discord-1
```
Replace ``` discord-bot-discord-1 ``` with your *container* name. ```-t``` provides timestamps. ```-n 20``` limits the logs to 20 lines max.
If you gucci, you'll see a message like
```discord.client: logging in using static token```
Means the bot successfully went online.

If you want to look at the logs that the bot is generating from running. Look into the dicord.log file that's within the container
```
docker exec -it discord-bot-discord-1 tail /usr/src/app/discord.log
```
This will print out the end of the file. If you want to try ```less``` instead of tail to make the output interactive remember that ```crtl+c``` will kill the bot. ```ctrl+p ctrl+q``` is to exit the sessin without killing the bot.
