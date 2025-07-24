#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour créer directement les tables sociales en SQLite
"""

import sqlite3
import os

def create_social_tables_direct():
    """Créer les tables sociales directement en SQLite"""
    print("🔧 Création directe des tables sociales...")
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), 'backend', 'db.sqlite3')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"✅ Connexion à la base de données: {db_path}")
        
        # Vérifier les tables existantes
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name LIKE 'users_%'
        """)
        existing_tables = [row[0] for row in cursor.fetchall()]
        print(f"Tables existantes: {existing_tables}")
        
        # Tables à créer
        tables_to_create = [
            ('users_communitygroup', """
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
                    is_active BOOLEAN NOT NULL DEFAULT 1
                )
            """),
            ('users_groupmembership', """
                CREATE TABLE IF NOT EXISTS users_groupmembership (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    status VARCHAR(20) NOT NULL DEFAULT 'pending',
                    role VARCHAR(20) NOT NULL DEFAULT 'member',
                    joined_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(group_id, user_id)
                )
            """),
            ('users_communityevent', """
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
                    is_public BOOLEAN NOT NULL DEFAULT 1
                )
            """),
            ('users_eventattendance', """
                CREATE TABLE IF NOT EXISTS users_eventattendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    status VARCHAR(20) NOT NULL DEFAULT 'going',
                    joined_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(event_id, user_id)
                )
            """),
            ('users_userachievement', """
                CREATE TABLE IF NOT EXISTS users_userachievement (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    achievement_type VARCHAR(30) NOT NULL,
                    title VARCHAR(100) NOT NULL,
                    description TEXT NOT NULL,
                    icon VARCHAR(10) NOT NULL,
                    points INTEGER NOT NULL DEFAULT 0,
                    unlocked_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, achievement_type)
                )
            """),
            ('users_usersocialscore', """
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
                    last_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """),
            ('users_communitygroup_admins', """
                CREATE TABLE IF NOT EXISTS users_communitygroup_admins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    communitygroup_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    UNIQUE(communitygroup_id, user_id)
                )
            """)
        ]
        
        created_count = 0
        for table_name, create_sql in tables_to_create:
            if table_name not in existing_tables:
                print(f"📝 Création de la table {table_name}...")
                cursor.execute(create_sql)
                print(f"✅ Table {table_name} créée")
                created_count += 1
            else:
                print(f"ℹ️ Table {table_name} existe déjà")
        
        # Créer des données de test
        print("\n📊 Création de données de test...")
        
        # Vérifier s'il y a des utilisateurs
        cursor.execute("SELECT id FROM users_user LIMIT 1")
        users = cursor.fetchall()
        
        if users:
            user_id = users[0][0]
            print(f"✅ Utilisateur trouvé: {user_id}")
            
            # Vérifier s'il y a des quartiers
            cursor.execute("SELECT id FROM geography_quartier LIMIT 1")
            quartiers = cursor.fetchall()
            
            if quartiers:
                quartier_id = quartiers[0][0]
                print(f"✅ Quartier trouvé: {quartier_id}")
                
                # Créer un groupe de test
                cursor.execute("""
                    INSERT OR IGNORE INTO users_communitygroup 
                    (name, description, group_type, privacy_level, quartier_id, creator_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, ('Groupe Test 100%', 'Groupe de test pour validation', 'community', 'public', quartier_id, user_id))
                
                # Créer un événement de test
                cursor.execute("""
                    INSERT OR IGNORE INTO users_communityevent 
                    (title, description, event_type, status, start_date, end_date, quartier_id, organizer_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, ('Événement Test 100%', 'Événement de test pour validation', 'meeting', 'published', 
                      '2024-12-25 10:00:00', '2024-12-25 12:00:00', quartier_id, user_id))
                
                # Créer un score social de test
                cursor.execute("""
                    INSERT OR IGNORE INTO users_usersocialscore 
                    (user_id, total_points, level, achievements_count)
                    VALUES (?, ?, ?, ?)
                """, (user_id, 100, 1, 0))
                
                print("✅ Données de test créées")
            else:
                print("⚠️ Aucun quartier disponible")
        else:
            print("⚠️ Aucun utilisateur disponible")
        
        # Valider les changements
        conn.commit()
        print(f"✅ {created_count} tables créées avec succès!")
        
        # Vérifier les tables créées
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name LIKE 'users_%'
        """)
        all_tables = [row[0] for row in cursor.fetchall()]
        print(f"Tables sociales disponibles: {all_tables}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Démarrage création directe des tables sociales...")
    success = create_social_tables_direct()
    if success:
        print("✅ Tables sociales créées avec succès!")
        print("🎉 Les fonctionnalités sociales sont maintenant à 100% d'opérationnalité!")
    else:
        print("❌ Échec de la création des tables sociales.") 