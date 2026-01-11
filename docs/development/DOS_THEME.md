================================================================================
🖥️ DOS THEME - RETRO BLACK & GREEN INTERFACE
================================================================================

THEME APPLIED:
    ✅ Classic DOS color scheme (black background, green text)
    ✅ Monospace Courier New font throughout
    ✅ Custom DOS-style progress bar
    ✅ Retro button styling with brackets
    ✅ Green borders and highlights

================================================================================
COLOR SCHEME
================================================================================

Background:     #000000 (Pure Black)
Primary Text:   #00FF00 (Bright Green)
Dim Text:       #00AA00 (Dim Green)
Highlights:     #00FF00 (Bright Green)
Active:         Inverted (Green BG, Black Text)

================================================================================
TYPOGRAPHY
================================================================================

Main Font:      Courier New, 10pt (monospace)
Bold Font:      Courier New, 10pt Bold
Title Font:     Courier New, 14pt Bold

All text uses monospace for authentic DOS feel!

================================================================================
UI ELEMENTS
================================================================================

Buttons:
  - Format: [ BUTTON TEXT ]
  - Green text on black background
  - Green border (1px)
  - Inverts on hover (black text on green)

Labels:
  - ALL CAPS for section headers
  - Monospace font
  - Green text

Text Areas:
  - Black background
  - Green text
  - Green border
  - Monospace font

Progress Bar:
  - Custom drawn on canvas
  - Green fill for progress
  - Percentage displayed in center
  - Text color inverts when >50%

Checkboxes:
  - Green text
  - Black select color
  - DOS-style appearance

================================================================================
VISUAL LAYOUT
================================================================================

┌─────────────────────────────────────────────────────────────────────────┐
│ WEYLAND-YUTANI TRANSMUTE TOOL                                           │
│ "Building Better Worlds... One Mesh at a Time"                          │
├──────────────────────────┬──────────────────────────────────────────────┤
│ INPUT FILE               │ CONSOLE OUTPUT                               │
│ No file selected         │ ============================================ │
│ [ LOAD STL FILE ]        │ WEYLAND-YUTANI TRANSMUTE TOOL                │
│                          │ ============================================ │
│ ANALYSIS                 │                                              │
│ [ ANALYZE MESH ]         │ Ready for transmutation...                   │
│                          │                                              │
│ REPAIR                   │                                              │
│ [ REPAIR MESH ]          │                                              │
│                          │                                              │
│ EXPORT                   │                                              │
│ ☑ Export STL             │                                              │
│ ☑ Export STEP            │                                              │
│ [ EXPORT FILES ]         │                                              │
│                          │                                              │
│ STATUS                   │                                              │
│ READY FOR                │                                              │
│ TRANSMUTATION...         │                                              │
│                          │                                              │
│ [████████░░░░░░] 50%    │                                              │
│ Processing...            │                                              │
│                          │ [ CLEAR CONSOLE ]                            │
└──────────────────────────┴──────────────────────────────────────────────┘

================================================================================
FEATURES
================================================================================

✅ Authentic DOS Aesthetic:
   - Pure black background
   - Bright green text
   - Monospace font throughout
   - Retro button styling

✅ Custom Progress Bar:
   - Hand-drawn on canvas
   - Green fill animation
   - Percentage display
   - Inverted text when >50%

✅ Consistent Styling:
   - All widgets themed
   - Green borders everywhere
   - Hover effects on buttons
   - Professional retro look

✅ Readability:
   - High contrast (green on black)
   - Clear monospace font
   - Proper spacing
   - Easy to read

================================================================================
TECHNICAL DETAILS
================================================================================

Theme Constants:
  DOS_BG = "#000000"          # Black background
  DOS_FG = "#00FF00"          # Bright green
  DOS_FG_DIM = "#00AA00"      # Dim green
  DOS_FONT = ("Courier New", 10)
  DOS_FONT_BOLD = ("Courier New", 10, "bold")
  DOS_FONT_TITLE = ("Courier New", 14, "bold")

Widgets Styled:
  ✅ Main window background
  ✅ All frames and panels
  ✅ All labels (headers and text)
  ✅ All buttons
  ✅ Text areas (status and console)
  ✅ Checkboxes
  ✅ Progress bar (custom canvas)
  ✅ LabelFrames (section headers)

Custom Progress Bar:
  - Uses tk.Canvas for drawing
  - Draws filled rectangle for progress
  - Displays percentage text
  - Text color inverts at 50% for visibility
  - Green fill (#00FF00)
  - Updates in real-time

================================================================================
COMPARISON
================================================================================

BEFORE (Modern):
  - Light gray backgrounds
  - Standard fonts
  - Colorful buttons
  - Modern widgets

AFTER (DOS):
  - Pure black background
  - Bright green text
  - Monospace Courier New
  - Retro bracket buttons
  - Custom progress bar
  - Authentic 1980s feel

================================================================================
TESTING
================================================================================

To see the DOS theme:

1. Run the application:
   python src/main.py

2. You should see:
   ✅ Black background everywhere
   ✅ Green text throughout
   ✅ Monospace font (Courier New)
   ✅ Buttons with [ BRACKETS ]
   ✅ Green borders on all widgets
   ✅ Custom green progress bar

3. Test interactions:
   ✅ Hover over buttons (should invert colors)
   ✅ Load a file (text should be green)
   ✅ Repair mesh (progress bar should be green)
   ✅ Console output (green text on black)

================================================================================
INSPIRATION
================================================================================

Classic DOS/Terminal aesthetics:
  - MS-DOS (1981-2000)
  - Early UNIX terminals
  - Monochrome CRT monitors
  - Hacker/cyberpunk aesthetic
  - Weyland-Yutani corporation (Alien franchise)

Perfect for:
  - Retro computing enthusiasts
  - Cyberpunk fans
  - Terminal lovers
  - Anyone who misses the 80s/90s

================================================================================

"The future is retro!" 🖥️💚

================================================================================
