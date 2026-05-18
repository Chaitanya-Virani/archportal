---
name: Precision & Structure
colors:
  surface: '#f9f9ff'
  surface-dim: '#cfdaf2'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f0f3ff'
  surface-container: '#e7eeff'
  surface-container-high: '#dee8ff'
  surface-container-highest: '#d8e3fb'
  on-surface: '#111c2d'
  on-surface-variant: '#464554'
  inverse-surface: '#263143'
  inverse-on-surface: '#ecf1ff'
  outline: '#767586'
  outline-variant: '#c7c4d7'
  surface-tint: '#494bd6'
  primary: '#4648d4'
  on-primary: '#ffffff'
  primary-container: '#6063ee'
  on-primary-container: '#fffbff'
  inverse-primary: '#c0c1ff'
  secondary: '#6b38d4'
  on-secondary: '#ffffff'
  secondary-container: '#8455ef'
  on-secondary-container: '#fffbff'
  tertiary: '#904900'
  on-tertiary: '#ffffff'
  tertiary-container: '#b55d00'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e1e0ff'
  primary-fixed-dim: '#c0c1ff'
  on-primary-fixed: '#07006c'
  on-primary-fixed-variant: '#2f2ebe'
  secondary-fixed: '#e9ddff'
  secondary-fixed-dim: '#d0bcff'
  on-secondary-fixed: '#23005c'
  on-secondary-fixed-variant: '#5516be'
  tertiary-fixed: '#ffdcc5'
  tertiary-fixed-dim: '#ffb783'
  on-tertiary-fixed: '#301400'
  on-tertiary-fixed-variant: '#703700'
  background: '#f9f9ff'
  on-background: '#111c2d'
  surface-variant: '#d8e3fb'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 8px
  container-padding: 24px
  gutter: 24px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 24px
---

## Brand & Style
The design system is engineered for the high-stakes environment of architectural project management. It balances technical rigor with administrative clarity, evoking an atmosphere of professional reliability, structural integrity, and architectural precision.

The design style is **Corporate / Modern** with a strong emphasis on functional minimalism. It utilizes a structured layout and a sophisticated slate-based palette to ensure that complex data—blueprints, timelines, and budgets—remains the primary focus. The aesthetic avoids decorative flourish in favor of utilitarian excellence, mirroring the discipline of the architects who use the platform.

## Colors
The palette is rooted in a "Slate" foundation to provide a neutral, professional backdrop that reduces eye strain during long working sessions. 

- **Primary & Secondary Accents:** Indigo and Violet are used sparingly for primary actions, active states, and brand moments, providing a modern "tech-forward" feel against the architectural grays.
- **Surface Logic:** The sidebar utilizes deep slates (`#0F172A`) to create a clear vertical hierarchy, separating navigation from the work surface (`#F1F5F9`).
- **Semantic Clarity:** Standardized colors for Success, Warning, Danger, and Info ensure that project statuses (e.g., permit approvals or budget overruns) are instantly recognizable.

## Typography
The typography system relies on **Inter** for its exceptional legibility in data-heavy interfaces and **JetBrains Mono** for technical strings or coordinate data.

- **Numerics:** Use tabular figures for financial tables to ensure Indian Rupee (₹) amounts align vertically.
- **Formatting:** Dates must consistently follow the `DD MMM YYYY` format (e.g., 12 OCT 2023) to avoid international ambiguity.
- **Hierarchy:** High contrast between Slate-800 body text and Slate-500 muted text is used to denote secondary information like metadata or timestamps.

## Layout & Spacing
This design system employs a **Fixed-Fluid Hybrid Grid**. The sidebar remains fixed at 280px, while the main content area utilizes a fluid 12-column grid.

- **Generous Whitespace:** A standard container padding of 24px is enforced to prevent the UI from feeling cramped, reflecting the "breathing room" found in architectural drafts.
- **Rhythm:** All spatial dimensions follow an 8px baseline. Elements are stacked using 8px (tight), 16px (medium), or 24px (loose) increments.
- **Breakpoints:** 
  - **Desktop:** 1280px+ (Full sidebar + 12 columns)
  - **Tablet:** 768px - 1279px (Collapsed sidebar + 8 columns)
  - **Mobile:** <767px (Bottom navigation or Hamburger + 4 columns, 16px margins)

## Elevation & Depth
Depth is handled through **Low-Contrast Outlines** and **Subtle Ambient Shadows**. 

- **Flat Foundation:** Surfaces are primarily defined by their background colors and 1px borders (`#CBD5E1`).
- **Shadows:** A singular, ultra-soft shadow (`0 1px 3px rgba(0,0,0,0.08)`) is used for interactive cards and dropdown menus to suggest hoverability without breaking the flat aesthetic.
- **Tonal Layers:** High-priority modals use a slightly more aggressive elevation, but background dimming (overlay) is the preferred method for maintaining focus rather than heavy drop shadows.

## Shapes
The shape language is "Soft-Technical." It uses variations in corner radii to distinguish between structural containers and actionable elements.

- **Containers & Inputs:** A mid-level radius of 8px is used for cards, modals, and text fields to provide a modern, approachable feel.
- **Interactive Elements:** Buttons utilize a sharper 4px radius, giving them a more "tool-like" and precise appearance compared to the layout containers.
- **Icons:** Use linear, 2px stroke icons to match the weight of the Inter typeface.

## Components
- **Buttons:** 4px radius. Primary buttons use Indigo-500 with white text. Secondary buttons use a Slate-300 border with Slate-800 text.
- **Inputs:** 8px radius. Use a 1px border (`#CBD5E1`). On focus, the border shifts to Indigo-500 with a subtle 2px outer glow.
- **Cards:** 8px radius. Background is pure white (`#FFFFFF`) with a 1px border and the defined ambient shadow. Padding is strictly 24px.
- **Chips/Badges:** Pill-shaped (fully rounded). Used for project tags or status indicators. Use 10% opacity of the semantic color for the background and 100% for the text.
- **Data Tables:** No outer border on the table itself. Rows are separated by 1px horizontal lines (`#CBD5E1`). Header row uses the `label-md` type style with a light gray background (`#F8FAFC`).
- **Sidebar Items:** High-contrast hover states. Active items use a left-edge Indigo-500 border-accent (4px width).