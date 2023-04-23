
from facebook import GraphAPI
from instagrapi import Client
from requests import get

from Config import Config

# Configura le tue credenziali
#! FACEBOOK_ACCESS_TOKEN = 'your_facebook_access_token'
#! INSTAGRAM_USERNAME = 'your_instagram_username'
#! INSTAGRAM_PASSWORD = 'your_instagram_password'

# Inizializza gli oggetti delle API
graph = GraphAPI(access_token=Config.FB_ACCESS_TOKEN)
instagram = Client()
instagram.login(Config.INSTA_USERNAME, Config.INSTA_USERNAME)


def get_recent_marketplace_posts(user_id):
    posts = graph.get_connections(user_id, 'feed')
    marketplace_posts = []
    for post in posts['data']:
        if post.get('message') and ('Per altre informazioni' in post['message']):
            marketplace_posts.append(post)
    return marketplace_posts


def already_shared(post_id):
    # Controlla se il post è già stato condiviso su Instagram
    # Puoi memorizzare gli ID dei post condivisi in un file o in un database
    with open('shared_posts.txt', 'r') as file:
        shared_posts = file.read().splitlines()
    return post_id in shared_posts


def mark_as_shared(post_id):
    # Memorizza l'ID del post come condiviso
    with open('shared_posts.txt', 'a') as file:
        file.write(post_id + '\n')


def post_to_instagram(title, description, price, image_url):
    # Scarica l'immagine sul tuo dispositivo
    image_data = get(image_url).content
    with open('image.jpg', 'wb') as file:
        file.write(image_data)

    # Posta l'immagine su Instagram
    instagram.photo_upload(
        'image.jpg', f'{title}\n\n{description}\n\nPrice: {price}')


def main():
    user_id = graph.get_object('me')['id']
    recent_posts = get_recent_marketplace_posts(user_id)
    print(recent_posts)
    # while True:
    #     user_id = graph.get_object('me')['id']
    #     recent_posts = get_recent_marketplace_posts(user_id)

    #     for post in recent_posts:
    #         if not already_shared(post['id']):
    #             title = post['marketplace_listing']['title']
    #             description = post['marketplace_listing']['description']
    #             price = post['marketplace_listing']['price']
    #             image_url = post['marketplace_listing']['images'][0]['source']

    #             post_to_instagram(title, description, price, image_url)
    #             mark_as_shared(post['id'])

    #     # Attendi un po' prima di controllare nuovamente i post
    #     time.sleep(60 * 10)  # Controlla ogni 10 minuti


if __name__ == '__main__':
    main()
