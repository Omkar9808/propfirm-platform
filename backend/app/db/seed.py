from sqlalchemy.orm import Session
from app.models.role import Role, RoleEnum
from app.repositories.role import RoleRepository

def init_roles(db: Session):
    """Initialize default roles"""
    # Check if roles already exist
    existing_roles = RoleRepository.get_roles(db)
    if existing_roles:
        print("Roles already initialized")
        return
    
    # Create default roles
    roles_data = [
        (RoleEnum.SUPER_ADMIN, "Super administrator with all privileges"),
        (RoleEnum.ADMIN, "Administrator with management privileges"),
        (RoleEnum.TRADER, "Regular trader user"),
        (RoleEnum.GUEST, "Guest user with limited access")
    ]
    
    for role_name, description in roles_data:
        RoleRepository.create_role(db, role_name, description)
        print(f"Created role: {role_name}")
    
    print("Roles initialization completed")

def init_admin_user(db: Session):
    """Initialize default admin user"""
    from app.repositories.user import UserRepository
    from app.schemas.auth import UserCreate
    from app.utils.security import get_password_hash
    
    # Check if admin user already exists
    admin_user = UserRepository.get_user_by_email(db, "admin@propfirm.com")
    if admin_user:
        print("Admin user already exists")
        return
    
    # Get super_admin role
    super_admin_role = RoleRepository.get_role_by_name(db, RoleEnum.SUPER_ADMIN)
    if not super_admin_role:
        print("Super admin role not found")
        return
    
    # Create admin user
    admin_data = UserCreate(
        email="admin@propfirm.com",
        username="admin",
        password="Admin123",  # Shorter password for testing
        first_name="System",
        last_name="Administrator"
    )
    
    admin_user = UserRepository.create_user(db, admin_data, super_admin_role.id)
    print(f"Created admin user: {admin_user.email}")

def init_base_challenge(db: Session):
    """Initialize base challenge record"""
    # This will be implemented in Phase 2
    print("Base challenge initialization - to be implemented in Phase 2")