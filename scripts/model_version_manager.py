#!/usr/bin/env python3
"""
Model Version Manager for CI/CD Pipeline
Handles model versioning, updates, and rollbacks
"""

import os
import sys
import json
import shutil
import hashlib
import pickle
from datetime import datetime
from pathlib import Path
import sqlite3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModelVersionManager:
    def __init__(self, models_dir="models", backup_dir="model_backups"):
        self.models_dir = Path(models_dir)
        self.backup_dir = Path(backup_dir)
        self.db_path = "model_versions.db"
        
        # Create directories if they don't exist
        self.models_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        
        # Initialize database
        self.init_database()
        
    def init_database(self):
        """Initialize the model version database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version_tag TEXT UNIQUE NOT NULL,
                model_files TEXT NOT NULL,
                checksums TEXT NOT NULL,
                performance_metrics TEXT,
                deployment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT FALSE,
                description TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Model version database initialized")
        
    def calculate_file_checksum(self, file_path):
        """Calculate SHA256 checksum of a file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
        
    def get_model_files_info(self):
        """Get information about current model files"""
        model_files = {}
        checksums = {}
        
        # Define model file patterns
        model_patterns = [
            "LR_Pipeline.pickle",
            "BestModel.h5",
            "tokenizer.pickle"
        ]
        
        for pattern in model_patterns:
            file_path = Path(pattern)
            if file_path.exists():
                model_files[pattern] = {
                    'size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    'path': str(file_path.absolute())
                }
                checksums[pattern] = self.calculate_file_checksum(file_path)
                
        return model_files, checksums
        
    def create_version(self, version_tag, description=""):
        """Create a new model version"""
        logger.info(f"Creating new model version: {version_tag}")
        
        try:
            # Get current model files info
            model_files, checksums = self.get_model_files_info()
            
            if not model_files:
                raise ValueError("No model files found to version")
                
            # Create backup of current models
            backup_path = self.backup_dir / f"version_{version_tag}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            backup_path.mkdir(exist_ok=True)
            
            # Copy model files to backup
            for filename in model_files.keys():
                src = Path(filename)
                dst = backup_path / filename
                shutil.copy2(src, dst)
                logger.info(f"Backed up {filename} to {dst}")
                
            # Store version information in database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO model_versions (version_tag, model_files, checksums, description)
                VALUES (?, ?, ?, ?)
            ''', (
                version_tag,
                json.dumps(model_files),
                json.dumps(checksums),
                description
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Version {version_tag} created successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create version {version_tag}: {str(e)}")
            return False
            
    def deploy_version(self, version_tag):
        """Deploy a specific model version"""
        logger.info(f"Deploying model version: {version_tag}")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get version information
            cursor.execute('SELECT * FROM model_versions WHERE version_tag = ?', (version_tag,))
            version_info = cursor.fetchone()
            
            if not version_info:
                raise ValueError(f"Version {version_tag} not found")
                
            # Deactivate all current versions
            cursor.execute('UPDATE model_versions SET is_active = FALSE')
            
            # Activate the target version
            cursor.execute('UPDATE model_versions SET is_active = TRUE WHERE version_tag = ?', (version_tag,))
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Version {version_tag} deployed successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to deploy version {version_tag}: {str(e)}")
            return False
            
    def rollback_to_version(self, version_tag):
        """Rollback to a previous model version"""
        logger.info(f"Rolling back to version: {version_tag}")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get version information
            cursor.execute('SELECT * FROM model_versions WHERE version_tag = ?', (version_tag,))
            version_info = cursor.fetchone()
            
            if not version_info:
                raise ValueError(f"Version {version_tag} not found")
                
            # Find backup directory for this version
            backup_dirs = [d for d in self.backup_dir.iterdir() if f"version_{version_tag}_" in d.name]
            
            if not backup_dirs:
                raise ValueError(f"No backup found for version {version_tag}")
                
            # Use the most recent backup
            backup_path = max(backup_dirs, key=lambda x: x.stat().st_mtime)
            
            # Restore model files from backup
            for model_file in backup_path.iterdir():
                if model_file.is_file():
                    dst = Path(model_file.name)
                    shutil.copy2(model_file, dst)
                    logger.info(f"Restored {model_file.name} from backup")
                    
            # Update database to mark this version as active
            cursor.execute('UPDATE model_versions SET is_active = FALSE')
            cursor.execute('UPDATE model_versions SET is_active = TRUE WHERE version_tag = ?', (version_tag,))
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Successfully rolled back to version {version_tag}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to rollback to version {version_tag}: {str(e)}")
            return False
            
    def list_versions(self):
        """List all available model versions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM model_versions ORDER BY deployment_date DESC')
        versions = cursor.fetchall()
        
        conn.close()
        
        print("📋 Available Model Versions")
        print("=" * 60)
        
        for version in versions:
            status = "🟢 ACTIVE" if version[6] else "⚪ INACTIVE"
            print(f"{status} {version[1]} - {version[5]}")
            if version[7]:  # description
                print(f"   Description: {version[7]}")
            print()
            
    def get_current_version(self):
        """Get the currently active model version"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT version_tag FROM model_versions WHERE is_active = TRUE')
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return result[0]
        else:
            return None
            
    def validate_version_integrity(self, version_tag):
        """Validate that a version's files haven't been corrupted"""
        logger.info(f"Validating integrity of version: {version_tag}")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get version information
            cursor.execute('SELECT checksums FROM model_versions WHERE version_tag = ?', (version_tag,))
            result = cursor.fetchone()
            
            if not result:
                raise ValueError(f"Version {version_tag} not found")
                
            stored_checksums = json.loads(result[0])
            current_checksums = {}
            
            # Calculate current checksums
            for filename in stored_checksums.keys():
                if Path(filename).exists():
                    current_checksums[filename] = self.calculate_file_checksum(filename)
                    
            # Compare checksums
            integrity_ok = True
            for filename, stored_checksum in stored_checksums.items():
                if filename in current_checksums:
                    if stored_checksum != current_checksums[filename]:
                        logger.warning(f"Checksum mismatch for {filename}")
                        integrity_ok = False
                else:
                    logger.warning(f"File {filename} not found")
                    integrity_ok = False
                    
            conn.close()
            
            if integrity_ok:
                logger.info(f"✅ Version {version_tag} integrity validated successfully")
            else:
                logger.warning(f"⚠️  Version {version_tag} integrity check failed")
                
            return integrity_ok
            
        except Exception as e:
            logger.error(f"❌ Failed to validate version {version_tag}: {str(e)}")
            return False
            
    def cleanup_old_versions(self, keep_versions=5):
        """Clean up old model versions, keeping only the specified number"""
        logger.info(f"Cleaning up old versions, keeping {keep_versions}")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get old versions (excluding active one)
            cursor.execute('''
                SELECT id, version_tag FROM model_versions 
                WHERE is_active = FALSE 
                ORDER BY deployment_date DESC
            ''')
            old_versions = cursor.fetchall()
            
            # Keep only the most recent versions
            if len(old_versions) > keep_versions:
                versions_to_delete = old_versions[keep_versions:]
                
                for version_id, version_tag in versions_to_delete:
                    # Delete from database
                    cursor.execute('DELETE FROM model_versions WHERE id = ?', (version_id,))
                    
                    # Delete backup directory
                    backup_dirs = [d for d in self.backup_dir.iterdir() if f"version_{version_tag}_" in d.name]
                    for backup_dir in backup_dirs:
                        shutil.rmtree(backup_dir)
                        logger.info(f"Deleted backup for version {version_tag}")
                        
                conn.commit()
                logger.info(f"✅ Cleaned up {len(versions_to_delete)} old versions")
                
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Failed to cleanup old versions: {str(e)}")

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Model Version Manager")
    parser.add_argument('action', choices=['create', 'deploy', 'rollback', 'list', 'current', 'validate', 'cleanup'])
    parser.add_argument('--version', help='Version tag for create/deploy/rollback actions')
    parser.add_argument('--description', help='Description for new version')
    parser.add_argument('--keep', type=int, default=5, help='Number of versions to keep during cleanup')
    
    args = parser.parse_args()
    
    manager = ModelVersionManager()
    
    if args.action == 'create':
        if not args.version:
            print("❌ Version tag required for create action")
            sys.exit(1)
        success = manager.create_version(args.version, args.description or "")
        sys.exit(0 if success else 1)
        
    elif args.action == 'deploy':
        if not args.version:
            print("❌ Version tag required for deploy action")
            sys.exit(1)
        success = manager.deploy_version(args.version)
        sys.exit(0 if success else 1)
        
    elif args.action == 'rollback':
        if not args.version:
            print("❌ Version tag required for rollback action")
            sys.exit(1)
        success = manager.rollback_to_version(args.version)
        sys.exit(0 if success else 1)
        
    elif args.action == 'list':
        manager.list_versions()
        
    elif args.action == 'current':
        current = manager.get_current_version()
        if current:
            print(f"🟢 Current active version: {current}")
        else:
            print("❌ No active version found")
            
    elif args.action == 'validate':
        if not args.version:
            print("❌ Version tag required for validate action")
            sys.exit(1)
        success = manager.validate_version_integrity(args.version)
        sys.exit(0 if success else 1)
        
    elif args.action == 'cleanup':
        manager.cleanup_old_versions(args.keep)

if __name__ == "__main__":
    main()
