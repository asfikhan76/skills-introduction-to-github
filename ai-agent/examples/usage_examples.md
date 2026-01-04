# Mobile AI Agent - Examples

This document provides practical examples of how to use the Mobile AI Agent.

## Basic Usage

### Python Example

```python
from ai_agent_core import AIAgentCore
from app_launcher import AppLauncher

# Initialize the AI agent
agent = AIAgentCore()

# Process a simple command
result = agent.process_command("Open Gmail")
print(result)
# Output: {
#   "success": True,
#   "action": "launch_app",
#   "app_name": "Gmail",
#   "message": "Successfully launched Gmail",
#   "timestamp": "2024-01-04T10:30:00"
# }

# Process a complex command
result = agent.process_command("When I arrive at work, silence my phone and open Slack")
print(result)
```

### App Launcher Example

```python
from app_launcher import AppLauncher

# Initialize launcher
launcher = AppLauncher()

# Launch an app
result = launcher.launch("spotify")
print(f"Launched: {result['app_name']}")

# Get smart suggestions based on time
suggestions = launcher.get_smart_suggestions()
print(f"Suggested apps: {suggestions}")

# Switch to recent app
launcher.switch_to_recent(0)  # Switch to most recent app

# Add app to favorites
launcher.add_to_favorites("gmail")
favorites = launcher.get_favorites()
print(f"Favorite apps: {favorites}")
```

## Voice Commands

### Opening Apps

```
"Open Gmail"
"Launch camera"
"Start Spotify"
"Open my email app"
```

### Multi-Step Commands

```
"Open Spotify and play my workout playlist"
"Launch camera and take a selfie"
"Open Maps and navigate to home"
"Start WhatsApp and call John"
```

### System Control

```
"Turn on WiFi"
"Enable Do Not Disturb mode"
"Set brightness to 50%"
"Turn off Bluetooth"
```

### Automation Commands

```
"Every morning at 7 AM, read my calendar"
"When battery is below 20%, enable power saving mode"
"When I arrive at work, silence my phone"
"If I'm driving, automatically respond to messages"
```

### Query Commands

```
"What's the weather today?"
"Show me my calendar for today"
"How many unread emails do I have?"
"What apps did I use most this week?"
```

## Advanced Features

### Task Chaining

```python
# Chain multiple tasks together
agent.process_command(
    "Open Gmail, mark all emails from boss as read, "
    "then open Calendar and show today's meetings"
)
```

### Conditional Automation

```python
# Create conditional automation
agent.process_command(
    "If location is gym, open Spotify and play workout playlist"
)

agent.process_command(
    "When it's after 10 PM, enable night mode and silence notifications"
)
```

### Context-Aware Actions

```python
# Provide context for better results
context = {
    "time": "morning",
    "location": "home",
    "activity": "getting_ready",
    "battery": 85
}

result = agent.process_command("What should I do now?", context=context)
# AI might suggest: "Check your calendar and weather for today"
```

### Learning from Patterns

```python
# Agent learns from usage
agent.process_command("Open Spotify")  # Used multiple times
agent.process_command("Open Spotify")
agent.process_command("Open Spotify")

# Now the agent learns and suggests
suggestions = agent.get_suggestions()
# Output: ["Open Spotify", "Launch camera", ...]
```

## Integration Examples

### Cross-App Actions

```
"Find the nearest coffee shop in Maps and share location on WhatsApp"
"Take a photo and post it to Instagram with caption 'Beautiful day'"
"Copy this text and paste it in Gmail"
```

### API Integration

```python
# Connect with third-party services
agent.process_command("Check my GitHub notifications")
agent.process_command("What's trending on Twitter?")
agent.process_command("Order my usual from Uber Eats")
```

### Cloud Sync

```python
# Export settings to sync across devices
agent.export_data("/path/to/export.json")

# Import on another device
# Settings, learned patterns, and preferences are synced
```

## Privacy Features

### Privacy Mode

```python
# Enable privacy mode (no recording/learning)
agent.config["privacy_mode"] = True

# Commands are still executed but not stored
result = agent.process_command("Open sensitive app")
```

### Data Management

```python
# View stored data
history_count = len(agent.command_history)
print(f"Commands in history: {history_count}")

# Export data
agent.export_data("my_ai_data.json")

# Clear all data
agent.clear_data()
```

### On-Device Processing

```python
# Force on-device processing (no cloud)
agent.processing_mode = ProcessingMode.ON_DEVICE

# Now all commands are processed locally
result = agent.process_command("Open private notes")
```

## Customization Examples

### Custom Wake Word

```python
# Change wake word
agent.config["wake_word"] = "Hey Jarvis"

# Now the agent responds to "Hey Jarvis"
```

### Custom Command Training

```python
# Train custom phrases
agent.process_command("When I say 'start work mode', enable Do Not Disturb and open Slack")

# Now you can use the custom command
agent.process_command("start work mode")
```

### Routine Creation

```python
# Create morning routine
agent.process_command(
    "Create a routine called 'morning' that opens Gmail, "
    "shows weather, reads calendar, and plays news"
)

# Execute routine
agent.process_command("Run morning routine")
```

## Error Handling

```python
# Handle app not found
result = agent.process_command("Open NonExistentApp")
if not result["success"]:
    print(f"Error: {result['error']}")
    print(f"Suggestions: {result.get('suggestions', [])}")

# Handle ambiguous commands
result = agent.process_command("Open app")
# Agent might ask: "Which app would you like to open?"
```

## Performance Tips

1. **Use specific app names** for faster execution
2. **Enable learning** to get better suggestions over time
3. **Use hybrid mode** for balance of speed and privacy
4. **Clear old history** periodically to improve performance
5. **Use context** when available for more accurate results

## Testing Commands

```python
# Test command recognition
test_commands = [
    "Open Gmail",
    "Launch camera",
    "When I arrive home, turn on WiFi",
    "What's the weather?",
    "Switch to recent app"
]

for cmd in test_commands:
    result = agent.process_command(cmd)
    print(f"Command: {cmd}")
    print(f"Success: {result['success']}")
    print(f"Action: {result.get('action', 'N/A')}")
    print("---")
```

## Mobile Platform Integration

### Android Example (Java)

```java
// Initialize AI Agent (through JNI bridge)
AIAgentCore agent = new AIAgentCore();

// Process command from user
String command = "Open Gmail";
JSONObject result = agent.processCommand(command);

if (result.getBoolean("success")) {
    String packageName = result.getString("package");
    // Launch app using Android Intent
    Intent intent = getPackageManager()
        .getLaunchIntentForPackage(packageName);
    startActivity(intent);
}
```

### iOS Example (Swift)

```swift
// Initialize AI Agent (through Swift bridge)
let agent = AIAgentCore()

// Process command from user
let command = "Open Gmail"
let result = agent.processCommand(command)

if result["success"] as? Bool == true {
    let appName = result["app_name"] as? String
    // Launch app using iOS URL scheme
    if let url = URL(string: "googlegmail://") {
        UIApplication.shared.open(url)
    }
}
```

## Conclusion

The Mobile AI Agent provides a powerful and flexible platform for mobile automation. These examples demonstrate the core capabilities, but the agent can be customized and extended for virtually any use case.

For more information, see:
- [Main Documentation](../AI_AGENT.md)
- [API Reference](../docs/api_reference.md)
- [Configuration Guide](../docs/configuration.md)
