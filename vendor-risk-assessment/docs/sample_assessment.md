# Sample Vendor Assessments

---

## Assessment 1 — Critical Risk Vendor

**Vendor**: EpsilonData Corp
**Country**: India (IN)
**Access Level**: Admin
**Data Sensitivity**: High
**Compliance**: None
**Business Criticality**: High

**Risk Score**: 100 / 100
**Risk Level**: 🔴 Critical

**Triggered Risk Factors**:
- +40 pts — Admin-level access — highest privilege tier
- +30 pts — No SOC2 or ISO27001 certification
- +30 pts — Accesses highly sensitive data
- +20 pts — Supports a business-critical function

**Recommendations**:
1. Escalate to CISO immediately — do not grant access until all factors are resolved.
2. Apply least-privilege access — no Admin rights without documented justification.
3. Require SOC2 Type II before onboarding.
4. Encrypt all data at rest and in transit.
5. Conduct a full third-party security audit.

---

## Assessment 2 — High Risk Vendor

**Vendor**: ThetaLogistics Co
**Country**: Russia (RU)
**Access Level**: Admin
**Data Sensitivity**: High
**Compliance**: None
**Business Criticality**: High

**Risk Score**: 100 / 100
**Risk Level**: 🔴 Critical

**Note**: Geopolitical risk from vendor domicile compounds the access/sensitivity exposure. This vendor should not be approved without explicit CISO sign-off and legal review.

---

## Assessment 3 — Low Risk Vendor

**Vendor**: AlphaTech Solutions
**Country**: United States (US)
**Access Level**: Read
**Data Sensitivity**: Low
**Compliance**: SOC2
**Business Criticality**: Low

**Risk Score**: 0 / 100
**Risk Level**: 🟢 Low

**Triggered Risk Factors**: None

**Recommendations**:
- No immediate actions required.
- Continue standard annual vendor review cycle.
- Verify SOC2 certification is renewed each year.
