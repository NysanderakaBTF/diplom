from datetime import datetime
from app.services.post_service import PostService
from app.services.social.instagram import publish_to_instagram
from app.services.social.pinterest import publish_to_pinterest
from app.services.social.facebook import publish_to_facebook
from app.services.social.vk import publish_to_vk

def main():
    posts = PostService.get_unpublished_posts()
    for post in posts:
        try:
            images = PostService.get_post_images(post.id)
            user_id = post.author_id  # User ID from the Post table
            # Publish to social networks
            publish_to_instagram(user_id, post.text, images)
            publish_to_pinterest(user_id, post.text, images)
            publish_to_facebook(user_id, post.text, images)
            publish_to_vk(user_id, post.text, images)
            # Mark post as published
            PostService.mark_post_as_published(post.id)
        except Exception as e:
            print(f"Error publishing post {post.id}: {e}")
            PostService.mark_post_as_error(post.id)

if __name__ == "__main__":
    main()