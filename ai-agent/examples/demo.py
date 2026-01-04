#!/usr/bin/env python3
"""
Mobile AI Agent Demo Script

This script demonstrates the capabilities of the mobile AI agent.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from ai_agent_core import AIAgentCore
from app_launcher import AppLauncher


def print_separator():
    print("\n" + "="*70)


def print_header(title):
    print_separator()
    print(f"  {title}")
    print_separator()


def demo_basic_commands():
    """Demonstrate basic command processing"""
    print_header("DEMO 1: Basic App Launching")
    
    agent = AIAgentCore()
    
    commands = [
        "Open Gmail",
        "Launch camera",
        "Start Spotify"
    ]
    
    for cmd in commands:
        print(f"\n🎤 Command: \"{cmd}\"")
        result = agent.process_command(cmd)
        if result["success"]:
            print(f"✅ {result['message']}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")


def demo_intent_detection():
    """Demonstrate intent detection"""
    print_header("DEMO 2: Intent Detection")
    
    agent = AIAgentCore()
    
    test_commands = [
        ("Open Gmail", "App Launch"),
        ("Enable WiFi", "System Control"),
        ("When I arrive home, turn on WiFi", "Automation"),
        ("What's the weather today?", "Query")
    ]
    
    for cmd, expected_type in test_commands:
        print(f"\n🎤 Command: \"{cmd}\"")
        intent = agent._analyze_intent(cmd)
        print(f"📊 Detected Intent: {intent.value}")
        print(f"📝 Expected Type: {expected_type}")


def demo_smart_suggestions():
    """Demonstrate smart suggestions"""
    print_header("DEMO 3: Smart App Suggestions")
    
    launcher = AppLauncher()
    
    # Simulate usage
    print("\n📱 Simulating app usage...")
    launcher.launch("gmail")
    launcher.launch("spotify")
    launcher.launch("camera")
    
    print("\n🤖 Getting smart suggestions based on context...")
    suggestions = launcher.get_smart_suggestions()
    
    print("\n💡 Suggested apps:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"   {i}. {suggestion['app']} - {suggestion['reason']}")


def demo_learning():
    """Demonstrate learning capabilities"""
    print_header("DEMO 4: Learning from Usage Patterns")
    
    agent = AIAgentCore()
    
    print("\n📚 Simulating command history...")
    commands = [
        "Open Gmail",
        "Open Gmail",
        "Open Gmail",
        "Launch camera",
        "Launch camera",
        "Start Spotify"
    ]
    
    for cmd in commands:
        agent.process_command(cmd)
    
    print(f"\n📊 Commands processed: {len(agent.command_history)}")
    
    print("\n🧠 Learning patterns from usage...")
    patterns = agent.learn_from_patterns()
    
    print("\n📈 Most frequent commands:")
    for cmd, count in patterns["frequent_commands"][:5]:
        print(f"   • \"{cmd}\" - used {count} times")
    
    print("\n💭 Smart suggestions based on learning:")
    suggestions = agent.get_suggestions()
    for i, suggestion in enumerate(suggestions[:5], 1):
        print(f"   {i}. {suggestion}")


def demo_app_categories():
    """Demonstrate app categories"""
    print_header("DEMO 5: App Categories and Organization")
    
    launcher = AppLauncher()
    
    from app_launcher import AppCategory
    
    categories = [
        AppCategory.COMMUNICATION,
        AppCategory.ENTERTAINMENT,
        AppCategory.PRODUCTIVITY
    ]
    
    for category in categories:
        apps = launcher.get_apps_by_category(category)
        print(f"\n📂 {category.value.upper()} apps:")
        for app in apps:
            print(f"   • {app['name']}")


def demo_favorites():
    """Demonstrate favorites functionality"""
    print_header("DEMO 6: Favorites Management")
    
    launcher = AppLauncher()
    
    print("\n⭐ Adding apps to favorites...")
    favorites_to_add = ["gmail", "spotify", "camera"]
    
    for app in favorites_to_add:
        success = launcher.add_to_favorites(app)
        if success:
            print(f"   ✓ Added {app} to favorites")
    
    print("\n❤️  Your favorite apps:")
    favorites = launcher.get_favorites()
    for i, fav in enumerate(favorites, 1):
        print(f"   {i}. {fav['name']} ({fav['category']})")


def demo_recent_apps():
    """Demonstrate recent apps tracking"""
    print_header("DEMO 7: Recent Apps Tracking")
    
    launcher = AppLauncher()
    
    print("\n🕒 Launching several apps...")
    apps_to_launch = ["gmail", "spotify", "camera", "maps", "instagram"]
    
    for app in apps_to_launch:
        result = launcher.launch(app)
        print(f"   ✓ Launched {result['app_name']}")
    
    print("\n📜 Recently used apps:")
    recent = launcher.get_recent_apps()
    for i, app in enumerate(recent[:5], 1):
        print(f"   {i}. {app['name']} ({app['category']})")


def demo_automation_examples():
    """Show automation command examples"""
    print_header("DEMO 8: Automation Examples")
    
    print("\n🤖 Automation commands you can create:")
    
    examples = [
        ("Time-Based", "Every morning at 7 AM, read my calendar and weather"),
        ("Location-Based", "When I arrive at work, silence my phone and open Slack"),
        ("Condition-Based", "If battery is below 20%, enable power saving mode"),
        ("Activity-Based", "When I start driving, open Maps and play music"),
        ("Multi-Action", "At bedtime, enable Do Not Disturb, set alarm, and turn off WiFi")
    ]
    
    for category, example in examples:
        print(f"\n📋 {category}:")
        print(f"   💬 \"{example}\"")


def main():
    """Run all demos"""
    print("\n")
    print("█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + " " * 15 + "MOBILE AI AGENT DEMONSTRATION" + " " * 24 + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    try:
        demo_basic_commands()
        demo_intent_detection()
        demo_smart_suggestions()
        demo_learning()
        demo_app_categories()
        demo_favorites()
        demo_recent_apps()
        demo_automation_examples()
        
        print_separator()
        print("\n✨ Demo completed successfully!")
        print("\n📚 For more information, see:")
        print("   • AI_AGENT.md - Full documentation")
        print("   • ai-agent/README.md - Quick start guide")
        print("   • ai-agent/docs/ARCHITECTURE.md - Technical details")
        print("   • ai-agent/examples/usage_examples.md - Code examples")
        print_separator()
        print()
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
