# TERMINAL MONOCHROME STYLE GUIDE

## DEFINITIVE STYLE SPECIFICATION FOR EDUCATIONAL MATERIALS

This document defines the **exact** black and white terminal-inspired aesthetic for all educational HTML lessons and Anki flashcards. Follow this specification **precisely** to ensure hard consistency across all future materials.

---

## TABLE OF CONTENTS

1. [Core Design Philosophy](#core-design-philosophy)
2. [Color Palette](#color-palette)
3. [Typography](#typography)
4. [HTML Structure](#html-structure)
5. [CSS Specifications](#css-specifications)
6. [Component Library](#component-library)
7. [Anki Card Styling](#anki-card-styling)
8. [Print/PDF Styling](#printpdf-styling)
9. [Complete HTML Template](#complete-html-template)
10. [Complete Anki Template](#complete-anki-template)
11. [Usage Examples](#usage-examples)

---

## 1. CORE DESIGN PHILOSOPHY

### Aesthetic Goals
- **Terminal-inspired**: Evoke classic command-line interfaces
- **Maximum readability**: Black on white (screen) or white on black (print-friendly)
- **Zero distractions**: No colors, gradients, or images (except ASCII art)
- **Brutalist simplicity**: Raw, functional, unadorned
- **Left-aligned text**: Never center body text (only headers in special cases)
- **Monospace everything**: Courier New exclusively

### Influence
Inspired by:
- Classic UNIX terminals
- ASCII art interfaces
- Brutalist web design
- Early computing documentation
- The provided "Harmonizer Lab" reference image

---

## 2. COLOR PALETTE

### Screen/Web View
```css
/* ONLY TWO COLORS ALLOWED */
--color-bg: #000000;      /* Pure black background */
--color-fg: #ffffff;      /* Pure white foreground */

/* Allowed shades for subtle backgrounds */
--color-bg-light: #0a0a0a;   /* Barely lighter black */
--color-bg-medium: #1a1a1a;  /* Subtle dark gray */
--color-bg-stripe: #0f0f0f;  /* For table stripes */

/* Border shades */
--color-border-thin: #333333;   /* Thin borders only */
--color-border-thick: #ffffff;  /* Thick borders */
```

### Print/PDF View
```css
@media print {
    --color-bg: #ffffff;      /* White background */
    --color-fg: #000000;      /* Black foreground */
    --color-bg-light: #f5f5f5;   /* Light gray */
    --color-bg-medium: #e0e0e0;  /* Medium gray */
}
```

### FORBIDDEN
- ❌ No colors (red, blue, green, etc.)
- ❌ No gradients
- ❌ No shadows
- ❌ No transparency/opacity (except for :hover transitions)

---

## 3. TYPOGRAPHY

### Font Stack
```css
/* USE EXCLUSIVELY - NO EXCEPTIONS */
font-family: 'Courier New', Consolas, Monaco, monospace;
```

### Font Sizes
```css
/* Exact sizes - do not deviate */
h1: 2.5em;     /* Main title only */
h2: 2.0em;     /* Section headers */
h3: 1.5em;     /* Subsection headers */
h4: 1.2em;     /* Minor headers */
p:  1.0em;     /* Body text (18px base) */
code: 0.9em;   /* Inline code */
pre: 1.0em;    /* Code blocks */
.category-badge: 11px;  /* Anki categories */
```

### Line Height
```css
line-height: 1.6;  /* All body text */
```

### Font Weight
```css
/* Only two weights allowed */
font-weight: normal;  /* Default (400) */
font-weight: bold;    /* Emphasis (700) */
/* NO font-weight: 500, 600, etc. */
```

### Letter Spacing
```css
h1, h2, h3, h4 {
    letter-spacing: 1px;  /* Headers only */
}

.action-button, .category-badge {
    letter-spacing: 1px;  /* UI elements */
}
```

---

## 4. HTML STRUCTURE

### Document Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Topic] - [Course Code]</title>
    <style>
        /* ALL CSS INLINE - NO EXTERNAL STYLESHEETS */
    </style>
</head>
<body>
    <!-- Header -->
    <div class="header">...</div>

    <!-- Table of Contents -->
    <div class="toc">...</div>

    <!-- Sections -->
    <div class="section" id="...">...</div>

    <!-- End Card -->
    <div style="text-align: center; ...">...</div>

    <!-- Action Buttons -->
    <div class="action-buttons">...</div>

    <!-- Scripts (minimal) -->
    <script>...</script>
</body>
</html>
```

### Section Structure
```html
<div class="section" id="unique-id">
    <h2>SECTION TITLE (UPPERCASE)</h2>

    <h3>Subsection Title (Title Case)</h3>
    <p>Body text goes here. Always left-aligned.</p>

    <h4>Minor Header (Title Case)</h4>
    <ul>
        <li>List item</li>
    </ul>

    <!-- Components as needed -->
    <div class="highlight">...</div>
    <div class="formula">...</div>
    <div class="note">...</div>
    <table>...</table>
    <pre><code>...</code></pre>
</div>
```

---

## 5. CSS SPECIFICATIONS

### Complete CSS Template

```css
/* ===== RESET ===== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* ===== BODY ===== */
body {
    font-family: 'Courier New', Consolas, Monaco, monospace;
    background-color: #000000;
    color: #ffffff;
    line-height: 1.6;
    padding: 20px;
    max-width: 1200px;  /* Constrain width */
    margin: 0 auto;     /* Center container */
}

/* ===== HEADINGS ===== */
h1, h2, h3, h4, h5, h6 {
    text-align: left;    /* ALWAYS left */
    margin: 30px 0 15px 0;
    font-weight: bold;
    letter-spacing: 1px;
}

h1 {
    font-size: 2.5em;
    border-bottom: 3px solid #ffffff;  /* Thick underline */
    padding-bottom: 10px;
    margin-bottom: 30px;
}

h2 {
    font-size: 2em;
    border-bottom: 2px solid #ffffff;  /* Medium underline */
    padding-bottom: 8px;
    margin-top: 50px;   /* Extra space before sections */
}

h3 {
    font-size: 1.5em;
    border-left: 5px solid #ffffff;  /* Left bar accent */
    padding-left: 15px;
}

h4 {
    font-size: 1.2em;
    text-decoration: underline;  /* Simple underline */
}

/* ===== TEXT ELEMENTS ===== */
p {
    margin: 15px 0;
    text-align: left;  /* CRITICAL: never center */
}

ul, ol {
    margin: 15px 0;
    padding-left: 40px;
    text-align: left;
}

li {
    margin: 8px 0;
}

strong {
    font-weight: bold;
    /* Optional: text-decoration: underline; for extra emphasis */
}

/* ===== CODE ===== */
code {
    background-color: #1a1a1a;
    color: #ffffff;
    padding: 2px 6px;
    border-radius: 3px;  /* Subtle rounding OK */
    font-family: 'Courier New', Consolas, Monaco, monospace;
    border: 1px solid #333333;
}

pre {
    background-color: #1a1a1a;
    color: #ffffff;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;  /* Horizontal scroll if needed */
    margin: 20px 0;
    border: 1px solid #333333;
    text-align: left;
}

pre code {
    background: none;
    border: none;
    padding: 0;
}

/* ===== TABLES ===== */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    background-color: #0a0a0a;
}

th, td {
    border: 1px solid #ffffff;
    padding: 12px;
    text-align: left;  /* ALWAYS left */
}

th {
    background-color: #1a1a1a;
    font-weight: bold;
}

tr:nth-child(even) {
    background-color: #0f0f0f;  /* Zebra striping */
}

/* ===== LINKS ===== */
a {
    color: #ffffff;
    text-decoration: underline;
}

a:hover {
    background-color: #ffffff;  /* Inverted on hover */
    color: #000000;
}

/* ===== HORIZONTAL RULE ===== */
hr {
    border: none;
    border-top: 1px solid #ffffff;
    margin: 40px 0;
}

/* ===== SPECIAL COMPONENTS ===== */
.header {
    text-align: center;  /* Exception: centered header */
    margin-bottom: 50px;
    padding: 30px;
    border: 3px solid #ffffff;
    background-color: #0a0a0a;
}

.header h1 {
    border: none;  /* Remove underline in header */
    margin: 0;
}

.header p {
    font-size: 1.2em;
    margin-top: 10px;
    text-align: center;  /* Exception: centered */
}

.toc {
    background-color: #1a1a1a;
    border: 2px solid #ffffff;
    padding: 20px;
    margin: 30px 0;
}

.toc h2 {
    margin-top: 0;
    border: none;  /* No underline in TOC */
}

.toc ul {
    list-style-type: none;
    padding-left: 20px;
}

.toc a {
    color: #ffffff;
    text-decoration: none;
    border-bottom: 1px dotted #ffffff;  /* Subtle underline */
}

.toc a:hover {
    background-color: #ffffff;
    color: #000000;
}

.section {
    margin: 40px 0;
    padding: 20px 0;
}

.highlight {
    background-color: #1a1a1a;
    border-left: 5px solid #ffffff;  /* Left accent */
    padding: 15px;
    margin: 20px 0;
}

.formula {
    text-align: center;  /* Exception: formulas centered */
    font-size: 1.2em;
    margin: 20px 0;
    padding: 15px;
    background-color: #1a1a1a;
    border: 1px solid #ffffff;
}

.important {
    font-weight: bold;
    text-decoration: underline;
}

.note {
    background-color: #1a1a1a;
    border: 2px solid #ffffff;
    padding: 15px;
    margin: 20px 0;
}

.note::before {
    content: "NOTE: ";
    font-weight: bold;
}

.diagram {
    text-align: center;  /* Exception: diagrams centered */
    margin: 30px 0;
    padding: 20px;
    background-color: #1a1a1a;
    border: 1px solid #ffffff;
    font-family: 'Courier New', monospace;
}

.ascii-art {
    display: inline-block;
    text-align: left;  /* ASCII art left-aligned within center */
}

/* ===== ACTION BUTTONS ===== */
.action-buttons {
    position: fixed;
    bottom: 30px;
    right: 30px;
    display: flex;
    flex-direction: column;
    gap: 15px;
    z-index: 1000;
}

.action-button {
    background-color: #ffffff;
    color: #000000;
    border: 3px solid #ffffff;
    padding: 15px 25px;
    font-family: 'Courier New', Consolas, Monaco, monospace;
    font-size: 14px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
    cursor: pointer;
    transition: all 0.2s;
    text-decoration: none;
    text-align: center;
    display: block;
}

.action-button:hover {
    background-color: #000000;
    color: #ffffff;
    transform: translateY(-2px);  /* Subtle lift */
}

.action-button:active {
    transform: translateY(0px);
}

/* ===== PRINT STYLES ===== */
@media print {
    .action-buttons {
        display: none;  /* Hide buttons in print */
    }

    body {
        background-color: #ffffff;
        color: #000000;
    }

    .header {
        background-color: #ffffff;
        border: 3px solid #000000;
    }

    .toc {
        background-color: #ffffff;
        border: 2px solid #000000;
    }

    .highlight, .note, .diagram {
        background-color: #f5f5f5;
        border-color: #000000;
    }

    code, pre {
        background-color: #f5f5f5;
        color: #000000;
        border: 1px solid #000000;
    }

    table {
        background-color: #ffffff;
    }

    th {
        background-color: #e0e0e0;
    }

    tr:nth-child(even) {
        background-color: #f5f5f5;
    }

    a {
        color: #000000;
    }
}
```

---

## 6. COMPONENT LIBRARY

### Header Block
```html
<div class="header">
    <h1>MAIN TOPIC TITLE</h1>
    <p>SUBTITLE OR CATEGORY</p>
    <p>Course Code - Assignment Name</p>
</div>
```

### Table of Contents
```html
<div class="toc">
    <h2>TABLE OF CONTENTS</h2>
    <ul>
        <li><a href="#section1">1. First Section</a></li>
        <li><a href="#section2">2. Second Section</a></li>
        <!-- ... -->
    </ul>
</div>
```

### Section
```html
<div class="section" id="section1">
    <h2>1. SECTION TITLE</h2>

    <h3>Subsection Title</h3>
    <p>Body text...</p>
</div>
```

### Highlight Box
```html
<div class="highlight">
    <p><strong>Important point:</strong></p>
    <ul>
        <li>Key detail 1</li>
        <li>Key detail 2</li>
    </ul>
</div>
```

### Formula
```html
<div class="formula">
    Output[i,j] = Σ Σ Input[i+m, j+n] × Kernel[m,n]
</div>
```

### Note Box
```html
<div class="note">
    This is automatically prefixed with "NOTE: "
</div>
```

### Code (Inline)
```html
<p>Use <code>nn.Conv2d(3, 64, 3)</code> for convolution.</p>
```

### Code Block
```html
<pre><code>def forward(self, x):
    x = self.conv1(x)
    return x</code></pre>
```

### Table
```html
<table>
    <tr>
        <th>Header 1</th>
        <th>Header 2</th>
    </tr>
    <tr>
        <td>Data 1</td>
        <td>Data 2</td>
    </tr>
    <tr>
        <td>Data 3</td>
        <td>Data 4</td>
    </tr>
</table>
```

### ASCII Diagram
```html
<div class="diagram">
    <pre class="ascii-art">
┌─────────────────┐
│  INPUT (32×32)  │
└────────┬────────┘
         ↓
    ┌────────┐
    │  CONV  │
    └────────┘
         ↓
    OUTPUT
    </pre>
</div>
```

### Action Buttons
```html
<div class="action-buttons">
    <button class="action-button" onclick="exportToPDF()">
        ⬇ EXPORT AS PDF
    </button>
    <a href="deck.apkg" download class="action-button">
        ⬇ DOWNLOAD ANKI DECK
    </a>
</div>

<script>
    function exportToPDF() {
        window.print();
    }
</script>
```

### End Card
```html
<hr>

<div style="text-align: center; margin: 50px 0; padding: 30px; border: 2px solid #ffffff;">
    <p style="font-size: 1.5em; text-align: center;"><strong>END OF LESSON</strong></p>
    <p style="text-align: center;">COURSE CODE - TOPIC</p>
    <p style="text-align: center;">ASSIGNMENT TITLE</p>
</div>
```

---

## 7. ANKI CARD STYLING

### Complete Anki CSS
```css
.card {
    font-family: 'Courier New', Consolas, Monaco, monospace;
    font-size: 18px;
    text-align: center;
    color: #ffffff;
    background-color: #000000;
    padding: 20px;
    line-height: 1.6;
}

.category-badge {
    display: inline-block;
    background: #ffffff;
    color: #000000;
    padding: 6px 14px;
    border-radius: 0px;  /* NO rounding for badges */
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 20px;
    border: 2px solid #ffffff;
}

.question {
    font-size: 24px;
    font-weight: 600;
    margin: 25px 0;
    color: #ffffff;
    text-align: left;  /* Questions left-aligned */
}

hr {
    border: none;
    border-top: 2px solid #ffffff;
    margin: 30px 0;
}

.answer {
    text-align: left;  /* Answers left-aligned */
    font-size: 17px;
    padding: 20px;
    background-color: #0a0a0a;
    border-radius: 0px;
    margin: 20px 0;
    border: 1px solid #ffffff;
}

.answer strong {
    color: #ffffff;
    font-weight: 700;
    text-decoration: underline;
}

.answer ul, .answer ol {
    margin: 15px 0;
    padding-left: 30px;
}

.answer li {
    margin: 10px 0;
}

.code-block {
    background-color: #0a0a0a;
    color: #ffffff;
    padding: 18px;
    border-radius: 0px;
    font-family: 'Courier New', Consolas, Monaco, monospace;
    font-size: 14px;
    text-align: left;
    overflow-x: auto;
    margin-top: 20px;
    white-space: pre-wrap;
    word-wrap: break-word;
    border: 2px solid #ffffff;
}
```

### Anki Card Templates

**Question Template:**
```html
<div class="card">
    <div class="category-badge">{{Category}}</div>
    <div class="question">{{Question}}</div>
</div>
```

**Answer Template:**
```html
<div class="card">
    <div class="category-badge">{{Category}}</div>
    <div class="question">{{Question}}</div>
    <hr>
    <div class="answer">{{Answer}}</div>
    {{#Code}}
    <div class="code-block">{{Code}}</div>
    {{/Code}}
</div>
```

---

## 8. PRINT/PDF STYLING

### Print Media Query Rules

```css
@media print {
    /* 1. Hide interactive elements */
    .action-buttons {
        display: none;
    }

    /* 2. Invert colors for printing */
    body {
        background-color: #ffffff;
        color: #000000;
    }

    /* 3. Update component backgrounds */
    .header {
        background-color: #ffffff;
        border: 3px solid #000000;
    }

    .toc {
        background-color: #ffffff;
        border: 2px solid #000000;
    }

    .highlight, .note, .diagram {
        background-color: #f5f5f5;  /* Light gray */
        border: 1px solid #000000;
    }

    code, pre {
        background-color: #f5f5f5;
        color: #000000;
        border: 1px solid #000000;
    }

    /* 4. Table adjustments */
    table {
        background-color: #ffffff;
    }

    th {
        background-color: #e0e0e0;
    }

    tr:nth-child(even) {
        background-color: #f5f5f5;
    }

    /* 5. Link colors */
    a {
        color: #000000;
        text-decoration: underline;
    }

    /* 6. Page breaks (optional) */
    .section {
        page-break-inside: avoid;
    }

    h2 {
        page-break-before: always;
    }

    h2:first-of-type {
        page-break-before: avoid;
    }
}
```

---

## 9. COMPLETE HTML TEMPLATE

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[TOPIC NAME] - [COURSE CODE]</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Courier New', Consolas, Monaco, monospace;
            background-color: #000000;
            color: #ffffff;
            line-height: 1.6;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }

        h1, h2, h3, h4, h5, h6 {
            text-align: left;
            margin: 30px 0 15px 0;
            font-weight: bold;
            letter-spacing: 1px;
        }

        h1 {
            font-size: 2.5em;
            border-bottom: 3px solid #ffffff;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }

        h2 {
            font-size: 2em;
            border-bottom: 2px solid #ffffff;
            padding-bottom: 8px;
            margin-top: 50px;
        }

        h3 {
            font-size: 1.5em;
            border-left: 5px solid #ffffff;
            padding-left: 15px;
        }

        h4 {
            font-size: 1.2em;
            text-decoration: underline;
        }

        p {
            margin: 15px 0;
            text-align: left;
        }

        ul, ol {
            margin: 15px 0;
            padding-left: 40px;
            text-align: left;
        }

        li {
            margin: 8px 0;
        }

        code {
            background-color: #1a1a1a;
            color: #ffffff;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', Consolas, Monaco, monospace;
            border: 1px solid #333333;
        }

        pre {
            background-color: #1a1a1a;
            color: #ffffff;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 20px 0;
            border: 1px solid #333333;
            text-align: left;
        }

        pre code {
            background: none;
            border: none;
            padding: 0;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background-color: #0a0a0a;
        }

        th, td {
            border: 1px solid #ffffff;
            padding: 12px;
            text-align: left;
        }

        th {
            background-color: #1a1a1a;
            font-weight: bold;
        }

        tr:nth-child(even) {
            background-color: #0f0f0f;
        }

        .toc {
            background-color: #1a1a1a;
            border: 2px solid #ffffff;
            padding: 20px;
            margin: 30px 0;
        }

        .toc h2 {
            margin-top: 0;
            border: none;
        }

        .toc ul {
            list-style-type: none;
            padding-left: 20px;
        }

        .toc a {
            color: #ffffff;
            text-decoration: none;
            border-bottom: 1px dotted #ffffff;
        }

        .toc a:hover {
            background-color: #ffffff;
            color: #000000;
        }

        .section {
            margin: 40px 0;
            padding: 20px 0;
        }

        .highlight {
            background-color: #1a1a1a;
            border-left: 5px solid #ffffff;
            padding: 15px;
            margin: 20px 0;
        }

        .formula {
            text-align: center;
            font-size: 1.2em;
            margin: 20px 0;
            padding: 15px;
            background-color: #1a1a1a;
            border: 1px solid #ffffff;
        }

        .important {
            font-weight: bold;
            text-decoration: underline;
        }

        .note {
            background-color: #1a1a1a;
            border: 2px solid #ffffff;
            padding: 15px;
            margin: 20px 0;
        }

        .note::before {
            content: "NOTE: ";
            font-weight: bold;
        }

        hr {
            border: none;
            border-top: 1px solid #ffffff;
            margin: 40px 0;
        }

        a {
            color: #ffffff;
            text-decoration: underline;
        }

        a:hover {
            background-color: #ffffff;
            color: #000000;
        }

        .header {
            text-align: center;
            margin-bottom: 50px;
            padding: 30px;
            border: 3px solid #ffffff;
            background-color: #0a0a0a;
        }

        .header h1 {
            border: none;
            margin: 0;
        }

        .header p {
            font-size: 1.2em;
            margin-top: 10px;
            text-align: center;
        }

        .diagram {
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background-color: #1a1a1a;
            border: 1px solid #ffffff;
            font-family: 'Courier New', monospace;
        }

        .ascii-art {
            display: inline-block;
            text-align: left;
        }

        .action-buttons {
            position: fixed;
            bottom: 30px;
            right: 30px;
            display: flex;
            flex-direction: column;
            gap: 15px;
            z-index: 1000;
        }

        .action-button {
            background-color: #ffffff;
            color: #000000;
            border: 3px solid #ffffff;
            padding: 15px 25px;
            font-family: 'Courier New', Consolas, Monaco, monospace;
            font-size: 14px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
            text-align: center;
            display: block;
        }

        .action-button:hover {
            background-color: #000000;
            color: #ffffff;
            transform: translateY(-2px);
        }

        .action-button:active {
            transform: translateY(0px);
        }

        @media print {
            .action-buttons {
                display: none;
            }
            body {
                background-color: #ffffff;
                color: #000000;
            }
            .header {
                background-color: #ffffff;
                border: 3px solid #000000;
            }
            .toc {
                background-color: #ffffff;
                border: 2px solid #000000;
            }
            .highlight, .note, .diagram {
                background-color: #f5f5f5;
                border: 1px solid #000000;
            }
            code, pre {
                background-color: #f5f5f5;
                color: #000000;
                border: 1px solid #000000;
            }
            table {
                background-color: #ffffff;
            }
            th {
                background-color: #e0e0e0;
            }
            tr:nth-child(even) {
                background-color: #f5f5f5;
            }
            a {
                color: #000000;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>[MAIN TITLE]</h1>
        <p>[SUBTITLE]</p>
        <p>[COURSE CODE] - [ASSIGNMENT]</p>
    </div>

    <div class="toc">
        <h2>TABLE OF CONTENTS</h2>
        <ul>
            <li><a href="#section1">1. First Section</a></li>
            <li><a href="#section2">2. Second Section</a></li>
        </ul>
    </div>

    <div class="section" id="section1">
        <h2>1. FIRST SECTION</h2>

        <h3>Subsection Title</h3>
        <p>Content goes here...</p>

        <div class="highlight">
            <p><strong>Important concept:</strong></p>
            <ul>
                <li>Key point 1</li>
                <li>Key point 2</li>
            </ul>
        </div>

        <table>
            <tr>
                <th>Column 1</th>
                <th>Column 2</th>
            </tr>
            <tr>
                <td>Data 1</td>
                <td>Data 2</td>
            </tr>
        </table>

        <pre><code>// Code example
function example() {
    return true;
}</code></pre>

        <div class="note">
            This is an important note about the topic.
        </div>

        <div class="formula">
            formula = a × b + c
        </div>
    </div>

    <hr>

    <div style="text-align: center; margin: 50px 0; padding: 30px; border: 2px solid #ffffff;">
        <p style="font-size: 1.5em; text-align: center;"><strong>END OF LESSON</strong></p>
        <p style="text-align: center;">[COURSE CODE] - [TOPIC]</p>
        <p style="text-align: center;">[ASSIGNMENT TITLE]</p>
    </div>

    <div class="action-buttons">
        <button class="action-button" onclick="exportToPDF()">
            ⬇ EXPORT AS PDF
        </button>
        <a href="deck.apkg" download class="action-button">
            ⬇ DOWNLOAD ANKI DECK
        </a>
    </div>

    <script>
        function exportToPDF() {
            window.print();
        }
    </script>
</body>
</html>
```

---

## 10. COMPLETE ANKI TEMPLATE

### Python Script (using genanki)

```python
import genanki
import random

# Generate unique IDs
DECK_ID = random.randrange(1 << 30, 1 << 31)
MODEL_ID = random.randrange(1 << 30, 1 << 31)

# Define model with terminal styling
model = genanki.Model(
    MODEL_ID,
    '[Topic] Flashcards',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'Category'},
        {'name': 'Code'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '''
                <div class="card">
                    <div class="category-badge">{{Category}}</div>
                    <div class="question">{{Question}}</div>
                </div>
            ''',
            'afmt': '''
                <div class="card">
                    <div class="category-badge">{{Category}}</div>
                    <div class="question">{{Question}}</div>
                    <hr>
                    <div class="answer">{{Answer}}</div>
                    {{#Code}}
                    <div class="code-block">{{Code}}</div>
                    {{/Code}}
                </div>
            ''',
        },
    ],
    css='''
        .card {
            font-family: 'Courier New', Consolas, Monaco, monospace;
            font-size: 18px;
            text-align: center;
            color: #ffffff;
            background-color: #000000;
            padding: 20px;
            line-height: 1.6;
        }

        .category-badge {
            display: inline-block;
            background: #ffffff;
            color: #000000;
            padding: 6px 14px;
            border-radius: 0px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 20px;
            border: 2px solid #ffffff;
        }

        .question {
            font-size: 24px;
            font-weight: 600;
            margin: 25px 0;
            color: #ffffff;
            text-align: left;
        }

        hr {
            border: none;
            border-top: 2px solid #ffffff;
            margin: 30px 0;
        }

        .answer {
            text-align: left;
            font-size: 17px;
            padding: 20px;
            background-color: #0a0a0a;
            border-radius: 0px;
            margin: 20px 0;
            border: 1px solid #ffffff;
        }

        .answer strong {
            color: #ffffff;
            font-weight: 700;
            text-decoration: underline;
        }

        .answer ul, .answer ol {
            margin: 15px 0;
            padding-left: 30px;
        }

        .answer li {
            margin: 10px 0;
        }

        .code-block {
            background-color: #0a0a0a;
            color: #ffffff;
            padding: 18px;
            border-radius: 0px;
            font-family: 'Courier New', Consolas, Monaco, monospace;
            font-size: 14px;
            text-align: left;
            overflow-x: auto;
            margin-top: 20px;
            white-space: pre-wrap;
            word-wrap: break-word;
            border: 2px solid #ffffff;
        }
    '''
)

# Create deck
deck = genanki.Deck(
    DECK_ID,
    '[Topic Name] - [Course Code]'
)

# Example cards
cards = [
    {
        'question': 'What is the main concept?',
        'answer': '''<strong>The main concept is...</strong>
<br><br>
<strong>Key points:</strong>
<ul>
<li><strong>Point 1:</strong> Explanation</li>
<li><strong>Point 2:</strong> More detail</li>
</ul>''',
        'category': 'Fundamentals',
        'code': '''def example():
    return "code"'''
    },
]

# Add cards to deck
for card_data in cards:
    note = genanki.Note(
        model=model,
        fields=[
            card_data['question'],
            card_data['answer'],
            card_data['category'],
            card_data.get('code', '')
        ]
    )
    deck.add_note(note)

# Generate deck
output_file = '[Topic]_Flashcards.apkg'
genanki.Package(deck).write_to_file(output_file)

print(f"Generated: {output_file}")
print(f"Total cards: {len(cards)}")
```

---

## 11. USAGE EXAMPLES

### Creating a New Lesson

1. **Copy the complete HTML template** from Section 9
2. **Replace placeholders:**
   - `[TOPIC NAME]` → e.g., "Recurrent Neural Networks"
   - `[COURSE CODE]` → e.g., "CMPUT 328"
   - `[ASSIGNMENT]` → e.g., "Assignment 5"
3. **Fill in table of contents** with actual section IDs
4. **Create sections** using the section structure
5. **Add components** as needed (tables, code, diagrams)
6. **Update action buttons** to point to correct .apkg file
7. **Save** as `[topic]_lesson.html`

### Creating Anki Cards

1. **Copy the complete Python template** from Section 10
2. **Update metadata:**
   - Deck name
   - Topic name
3. **Create card data** following the example format
4. **Categories to use:**
   - Fundamentals
   - Definitions
   - Formulas
   - Implementation
   - Best Practices
   - Common Pitfalls
   - etc.
5. **Answer formatting:**
   - Use `<strong>` for emphasis
   - Use `<br><br>` for spacing
   - Use `<ul>` and `<li>` for lists
   - Use `code` field for code examples
6. **Run script** to generate .apkg file

### ASCII Art Guidelines

**Use box-drawing characters:**
```
┌ ┐ └ ┘  # Corners
─ │      # Lines
├ ┤ ┬ ┴  # T-junctions
┼        # Cross
```

**Use arrows:**
```
→ ← ↑ ↓  # Directional
```

**Example structure:**
```
┌──────────────┐
│    INPUT     │
└──────┬───────┘
       ↓
  ┌─────────┐
  │ PROCESS │
  └─────────┘
       ↓
    OUTPUT
```

---

## APPENDIX: DESIGN RULES CHECKLIST

When creating new materials, verify ALL of these:

### Colors
- [ ] Only #000000 and #ffffff used (plus subtle grays)
- [ ] No colors, gradients, or shadows
- [ ] Print styles invert colors appropriately

### Typography
- [ ] Courier New exclusively
- [ ] Font sizes match specification
- [ ] Line height is 1.6
- [ ] Letter spacing on headers and UI elements only

### Layout
- [ ] Body text is left-aligned
- [ ] Max-width: 1200px
- [ ] Adequate margins and padding
- [ ] Sections have clear visual separation

### Components
- [ ] Headers have correct underlines/borders
- [ ] Tables have zebra striping
- [ ] Code blocks have dark background
- [ ] Formulas are centered
- [ ] Notes have "NOTE:" prefix
- [ ] Links invert on hover

### Functionality
- [ ] Export PDF button present and functional
- [ ] Download Anki button links to correct file
- [ ] TOC links work correctly
- [ ] Print styles are defined

### Consistency
- [ ] All sections follow same structure
- [ ] Spacing is uniform
- [ ] Component styling matches exactly
- [ ] No deviations from specification

---

**END OF STYLE GUIDE**

This document is the single source of truth for the terminal monochrome aesthetic. Follow it precisely for perfect consistency across all educational materials.
