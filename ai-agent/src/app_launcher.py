"""
App Launcher Module

Handles launching and managing applications on mobile devices.
Provides advanced features like smart suggestions, app switching, and task management.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum


class AppCategory(Enum):
    """Categories of mobile applications"""
    SOCIAL = "social"
    PRODUCTIVITY = "productivity"
    ENTERTAINMENT = "entertainment"
    COMMUNICATION = "communication"
    UTILITY = "utility"
    PHOTOGRAPHY = "photography"
    SHOPPING = "shopping"
    HEALTH = "health"
    NAVIGATION = "navigation"
    OTHER = "other"


class AppLauncher:
    """
    Advanced app launcher with smart features and context awareness.
    """

    def __init__(self):
        """Initialize the app launcher"""
        self.logger = logging.getLogger("AppLauncher")
        self.installed_apps: Dict[str, Dict] = {}
        self.app_usage_stats: Dict[str, Dict] = {}
        self.recent_apps: List[str] = []
        self.favorites: List[str] = []
        self._initialize_app_database()

    def _initialize_app_database(self) -> None:
        """Initialize database of known apps"""
        # Common app database (in production, scan installed apps)
        self.installed_apps = {
            "gmail": {
                "name": "Gmail",
                "package": "com.google.android.gm",
                "category": AppCategory.COMMUNICATION,
                "icon": "gmail_icon"
            },
            "chrome": {
                "name": "Chrome",
                "package": "com.android.chrome",
                "category": AppCategory.PRODUCTIVITY,
                "icon": "chrome_icon"
            },
            "camera": {
                "name": "Camera",
                "package": "com.android.camera",
                "category": AppCategory.PHOTOGRAPHY,
                "icon": "camera_icon"
            },
            "spotify": {
                "name": "Spotify",
                "package": "com.spotify.music",
                "category": AppCategory.ENTERTAINMENT,
                "icon": "spotify_icon"
            },
            "maps": {
                "name": "Google Maps",
                "package": "com.google.android.apps.maps",
                "category": AppCategory.NAVIGATION,
                "icon": "maps_icon"
            },
            "whatsapp": {
                "name": "WhatsApp",
                "package": "com.whatsapp",
                "category": AppCategory.COMMUNICATION,
                "icon": "whatsapp_icon"
            },
            "instagram": {
                "name": "Instagram",
                "package": "com.instagram.android",
                "category": AppCategory.SOCIAL,
                "icon": "instagram_icon"
            },
            "slack": {
                "name": "Slack",
                "package": "com.slack",
                "category": AppCategory.PRODUCTIVITY,
                "icon": "slack_icon"
            }
        }

    def launch(self, app_identifier: str, parameters: Optional[Dict] = None) -> Dict:
        """
        Launch an application with optional parameters.

        Args:
            app_identifier: App name or package name
            parameters: Optional launch parameters (deep links, actions, etc.)

        Returns:
            Launch result dictionary
        """
        # Normalize app identifier
        app_key = app_identifier.lower().strip()

        # Find app in database
        app_info = self._find_app(app_key)

        if not app_info:
            return {
                "success": False,
                "error": f"App '{app_identifier}' not found",
                "suggestions": self._get_similar_apps(app_key)
            }

        # Update usage statistics
        self._update_usage_stats(app_key)

        # Add to recent apps
        self._add_to_recent(app_key)

        # In production, this would use Android Intent or iOS URL schemes
        self.logger.info(f"Launching {app_info['name']} ({app_info['package']})")

        result = {
            "success": True,
            "app_name": app_info["name"],
            "package": app_info["package"],
            "category": app_info["category"].value,
            "timestamp": datetime.now().isoformat(),
            "message": f"Successfully launched {app_info['name']}"
        }

        # Handle deep linking if parameters provided
        if parameters:
            result["deep_link"] = self._create_deep_link(app_info, parameters)

        return result

    def _find_app(self, app_identifier: str) -> Optional[Dict]:
        """
        Find app by identifier (name or package).

        Args:
            app_identifier: App name or package

        Returns:
            App info dictionary or None
        """
        # Check direct match
        if app_identifier in self.installed_apps:
            return self.installed_apps[app_identifier]

        # Check by display name
        for key, app in self.installed_apps.items():
            if app["name"].lower() == app_identifier:
                return app

        # Check partial matches
        for key, app in self.installed_apps.items():
            if app_identifier in app["name"].lower() or app_identifier in key:
                return app

        return None

    def _get_similar_apps(self, app_identifier: str) -> List[str]:
        """
        Get suggestions for similar apps.

        Args:
            app_identifier: Search term

        Returns:
            List of similar app names
        """
        suggestions = []

        for key, app in self.installed_apps.items():
            # Simple similarity check
            if (app_identifier in key or 
                app_identifier in app["name"].lower() or
                self._calculate_similarity(app_identifier, key) > 0.5):
                suggestions.append(app["name"])

        return suggestions[:5]

    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """
        Calculate simple string similarity.

        Args:
            str1: First string
            str2: Second string

        Returns:
            Similarity score (0-1)
        """
        # Simple Jaccard similarity
        set1 = set(str1.lower())
        set2 = set(str2.lower())

        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        return intersection / union if union > 0 else 0

    def _update_usage_stats(self, app_key: str) -> None:
        """
        Update usage statistics for an app.

        Args:
            app_key: App identifier
        """
        if app_key not in self.app_usage_stats:
            self.app_usage_stats[app_key] = {
                "launch_count": 0,
                "last_used": None,
                "total_time": 0
            }

        stats = self.app_usage_stats[app_key]
        stats["launch_count"] += 1
        stats["last_used"] = datetime.now().isoformat()

    def _add_to_recent(self, app_key: str) -> None:
        """
        Add app to recent apps list.

        Args:
            app_key: App identifier
        """
        # Remove if already in list
        if app_key in self.recent_apps:
            self.recent_apps.remove(app_key)

        # Add to front
        self.recent_apps.insert(0, app_key)

        # Keep only last 20
        self.recent_apps = self.recent_apps[:20]

    def _create_deep_link(self, app_info: Dict, parameters: Dict) -> str:
        """
        Create deep link for app with parameters.

        Args:
            app_info: App information
            parameters: Deep link parameters

        Returns:
            Deep link URL
        """
        # In production, create actual deep links
        return f"{app_info['package']}://action?{parameters}"

    def get_smart_suggestions(self, context: Optional[Dict] = None) -> List[Dict]:
        """
        Get smart app suggestions based on context.

        Args:
            context: Context information (time, location, activity, etc.)

        Returns:
            List of suggested apps with reasons
        """
        suggestions = []

        # Time-based suggestions
        hour = datetime.now().hour
        
        if 6 <= hour < 9:
            # Morning suggestions
            suggestions.extend([
                {"app": "gmail", "reason": "Check morning emails"},
                {"app": "chrome", "reason": "Read news"},
            ])
        elif 9 <= hour < 17:
            # Work hours
            suggestions.extend([
                {"app": "slack", "reason": "Work communication"},
                {"app": "gmail", "reason": "Check emails"},
            ])
        elif 17 <= hour < 22:
            # Evening suggestions
            suggestions.extend([
                {"app": "spotify", "reason": "Evening music"},
                {"app": "instagram", "reason": "Social time"},
            ])

        # Add frequently used apps
        frequent_apps = self._get_frequent_apps()
        for app_key in frequent_apps[:3]:
            if app_key in self.installed_apps:
                suggestions.append({
                    "app": app_key,
                    "reason": "Frequently used"
                })

        # Context-based suggestions
        if context:
            if context.get("activity") == "driving":
                suggestions.append({
                    "app": "maps",
                    "reason": "Navigation while driving"
                })
            if context.get("location") == "gym":
                suggestions.append({
                    "app": "spotify",
                    "reason": "Workout music"
                })

        return suggestions[:5]

    def _get_frequent_apps(self) -> List[str]:
        """
        Get list of frequently used apps.

        Returns:
            List of app keys sorted by frequency
        """
        sorted_apps = sorted(
            self.app_usage_stats.items(),
            key=lambda x: x[1]["launch_count"],
            reverse=True
        )
        return [app[0] for app in sorted_apps]

    def get_recent_apps(self) -> List[Dict]:
        """
        Get recently used apps.

        Returns:
            List of recent apps with info
        """
        recent = []
        for app_key in self.recent_apps:
            if app_key in self.installed_apps:
                recent.append({
                    "key": app_key,
                    "name": self.installed_apps[app_key]["name"],
                    "category": self.installed_apps[app_key]["category"].value
                })
        return recent

    def switch_to_recent(self, index: int = 0) -> Dict:
        """
        Switch to a recent app by index.

        Args:
            index: Index in recent apps list

        Returns:
            Launch result
        """
        if index >= len(self.recent_apps):
            return {
                "success": False,
                "error": "Invalid recent app index"
            }

        app_key = self.recent_apps[index]
        return self.launch(app_key)

    def add_to_favorites(self, app_identifier: str) -> bool:
        """
        Add app to favorites.

        Args:
            app_identifier: App to add

        Returns:
            Success status
        """
        app_key = app_identifier.lower().strip()
        app_info = self._find_app(app_key)

        if app_info and app_key not in self.favorites:
            self.favorites.append(app_key)
            return True
        return False

    def get_favorites(self) -> List[Dict]:
        """
        Get favorite apps.

        Returns:
            List of favorite apps
        """
        favorites = []
        for app_key in self.favorites:
            if app_key in self.installed_apps:
                favorites.append({
                    "key": app_key,
                    "name": self.installed_apps[app_key]["name"],
                    "category": self.installed_apps[app_key]["category"].value
                })
        return favorites

    def get_apps_by_category(self, category: AppCategory) -> List[Dict]:
        """
        Get all apps in a category.

        Args:
            category: App category

        Returns:
            List of apps in category
        """
        apps = []
        for key, app in self.installed_apps.items():
            if app["category"] == category:
                apps.append({
                    "key": key,
                    "name": app["name"],
                    "package": app["package"]
                })
        return apps


if __name__ == "__main__":
    # Example usage
    launcher = AppLauncher()
    
    # Launch an app
    result = launcher.launch("gmail")
    print(f"Launch result: {result}")
    
    # Get smart suggestions
    suggestions = launcher.get_smart_suggestions()
    print(f"Smart suggestions: {suggestions}")
    
    # Get recent apps
    recent = launcher.get_recent_apps()
    print(f"Recent apps: {recent}")
