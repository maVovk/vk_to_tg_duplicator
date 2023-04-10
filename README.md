# vk_to_tg_duplicator
Automatically duplicate your posts from VK to Telegram channel

![](https://i.ibb.co/FxY2p1c/vk-post.jpg)

Automatically copies all photos, videos are provided as links to VK video(example https://vk.com/video227594082_456241827). Also, if the author is mentioned in VK post, link to his profile will be added to Telegram message. All posts that are marked as advertisiment won't be posted in Telegram(can be changed)
## Setup
1. `git clone https://github.com/maVovk/vk_to_tg_duplicator.git`
2. Set all token variables in `.env` file. Instructions on how to get all tokens are given there.
3. Make bot an administrator in Telegram channel
4. <b>For debug</b>
`pip install -r requirements.txt`
`python main.py`
<b>For production</b>
`docker build -t vk_to_tg .`
`docker run vk_to_tg`

## .env variables
### VK_ACCESS_TOKEN
Go to https://vkhost.github.io/. Then click on VK Admin and follow the instructions.

![](https://i.ibb.co/yfRgSFd/image.png)

Your acces token will be in the url between access_token and &expires_in
### VK_GROUP_TOKEN
Open your community, then Manage->API usage

![](https://i.ibb.co/zNJ1bVY/image.png)
![](https://i.ibb.co/mNz4wSm/image.png)

Enable LongPoll API and turn on notifications about new posts in Event types

![](https://i.ibb.co/HF5xxdg/image.png)
![](https://i.ibb.co/bB2pMkB/image.png)

Now create access token for your group, allow access to community's wall and copy token to .env file

![](https://i.ibb.co/ryWhBc7/image.png)
![](https://i.ibb.co/9cRmq8k/image.png)

###  VK_GROUP_ID_TOKEN
Go to https://regvk.com/id/, enter link to the group, click the button and copy public ID

![](https://i.ibb.co/5xN2z3j/image.png)
### TELEGRAM_TOKEN
Create your own bot via @BotFather, then copy access token

![](https://i.ibb.co/J55zfZQ/image.png)
Go to your channel and add your bot as an administrator

![](https://i.ibb.co/7pgh1dx/image.png)

### TELEGRAM_CHANNEL_ID
Forward any post from your channel to @JsonDumpBot, find `forward_from_chat` field and copy id to `.env` file

![](https://i.ibb.co/W5bbL8y/image.png)

If you need Telegram to Vk duplicator check here -> https://github.com/VeryBigSad/telegram_to_vk
