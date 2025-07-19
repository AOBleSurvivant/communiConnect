#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from django.contrib.auth import get_user_model
from geography.models import Quartier
from posts.models import Post, Media, PostComment, PostLike
from django.utils import timezone

User = get_user_model()

def create_test_users():
    """Créer des utilisateurs de test"""
    quartiers = list(Quartier.objects.all()[:5])  # Prendre les 5 premiers quartiers
    
    test_users = [
        {
            'username': 'mariam_diallo',
            'email': 'mariam.diallo@test.gn',
            'password': 'test123456',
            'first_name': 'Mariam',
            'last_name': 'Diallo',
            'quartier': quartiers[0] if quartiers else None
        },
        {
            'username': 'ahmed_sylla',
            'email': 'ahmed.sylla@test.gn',
            'password': 'test123456',
            'first_name': 'Ahmed',
            'last_name': 'Sylla',
            'quartier': quartiers[1] if len(quartiers) > 1 else quartiers[0]
        },
        {
            'username': 'fatou_toure',
            'email': 'fatou.toure@test.gn',
            'password': 'test123456',
            'first_name': 'Fatou',
            'last_name': 'Touré',
            'quartier': quartiers[2] if len(quartiers) > 2 else quartiers[0]
        },
        {
            'username': 'moussa_camara',
            'email': 'moussa.camara@test.gn',
            'password': 'test123456',
            'first_name': 'Moussa',
            'last_name': 'Camara',
            'quartier': quartiers[3] if len(quartiers) > 3 else quartiers[0]
        }
    ]
    
    created_users = []
    for user_data in test_users:
        if not User.objects.filter(username=user_data['username']).exists():
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                quartier=user_data['quartier']
            )
            created_users.append(user)
            print(f"Utilisateur créé: {user.username} ({user.first_name} {user.last_name})")
        else:
            user = User.objects.get(username=user_data['username'])
            created_users.append(user)
            print(f"Utilisateur existant: {user.username}")
    
    return created_users

def create_test_posts(users):
    """Créer des posts de test"""
    if not users:
        print("Aucun utilisateur disponible pour créer des posts")
        return
    
    test_posts = [
        {
            'content': 'Bonjour à tous ! Je suis ravie de rejoindre cette communauté locale. J\'espère pouvoir contribuer positivement à notre quartier.',
            'post_type': 'info',
            'author': users[0]
        },
        {
            'content': 'Quelqu\'un connaît-il un bon mécanicien dans le quartier ? Ma voiture a un problème et j\'ai besoin d\'aide.',
            'post_type': 'help',
            'author': users[1]
        },
        {
            'content': 'Rappel : Réunion du comité de quartier ce samedi à 15h à la place du marché. Venez nombreux !',
            'post_type': 'event',
            'author': users[2]
        },
        {
            'content': 'Nouvelle initiative : Création d\'un groupe d\'entraide pour les personnes âgées. Si vous êtes intéressés, contactez-moi.',
            'post_type': 'announcement',
            'author': users[3]
        },
        {
            'content': 'Que pensez-vous de l\'idée d\'organiser une fête de quartier pour célébrer notre communauté ?',
            'post_type': 'discussion',
            'author': users[0]
        }
    ]
    
    created_posts = []
    for i, post_data in enumerate(test_posts):
        # Créer le post avec une date différente pour chaque post
        post = Post.objects.create(
            author=post_data['author'],
            quartier=post_data['author'].quartier,
            content=post_data['content'],
            post_type=post_data['post_type'],
            created_at=timezone.now() - timedelta(days=i+1)  # Posts sur plusieurs jours
        )
        created_posts.append(post)
        print(f"Post créé: {post.content[:50]}... par {post.author.username}")
    
    return created_posts

def create_test_comments(posts, users):
    """Créer des commentaires de test"""
    if not posts or not users:
        return
    
    test_comments = [
        "Bienvenue dans la communauté !",
        "Je peux vous aider avec ça.",
        "Excellente idée !",
        "Je serai là !",
        "Merci pour l'information.",
        "C'est une très bonne initiative.",
        "Je suis d'accord avec vous.",
        "Comment puis-je participer ?"
    ]
    
    for post in posts:
        # Ajouter 2-3 commentaires par post
        num_comments = random.randint(2, 3)
        for i in range(num_comments):
            comment_author = random.choice(users)
            comment_content = random.choice(test_comments)
            
            PostComment.objects.create(
                post=post,
                author=comment_author,
                content=comment_content
            )
            print(f"Commentaire ajouté sur le post de {post.author.username}: {comment_content[:30]}...")

def create_test_likes(posts, users):
    """Créer des likes de test"""
    if not posts or not users:
        return
    
    for post in posts:
        # 2-4 utilisateurs likent chaque post
        num_likes = random.randint(2, 4)
        likers = random.sample(users, min(num_likes, len(users)))
        
        for liker in likers:
            if not PostLike.objects.filter(post=post, user=liker).exists():
                PostLike.objects.create(post=post, user=liker)
                post.increment_likes()
                print(f"Like ajouté par {liker.username} sur le post de {post.author.username}")

def main():
    print("=== Création des données de test ===")
    
    # Vérifier qu'il y a des quartiers
    if not Quartier.objects.exists():
        print("Aucun quartier trouvé. Veuillez d'abord importer les données géographiques.")
        return
    
    print(f"Quartiers disponibles: {Quartier.objects.count()}")
    
    # Créer les utilisateurs de test
    users = create_test_users()
    
    # Créer les posts de test
    posts = create_test_posts(users)
    
    # Créer les commentaires de test
    create_test_comments(posts, users)
    
    # Créer les likes de test
    create_test_likes(posts, users)
    
    print("\n=== Données de test créées avec succès ===")
    print(f"Utilisateurs: {len(users)}")
    print(f"Posts: {len(posts)}")
    print(f"Commentaires: {PostComment.objects.count()}")
    print(f"Likes: {PostLike.objects.count()}")
    
    print("\n=== Informations de connexion ===")
    print("Super utilisateur:")
    print("  Username: admin")
    print("  Password: admin123456")
    print("\nUtilisateurs de test:")
    for user in users:
        print(f"  {user.username} / test123456")

if __name__ == '__main__':
    main() 