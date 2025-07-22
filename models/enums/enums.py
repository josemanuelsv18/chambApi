from enum import Enum as PyEnum

#user.py
class UserRole(PyEnum):
    WORKER = "worker"
    COMPANY = "company"
    ADMIN = "admin"

#worker.py
class ExperienceLevel(PyEnum):
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'

#company.py
class CompanyStatus(PyEnum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    SUSPENDED = 'suspended'

#administrator.py
class AdminLevel(PyEnum):
    SUPER_ADMIN = 'super_admin'
    MODERATOR = 'moderator'

#job_offer.py
class JobCategory(PyEnum):
    EVENTS = 'events'
    CATERING = 'catering'
    CLEANING = 'cleaning'
    DELIVERY = 'delivery'
    OTHER = 'other'
class JobStatus(PyEnum):
    AVAILABLE = 'available'
    NOT_AVAILABLE = 'not available'
    CANCELLED = 'cancelled'

#application.py
class ApplicationStatus(PyEnum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    WITHDRAWN = 'withdrawn'

#job.py
class JobStatus(PyEnum):
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

#payment.py
class PaymentStatus(PyEnum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'

#review.py
class ReviewerType(PyEnum):
    WORKER = 'worker'
    COMPANY = 'company'
