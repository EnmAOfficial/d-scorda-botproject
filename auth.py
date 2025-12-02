from config import AUTH_ROLE_IDS

def has_required_role(member) -> bool:
    """Kullanıcının gerekli rollerden en az birine sahip olup olmadığını kontrol eder."""
    user_role_ids = [role.id for role in member.roles]
    return any(role_id in user_role_ids for role_id in AUTH_ROLE_IDS)
