Fun project of converting Space King's improv tabletop rule set into discord bot form. No affiliation, just a way to learn discord API.

TODO:
1. Add support for python slash commands
2. Add auto-complete support
3. Refactor SQL queries and updates - potentially move away from sqlite

## Build the docker image
```
make build
```

Imagine must exist for the start command to work. Assumes you have docker daemon running with the image 'discord'

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

Docker container has to exist for cp command to work

**Please remember to never include the token in any commits**
