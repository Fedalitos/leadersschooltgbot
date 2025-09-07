# ============================================
# 🔹 data/admins.py — administratorlar ro'yxati
# ============================================

# Administratorlarning IDlari (o'zingizniki bilan almashtiring)
ADMINS = [
    7296673831,    # Администратор
    5523530887, # Директор
]

def is_admin(user_id: int) -> bool:
    """Foydalanuvchi administratormi tekshirish"""
    return user_id in ADMINS