# Debug Window Quick Reference

## 🚀 Quick Start

### Enable Debug Window
```python
# Already integrated! Just press Ctrl+D to toggle
```

### Basic Logging
```python
# Info (green) - normal operations
self.debug_window.log_info("Operation started")

# Warning (yellow) - potential issues
self.debug_window.log_warning("File not found, using default")

# Error (red) - critical problems
self.debug_window.log_error("Failed to load mesh")
```

### Operation Tracking
```python
def my_operation(self):
    try:
        # Start tracking
        self.debug_window.start_operation("my_operation")
        
        # Your code here
        result = do_something()
        
        # End tracking
        self.debug_window.end_operation("my_operation")
        return result
    except Exception as e:
        self.debug_window.log_error(f"Error: {e}")
        self.debug_window.end_operation("my_operation")
        raise
```

## 📋 Common Patterns

### Pattern 1: Simple Operation
```python
def simple_task(self):
    self.debug_window.log_info("Starting simple task")
    # ... do work ...
    self.debug_window.log_info("Task completed")
```

### Pattern 2: Operation with Validation
```python
def validated_task(self):
    try:
        self.debug_window.start_operation("validated_task")
        
        if not self.is_ready():
            self.debug_window.log_warning("Not ready, skipping")
            return
        
        result = self.perform_task()
        
        if result.has_errors:
            self.debug_window.log_error("Task failed")
        elif result.has_warnings:
            self.debug_window.log_warning("Task completed with warnings")
        else:
            self.debug_window.log_info("Task completed successfully")
        
        self.debug_window.end_operation("validated_task")
    except Exception as e:
        self.debug_window.log_error(f"Exception: {e}")
        self.debug_window.end_operation("validated_task")
        raise
```

### Pattern 3: Long Operation with Progress
```python
def long_task(self):
    try:
        self.debug_window.start_operation("long_task")
        
        for i, item in enumerate(items):
            self.debug_window.log_info(f"Processing {i+1}/{len(items)}")
            process(item)
        
        self.debug_window.log_info("All items processed")
        self.debug_window.end_operation("long_task")
    except Exception as e:
        self.debug_window.log_error(f"Failed at item {i}: {e}")
        self.debug_window.end_operation("long_task")
        raise
```

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+D` | Toggle debug window visibility |

## 🎨 Log Colors

| Level | Color | When to Use |
|-------|-------|-------------|
| **Info** | 🟢 Green | Normal operations, progress updates |
| **Warning** | 🟡 Yellow | Potential issues, validation warnings |
| **Error** | 🔴 Red | Critical failures, exceptions |

## 🔍 Auto-Show Triggers

The debug window automatically appears when:
- ❌ An error is logged
- ⚠️ A warning is logged
- ⏱️ An operation exceeds 30 seconds (hang detection)
- 💥 An unhandled exception occurs

## 📊 Status Label

Shows real-time counts:
```
Errors: 2 | Warnings: 5
```

## 🛠️ Debug Window Controls

| Button | Action |
|--------|--------|
| `[ CLEAR ]` | Clear all log entries |
| `[ HIDE ]` | Hide the debug window |
| `[ TOGGLE ]` | Toggle window visibility |

## 🎯 Best Practices

### ✅ DO
- Log at operation boundaries (start/end)
- Use appropriate log levels
- Include context in messages
- Track long-running operations
- Log user actions
- Log validation results

### ❌ DON'T
- Log inside tight loops (use periodic logging)
- Log sensitive data (passwords, keys)
- Use generic messages ("Error occurred")
- Forget to end operations
- Log excessively (spam)

## 📝 Message Format Examples

### Good Messages ✅
```python
self.debug_window.log_info("Loading mesh from: cube.stl")
self.debug_window.log_warning("Mesh has 5 non-manifold edges")
self.debug_window.log_error("Failed to export STEP: FreeCAD not found")
```

### Bad Messages ❌
```python
self.debug_window.log_info("Loading")  # Too vague
self.debug_window.log_error("Error")   # No context
self.debug_window.log_warning("Warning: " + str(e))  # Redundant prefix
```

## 🔧 Troubleshooting

### Debug window not showing
1. Check if initialized: `self.debug_window = DebugWindow(root)`
2. Try manual toggle: Press `Ctrl+D`
3. Check exception handler: `self.exception_handler.install()`

### Logs not appearing
1. Verify logging calls exist
2. Check operation is wrapped in try/except
3. Ensure `start_operation` and `end_operation` are called

### Performance issues
1. Reduce logging frequency in loops
2. Check for excessive log messages
3. Clear logs periodically

## 📚 Integration Checklist

When adding debug logging to a new operation:

- [ ] Import debug window in class
- [ ] Add `start_operation()` at beginning
- [ ] Add `end_operation()` at end
- [ ] Wrap in try/except block
- [ ] Log errors in except block
- [ ] Log info for success
- [ ] Log warnings for issues
- [ ] Test with Ctrl+D toggle

## 🎓 Example: Complete Integration

```python
def complete_example(self):
    """Complete example with all best practices"""
    try:
        # Start tracking
        self.debug_window.start_operation("complete_example")
        
        # Log start
        self.debug_window.log_info("Starting complete example operation")
        
        # Validate preconditions
        if not self.is_ready():
            self.debug_window.log_warning("Preconditions not met")
            self.debug_window.end_operation("complete_example")
            return None
        
        # Perform operation
        self.debug_window.log_info("Processing data...")
        result = self.process_data()
        
        # Validate result
        if not result.is_valid():
            self.debug_window.log_error("Result validation failed")
            self.debug_window.end_operation("complete_example")
            return None
        
        # Check for warnings
        if result.has_warnings():
            warning_count = len(result.warnings)
            self.debug_window.log_warning(
                f"Operation completed with {warning_count} warnings"
            )
        else:
            self.debug_window.log_info("Operation completed successfully")
        
        # End tracking
        self.debug_window.end_operation("complete_example")
        return result
        
    except ValueError as e:
        self.debug_window.log_error(f"Invalid value: {e}")
        self.debug_window.end_operation("complete_example")
        raise
    except IOError as e:
        self.debug_window.log_error(f"IO error: {e}")
        self.debug_window.end_operation("complete_example")
        raise
    except Exception as e:
        self.debug_window.log_error(f"Unexpected error: {e}")
        self.debug_window.end_operation("complete_example")
        raise
```

## 🌟 Pro Tips

1. **Use descriptive operation names**: `"mesh_repair"` not `"repair"`
2. **Include relevant data**: `"Loaded 1234 vertices"` not `"Loaded mesh"`
3. **Log before and after**: Start and completion messages
4. **Use consistent formatting**: Follow existing patterns
5. **Test error paths**: Verify errors are logged correctly
6. **Monitor performance**: Watch for operations >30 seconds
7. **Clear logs regularly**: Use `[ CLEAR ]` button during testing

## 📞 Support

For issues or questions:
1. Check `DEBUG_WINDOW_INTEGRATION.md` for detailed documentation
2. Review `src/ui/debug_window.py` for implementation details
3. Run `test_debug_integration.py` to verify setup

---

**Remember**: The debug window is your friend! Use it to track down issues and monitor application health. 🚀
