# DiscordBot

## Introduction
This is a discord bot. Using this program, users can interact with the bot to play music, to register for github score and to register for the challenge of the day.

Github score is calculeted from the day when you are registered to the current day.

Challenges are different every day. (you need to add them in the storageChallenge/storage.txt)

## Setup
Install python 3.x.

```pip install discord```

```pip install youtube_dl```

```pip install PyNaCl```

## Usage

Add the token in main.py (TOKEN) and then to run the computer program, you can use: ```python main.py```

## Commands

### Bot:

- ```!help``` It will show the all commands that this bot supports.

- ```!botlogout``` Logout bot

### Challenge of the day:

- ```!chcomplete``` Complete the challege for this day

- ```!chdeleteme``` Delete me from ChallengeScore

- ```!chregister``` Register for Challenge

- ```!chsave```     Save ChallengeScore

- ```!chshow```     Show the challenge for today

- ```!chsshow```    Show the scores of the people that are in challenge do

### GithubScore:

- ```!ghdeleteme``` Delete me from GithubScore

- ```!ghregister``` Register for GithubScore

- ```!ghsave```     Save GithubScore

- ```!ghshow```     Show the score of the people of the server on Github

### Music:

- ```!join```       Joins a voice channel

- ```!leave```      Disconnects the bot from voice and delete the playlist

- ```!play```       Play the queue

- ```!qadd```       Add song

- ```!qclear```     Clear songs

- ```!qremove```    Remove song

- ```!qshow```      Show songs

- ```!repeat```     Repeat songs (None or ->, Repeat1 or 1, RepeatQueue or l)

- ```skip```       Play next song
