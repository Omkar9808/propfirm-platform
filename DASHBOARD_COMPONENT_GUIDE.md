# Dashboard Component Reference Guide

## 📚 Component Documentation

This guide provides detailed documentation for all dashboard components.

---

## Core Components

### 1. DashboardLayout

**File:** `dashboard/DashboardLayout.tsx`

**Purpose:** Main layout wrapper that orchestrates sidebar, topbar, and content

**Props:** None (root component)

**State:**
```javascript
- sidebarOpen: boolean
- mobileMenuOpen: boolean
```

**Usage:**
```jsx
<DashboardLayout />
```

**Features:**
- Manages sidebar state
- Handles mobile menu overlay
- Responsive layout switching
- Context provider wrapper

---

### 2. Sidebar

**File:** `dashboard/Sidebar.tsx`

**Purpose:** Navigation sidebar with collapsible functionality

**Props:**
```typescript
{
  isOpen: boolean;
  toggleSidebar: () => void;
  mobileOpen: boolean;
  setMobileOpen: (open: boolean) => void;
}
```

**Features:**
- Desktop collapsible sidebar (256px ↔ 80px)
- Mobile slide-out menu
- Active state highlighting
- Hover tooltips
- Smooth Framer Motion animations
- Logout functionality

**Menu Structure:**
```javascript
const menuItems = [
  { icon: 'fa-home', label: 'Dashboard', path: '/dashboard' },
  { icon: 'fa-chart-line', label: 'Practice Trading', path: '/dashboard/practice' },
  // ... more items
];
```

**Customization:**
- Add menu items by extending the array
- Change icons using Font Awesome classes
- Modify colors in Tailwind classes

---

### 3. Topbar

**File:** `dashboard/Topbar.tsx`

**Purpose:** Top navigation bar displaying account metrics

**Props:**
```typescript
{
  toggleSidebar: () => void;
  toggleMobileMenu: () => void;
  account: AccountData;
}
```

**Sections:**
1. **Left Side:**
   - Mobile hamburger menu
   - Sidebar toggle button
   - Account selector dropdown

2. **Right Side:**
   - Notification bell with badge
   - User avatar
   - Username display

3. **Metrics Bar:**
   - Balance
   - Daily Drawdown
   - Max Drawdown
   - Profit Target %
   - Phase indicator

**Helper Functions:**
```javascript
formatCurrency(value) // Formats as USD
formatPercent(value)  // Formats as percentage
```

---

## Dashboard Content Components

### 4. DashboardContent

**File:** `components/dashboard/DashboardContent.js`

**Purpose:** Main dashboard content area with all widgets

**Props:**
```typescript
{
  account: AccountData;
}
```

**Sections Rendered:**
1. Welcome header
2. Account overview cards (4 cards)
3. Progress indicators (3 cards)
4. Equity chart + Quick actions
5. Recent trades + Notifications
6. Performance statistics

**Layout:**
```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
  {/* Cards go here */}
</div>
```

---

### 5. MetricCard

**File:** `components/dashboard/MetricCard.js`

**Purpose:** Display individual metric with icon and value

**Props:**
```typescript
{
  icon: string;        // Font Awesome icon class
  title: string;       // Card title
  value: string;       // Main value to display
  subtext: string;     // Additional info below value
  color: string;       // Gradient class (e.g., "from-green-500 to-emerald-600")
  delay: number;       // Animation delay in seconds
}
```

**Usage Example:**
```jsx
<MetricCard
  icon="fa-wallet"
  title="Account Balance"
  value="$5,000.00"
  subtext="Initial: $5,000"
  color="from-green-500 to-emerald-600"
  delay={0.1}
/>
```

**Features:**
- Hover lift animation
- Gradient icon background
- Staggered entrance
- Glow effect on hover

---

### 6. ProgressCard

**File:** `components/dashboard/ProgressCard.js`

**Purpose:** Display progress bar with metrics

**Props:**
```typescript
{
  title: string;
  current: number;
  target: number;
  percent: number;
  color: string;      // Text color class
  icon: string;       // Font Awesome icon
}
```

**Usage Example:**
```jsx
<ProgressCard
  title="Profit Target"
  current={247}
  target={800}
  percent={30.9}
  color="text-green-400"
  icon="fa-bullseye"
/>
```

**Features:**
- Animated progress bar fill
- Current vs target display
- Color-coded indicators
- Icon association

---

### 7. EquityChart

**File:** `components/dashboard/EquityChart.js`

**Purpose:** Display equity performance over time

**Props:**
```typescript
{
  data: Array<{
    date: string;
    equity: number;
    balance: number;
  }>;
}
```

**Chart Type:** AreaChart with gradient fill

**Libraries Used:**
- Recharts for charting
- Framer Motion for animations

**Features:**
- Responsive container
- Interactive tooltips
- Gradient fill effect
- Grid lines
- Custom styling

**Customization:**
```jsx
// Change chart type
<AreaChart> → <LineChart> or <BarChart>

// Modify colors
stopColor="#00ff9d" // Change gradient color

// Adjust height
className="h-80" // Change to h-64 or h-96
```

---

### 8. RecentTradesTable

**File:** `components/dashboard/RecentTradesTable.js`

**Purpose:** Display recent trading history

**Props:**
```typescript
{
  trades: Array<{
    symbol: string;
    direction: 'BUY' | 'SELL';
    entry: number;
    exit: number;
    profit: number;
    date: string;
    status: string;
  }>;
}
```

**Columns:**
1. Symbol
2. Direction (with colored badges)
3. Entry Price
4. Exit Price
5. Profit/Loss (color-coded)
6. Date
7. Status

**Features:**
- Staggered row animations
- Hover effects
- Color-coded direction badges
- Conditional profit coloring

**Styling:**
```jsx
// BUY badge
className="bg-green-500/20 text-green-400"

// SELL badge  
className="bg-red-500/20 text-red-400"

// Positive profit
className="text-green-400"

// Negative profit
className="text-red-400"
```

---

### 9. NotificationsPanel

**File:** `components/dashboard/NotificationsPanel.js`

**Purpose:** Display system notifications

**Props:**
```typescript
{
  notifications: Array<{
    id: number;
    type: 'success' | 'warning' | 'info';
    message: string;
    time: string;
  }>;
}
```

**Icon Mapping:**
```javascript
success → fa-check-circle (green)
warning → fa-exclamation-triangle (yellow)
info → fa-info-circle (blue)
```

**Features:**
- Icon coding by type
- Timestamp display
- Staggered appearance animation
- Clean card design

---

### 10. QuickActions

**File:** `components/dashboard/QuickActions.js`

**Purpose:** Provide quick access to common actions

**Actions Array:**
```javascript
[
  { 
    icon: 'fa-play', 
    label: 'Start Practice Trade', 
    color: 'from-green-500 to-emerald-600' 
  },
  // ... more actions
]
```

**Features:**
- Gradient backgrounds
- Icon + text layout
- Hover scale animation
- Tap feedback
- 2-column grid

**Customization:**
Add new actions by extending the array.

---

## Data Structures

### AccountData Object

```typescript
interface AccountData {
  // Basic Info
  id: string;
  name: string;
  accountSize: number;
  status: string;
  
  // Financial Metrics
  balance: number;
  equity: number;
  floatingPnL: number;
  profit: number;
  
  // Risk Metrics
  profitTarget: number;
  maxDailyLoss: number;
  dailyLoss: number;
  maxDrawdown: number;
  drawdown: number;
  
  // Time Tracking
  tradingDays: number;
  totalDays: number;
  startDate: string;
  
  // Performance Stats
  winRate: number;
  wins: number;
  losses: number;
  profitFactor: number;
  disciplineScore: number;
  avgTradeDuration: number;
  profitPerTrade: number;
  
  // Arrays
  equityHistory: EquityData[];
  recentTrades: TradeData[];
  notifications: NotificationData[];
  
  // UI State
  sidebarOpen: boolean;
  isUpdating: boolean;
}
```

### EquityData

```typescript
{
  date: string;
  equity: number;
  balance: number;
}
```

### TradeData

```typescript
{
  symbol: string;
  direction: 'BUY' | 'SELL';
  entry: number;
  exit: number;
  profit: number;
  date: string;
  status: 'Closed' | 'Open';
}
```

### NotificationData

```typescript
{
  id: number;
  type: 'success' | 'warning' | 'info';
  message: string;
  time: string;
}
```

---

## Context API

### AccountContext

**Location:** Global context in dashboard-new.html

**Provider:** AccountProvider

**Value:**
```javascript
{
  selectedAccountId: string;
  selectedAccount: AccountData;
  switchAccount: (id: string) => void;
  accounts: Object;
  isUpdating: boolean;
  sidebarOpen: boolean;
  toggleSidebar: () => void;
}
```

**Usage:**
```jsx
import { useContext } from 'react';
import { AccountContext } from './AccountContext';

const MyComponent = () => {
  const { selectedAccount, switchAccount } = useContext(AccountContext);
  
  return <div>{/* Use account data */}</div>;
};
```

---

## Animation Variants

### Framer Motion Presets

**Fade In:**
```javascript
initial={{ opacity: 0 }}
animate={{ opacity: 1 }}
transition={{ duration: 0.4 }}
```

**Slide Up:**
```javascript
initial={{ opacity: 0, y: 20 }}
animate={{ opacity: 1, y: 0 }}
transition={{ duration: 0.5 }}
```

**Scale In:**
```javascript
initial={{ opacity: 0, scale: 0.9 }}
animate={{ opacity: 1, scale: 1 }}
transition={{ duration: 0.3 }}
```

**Stagger Children:**
```javascript
// Parent
variants={{
  open: { transition: { staggerChildren: 0.1 } }
}}

// Child
variants={{
  open: { opacity: 1, y: 0 },
  closed: { opacity: 0, y: 20 }
}}
```

---

## Styling Guide

### Tailwind Classes Reference

**Backgrounds:**
```css
bg-[#0E0E11]        // Main background
bg-[#0a0a0c]        // Darker background
bg-gray-900/50      // Semi-transparent gray
```

**Borders:**
```css
border-white/10     // Subtle white border
border-[#00ff9d]/30 // Green accent border
```

**Text Colors:**
```css
text-white          // Primary text
text-gray-400       // Secondary text
text-[#00ff9d]      // Brand green
text-green-400      // Success
text-red-400        // Danger
text-yellow-400     // Warning
```

**Gradients:**
```css
from-green-500 to-emerald-600
from-blue-500 to-cyan-600
from-purple-500 to-pink-600
```

**Spacing:**
```css
p-6                 // 24px padding
m-4                 // 16px margin
gap-6               // 24px gap
```

---

## Common Patterns

### Card Layout Pattern

```jsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ delay: 0.1 }}
  className="bg-gradient-to-br from-gray-900/50 to-gray-800/50 rounded-xl p-6 border border-white/10"
>
  <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
    <i className="fas fa-icon text-color"></i>
    Title
  </h3>
  {/* Content */}
</motion.div>
```

### Grid Layout Pattern

```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
  {/* Cards */}
</div>
```

### Table Pattern

```jsx
<table className="w-full">
  <thead>
    <tr className="text-left text-gray-400 text-sm border-b border-white/10">
      <th className="pb-3 pr-4">Header</th>
    </tr>
  </thead>
  <tbody>
    {data.map((item, index) => (
      <motion.tr
        key={index}
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: index * 0.05 }}
        className="border-b border-white/5 hover:bg-white/5"
      >
        <td className="py-3 pr-4">Content</td>
      </motion.tr>
    ))}
  </tbody>
</table>
```

---

## Best Practices

### Performance
1. Use React.memo for static components
2. Implement virtual scrolling for large lists
3. Lazy load heavy components
4. Debounce resize handlers

### Code Organization
1. Keep components small and focused
2. Extract reusable logic to hooks
3. Use PropTypes or TypeScript
4. Document props and state

### Accessibility
1. Add aria-labels to buttons
2. Ensure color contrast ratios
3. Support keyboard navigation
4. Use semantic HTML

### Testing
1. Test on multiple browsers
2. Verify responsive behavior
3. Check animation performance
4. Validate form inputs

---

## Troubleshooting

### Component Not Rendering

**Check:**
1. Is React loaded? (check CDN)
2. Are props being passed correctly?
3. Is there a JavaScript error in console?
4. Is the component imported/exported correctly?

### Animations Not Working

**Check:**
1. Is Framer Motion loaded?
2. Are initial/animate props set?
3. Is transition duration > 0?
4. Any CSS overriding transforms?

### Styles Not Applying

**Check:**
1. Is TailwindCSS loaded?
2. Are class names spelled correctly?
3. Any CSS specificity conflicts?
4. Browser cache cleared?

---

## Extension Examples

### Adding a New Metric Card

```jsx
<MetricCard
  icon="fa-users"
  title="Social Score"
  value="87"
  subtext="Top 10% of traders"
  color="from-pink-500 to-rose-600"
  delay={0.5}
/>
```

### Adding a New Chart

```jsx
<div className="lg:col-span-1">
  <PieChart width={400} height={300}>
    <Pie
      data={data}
      cx={200}
      cy={150}
      outerRadius={100}
      fill="#00ff9d"
      dataKey="value"
    />
  </PieChart>
</div>
```

### Adding a New Menu Item

```javascript
{ 
  icon: 'fa-gift', 
  label: 'Rewards', 
  path: '/dashboard/rewards' 
}
```

---

## Resources

### Documentation Links
- [React Docs](https://react.dev)
- [Framer Motion](https://www.framer.com/motion/)
- [Recharts](https://recharts.org)
- [TailwindCSS](https://tailwindcss.com)
- [Font Awesome](https://fontawesome.com)

### Code Examples
See existing components in `dashboard-new.html` for reference implementations.

---

*Last Updated: March 7, 2026*
*Version: 1.0.0*
