# Practical 8 — Organizational Data Privacy Audit

## Objective
Assess how a fictional organization collects, uses, stores, shares and disposes of personal data. This is a classroom example, not an audit of a real company.

## Organization profile (fictional)
**Organization:** CampusConnect, a fictional student-services portal  
**Data:** student name, email, phone, course, attendance and support requests  
**Systems:** website, cloud database, email platform and administrator laptops

## Audit scope and method
1. Identify personal-data assets and data flows.
2. Interview process owners (simulated for this assignment).
3. Review notices, consent records, access roles, retention and vendor contracts.
4. Check technical safeguards and incident response.
5. Rate likelihood and impact; prioritize remediation.

## Sample findings register

| ID | Finding | Risk | Likelihood | Impact | Recommended control |
|---|---|---|---|---|---|
| F-01 | All staff can view all student records | Excessive access | High | High | Role-based access, least privilege, quarterly review |
| F-02 | No documented deletion schedule | Excess retention | Medium | High | Retention schedule and verified deletion |
| F-03 | Support exports sent as email attachments | Accidental disclosure | Medium | High | Secure portal, encryption, access expiry |
| F-04 | No documented vendor review | Third-party exposure | Medium | High | Vendor due diligence and processor clauses |
| F-05 | No tested incident response procedure | Delayed response | Medium | High | Response playbook and tabletop exercise |
| F-06 | Privacy notice is vague | Lack of transparency | Medium | Medium | Clear purpose-specific notice |

## Risk scoring
Use a simple classroom scale: likelihood 1–3 and impact 1–3. Score = likelihood × impact.  
1–2 Low, 3–4 Medium, 6–9 High. Scores are prioritization aids, not legal determinations.

## Remediation roadmap
- **0–30 days:** inventory data, remove unnecessary access, stop insecure email exports.
- **31–60 days:** publish clear privacy notice, document purposes and retention, review vendors.
- **61–90 days:** implement access reviews, train staff, test incident response and deletion process.

## Evidence to collect in a real audit
Approved privacy notice; data inventory; consent/notice logs; access-control exports; retention schedule; processor contracts; security test results; incident register; training records; deletion evidence.

## Conclusion
The fictional organization has material risks around access control, retention, sharing and incident readiness. Assign an owner and due date to each corrective action, then retest effectiveness.
