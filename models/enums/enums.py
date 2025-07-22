from enum import Enum as PyEnum

class UserRole(PyEnum):
    WORKER = "worker"
    COMPANY = "company"
    ADMIN = "admin"

class ExperienceLevel(PyEnum):
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'
