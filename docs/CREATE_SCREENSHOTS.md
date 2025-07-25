# Creating Screenshots and GIFs for Industrace

This guide helps you create visual content to showcase Industrace features.

## 🛠️ Tools Needed

### For Screenshots:
- **macOS**: Built-in Screenshot app or `Cmd + Shift + 4`
- **Windows**: Snipping Tool or `Win + Shift + S`
- **Linux**: `gnome-screenshot` or `flameshot`

### For GIF Animations:
- **ScreenToGif** (Windows): https://www.screentogif.com/
- **Gifox** (macOS): https://gifox.io/
- **Peek** (Linux): https://github.com/phw/peek
- **Online**: https://www.screentogif.com/ (browser-based)

## 📸 Screenshots to Create

### 1. Dashboard Overview (`dashboard-overview.png`)
- **What to show**: Main dashboard with asset cards, risk scores, system status
- **Size**: 1920x1080 or 1440x900
- **Focus**: Overall system overview and key metrics

### 2. Asset Details (`asset-details.png`)
- **What to show**: Detailed asset view with tabs (Info, Interfaces, Connections, Documents)
- **Size**: 1920x1080
- **Focus**: Rich information display and navigation

### 3. Audit Trail (`audit-trail.png`)
- **What to show**: Audit logs page with activity history
- **Size**: 1920x1080
- **Focus**: Compliance and tracking features

### 4. Mobile View (`mobile-view.png`)
- **What to show**: Application on mobile device or browser mobile view
- **Size**: 375x667 (iPhone) or 360x640 (Android)
- **Focus**: Responsive design and mobile usability

## 🎬 GIF Animations to Create

### 1. Asset Management (`asset-management.gif`)
- **Duration**: 15-20 seconds
- **Actions to record**:
  1. Navigate to Assets page
  2. Create a new asset
  3. Fill in asset details
  4. Add interfaces
  5. Save and view the asset
- **Focus**: Complete asset creation workflow

### 2. Network Topology (`network-topology.gif`)
- **Duration**: 20-25 seconds
- **Actions to record**:
  1. Open Network Topology page
  2. Show interactive graph
  3. Zoom in/out on connections
  4. Click on assets to show details
  5. Highlight communication paths
- **Focus**: Interactive network visualization

### 3. User Management (`user-management.gif`)
- **Duration**: 15-20 seconds
- **Actions to record**:
  1. Navigate to Users page
  2. Create a new user
  3. Assign roles and permissions
  4. Show role configuration
  5. Demonstrate access control
- **Focus**: RBAC system and user administration

### 4. Floor Plan (`floor-plan.gif`)
- **Duration**: 15-20 seconds
- **Actions to record**:
  1. Open Floor Plan page
  2. Upload a floor plan image
  3. Place assets on the plan
  4. Show asset positioning
  5. Demonstrate interactive features
- **Focus**: Visual asset placement and mapping

## 🎯 Best Practices

### Screenshots:
- Use consistent resolution (1920x1080 recommended)
- Ensure good lighting and contrast
- Hide sensitive data (emails, IPs, etc.)
- Use descriptive filenames
- Optimize for web (compress if needed)

### GIF Animations:
- Keep duration under 30 seconds
- Use smooth, deliberate movements
- Highlight key features clearly
- Avoid rapid mouse movements
- Use consistent frame rate (10-15 fps)
- Optimize file size (under 5MB if possible)

## 📁 File Organization

Save all files in `docs/images/` with these naming conventions:
- Screenshots: `feature-name.png`
- GIFs: `feature-name.gif`
- Use kebab-case for filenames

## 🔄 Updating README

After creating the images, update the README.md file to reference the correct filenames and add appropriate descriptions.

## 🚀 Publishing

Once all images are created:
1. Add them to the repository
2. Update README.md with correct paths
3. Commit and push changes
4. Verify images display correctly on GitHub

## 📝 Example Workflow

```bash
# 1. Start the application
make dev

# 2. Create screenshots and GIFs
# (Use your preferred tools)

# 3. Save files to docs/images/

# 4. Update README.md if needed

# 5. Commit changes
git add docs/images/
git commit -m "docs: add screenshots and demo GIFs"
git push origin main
```

## 🎨 Design Tips

- **Consistency**: Use same browser, theme, and window size
- **Clarity**: Focus on one feature per image/GIF
- **Professional**: Clean, uncluttered interface
- **Accessible**: Good contrast and readable text
- **Modern**: Show the application's contemporary design 