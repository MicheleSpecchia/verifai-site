# VerifAI website

Static, dependency-free website for the open-source [VerifAI project](https://github.com/MicheleSpecchia/VerifAI). This repository contains only public site content. The application and Google OIDC laboratory remain in the separate project repository.

## Local preview

From the repository root run `python3 -m http.server 8000`, then open `http://localhost:8000/`. The site also works from a subpath because page and asset links are relative. Run `python3 scripts/check_site.py` before submitting changes. No build step or package installation is required.

## GitHub Pages

1. Merge a reviewed pull request into `main` only after the site content and privacy placeholders are approved.
2. In **Settings → Pages**, choose **GitHub Actions** as the build and deployment source. Allow the repository's Actions workflow to run.
3. The workflow checks pull requests without deploying them. A push to `main` uploads only the public site files and deploys them with GitHub's official Pages actions.
4. Inspect the Pages deployment in **Actions** and **Settings → Pages**, then open the reported URL over HTTPS. The expected project path is `https://michelespecchia.github.io/verifai-site/`; do not treat it as live until the deployment succeeds and the page is checked.

## Future custom domain and Google Auth Platform branding

GitHub Pages may later serve a custom domain. Add the domain in **Settings → Pages**, create the DNS records GitHub specifies, then verify DNS and HTTPS. With a custom GitHub Actions workflow, GitHub ignores `CNAME`; no `CNAME` file is needed. Keep internal links relative. Update the Open Graph image URL to the custom domain after activation. Verify ownership of the custom domain in **Google Search Console** with the method Google provides; a `github.io` project URL is not automatically an eligible verified domain for Google OAuth branding.

In Google Auth Platform, add the Search Console verified domain to **Authorized domains** before entering the final public HTTPS homepage, public privacy URL and configured support email in **Branding**. Review the privacy draft with the controller and fill every marked item first. The homepage and Branding privacy links must point to the same final notice. Configure the Google Web OIDC client, authorized redirect URI and secrets **only in a trusted backend deployment**, never in this GitHub Pages repository. Pages is not an OAuth callback endpoint. The Google profile in VerifAI requests `openid email`, uses the signed `sub` with an administrator-managed binding, and explicitly requests essential `auth_time` via the OIDC `claims` parameter. The client configuration must enable this claim; a missing claim is rejected. Follow the current Google verification steps for the chosen scopes, domain and branding before presenting the integration as public or production-ready. The Calendar OAuth laboratory uses a separate Desktop client and scope.

Official references: [GitHub Pages custom Actions source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site), [custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site), [Google Auth Platform branding](https://support.google.com/cloud/answer/15549049), [verification requirements](https://support.google.com/cloud/answer/13464321), and [Google OIDC claims](https://developers.google.com/identity/openid-connect/openid-connect).

## Content provenance and status

The homepage reflects the VerifAI README and documentation, especially `docs/threat_model.md`, `docs/policy_evaluation.md`, `docs/execution_gateway.md`, `docs/secure_approvals.md`, `docs/replay_protection.md`, `docs/independent_audit.md`, `docs/browser_approvals.md`, `docs/trusted_identity.md`, and `docs/adr/0015-google-oidc-web-interoperability.md`. The privacy page also reflects `src/verifai/human_approval/store.py` and the opt-in Google OIDC lab runbook. This site does not offer login, run the gateway, store visitor accounts or set tracking cookies.

The privacy page is a **draft**. Before publication as a final notice, the controller must supply its identity and contact, establish the legal basis and actual deployment, confirm any processors/transfers and retention/deletion procedures, and approve the text. See the checklist on the page. Support and privacy email addresses are likewise unconfigured.
