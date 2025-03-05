from datetime import datetime, timedelta
from app.database import get_db, Post, Image, Token


class PostService:
    @staticmethod
    def get_unpublished_posts():
        with get_db() as db:
            current_time = datetime.now()
            posts = db.query(Post).where(
                Post.pub_datetime <= current_time,
                Post.pub_datetime >= current_time - timedelta(minutes=15),
                Post.status == 0
            ).all()
            return posts

    @staticmethod
    def get_post_images(post_id):
        with get_db() as db:
            images = db.query(Image).filter(Image.post_id == post_id).all()
            return images

    @staticmethod
    def mark_post_as_published(post_id):
        with get_db() as db:
            post = db.query(Post).filter(Post.id == post_id).first()
            if post:
                post.status = 1  # Mark as published
                db.commit()
                db.refresh(post)
            return post

    @staticmethod
    def mark_post_as_error(post_id):
        with get_db() as db:
            post = db.query(Post).filter(Post.id == post_id).first()
            if post:
                post.status = 2  # Mark as error
                db.commit()
                db.refresh(post)
            return post

    @staticmethod
    def get_user_token(user_id, platform):
        with get_db() as db:
            token = db.query(Token).filter(
                Token.c.user_id == user_id,
                Token.c.platform == platform
            ).first()
            return token