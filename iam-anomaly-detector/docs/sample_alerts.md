# Sample Alerts

## Alert 1 — Brute Force Attempt (Critical)

**What happened**: User `user5` failed authentication 8 consecutive times within a 90-second window, then successfully authenticated.

**Why it's suspicious**: This access pattern is consistent with a credential-stuffing or password-spraying attack. A successful login after repeated failures suggests the attacker eventually obtained valid credentials.

**Severity**: `Critical`

**Recommendation**: Immediately invalidate the session, reset the user's credentials, and block the originating source IP. Review recent activity from this account.

---

## Alert 2 — Impossible Travel (High)

**What happened**: User `user12` authenticated successfully from `United States`, then authenticated from `Russia` 30 minutes later.

**Why it's suspicious**: The physical distance between the two locations cannot be traversed in 30 minutes. This strongly suggests account sharing or credential compromise by a foreign threat actor.

**Severity**: `High`

**Recommendation**: Suspend the account pending investigation, verify the user's actual location, and enforce multi-factor authentication (MFA) going forward.

---

## Alert 3 — Off-Hours Privileged Access (Medium)

**What happened**: Admin account `admin1` successfully authenticated at 03:15 AM local time, outside the defined business hours window (8 AM – 8 PM).

**Why it's suspicious**: Privileged account activity outside business hours can indicate unauthorized access, insider threat behavior, or a compromised credential being used covertly.

**Severity**: `Medium`

**Recommendation**: Confirm whether a maintenance window was scheduled for this time. If unplanned, investigate the session and consider restricting admin access to business hours unless pre-approved.

