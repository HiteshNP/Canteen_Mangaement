# 🍽️ Canteen Management & Food Ordering System

A complete, beautifully designed canteen food‑ordering web application built with **Python Flask** and server‑rendered HTML templates. All pricing is in **Indian Rupees (₹)**. The app ships with rich **mock data** so every feature can be experienced end‑to‑end without any database setup.

> This README is a **reviewer walkthrough**. Follow it top‑to‑bottom to experience every single feature across the three user roles: **Customer**, **Kitchen Staff**, and **Admin**.

---

## 📑 Table of Contents

1. [Tech Stack](#-tech-stack)
2. [Quick Start](#-quick-start)
3. [Demo Login Credentials](#-demo-login-credentials)
4. [Feature Walkthrough (Reviewer Guide)](#-feature-walkthrough-reviewer-guide)
   - [A. Customer Journey](#a-customer-journey)
   - [B. Kitchen Staff Journey](#b-kitchen-staff-journey)
   - [C. Admin Journey](#c-admin-journey)
5. [Full Route Reference](#-full-route-reference)
6. [Project Structure](#-project-structure)
7. [Notes for Reviewers](#-notes-for-reviewers)

---

## 🛠 Tech Stack

| Layer      | Technology                                   |
| ---------- | -------------------------------------------- |
| Backend    | Python 3 + Flask 3.x                         |
| Templating | Jinja2 (server‑rendered HTML)                |
| Styling    | Custom CSS (fresh green/teal theme)          |
| Charts     | Chart.js (admin analytics)                   |
| State      | Flask `session` (cart, auth, mock orders)    |
| Data       | In‑memory **mock data** (no DB required)     |

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+** installed and on your PATH.

### 1. (Optional) Create a virtual environment
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 2. Install dependencies
```powershell
pip install flask
```

### 3. Run the app
```powershell
python app.py
```

### 4. Open in your browser
```
http://127.0.0.1:5000
```

> The server runs in debug mode on **port 5000**. Press `Ctrl + C` in the terminal to stop it.

---

## 🔑 Demo Login Credentials

Authentication is **mocked** — you can log in with **any email and any password**. The **Role** you select on the login screen decides which experience you get and where you land after login.

| Role            | How to log in                                              | Lands on              |
| --------------- | ---------------------------------------------------------- | --------------------- |
| 👤 Customer     | Any email + password, select **Customer**                  | Menu page             |
| 👨‍🍳 Kitchen Staff | Any email + password, select **Staff / Kitchen**        | Kitchen dashboard     |
| 🛡️ Admin        | Any email + password, select **Admin**                     | Admin dashboard       |

> 💡 Example: `rahul@demo.com` / `anything` with role **Customer**. The name shown in the app is derived from the email (e.g. `rahul@demo.com` → "Rahul").

---

## 🧭 Feature Walkthrough (Reviewer Guide)

Work through these three journeys to touch **every feature**.

### A. Customer Journey

**Goal:** Browse → add to cart → checkout → track order → view history.

1. **Landing Page** — Visit `http://127.0.0.1:5000/`.
   - See the hero section, highlights, and a **Popular Dishes** showcase (6 featured items).
   - Notice the live **cart counter** in the navbar.

2. **Browse the Menu** — Click **Menu** (or go to `/menu`).
   - **Category filter:** switch between Breakfast, Lunch, Snacks, Beverages, Desserts.
   - **Search:** type a dish name (e.g. "dosa", "biryani") to filter live.
   - **Veg / Non‑veg** indicators, **star ratings**, **prices in ₹**, and **Popular** badges.
   - Try an item marked **unavailable** (e.g. *Chole Bhature*) — it cannot be added.

3. **Add to Cart** — Click **Add** on a few items. Watch the navbar cart count increase.

4. **Manage Cart** — Open **Cart** (`/cart`).
   - **Increase / decrease** quantity, **remove** items, and see the **live total in ₹** recalculate.

5. **Log In** (required for checkout) — Click **Checkout**; you'll be redirected to the login page.
   - Log in as a **Customer** (any email/password). You'll return to checkout automatically.

6. **Checkout** — On `/checkout`:
   - Review the order summary and total.
   - Choose a **payment method**: **UPI / Card / Wallet / Cash**.
   - Click **Place Order** to generate a unique **Order ID** and **token number**.

7. **Track Your Order** — You're redirected to the **order tracking** page.
   - Follow the **status stepper**: `Placed → Preparing → Ready → Served`.
   - See order items, totals, token, and payment method.

8. **Order History** — Open **My Orders** (`/orders`) to see all orders placed under your name.

9. **Log Out** — Use the navbar menu to log out and confirm the session clears.

---

### B. Kitchen Staff Journey

**Goal:** View incoming orders and advance them through the kitchen workflow.

1. **Log in as Staff** — On the login page, select role **Staff / Kitchen**. You land on the **Kitchen Dashboard** (`/kitchen`).

2. **Live Order Queue** — See all **active orders** (anything not yet *Served*) as cards with:
   - Order ID, token, customer name, item list, total, payment type, and elapsed time.

3. **Advance an Order** — Click the **advance** button on a card to move it to the next stage:
   `Placed → Preparing → Ready → Served`.
   - Advance an order all the way to **Served** and watch it move into the **Recently Served** list.

4. **Cross‑check with Customer view** — Tip: place an order as a Customer (Journey A), then log in as Staff to see that exact order appear and advance it. Reopen the customer's tracking page to see the updated status.

---

### C. Admin Journey

**Goal:** Review analytics and manage menu availability.

1. **Log in as Admin** — On the login page, select role **Admin**. You land on the **Admin Dashboard** (`/admin`).

2. **KPI Cards** — Review headline stats: **total revenue (₹)**, **total orders**, **average order value (₹)**, and **menu item count**.

3. **Analytics Charts** (Chart.js):
   - **Weekly Revenue** (Mon–Sun) bar/line chart.
   - **Hourly Orders** distribution (8 AM–5 PM).
   - **Top‑Selling Items** with units sold and revenue.

4. **Operational Widgets:**
   - **Recent Orders** feed.
   - **Low‑Stock Alerts** — items with stock ≤ 25 are flagged.

5. **Menu Management** — Open **Manage Menu** (`/admin/menu`).
   - See the full catalogue with price, category, stock, and availability.
   - **Toggle availability** on any item. Then switch to the **Customer menu** to confirm that item becomes (un)orderable — demonstrating live admin → customer impact.

---

## 🗺 Full Route Reference

| Route                              | Method    | Role        | Description                              |
| ---------------------------------- | --------- | ----------- | ---------------------------------------- |
| `/`                                | GET       | Public      | Landing page with popular dishes         |
| `/menu`                            | GET       | Public      | Menu with category filter + search       |
| `/cart`                            | GET       | Public      | View cart                                |
| `/cart/add/<id>`                   | POST      | Public      | Add item to cart                         |
| `/cart/update/<id>`                | POST      | Public      | Increase / decrease / remove cart item   |
| `/checkout`                        | GET/POST  | Customer    | Place an order (login required)          |
| `/order/<order_id>`                | GET       | Customer    | Track an order's status                  |
| `/orders`                          | GET       | Customer    | Order history                            |
| `/login`                           | GET/POST  | Public      | Mock login (role selector)               |
| `/signup`                          | GET/POST  | Public      | Mock signup (creates a customer)         |
| `/logout`                          | GET       | Any         | Clear session                            |
| `/kitchen`                         | GET       | Staff       | Kitchen order queue                      |
| `/kitchen/advance/<order_id>`      | POST      | Staff       | Advance order to next status             |
| `/admin`                           | GET       | Admin       | Analytics dashboard                      |
| `/admin/menu`                      | GET       | Admin       | Menu management                          |
| `/admin/menu/toggle/<id>`          | POST      | Admin       | Toggle item availability                 |

---

## 📂 Project Structure

```
Canteen Management/
├── app.py                      # Flask backend: routes, mock data, helpers
├── SYNOPSIS.md                 # Problem statement, solution & execution plan
├── README.md                   # This file
├── static/
│   ├── css/
│   │   └── style.css           # Fresh green/teal theme
│   └── js/
│       └── main.js             # Client interactions
└── templates/
    ├── base.html               # Shared layout (navbar, footer, flash messages)
    ├── landing.html            # Landing page
    ├── menu.html               # Menu + filters + search
    ├── cart.html               # Cart management
    ├── checkout.html           # Checkout + payment
    ├── order_tracking.html     # Order status stepper
    ├── orders.html             # Order history
    ├── login.html              # Login (role selector)
    ├── signup.html             # Signup
    ├── kitchen.html            # Kitchen dashboard
    ├── admin_dashboard.html    # Admin analytics
    └── admin_menu.html         # Admin menu management
```

---

## 📝 Notes for Reviewers

- **No database required** — all data lives in memory as mock data in `app.py`. Restarting the server resets everything (new orders, availability toggles, etc.).
- **Auth is mocked** — any credentials work; the **role selector** drives the experience. There is no real password checking (by design, for easy demoing).
- **Currency** — every price and total is displayed in **INR (₹)** via a custom `inr` template filter.
- **Best demo path** — place an order as a **Customer**, advance it as **Kitchen Staff**, then review it in the **Admin** dashboard to see all three roles interact with the same order.
- For the project's problem statement, proposed solution, and execution plan, see [SYNOPSIS.md](SYNOPSIS.md).

---

Enjoy exploring the system! 🎉
