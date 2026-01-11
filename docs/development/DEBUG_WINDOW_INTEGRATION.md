# Debug Window Integration

## Overview

The Weyland-Yutani Transmute Tool now includes a comprehensive debug monitoring system that automatically tracks operations, logs errors/warnings, and detects performance issues.

## Features

### 1. **Automatic Error Detection**
- Debug window stays hidden until problems occur
- Automatically shows when errors or warnings are logged
- Displays error count in status label

### 2. **Operation Tracking**
- Tracks start/end times of all major operations
- Warns if operations exceed 30 seconds (potential hang)
- Logs operation duration on completion

### 3. **Exception Handling**
- Catches and logs all unhandled exceptions
- Provides detailed error information with timestamps
- Prevents application crashes from propagating silently

### 4. **Color-Coded Logging**
- **Red**: Errors (critical issues)
- **Yellow**: Warnings (potential problems)
- **Green**: Info (normal operation logs)

### 5. **Performance Monitoring**
- Background thread monitors for hung operations
- Configurable timeout threshold (default: 30 seconds)
- Automatic warning generation for slow operations

## Usage

### Keyboard Shortcuts
- **Ctrl+D**: Toggle debug window visibility

### Debug Window Controls
- **[ CLEAR ]**: Clear all log entries
- **[ HIDE ]**: Hide the debug window
- **[ TOGGLE ]**: Toggle window visibility

### Status Label
Shows current error and warning counts:
```
Errors: 0 | Warnings: 0
```

## Integration Points

The debug window is integrated into the following operations:

### 1. **File Loading** (`load_file`)
```python
- Logs file dialog opening
- Logs successful file selection
- Logs cancellation
- Catches and logs any errors
```

### 2. **Mesh Analysis** (`analyze_mesh`)
```python
- Warns if attempted without file
- Logs analysis start
- Logs analysis results (severity, issue count)
- Warns on high/critical severity
- Catches and logs any errors
```

### 3. **Mesh Repair** (`repair_mesh`)
```python
- Warns if attempted without file or analysis
- Logs repair start
- Logs progress updates
- Logs validation results
- Warns on validation failures
- Catches and logs any errors
```

### 4. **File Export** (`export_files`)
```python
- Warns if attempted without repaired mesh
- Logs output directory selection
- Logs each export operation (STL/STEP)
- Logs success/failure for each format
- Warns if FreeCAD unavailable
- Catches and logs any errors
```

## Architecture

### Components

1. **DebugWindow** (`src/ui/debug_window.py`)
   - Main debug window class
   - Handles UI and logging
   - Manages performance monitoring thread

2. **DebugExceptionHandler** (`src/ui/debug_window.py`)
   - Global exception handler
   - Catches unhandled exceptions
   - Logs to debug window

3. **Integration** (`src/ui/main_window.py`)
   - Creates debug window instance
   - Installs exception handler
   - Adds logging to all operations
   - Sets up keyboard shortcuts

### Logging Methods

```python
# Log an informational message (green)
self.debug_window.log_info("Operation started")

# Log a warning (yellow)
self.debug_window.log_warning("Potential issue detected")

# Log an error (red)
self.debug_window.log_error("Critical error occurred")

# Track operation timing
self.debug_window.start_operation("operation_name")
# ... perform operation ...
self.debug_window.end_operation("operation_name")
```

## Testing

Run the test script to verify integration:

```bash
python test_debug_integration.py
```

### Test Scenarios

1. **Normal Operation**
   - Load file → Analyze → Repair → Export
   - Debug window should log all steps
   - No errors or warnings

2. **Error Scenarios**
   - Try to analyze without loading file
   - Try to repair without analysis
   - Try to export without repair
   - Debug window should show warnings

3. **Performance Monitoring**
   - Simulate long operation (>30 seconds)
   - Debug window should warn about potential hang

4. **Exception Handling**
   - Trigger an unhandled exception
   - Debug window should catch and log it

## DOS Theme Consistency

The debug window maintains the retro DOS aesthetic:
- **Background**: Pure black (#000000)
- **Text**: Bright green (#00FF00)
- **Font**: Courier New monospace
- **Buttons**: `[ BUTTON TEXT ]` style with green borders

## Performance Impact

- **Minimal overhead**: Logging is lightweight
- **Background thread**: Performance monitoring runs separately
- **Conditional display**: Window only shows when needed
- **Memory efficient**: Log entries are stored in text widget

## Future Enhancements

Potential improvements for future versions:

1. **Log Export**: Save debug logs to file
2. **Log Filtering**: Filter by severity level
3. **Search**: Search through log entries
4. **Statistics**: Show operation timing statistics
5. **Alerts**: Audio/visual alerts for critical errors
6. **Remote Logging**: Send logs to external service

## Troubleshooting

### Debug window not appearing
- Check if Ctrl+D shortcut is working
- Verify debug window is initialized in `__init__`
- Check exception handler installation

### Logs not appearing
- Verify logging calls are present in operations
- Check if operations are wrapped in try/except
- Ensure `start_operation` and `end_operation` are called

### Performance monitoring not working
- Check if monitoring thread is started
- Verify timeout threshold is reasonable
- Check thread safety of logging calls

## Code Example

Complete example of integrating debug logging:

```python
def my_operation(self):
    """Example operation with debug logging"""
    try:
        # Start operation tracking
        self.debug_window.start_operation("my_operation")
        
        # Log start
        self.debug_window.log_info("Starting my operation...")
        
        # Perform operation
        result = self.do_something()
        
        # Check result
        if result.has_warnings:
            self.debug_window.log_warning(f"Operation completed with {len(result.warnings)} warnings")
        else:
            self.debug_window.log_info("Operation completed successfully")
        
        # End operation tracking
        self.debug_window.end_operation("my_operation")
        
        return result
        
    except Exception as e:
        # Log error
        self.debug_window.log_error(f"Error in my_operation: {str(e)}")
        
        # End operation tracking
        self.debug_window.end_operation("my_operation")
        
        # Re-raise exception
        raise
```

## Summary

The debug window integration provides comprehensive monitoring and error tracking for the Weyland-Yutani Transmute Tool. It enhances debugging capabilities while maintaining the retro DOS aesthetic and minimal performance impact.
