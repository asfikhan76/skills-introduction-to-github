"""
Test suite for Mobile AI Agent

This file contains basic tests to demonstrate the AI agent functionality.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from ai_agent_core import AIAgentCore, CommandType, ProcessingMode
from app_launcher import AppLauncher, AppCategory


def test_agent_initialization():
    """Test that agent initializes correctly"""
    agent = AIAgentCore()
    assert agent is not None
    assert agent.config is not None
    assert agent.processing_mode == ProcessingMode.HYBRID
    print("✓ Agent initialization test passed")


def test_simple_app_launch():
    """Test basic app launching"""
    agent = AIAgentCore()
    result = agent.process_command("Open Gmail")
    
    assert result["success"] == True
    assert result["action"] == "launch_app"
    assert "Gmail" in result["message"]
    print(f"✓ Simple app launch test passed: {result}")


def test_multiple_commands():
    """Test processing multiple commands"""
    agent = AIAgentCore()
    
    commands = [
        "Open Gmail",
        "Launch camera",
        "Start Spotify",
        "Open Maps"
    ]
    
    for cmd in commands:
        result = agent.process_command(cmd)
        assert result["success"] == True
    
    print(f"✓ Multiple commands test passed: {len(commands)} commands executed")


def test_command_history():
    """Test that command history is stored"""
    agent = AIAgentCore()
    
    agent.process_command("Open Gmail")
    agent.process_command("Launch camera")
    
    assert len(agent.command_history) == 2
    print(f"✓ Command history test passed: {len(agent.command_history)} commands stored")


def test_intent_detection():
    """Test intent detection for different command types"""
    agent = AIAgentCore()
    
    # Test app launch intent
    intent = agent._analyze_intent("Open Gmail")
    assert intent == CommandType.LAUNCH_APP
    
    # Test system control intent
    intent = agent._analyze_intent("Enable WiFi")
    assert intent == CommandType.SYSTEM_CONTROL
    
    # Test automation intent
    intent = agent._analyze_intent("When I arrive home, turn on lights")
    assert intent == CommandType.AUTOMATION
    
    # Test query intent
    intent = agent._analyze_intent("What's the weather?")
    assert intent == CommandType.QUERY
    
    print("✓ Intent detection test passed")


def test_app_launcher():
    """Test the app launcher module"""
    launcher = AppLauncher()
    
    # Test launching an app
    result = launcher.launch("gmail")
    assert result["success"] == True
    assert result["app_name"] == "Gmail"
    
    # Test app not found
    result = launcher.launch("nonexistentapp")
    assert result["success"] == False
    assert "not found" in result["error"]
    
    print("✓ App launcher test passed")


def test_recent_apps():
    """Test recent apps tracking"""
    launcher = AppLauncher()
    
    # Launch several apps
    launcher.launch("gmail")
    launcher.launch("camera")
    launcher.launch("spotify")
    
    # Get recent apps
    recent = launcher.get_recent_apps()
    assert len(recent) == 3
    assert recent[0]["name"] == "Spotify"  # Most recent
    
    print(f"✓ Recent apps test passed: {len(recent)} recent apps tracked")


def test_smart_suggestions():
    """Test smart suggestion generation"""
    launcher = AppLauncher()
    
    # Launch some apps to build history
    launcher.launch("gmail")
    launcher.launch("gmail")  # Launch twice to make it frequent
    
    # Get suggestions
    suggestions = launcher.get_smart_suggestions()
    assert len(suggestions) > 0
    
    print(f"✓ Smart suggestions test passed: {len(suggestions)} suggestions generated")


def test_favorites():
    """Test favorites functionality"""
    launcher = AppLauncher()
    
    # Add to favorites
    success = launcher.add_to_favorites("gmail")
    assert success == True
    
    # Get favorites
    favorites = launcher.get_favorites()
    assert len(favorites) == 1
    assert favorites[0]["name"] == "Gmail"
    
    print("✓ Favorites test passed")


def test_learning_patterns():
    """Test learning from usage patterns"""
    agent = AIAgentCore()
    
    # Execute several commands
    agent.process_command("Open Gmail")
    agent.process_command("Open Gmail")
    agent.process_command("Launch camera")
    
    # Learn patterns
    patterns = agent.learn_from_patterns()
    assert "frequent_commands" in patterns
    
    print(f"✓ Learning patterns test passed: {patterns}")


def test_data_export():
    """Test data export functionality"""
    agent = AIAgentCore()
    
    # Add some data
    agent.process_command("Open Gmail")
    
    # Export data
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        filepath = f.name
    
    success = agent.export_data(filepath)
    assert success == True
    
    # Verify file exists
    assert os.path.exists(filepath)
    
    # Clean up
    os.unlink(filepath)
    
    print("✓ Data export test passed")


def test_clear_data():
    """Test data clearing functionality"""
    agent = AIAgentCore()
    
    # Add some data
    agent.process_command("Open Gmail")
    assert len(agent.command_history) > 0
    
    # Clear data
    success = agent.clear_data()
    assert success == True
    assert len(agent.command_history) == 0
    
    print("✓ Clear data test passed")


def test_get_suggestions():
    """Test getting suggestions from agent"""
    agent = AIAgentCore()
    
    # Add some commands to history
    agent.process_command("Open Gmail")
    agent.process_command("Launch camera")
    
    # Get suggestions
    suggestions = agent.get_suggestions()
    assert isinstance(suggestions, list)
    
    print(f"✓ Get suggestions test passed: {suggestions}")


def test_apps_by_category():
    """Test getting apps by category"""
    launcher = AppLauncher()
    
    # Get communication apps
    comm_apps = launcher.get_apps_by_category(AppCategory.COMMUNICATION)
    assert len(comm_apps) > 0
    
    # Verify all are communication apps
    for app in comm_apps:
        app_info = launcher.installed_apps.get(app["key"])
        assert app_info["category"] == AppCategory.COMMUNICATION
    
    print(f"✓ Apps by category test passed: {len(comm_apps)} communication apps found")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("Running Mobile AI Agent Tests")
    print("="*60 + "\n")
    
    tests = [
        test_agent_initialization,
        test_simple_app_launch,
        test_multiple_commands,
        test_command_history,
        test_intent_detection,
        test_app_launcher,
        test_recent_apps,
        test_smart_suggestions,
        test_favorites,
        test_learning_patterns,
        test_data_export,
        test_clear_data,
        test_get_suggestions,
        test_apps_by_category
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
