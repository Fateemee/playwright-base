from enum import Enum

class SsLJobType:
    CREATE_ORDER = "CreateOrderJob"
    RENEW = "RenewJob"
    REISSUE = "ReissueJob"
    REVOKE = "RevokeJob"
    RESEND_VERIFICATION = "ResendVerificationJob"
