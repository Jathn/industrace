# Contributing to Industrace Translations

Thank you for your interest in contributing to Industrace translations! This guide will help you get started with translating the application into your language.

## Table of Contents

- [Quick Start](#quick-start)
- [Translation Structure](#translation-structure)
- [Getting Started](#getting-started)
- [Translation Workflow](#translation-workflow)
- [Validation and Testing](#validation-and-testing)
- [Best Practices](#best-practices)
- [File Organization](#file-organization)
- [Common Issues](#common-issues)
- [Getting Help](#getting-help)

## Quick Start

1. **Fork the repository**
2. **Copy the template**: `cp src/locales/translation-template.json src/locales/your-language-code/`
3. **Update metadata**: Edit the `_meta` section in your new file
4. **Start translating**: Replace `"TRANSLATE_HERE"` with your translations
5. **Test your translations**: Use the validation tools
6. **Submit a pull request**

## Translation Structure

The application uses a modular translation system with the following files:

- **`common.json`** - Common actions, statuses, and UI elements
- **`assets.json`** - Asset management and device-related content
- **`users.json`** - User management, authentication, and roles
- **`sites.json`** - Site and location management
- **`suppliers.json`** - Supplier and manufacturer management
- **`setup.json`** - System setup and configuration
- **`forms.json`** - Generic form elements and validation

## Getting Started

### Prerequisites

- Node.js (version 16 or higher)
- Git
- Basic knowledge of JSON format

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/industrace.git
   cd industrace/frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Create your language directory**:
   ```bash
   mkdir -p src/locales/your-language-code
   ```

4. **Copy the template**:
   ```bash
   cp src/locales/translation-template.json src/locales/your-language-code/
   ```

### Language Codes

Use standard ISO 639-1 language codes:
- `en` - English
- `it` - Italian
- `es` - Spanish
- `fr` - French
- `de` - German
- `pt` - Portuguese
- `ru` - Russian
- `zh` - Chinese
- `ja` - Japanese
- `ko` - Korean

## Translation Workflow

### Step 1: Update Metadata

Edit the `_meta` section in your translation file:

```json
{
  "_meta": {
    "language": "es",
    "native_name": "Español",
    "contributor": "Your Name",
    "status": "in_progress",
    "created_date": "2024-01-15",
    "last_updated": "2024-01-15",
    "completion_percentage": 0
  }
}
```

### Step 2: Start Translating

Replace all instances of `"TRANSLATE_HERE"` with your translations:

```json
{
  "common": {
    "actions": {
      "create": "Crear",
      "edit": "Editar",
      "delete": "Eliminar"
    }
  }
}
```

### Step 3: Validate Your Work

Run the validation script to check for issues:

```bash
npm run validate-translations
```

### Step 4: Test Locally

Start the development server to see your translations in action:

```bash
npm run dev
```

Then change the language in the application to test your translations.

## Validation and Testing

### Automatic Validation

The application includes built-in validation tools:

1. **Missing Keys Check**: Ensures all required keys are present
2. **Extra Keys Check**: Identifies unused translations
3. **JSON Format Validation**: Checks for syntax errors
4. **Placeholder Validation**: Ensures placeholders are preserved

### Manual Testing

1. **Start the development server**:
   ```bash
   npm run dev
   ```

2. **Navigate through the application** to test different sections:
   - Login page
   - Asset management
   - User management
   - Site management
   - Supplier management
   - System setup

3. **Check for**:
   - Missing translations (shows as keys)
   - Context-appropriate translations
   - Proper formatting
   - Consistent terminology

### Validation Commands

```bash
# Check for missing/extra keys
npm run validate-translations

# Check JSON syntax
npm run lint:translations

# Run full validation suite
npm run test:translations
```

## Best Practices

### Translation Guidelines

1. **Maintain Context**: Understand what each string is used for
2. **Be Consistent**: Use the same terms for the same concepts
3. **Preserve Placeholders**: Keep `{variable}` placeholders intact
4. **Respect Length**: Consider UI space constraints
5. **Use Proper Grammar**: Ensure translations are grammatically correct

### Terminology Consistency

Use consistent terms for common concepts:

| English | Your Language | Context |
|---------|---------------|---------|
| Asset | [Your term] | Device/equipment |
| Site | [Your term] | Physical location |
| Supplier | [Your term] | Vendor/provider |
| User | [Your term] | System user |
| Role | [Your term] | User permissions |

### Technical Considerations

1. **JSON Format**: Ensure valid JSON syntax
2. **Character Encoding**: Use UTF-8 encoding
3. **Line Length**: Keep lines under 120 characters
4. **Nesting**: Maintain the same structure as the English version

### Common Patterns

#### Placeholders
```json
{
  "selectedItems": "{count} elementi selezionati",
  "confirmBulkAction": "Sei sicuro di voler {action} {count} elementi?"
}
```

#### Pluralization
```json
{
  "asset": "asset",
  "assets": "asset",
  "noAssets": "Nessun asset",
  "oneAsset": "1 asset",
  "multipleAssets": "{count} asset"
}
```

## File Organization

### Directory Structure

```
src/locales/
├── en/                    # English (base language)
│   ├── common.json
│   ├── assets.json
│   ├── users.json
│   ├── sites.json
│   ├── suppliers.json
│   ├── setup.json
│   └── forms.json
├── it/                    # Italian
│   ├── common.json
│   ├── assets.json
│   └── ...
├── your-language-code/    # Your language
│   ├── common.json
│   ├── assets.json
│   └── ...
├── loader.js              # Translation loader
└── translation-template.json
```

### File Responsibilities

- **`common.json`**: Shared UI elements, actions, statuses
- **`assets.json`**: Device management, connections, communications
- **`users.json`**: Authentication, user management, roles
- **`sites.json`**: Location management, floorplans
- **`suppliers.json`**: Vendor management, contacts
- **`setup.json`**: System configuration, dashboard
- **`forms.json`**: Form elements, validation messages

## Common Issues

### Missing Translations

If you see translation keys instead of translated text:

1. Check that the key exists in your translation file
2. Verify the key path matches exactly
3. Ensure the JSON syntax is valid

### Placeholder Issues

If placeholders appear as `{variable}` in the UI:

1. Check that placeholders are preserved exactly
2. Verify the variable names match
3. Ensure no extra spaces or characters

### JSON Syntax Errors

Common JSON issues:

1. **Missing commas**: Between object properties
2. **Extra commas**: After the last property
3. **Unescaped quotes**: Use `\"` for quotes in strings
4. **Invalid characters**: Use UTF-8 encoding

### Validation Errors

If validation fails:

1. Check the error message for specific issues
2. Verify all required keys are present
3. Ensure no extra keys exist
4. Check JSON syntax

## Getting Help

### Resources

- **Translation Guidelines**: This document
- **Template File**: `src/locales/translation-template.json`
- **Base Language**: `src/locales/en/` (for reference)
- **Validation Tools**: Built into the application

### Support Channels

- **GitHub Issues**: Report bugs or request help
- **Discussions**: Ask questions in GitHub Discussions
- **Pull Requests**: Submit your translations

### Before Submitting

1. **Complete the translation**: All keys should be translated
2. **Run validation**: Ensure no errors
3. **Test locally**: Verify everything works
4. **Update metadata**: Set completion percentage to 100
5. **Write a clear description**: Explain your changes

### Pull Request Template

```markdown
## Translation: [Language Name]

### Changes Made
- Added translation for [Language Name]
- Translated all [X] files
- Updated metadata and completion status

### Testing
- [ ] All translations validated
- [ ] Tested locally in development
- [ ] No missing or extra keys
- [ ] JSON syntax is valid

### Notes
- Any special considerations or context
- Terminology decisions made
- Areas that might need review
```

## Recognition

Contributors will be recognized in:

- The application's about page
- GitHub contributors list
- Release notes
- Documentation

Thank you for contributing to making Industrace accessible to users worldwide! 