"""
Canteen Management & Food Ordering System
Flask backend with mock data. All prices in INR (₹).
"""
from __future__ import annotations

import random
from datetime import datetime, timedelta
from functools import wraps

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

app = Flask(__name__)
app.secret_key = "canteen-management-secret-key-demo"


# ---------------------------------------------------------------------------
# Mock data
# ---------------------------------------------------------------------------

CATEGORIES = [
    {"id": "breakfast", "name": "Breakfast", "icon": "🍳"},
    {"id": "lunch", "name": "Lunch", "icon": "🍛"},
    {"id": "snacks", "name": "Snacks", "icon": "🍟"},
    {"id": "beverages", "name": "Beverages", "icon": "☕"},
    {"id": "desserts", "name": "Desserts", "icon": "🍰"},
]

MENU_ITEMS = [
    # Breakfast
    {"id": 1, "name": "Masala Dosa", "category": "breakfast", "price": 60,
     "desc": "Crispy rice crepe stuffed with spiced potato masala, served with sambar & chutney.",
     "img": "https://images.unsplash.com/photo-1630383249896-424e482df921?w=500",
     "veg": True, "rating": 4.6, "available": True, "stock": 40, "popular": True},
    {"id": 2, "name": "Idli Vada Combo", "category": "breakfast", "price": 50,
     "desc": "Two soft steamed idlis and a crispy medu vada with coconut chutney.",
     "img": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=500",
     "veg": True, "rating": 4.4, "available": True, "stock": 35, "popular": False},
    {"id": 3, "name": "Poha", "category": "breakfast", "price": 40,
     "desc": "Flattened rice cooked with onions, peanuts, curry leaves and lemon.",
     "img": "https://images.unsplash.com/photo-1626500155537-9c3f6d1c5c5b?w=500",
     "veg": True, "rating": 4.2, "available": True, "stock": 25, "popular": False},
    {"id": 4, "name": "Aloo Paratha", "category": "breakfast", "price": 55,
     "desc": "Whole-wheat flatbread stuffed with spiced potato, served with curd & pickle.",
     "img": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500",
     "veg": True, "rating": 4.7, "available": True, "stock": 30, "popular": True},

    # Lunch
    {"id": 5, "name": "Veg Thali", "category": "lunch", "price": 120,
     "desc": "Wholesome platter: 2 sabzi, dal, rice, 3 rotis, salad, papad & sweet.",
     "img": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=500",
     "veg": True, "rating": 4.8, "available": True, "stock": 50, "popular": True},
    {"id": 6, "name": "Paneer Butter Masala", "category": "lunch", "price": 140,
     "desc": "Cottage cheese cubes in a rich, creamy tomato gravy. Served with rice/roti.",
     "img": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=500",
     "veg": True, "rating": 4.7, "available": True, "stock": 40, "popular": True},
    {"id": 7, "name": "Chicken Biryani", "category": "lunch", "price": 180,
     "desc": "Fragrant basmati rice layered with spiced chicken, served with raita.",
     "img": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=500",
     "veg": False, "rating": 4.9, "available": True, "stock": 45, "popular": True},
    {"id": 8, "name": "Rajma Chawal", "category": "lunch", "price": 100,
     "desc": "Red kidney beans curry served over steamed basmati rice.",
     "img": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=500",
     "veg": True, "rating": 4.5, "available": True, "stock": 38, "popular": False},
    {"id": 9, "name": "Chole Bhature", "category": "lunch", "price": 90,
     "desc": "Spiced chickpea curry with two fluffy deep-fried bhature.",
     "img": "https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=500",
     "veg": True, "rating": 4.6, "available": False, "stock": 0, "popular": False},

    # Snacks
    {"id": 10, "name": "Samosa (2 pcs)", "category": "snacks", "price": 30,
     "desc": "Crispy pastry filled with spiced potato and peas.",
     "img": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500",
     "veg": True, "rating": 4.5, "available": True, "stock": 60, "popular": True},
    {"id": 11, "name": "Veg Sandwich", "category": "snacks", "price": 45,
     "desc": "Grilled sandwich with fresh veggies, cheese and mint chutney.",
     "img": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=500",
     "veg": True, "rating": 4.3, "available": True, "stock": 40, "popular": False},
    {"id": 12, "name": "French Fries", "category": "snacks", "price": 70,
     "desc": "Golden crispy fries tossed with peri-peri seasoning.",
     "img": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=500",
     "veg": True, "rating": 4.4, "available": True, "stock": 50, "popular": True},
    {"id": 13, "name": "Pav Bhaji", "category": "snacks", "price": 80,
     "desc": "Spiced mashed-vegetable curry with buttered pav buns.",
     "img": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=500",
     "veg": True, "rating": 4.7, "available": True, "stock": 35, "popular": False},

    # Beverages
    {"id": 14, "name": "Masala Chai", "category": "beverages", "price": 20,
     "desc": "Hot Indian spiced tea brewed with milk and aromatic spices.",
     "img": "https://images.unsplash.com/photo-1561336313-0bd5e0b27ec8?w=500",
     "veg": True, "rating": 4.8, "available": True, "stock": 100, "popular": True},
    {"id": 15, "name": "Filter Coffee", "category": "beverages", "price": 25,
     "desc": "South-Indian style strong filter coffee with frothy milk.",
     "img": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=500",
     "veg": True, "rating": 4.7, "available": True, "stock": 80, "popular": False},
    {"id": 16, "name": "Fresh Lime Soda", "category": "beverages", "price": 35,
     "desc": "Refreshing lime soda — sweet, salted or mixed.",
     "img": "https://images.unsplash.com/photo-1437418747212-8d9709afab22?w=500",
     "veg": True, "rating": 4.5, "available": True, "stock": 60, "popular": False},
    {"id": 17, "name": "Mango Lassi", "category": "beverages", "price": 50,
     "desc": "Thick, creamy yogurt smoothie blended with sweet mango.",
     "img": "https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=500",
     "veg": True, "rating": 4.6, "available": True, "stock": 45, "popular": True},

    # Desserts
    {"id": 18, "name": "Gulab Jamun (2 pcs)", "category": "desserts", "price": 40,
     "desc": "Soft milk-solid dumplings soaked in rose-cardamom sugar syrup.",
     "img": "https://images.unsplash.com/photo-1602492638740-96c0d6c6f3f4?w=500",
     "veg": True, "rating": 4.8, "available": True, "stock": 50, "popular": True},
    {"id": 19, "name": "Ice Cream Scoop", "category": "desserts", "price": 45,
     "desc": "Choice of vanilla, chocolate or strawberry.",
     "img": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=500",
     "veg": True, "rating": 4.5, "available": True, "stock": 40, "popular": False},
    {"id": 20, "name": "Rasmalai (2 pcs)", "category": "desserts", "price": 55,
     "desc": "Soft paneer discs in saffron-flavoured sweetened milk.",
     "img": "https://images.unsplash.com/photo-1605197788044-5a32c7078486?w=500",
     "veg": True, "rating": 4.7, "available": True, "stock": 30, "popular": False},
]

ORDER_STATUSES = ["Placed", "Preparing", "Ready", "Served"]

# Mock live/historical orders (used by kitchen + admin + order history)
MOCK_ORDERS = [
    {"id": "ORD1042", "token": "A12", "customer": "Rahul Sharma", "status": "Preparing",
     "items": [{"name": "Chicken Biryani", "qty": 1, "price": 180},
               {"name": "Mango Lassi", "qty": 1, "price": 50}],
     "total": 230, "payment": "UPI", "time": datetime.now() - timedelta(minutes=8)},
    {"id": "ORD1041", "token": "A11", "customer": "Priya Nair", "status": "Placed",
     "items": [{"name": "Veg Thali", "qty": 1, "price": 120},
               {"name": "Masala Chai", "qty": 2, "price": 20}],
     "total": 160, "payment": "Wallet", "time": datetime.now() - timedelta(minutes=4)},
    {"id": "ORD1040", "token": "A10", "customer": "Amit Patel", "status": "Ready",
     "items": [{"name": "Masala Dosa", "qty": 2, "price": 60},
               {"name": "Filter Coffee", "qty": 2, "price": 25}],
     "total": 170, "payment": "Card", "time": datetime.now() - timedelta(minutes=15)},
    {"id": "ORD1039", "token": "A09", "customer": "Sneha Reddy", "status": "Served",
     "items": [{"name": "Paneer Butter Masala", "qty": 1, "price": 140},
               {"name": "Gulab Jamun (2 pcs)", "qty": 1, "price": 40}],
     "total": 180, "payment": "UPI", "time": datetime.now() - timedelta(minutes=45)},
    {"id": "ORD1038", "token": "A08", "customer": "Vikram Singh", "status": "Served",
     "items": [{"name": "Pav Bhaji", "qty": 1, "price": 80},
               {"name": "Fresh Lime Soda", "qty": 1, "price": 35}],
     "total": 115, "payment": "Cash", "time": datetime.now() - timedelta(hours=1, minutes=10)},
]

# Analytics mock data (admin dashboard)
TOP_SELLING = [
    {"name": "Chicken Biryani", "sold": 142, "revenue": 25560},
    {"name": "Veg Thali", "sold": 128, "revenue": 15360},
    {"name": "Masala Chai", "sold": 320, "revenue": 6400},
    {"name": "Paneer Butter Masala", "sold": 96, "revenue": 13440},
    {"name": "Samosa (2 pcs)", "sold": 210, "revenue": 6300},
]

WEEKLY_REVENUE = [
    {"day": "Mon", "amount": 18450},
    {"day": "Tue", "amount": 21300},
    {"day": "Wed", "amount": 19800},
    {"day": "Thu", "amount": 24100},
    {"day": "Fri", "amount": 28650},
    {"day": "Sat", "amount": 15200},
    {"day": "Sun", "amount": 9800},
]

HOURLY_ORDERS = [
    {"hour": "8AM", "orders": 22}, {"hour": "9AM", "orders": 35},
    {"hour": "10AM", "orders": 18}, {"hour": "11AM", "orders": 25},
    {"hour": "12PM", "orders": 68}, {"hour": "1PM", "orders": 82},
    {"hour": "2PM", "orders": 54}, {"hour": "3PM", "orders": 30},
    {"hour": "4PM", "orders": 28}, {"hour": "5PM", "orders": 40},
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_item(item_id: int) -> dict | None:
    return next((i for i in MENU_ITEMS if i["id"] == item_id), None)


def get_cart() -> dict:
    return session.get("cart", {})


def cart_detailed() -> tuple[list[dict], int]:
    """Return cart lines with item info and the total amount."""
    cart = get_cart()
    lines: list[dict] = []
    total = 0
    for item_id, qty in cart.items():
        item = get_item(int(item_id))
        if not item:
            continue
        subtotal = item["price"] * qty
        total += subtotal
        lines.append({"item": item, "qty": qty, "subtotal": subtotal})
    return lines, total


def cart_count() -> int:
    return sum(get_cart().values())


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("user"):
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login", next=request.path))
        return func(*args, **kwargs)
    return wrapper


@app.context_processor
def inject_globals():
    return {
        "cart_count": cart_count(),
        "current_user": session.get("user"),
        "categories": CATEGORIES,
        "year": datetime.now().year,
    }


@app.template_filter("inr")
def inr_filter(value) -> str:
    try:
        return f"₹{int(value):,}"
    except (ValueError, TypeError):
        return f"₹{value}"


# ---------------------------------------------------------------------------
# Public / customer routes
# ---------------------------------------------------------------------------

@app.route("/")
def landing():
    popular = [i for i in MENU_ITEMS if i.get("popular")][:6]
    return render_template("landing.html", popular=popular)


@app.route("/menu")
def menu():
    active = request.args.get("category", "all")
    query = request.args.get("q", "").strip().lower()
    items = MENU_ITEMS
    if active != "all":
        items = [i for i in items if i["category"] == active]
    if query:
        items = [i for i in items if query in i["name"].lower()]
    return render_template("menu.html", items=items, active=active, query=query)


@app.route("/cart")
def cart():
    lines, total = cart_detailed()
    return render_template("cart.html", lines=lines, total=total)


@app.route("/cart/add/<int:item_id>", methods=["POST"])
def cart_add(item_id: int):
    item = get_item(item_id)
    if not item or not item["available"]:
        flash("Item is not available right now.", "danger")
        return redirect(request.referrer or url_for("menu"))
    cart = get_cart()
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    session["cart"] = cart
    flash(f"Added {item['name']} to cart.", "success")
    return redirect(request.referrer or url_for("menu"))


@app.route("/cart/update/<int:item_id>", methods=["POST"])
def cart_update(item_id: int):
    action = request.form.get("action")
    cart = get_cart()
    key = str(item_id)
    if key in cart:
        if action == "inc":
            cart[key] += 1
        elif action == "dec":
            cart[key] -= 1
            if cart[key] <= 0:
                cart.pop(key)
        elif action == "remove":
            cart.pop(key)
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    lines, total = cart_detailed()
    if not lines:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("menu"))

    if request.method == "POST":
        payment = request.form.get("payment", "UPI")
        order_id = f"ORD{random.randint(1043, 9999)}"
        token = f"B{random.randint(10, 99)}"
        order = {
            "id": order_id,
            "token": token,
            "customer": session["user"]["name"],
            "status": "Placed",
            "items": [{"name": l["item"]["name"], "qty": l["qty"],
                       "price": l["item"]["price"]} for l in lines],
            "total": total,
            "payment": payment,
            "time": datetime.now(),
        }
        MOCK_ORDERS.insert(0, order)
        session["cart"] = {}
        session["last_order"] = order_id
        flash("Order placed successfully!", "success")
        return redirect(url_for("order_tracking", order_id=order_id))

    return render_template("checkout.html", lines=lines, total=total)


@app.route("/order/<order_id>")
@login_required
def order_tracking(order_id: str):
    order = next((o for o in MOCK_ORDERS if o["id"] == order_id), None)
    if not order:
        flash("Order not found.", "danger")
        return redirect(url_for("orders"))
    step_index = ORDER_STATUSES.index(order["status"])
    return render_template("order_tracking.html", order=order,
                           statuses=ORDER_STATUSES, step_index=step_index)


@app.route("/orders")
@login_required
def orders():
    name = session["user"]["name"]
    my_orders = [o for o in MOCK_ORDERS if o["customer"] == name]
    return render_template("orders.html", orders=my_orders)


# ---------------------------------------------------------------------------
# Auth routes (mock)
# ---------------------------------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        role = request.form.get("role", "customer")
        name = email.split("@")[0].title() if email else "Guest User"
        session["user"] = {"name": name, "email": email, "role": role}
        flash(f"Welcome back, {name}!", "success")
        nxt = request.args.get("next")
        if role == "admin":
            return redirect(url_for("admin_dashboard"))
        if role == "staff":
            return redirect(url_for("kitchen"))
        return redirect(nxt or url_for("menu"))
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", "Guest User").strip() or "Guest User"
        email = request.form.get("email", "").strip()
        session["user"] = {"name": name, "email": email, "role": "customer"}
        flash(f"Account created. Welcome, {name}!", "success")
        return redirect(url_for("menu"))
    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("landing"))


# ---------------------------------------------------------------------------
# Kitchen / staff routes
# ---------------------------------------------------------------------------

@app.route("/kitchen")
@login_required
def kitchen():
    active = [o for o in MOCK_ORDERS if o["status"] != "Served"]
    served = [o for o in MOCK_ORDERS if o["status"] == "Served"][:5]
    return render_template("kitchen.html", active=active, served=served,
                           statuses=ORDER_STATUSES)


@app.route("/kitchen/advance/<order_id>", methods=["POST"])
@login_required
def kitchen_advance(order_id: str):
    order = next((o for o in MOCK_ORDERS if o["id"] == order_id), None)
    if order:
        idx = ORDER_STATUSES.index(order["status"])
        if idx < len(ORDER_STATUSES) - 1:
            order["status"] = ORDER_STATUSES[idx + 1]
            flash(f"{order_id} marked as {order['status']}.", "success")
    return redirect(url_for("kitchen"))


# ---------------------------------------------------------------------------
# Admin routes
# ---------------------------------------------------------------------------

@app.route("/admin")
@login_required
def admin_dashboard():
    total_revenue = sum(d["amount"] for d in WEEKLY_REVENUE)
    total_orders = sum(d["orders"] for d in HOURLY_ORDERS)
    avg_order = round(total_revenue / max(total_orders, 1))
    stats = {
        "revenue": total_revenue,
        "orders": total_orders,
        "avg_order": avg_order,
        "items": len(MENU_ITEMS),
    }
    low_stock = [i for i in MENU_ITEMS if i["stock"] <= 25]
    return render_template(
        "admin_dashboard.html",
        stats=stats,
        weekly=WEEKLY_REVENUE,
        hourly=HOURLY_ORDERS,
        top_selling=TOP_SELLING,
        recent_orders=MOCK_ORDERS[:6],
        low_stock=low_stock,
    )


@app.route("/admin/menu")
@login_required
def admin_menu():
    return render_template("admin_menu.html", items=MENU_ITEMS)


@app.route("/admin/menu/toggle/<int:item_id>", methods=["POST"])
@login_required
def admin_toggle(item_id: int):
    item = get_item(item_id)
    if item:
        item["available"] = not item["available"]
        flash(f"{item['name']} is now "
              f"{'available' if item['available'] else 'unavailable'}.", "info")
    return redirect(url_for("admin_menu"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)