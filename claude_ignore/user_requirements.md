Here is the **Human-in-the-Loop Execution Plan**.

This plan is designed for a **Semi-Autonomous Browser Script** (like a Python Selenium/Puppeteer script or an AI Agent). The browser handles the navigation, typing, and complex configuration, but it **pauses** to ask you for authentication and critical decisions.

---

### 🚦 Pre-Flight Checklist

**Before running the script, ensure you have:**

1. **Your Phone:** For 2FA/MFA verification on all platforms.
2. **Password Manager:** Open and ready to copy-paste passwords.
3. **Credit Card:** (Optional) In case GCP/AWS prompts for billing verification.

---

### Phase 1: AWS Setup (The Foundation)

**1. Login & Verification**

* **🤖 Browser Action:** Opens `https://console.aws.amazon.com/console/home`
* **👤 User Prompt:**
> "I have opened the AWS Console. Please log in with your **Root** or **Administrator** account. Handle any MFA prompts. Press **ENTER** here when you see the AWS Dashboard."



**2. S3 Bucket Creation**

* **🤖 Browser Action:** Navigates to `https://s3.console.aws.amazon.com/s3/bucket/create`
* **🤖 Browser Action:** Fills `Bucket name` with `deployment-assets`.
* **👤 User Prompt:**
> "I've filled in the bucket name 'deployment-assets'.
> **Action Required:** Please scroll down and verify 'Block all Public Access' is checked.
> Then click **'Create bucket'** manually to confirm. Press **ENTER** here once done."



**3. IAM User & Keys**

* **🤖 Browser Action:** Navigates to `https://console.aws.amazon.com/iamv2/home#/users/create`
* **🤖 Browser Action:** Fills User name: `svc-frontend-orchestrator`.
* **🤖 Browser Action:** Clicks `Next` > Selects `Attach policies directly` > Types `auto-deployer-policy`.
* **👤 User Prompt:**
> "I cannot create the policy automatically without interrupting the flow.
> **Action Required:** Please click 'Create policy' in the new tab that opens, paste the JSON I provided in the chat window earlier, and save it as `auto-deployer-policy`.
> Once the policy is created and attached to this user, click **'Create User'**.
> Navigate to the user's 'Security Credentials' tab and click **'Create Access Key'**.
> **STOP HERE.** Do not close the popup with the keys. Press **ENTER** when the keys are visible on screen."


* **🤖 Browser Action:** Scrapes the `Access Key ID` and `Secret Access Key` from the screen.
* **🤖 Browser Internal:** Stores keys in memory.

---

### Phase 2: GitHub Configuration

**4. Authentication & Org Selection**

* **🤖 Browser Action:** Opens `https://github.com/login`
* **👤 User Prompt:**
> "Please log in to GitHub. Press **ENTER** when you are on your dashboard."



**5. Token Generation**

* **🤖 Browser Action:** Navigates to `https://github.com/settings/personal-access-tokens/new`
* **🤖 Browser Action:** Fills Token Name: `auto-deployer-production`.
* **👤 User Prompt:**
> "**Critical Decision:** Please select the **Resource Owner** (Organization) from the dropdown menu.
> Then, verify I have selected 'All Repositories'.
> I will now attempt to check the permission boxes for Administration, Contents, and Metadata.
> **Verify my selections**, then scroll down and click **'Generate token'**.
> Press **ENTER** when the new token is visible."


* **🤖 Browser Action:** Scrapes the token starting with `github_pat_...`.
* **🤖 Browser Internal:** Stores token in memory.

---

### Phase 3: Cloudflare Setup

**6. Authentication**

* **🤖 Browser Action:** Opens `https://dash.cloudflare.com/login`
* **👤 User Prompt:**
> "Please log in to Cloudflare. Press **ENTER** when you see the dashboard."



**7. Token Creation**

* **🤖 Browser Action:** Navigates to `https://dash.cloudflare.com/profile/api-tokens/create`
* **🤖 Browser Action:** Clicks `Create Custom Token`.
* **👤 User Prompt:**
> "I am setting up the permissions matrix (Pages:Edit, DNS:Edit).
> **Action Required:** Under 'Account Resources', please select your specific **Account** from the dropdown.
> Under 'Zone Resources', select 'All zones' or your specific site.
> Click **'Continue to summary'** -> **'Create Token'**.
> Press **ENTER** when the token is visible."


* **🤖 Browser Action:** Scrapes the long API token string.
* **🤖 Browser Internal:** Stores token in memory.

---

### Phase 4: Google Cloud Platform (GCP)

**8. Login & Project**

* **🤖 Browser Action:** Opens `https://console.cloud.google.com/projectcreate`
* **👤 User Prompt:**
> "Please log in to Google Cloud.
> **Action Required:** If prompted, select your Organization.
> I have typed 'automation-host-prod' as the Project Name.
> Click **'Create'** and wait for the notification bell to finish.
> **Crucial:** Click 'Select Project' in the notification to ensure we are in the new project.
> Press **ENTER** when you are inside the `automation-host-prod` dashboard."



**9. Service Account & Key**

* **🤖 Browser Action:** Navigates to `https://console.cloud.google.com/iam-admin/serviceaccounts/create?project=automation-host-prod`
* **🤖 Browser Action:** Fills Service Account ID: `auto-deployer-sa`.
* **👤 User Prompt:**
> "Please click **'Create and Continue'**.
> Click **'Done'** (skip role assignment for now).
> Click on the newly created email address in the list.
> Go to the **'Keys'** tab -> **'Add Key'** -> **'Create new key'** -> **'JSON'** -> **'Create'**.
> **Action Required:** This downloaded a file to your computer. Please find the file path of this JSON file.
> **Input:** Paste the full file path of the downloaded JSON key here:"


* **🤖 Browser Internal:** Reads file from path, Base64 encodes it, and stores it in memory.

**10. Billing Setup (The most common failure point)**

* **🤖 Browser Action:** Navigates to `https://console.cloud.google.com/billing`
* **👤 User Prompt:**
> "Please select the Billing Account you wish to use.
> Click **'Account Management'** on the right side.
> Click **'Add Principal'**.
> **Input:** In the 'New principals' box, paste this email: `auto-deployer-sa@automation-host-prod.iam.gserviceaccount.com`
> **Role:** Select 'Billing Account User'.
> Click **'Save'**.
> Press **ENTER** when done."



---

### Phase 5: Secure Storage (The Finish Line)

**11. Auto-fill Secrets**

* **🤖 Browser Action:** Navigates to `https://console.aws.amazon.com/secretsmanager/new?region=us-east-1`
* **🤖 Browser Action:** Selects `Other type of secret`.
* **🤖 Browser Action:** Automatically fills the Key/Value rows with the data collected in previous steps:
* `GITHUB_TOKEN`
* `CLOUDFLARE_API_TOKEN`
* `GCP_SERVICE_ACCOUNT_JSON`
* `AWS_KEYS` (Optional, usually kept separate, but can be stored here for backup)


* **👤 User Prompt:**
> "I have filled in all the secrets.
> **Action Required:** Click **'Next'**.
> Name the secret: `prod/auto-deployer/keys`.
> Click **'Next'** -> **'Next'** -> **'Store'**.
> **Congratulations! Setup Complete.**"