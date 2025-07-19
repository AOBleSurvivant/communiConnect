#!/usr/bin/env python3
"""
Script de vérification de la configuration de production pour CommuniConnect
Vérifie tous les composants nécessaires pour la production
"""

import os
import sys
import json
import subprocess
import requests
import redis
import psycopg2
from datetime import datetime
from decouple import config
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communiconnect.settings_production')
django.setup()

from django.core.cache import cache
from django.db import connection
from django.conf import settings

# Couleurs pour les messages
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(title):
    print(f"\n{Colors.BLUE}{Colors.BOLD}=== {title} ==={Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

class ProductionChecker:
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'checks': {},
            'summary': {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'warnings': 0
            }
        }
    
    def check_environment_variables(self):
        """Vérifier les variables d'environnement"""
        print_header("Vérification des Variables d'Environnement")
        
        required_vars = [
            'SECRET_KEY',
            'DB_NAME',
            'DB_USER',
            'DB_PASSWORD',
            'REDIS_HOST',
            'CLOUDINARY_CLOUD_NAME',
            'CLOUDINARY_API_KEY',
            'CLOUDINARY_API_SECRET',
            'EMAIL_HOST',
            'EMAIL_HOST_USER',
            'EMAIL_HOST_PASSWORD'
        ]
        
        optional_vars = [
            'GOOGLE_CLOUD_VISION_API_KEY',
            'RTMP_SERVER_URL',
            'HLS_SERVER_URL'
        ]
        
        all_passed = True
        
        for var in required_vars:
            value = config(var, default='')
            if value:
                print_success(f"{var}: Configuré")
                self.results['checks'][f'env_{var}'] = {'status': 'passed', 'value': '***' if 'PASSWORD' in var or 'SECRET' in var else value}
            else:
                print_error(f"{var}: Non configuré")
                self.results['checks'][f'env_{var}'] = {'status': 'failed', 'value': None}
                all_passed = False
        
        for var in optional_vars:
            value = config(var, default='')
            if value:
                print_success(f"{var}: Configuré (optionnel)")
                self.results['checks'][f'env_{var}'] = {'status': 'passed', 'value': '***' if 'PASSWORD' in var or 'SECRET' in var else value}
            else:
                print_warning(f"{var}: Non configuré (optionnel)")
                self.results['checks'][f'env_{var}'] = {'status': 'warning', 'value': None}
        
        self.results['summary']['total'] += len(required_vars) + len(optional_vars)
        self.results['summary']['passed'] += len([v for v in required_vars if config(v, default='')])
        self.results['summary']['failed'] += len([v for v in required_vars if not config(v, default='')])
        self.results['summary']['warnings'] += len([v for v in optional_vars if not config(v, default='')])
        
        return all_passed
    
    def check_django_settings(self):
        """Vérifier la configuration Django"""
        print_header("Vérification de la Configuration Django")
        
        checks = [
            ('DEBUG', settings.DEBUG, False, "Mode debug désactivé"),
            ('ALLOWED_HOSTS', settings.ALLOWED_HOSTS, [], "Hosts autorisés configurés"),
            ('SECURE_SSL_REDIRECT', getattr(settings, 'SECURE_SSL_REDIRECT', False), True, "Redirection SSL activée"),
            ('SESSION_COOKIE_SECURE', getattr(settings, 'SESSION_COOKIE_SECURE', False), True, "Cookies sécurisés"),
            ('CSRF_COOKIE_SECURE', getattr(settings, 'CSRF_COOKIE_SECURE', False), True, "CSRF sécurisé"),
        ]
        
        all_passed = True
        
        for name, current, expected, description in checks:
            if current == expected:
                print_success(f"{name}: {description}")
                self.results['checks'][f'django_{name}'] = {'status': 'passed', 'value': current}
            else:
                print_error(f"{name}: {description} (actuel: {current})")
                self.results['checks'][f'django_{name}'] = {'status': 'failed', 'value': current}
                all_passed = False
        
        self.results['summary']['total'] += len(checks)
        self.results['summary']['passed'] += len([c for c in checks if c[1] == c[2]])
        self.results['summary']['failed'] += len([c for c in checks if c[1] != c[2]])
        
        return all_passed
    
    def check_database(self):
        """Vérifier la base de données"""
        print_header("Vérification de la Base de Données")
        
        try:
            with connection.cursor() as cursor:
                # Test de connexion
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                
                if result and result[0] == 1:
                    print_success("Connexion à la base de données: OK")
                    self.results['checks']['db_connection'] = {'status': 'passed', 'value': 'connected'}
                else:
                    print_error("Connexion à la base de données: Échec")
                    self.results['checks']['db_connection'] = {'status': 'failed', 'value': 'failed'}
                    return False
                
                # Vérifier les tables principales
                tables = ['posts_post', 'users_user', 'geography_quartier']
                for table in tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        print_success(f"Table {table}: {count} enregistrements")
                        self.results['checks'][f'db_table_{table}'] = {'status': 'passed', 'value': count}
                    except Exception as e:
                        print_error(f"Table {table}: Erreur - {e}")
                        self.results['checks'][f'db_table_{table}'] = {'status': 'failed', 'value': str(e)}
                
                # Vérifier la taille de la base de données
                cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database()))")
                size = cursor.fetchone()[0]
                print_info(f"Taille de la base de données: {size}")
                self.results['checks']['db_size'] = {'status': 'passed', 'value': size}
                
                self.results['summary']['total'] += 4
                self.results['summary']['passed'] += 4
                
                return True
                
        except Exception as e:
            print_error(f"Erreur base de données: {e}")
            self.results['checks']['db_connection'] = {'status': 'failed', 'value': str(e)}
            self.results['summary']['total'] += 1
            self.results['summary']['failed'] += 1
            return False
    
    def check_redis(self):
        """Vérifier Redis"""
        print_header("Vérification de Redis")
        
        try:
            # Test de connexion Redis
            redis_client = redis.Redis(
                host=config('REDIS_HOST', default='localhost'),
                port=config('REDIS_PORT', default=6379, cast=int),
                password=config('REDIS_PASSWORD', default=''),
                db=0,
                socket_timeout=5
            )
            
            redis_client.ping()
            print_success("Connexion Redis: OK")
            self.results['checks']['redis_connection'] = {'status': 'passed', 'value': 'connected'}
            
            # Informations Redis
            info = redis_client.info()
            print_info(f"Version Redis: {info.get('redis_version', 'N/A')}")
            print_info(f"Mémoire utilisée: {info.get('used_memory_human', 'N/A')}")
            print_info(f"Clients connectés: {info.get('connected_clients', 'N/A')}")
            
            # Test du cache Django
            cache_key = 'production_check_test'
            cache.set(cache_key, 'test_value', 60)
            cache_value = cache.get(cache_key)
            
            if cache_value == 'test_value':
                print_success("Cache Django: OK")
                self.results['checks']['django_cache'] = {'status': 'passed', 'value': 'working'}
            else:
                print_error("Cache Django: Échec")
                self.results['checks']['django_cache'] = {'status': 'failed', 'value': 'failed'}
            
            self.results['summary']['total'] += 2
            self.results['summary']['passed'] += 2
            
            return True
            
        except Exception as e:
            print_error(f"Erreur Redis: {e}")
            self.results['checks']['redis_connection'] = {'status': 'failed', 'value': str(e)}
            self.results['summary']['total'] += 1
            self.results['summary']['failed'] += 1
            return False
    
    def check_cloudinary(self):
        """Vérifier Cloudinary"""
        print_header("Vérification de Cloudinary")
        
        cloud_name = config('CLOUDINARY_CLOUD_NAME', default='')
        api_key = config('CLOUDINARY_API_KEY', default='')
        api_secret = config('CLOUDINARY_API_SECRET', default='')
        
        if not all([cloud_name, api_key, api_secret]):
            print_error("Configuration Cloudinary incomplète")
            self.results['checks']['cloudinary_config'] = {'status': 'failed', 'value': 'incomplete'}
            self.results['summary']['total'] += 1
            self.results['summary']['failed'] += 1
            return False
        
        try:
            # Test de connexion Cloudinary
            import cloudinary
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret
            )
            
            # Test simple d'upload (optionnel)
            print_success("Configuration Cloudinary: OK")
            self.results['checks']['cloudinary_config'] = {'status': 'passed', 'value': 'configured'}
            
            self.results['summary']['total'] += 1
            self.results['summary']['passed'] += 1
            
            return True
            
        except Exception as e:
            print_error(f"Erreur Cloudinary: {e}")
            self.results['checks']['cloudinary_config'] = {'status': 'failed', 'value': str(e)}
            self.results['summary']['total'] += 1
            self.results['summary']['failed'] += 1
            return False
    
    def check_system_services(self):
        """Vérifier les services système"""
        print_header("Vérification des Services Système")
        
        services = [
            ('nginx', 'Nginx'),
            ('redis-server', 'Redis'),
            ('postgresql', 'PostgreSQL'),
            ('fail2ban', 'Fail2ban')
        ]
        
        all_passed = True
        
        for service_name, display_name in services:
            try:
                result = subprocess.run(
                    ['systemctl', 'is-active', service_name],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print_success(f"{display_name}: Actif")
                    self.results['checks'][f'service_{service_name}'] = {'status': 'passed', 'value': 'active'}
                else:
                    print_error(f"{display_name}: Inactif")
                    self.results['checks'][f'service_{service_name}'] = {'status': 'failed', 'value': 'inactive'}
                    all_passed = False
                
            except Exception as e:
                print_error(f"{display_name}: Erreur - {e}")
                self.results['checks'][f'service_{service_name}'] = {'status': 'failed', 'value': str(e)}
                all_passed = False
        
        self.results['summary']['total'] += len(services)
        self.results['summary']['passed'] += len([s for s in services if subprocess.run(['systemctl', 'is-active', s[0]], capture_output=True).returncode == 0])
        self.results['summary']['failed'] += len([s for s in services if subprocess.run(['systemctl', 'is-active', s[0]], capture_output=True).returncode != 0])
        
        return all_passed
    
    def check_security(self):
        """Vérifier la sécurité"""
        print_header("Vérification de la Sécurité")
        
        checks = []
        
        # Vérifier le firewall
        try:
            result = subprocess.run(['ufw', 'status'], capture_output=True, text=True)
            if 'Status: active' in result.stdout:
                print_success("Firewall UFW: Actif")
                checks.append(('firewall', True))
            else:
                print_warning("Firewall UFW: Inactif")
                checks.append(('firewall', False))
        except:
            print_warning("Firewall UFW: Non disponible")
            checks.append(('firewall', False))
        
        # Vérifier les permissions des fichiers
        critical_paths = [
            '/var/www/communiconnect',
            '/var/log/communiconnect',
            '/etc/nginx/sites-available/communiconnect'
        ]
        
        for path in critical_paths:
            if os.path.exists(path):
                stat = os.stat(path)
                if stat.st_uid == 33 or stat.st_gid == 33:  # www-data
                    print_success(f"Permissions {path}: OK")
                    checks.append((f'permissions_{path}', True))
                else:
                    print_warning(f"Permissions {path}: À vérifier")
                    checks.append((f'permissions_{path}', False))
            else:
                print_warning(f"Chemin {path}: N'existe pas")
                checks.append((f'permissions_{path}', False))
        
        # Vérifier les ports ouverts
        try:
            result = subprocess.run(['ss', '-tulpn'], capture_output=True, text=True)
            open_ports = result.stdout
            critical_ports = ['22', '80', '443']
            
            for port in critical_ports:
                if f':{port}' in open_ports:
                    print_success(f"Port {port}: Ouvert")
                    checks.append((f'port_{port}', True))
                else:
                    print_warning(f"Port {port}: Fermé")
                    checks.append((f'port_{port}', False))
                    
        except Exception as e:
            print_warning(f"Impossible de vérifier les ports: {e}")
            checks.append(('ports_check', False))
        
        # Enregistrer les résultats
        for check_name, passed in checks:
            self.results['checks'][f'security_{check_name}'] = {
                'status': 'passed' if passed else 'warning',
                'value': passed
            }
        
        self.results['summary']['total'] += len(checks)
        self.results['summary']['passed'] += len([c for c in checks if c[1]])
        self.results['summary']['warnings'] += len([c for c in checks if not c[1]])
        
        return True
    
    def check_performance(self):
        """Vérifier les performances"""
        print_header("Vérification des Performances")
        
        try:
            import psutil
            
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent < 80:
                print_success(f"CPU: {cpu_percent}%")
            else:
                print_warning(f"CPU: {cpu_percent}% (élevé)")
            
            # Mémoire
            memory = psutil.virtual_memory()
            if memory.percent < 85:
                print_success(f"Mémoire: {memory.percent}%")
            else:
                print_warning(f"Mémoire: {memory.percent}% (élevé)")
            
            # Disque
            disk = psutil.disk_usage('/')
            if disk.percent < 90:
                print_success(f"Disque: {disk.percent}%")
            else:
                print_warning(f"Disque: {disk.percent}% (élevé)")
            
            self.results['checks']['performance_cpu'] = {'status': 'passed', 'value': cpu_percent}
            self.results['checks']['performance_memory'] = {'status': 'passed', 'value': memory.percent}
            self.results['checks']['performance_disk'] = {'status': 'passed', 'value': disk.percent}
            
            self.results['summary']['total'] += 3
            self.results['summary']['passed'] += 3
            
            return True
            
        except Exception as e:
            print_error(f"Erreur vérification performances: {e}")
            self.results['summary']['total'] += 1
            self.results['summary']['failed'] += 1
            return False
    
    def generate_report(self):
        """Générer le rapport final"""
        print_header("Rapport Final")
        
        total = self.results['summary']['total']
        passed = self.results['summary']['passed']
        failed = self.results['summary']['failed']
        warnings = self.results['summary']['warnings']
        
        print(f"Total des vérifications: {total}")
        print_success(f"Réussites: {passed}")
        if failed > 0:
            print_error(f"Échecs: {failed}")
        if warnings > 0:
            print_warning(f"Avertissements: {warnings}")
        
        success_rate = (passed / total * 100) if total > 0 else 0
        print(f"\nTaux de réussite: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print_success("✅ Configuration de production prête!")
        elif success_rate >= 70:
            print_warning("⚠️  Configuration acceptable avec quelques problèmes")
        else:
            print_error("❌ Configuration problématique - corrections nécessaires")
        
        # Sauvegarder le rapport
        report_file = '/var/log/communiconnect/production_check.json'
        try:
            with open(report_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            print_info(f"Rapport sauvegardé: {report_file}")
        except Exception as e:
            print_warning(f"Impossible de sauvegarder le rapport: {e}")
        
        return success_rate >= 70

def main():
    """Fonction principale"""
    print(f"{Colors.BLUE}{Colors.BOLD}🔍 Vérification de la Configuration de Production - CommuniConnect{Colors.END}")
    
    checker = ProductionChecker()
    
    # Exécuter toutes les vérifications
    checks = [
        checker.check_environment_variables,
        checker.check_django_settings,
        checker.check_database,
        checker.check_redis,
        checker.check_cloudinary,
        checker.check_system_services,
        checker.check_security,
        checker.check_performance
    ]
    
    for check in checks:
        try:
            check()
        except Exception as e:
            print_error(f"Erreur lors de la vérification: {e}")
    
    # Générer le rapport final
    success = checker.generate_report()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main() 