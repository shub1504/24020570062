# Practical 11: Website Privacy Audit (Passive Scan)

## Aim
To audit how a website handles user privacy and security by combining an automated passive scan (custom Python script) with a manual review of its privacy policy.

> Use this tool only on sites you own or have written permission to test. The script sends a single GET request, the same as a browser. Active scanners such as `dirb` or `nikto` need explicit permission.

## Run
```bash
python -m pip install requests beautifulsoup4
python privacy_audit.py https://your-own-site.com > sample_output.json
```
(The package is `beautifulsoup4`, but it is imported as `bs4`.)

## What the script checks
| Check | Why it matters |
|---|---|
| HTTPS | Data in transit is encrypted |
| Security headers (HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy) | Protect against downgrade, XSS, clickjacking, MIME sniffing and referrer leakage |
| Cookie flags (Secure, HttpOnly) | Stop session cookies leaking over HTTP or being read by scripts |
| Third-party scripts / trackers | Shows where visitor data may flow |
| Forms and personal-data fields | Shows what personal data is collected |
| Privacy policy link, cookie banner hint | Notice and consent transparency |

## Sample result (L'Oréal Brandstorm India community page)
See `sample_output.json`.

| Finding | Result |
|---|---|
| HTTPS | Yes |
| HSTS | Not found in this response |
| CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy | Present |
| Cookie `__cf_bm` (Cloudflare bot management) | Secure and HttpOnly |
| Trackers / third-party scripts | None in page source |
| Forms, privacy policy link, cookie banner | Not seen by the script (**inconclusive**, see Limitations) |

### Manual review of the privacy policy (https://brandstorm.loreal.com/en/privacy)
A privacy policy **exists**, which contradicts the script's `privacy_policy_link: false`. The policy is GDPR-based and lists data collected, purposes, legal bases, retention (maximum 2 years for account data), third-party sharing, hosting in Europe and user rights. Observed gaps: no mention of India's DPDP Act 2023 although the page targets Indian users, vague retention for other data categories, generic security statements, no named DPO or grievance officer, and access requests that may take up to 3 months.

## Limitations
The script reads **static HTML only**. Many modern sites render forms, footer links and consent banners with JavaScript, so `False` or empty results for those checks are **inconclusive**. They must be verified manually in a browser (footer links, consent banner on first visit, and the Network and Application tabs in DevTools). Backend storage, retention and access control cannot be assessed by a passive scan.

## Conclusion
A passive scan plus a manual policy review showed good baseline security (HTTPS and four of five security headers, secure cookie flags, no third-party trackers in the page source) and a clear, GDPR-style privacy policy. The main improvements are HSTS and alignment with the DPDP Act 2023. The exercise also showed that automated scanning works best when combined with manual review.

## Viva questions
- Why did the script say "no privacy policy" when one exists? The page is JavaScript-rendered and the script reads only the static HTML.
- Secure vs HttpOnly cookie? Secure: sent only over HTTPS. HttpOnly: not readable by JavaScript (limits XSS cookie theft).
- What does HSTS do? Forces browsers to always use HTTPS, preventing downgrade attacks.
- Passive vs active scan? Passive only observes normal responses; active (nikto, dirb) probes for vulnerabilities and needs permission.
