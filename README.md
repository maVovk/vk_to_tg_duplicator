# vk_to_tg_duplicator
Automatically duplicate your posts from VK to Telegram channel

![](https://i.ibb.co/FxY2p1c/vk-post.jpg)

Automatically copies all photos, videos are provided as links to VK video(example https://vk.com/video227594082_456241827). Also, if the author is mentioned in VK post, link to his profile will be added to Telegram message. All posts that are marked as advertisiment won't be posted in Telegram(can be changed)
## Setup
1. `git clone https://github.com/maVovk/vk_to_tg_duplicator.git`
2. Set all token variables in `.env` file. Instructions on how to get all tokens are given there.
3. <b>For debug</b>
`pip install -r requirements.txt`
`python main.py`
<b>For production</b>
`docker build -t vk_to_tg .`
`docker run vk_to_tg`

If you need Telegram to Vk duplicator check here -> https://github.com/VeryBigSad/telegram_to_vk
