# DeskFlow – Setup Guide (Step by Step)

## 1. Project chalu karne ke liye

```bash
# 1. Virtual environment banao (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Django install karo
pip install -r requirements.txt

# 3. Database tables banao
python manage.py makemigrations
python manage.py migrate

# 4. Admin/IT account banao (superuser)
python manage.py createsuperuser
# -> username, email, password dalo

# 5. Server chalu karo
python manage.py runserver
```

Browser me kholo: **http://127.0.0.1:8000/**

## 2. Kaise use karein

### Employee ke roop me:
1. `/register/` pe jaake naya account banao.
2. Login karne ke baad dashboard pe apne assigned assets dikhenge.
3. Form fill karke naya request (Laptop/Mouse/etc) submit karo.

### Admin/IT Team ke roop me:
1. Superuser account se login karo (jo aapne `createsuperuser` se banaya).
2. Aapko seedha **Admin Dashboard** dikhega — sabhi requests ek list me.
3. Username se **search** kar sakte ho, status se **filter** kar sakte ho.
4. Har "Pending" request ke saamne **Approve / Reject** button hai.
5. Approve karne par automatically ek Asset record ban jata hai jo employee ko assign ho jata hai.

### Naye Assets bulk me add karne ke liye (Django Admin Panel):
1. `/admin/` pe jaake superuser se login karo.
2. "Assets" section me jaake "Add Asset" se naye Laptop/Keyboard/Chair add karo.
3. Kisi existing user ko bhi "Staff status" tick karke Admin/IT team bana sakte ho.

## 3. Project Structure

```
deskflow_project/
├── manage.py
├── requirements.txt
├── deskflow/          -> project settings, urls
├── core/               -> our app (models, views, forms, admin)
│   ├── models.py       -> Asset, RequestTicket
│   ├── views.py        -> saari logic yahan hai
│   ├── forms.py        -> Register form, Request Ticket form
│   ├── urls.py
│   ├── admin.py        -> Django admin registration
│   ├── static/core/style.css  -> plain CSS (no framework)
│   └── templates/core/ -> login, register, employee & admin dashboard
└── templates/base.html -> common navbar + layout
```

## 4. Models Overview

- **Asset**: `name`, `asset_type`, `status` (Available/Assigned), `assigned_to` (User)
- **RequestTicket**: `user`, `asset_type`, `reason`, `status` (Pending/Approved/Rejected), `created_at`

Bas itna hi — koi extra complexity nahi. Agar aage koi feature add karna ho (jaise email notification, asset return request, etc.) toh bata dena, step by step add kar denge.
