#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger les modèles sociaux et créer les tables
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def create_social_tables():
    """Créer les tables pour les modèles sociaux"""
    print("🔧 Création des tables pour les modèles sociaux...")
    
    try:
        # Créer les tables manuellement
        with connection.cursor() as cursor:
            # Table CommunityGroup
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users_communitygroup (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    group_type VARCHAR(20) NOT NULL DEFAULT 'community',
                    privacy_level VARCHAR(10) NOT NULL DEFAULT 'public',
                    quartier_id INTEGER NOT NULL,
                    creator_id INTEGER NOT NULL,
                    cover_image VARCHAR(100),
                    profile_image VARCHAR(100),
                    member_count INTEGER NOT NULL DEFAULT 0,
                    post_count INTEGER NOT NULL DEFAULT 0,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN NOT NULL DEFAULT 1,
                    FOREIGN KEY (quartier_id) REFERENCES geography_quartier (id),
                    FOREIGN KEY (creator_id) REFERENCES users_user (id)
                )
            """)
            
            # Table GroupMembership
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users_groupmembership (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    status VARCHAR(20) NOT NULL DEFAULT 'pending',
                    role VARCHAR(20) NOT NULL DEFAULT 'member',
                    joined_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(group_id, user_id),
                    FOREIGN KEY (group_id) REFERENCES users_communitygroup (id),
                    FOREIGN KEY (user_id) REFERENCES users_user (id)
                )
            """)
            
            # Table CommunityEvent
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users_communityevent (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(200) NOT NULL,
                    description TEXT NOT NULL,
                    event_type VARCHAR(20) NOT NULL DEFAULT 'meeting',
                    status VARCHAR(20) NOT NULL DEFAULT 'draft',
                    start_date DATETIME NOT NULL,
                    end_date DATETIME NOT NULL,
                    quartier_id INTEGER NOT NULL,
                    location_details VARCHAR(500),
                    organizer_id INTEGER NOT NULL,
                    group_id INTEGER,
                    cover_image VARCHAR(100),
                    attendee_count INTEGER NOT NULL DEFAULT 0,
                    max_attendees INTEGER,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    is_public BOOLEAN NOT NULL DEFAULT 1,
                    FOREIGN KEY (quartier_id) REFERENCES geography_quartier (id),
                    FOREIGN KEY (organizer_id) REFERENCES users_user (id),
                    FOREIGN KEY (group_id) REFERENCES users_communitygroup (id)
                )
            """)
            
            # Table EventAttendance
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users_eventattendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    status VARCHAR(20) NOT NULL DEFAULT 'going',
                    joined_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(event_id, user_id),
                    FOREIGN KEY (event_id) REFERENCES users_communityevent (id),
                    FOREIGN KEY (user_id) REFERENCES users_user (id)
                )
            """)
            
            # Table UserAchievement
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users_userachievement (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    achievement_type VARCHAR(30) NOT NULL,
                    title VARCHAR(100) NOT NULL,
                    description TEXT NOT NULL,
                    icon VARCHAR(10) NOT NULL,
                    points INTEGER NOT NULL DEFAULT 0,
                    unlocked_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, achievement_type),
                    FOREIGN KEY (user_id) REFERENCES users_user (id)
                )
            """)
            
            # Table UserSocialScore
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users_usersocialscore (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL UNIQUE,
                    total_points INTEGER NOT NULL DEFAULT 0,
                    level INTEGER NOT NULL DEFAULT 1,
                    achievements_count INTEGER NOT NULL DEFAULT 0,
                    posts_count INTEGER NOT NULL DEFAULT 0,
                    friends_count INTEGER NOT NULL DEFAULT 0,
                    groups_count INTEGER NOT NULL DEFAULT 0,
                    events_count INTEGER NOT NULL DEFAULT 0,
                    likes_received INTEGER NOT NULL DEFAULT 0,
                    comments_received INTEGER NOT NULL DEFAULT 0,
                    last_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users_user (id)
                )
            """)
            
            # Table de liaison pour les admins de groupes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users_communitygroup_admins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    communitygroup_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    UNIQUE(communitygroup_id, user_id),
                    FOREIGN KEY (communitygroup_id) REFERENCES users_communitygroup (id),
                    FOREIGN KEY (user_id) REFERENCES users_user (id)
                )
            """)
            
            print("✅ Tables créées avec succès!")
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Démarrage création des tables sociales...")
    success = create_social_tables()
    if success:
        print("✅ Tables sociales créées avec succès!")
    else:
        print("❌ Échec de la création des tables sociales.") 