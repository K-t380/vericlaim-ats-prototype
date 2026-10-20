import streamlit as st
import json
import re
import time


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="VeriClaim AI Prototype",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ VeriClaim AI — ATS Recruiter Triage Gateway")

st.markdown(
    "**Vendor-Neutral B2B AI Middleware for Resume Claim Extraction "
    "& OpenID4VP Wallet Requests**"
)

st.divider()


# ==========================================
# SIDEBAR: CANDIDATE SELECTION & UPLOAD
# ==========================================

st.sidebar.header("📁 Candidate Application Portal")

preset = st.sidebar.selectbox(
    "Select Synthetic Candidate Preset:",
    [
        "Sarah Jenkins (Mixed: Verified + Ghost Claim)",
        "Marc Dubois (Fully Verified Candidate)",
        "Alexander Vance (Unbacked / Ghost Claim Only)"
    ]
)


# ==========================================
# SYNTHETIC DATA PRESETS
# ==========================================

PRESETS = {

    "Sarah Jenkins (Mixed: Verified + Ghost Claim)": """
Sarah Jenkins | AHV: 756.9218.3491.12 | Email: sarah.j@example.com
Phone: +41 79 123 45 67 | Address: Zurich, Switzerland

EDUCATION & CERTIFICATIONS:
• Master of Science in Business Administration,
  Lucerne University of Applied Sciences and Arts (2026)

• Senior AI Strategy Consultant,
  Global AI Institute (2025)
""",

    "Marc Dubois (Fully Verified Candidate)": """
Marc Dubois | AHV: 756.1092.8374.01 | Email: marc@dubois.ch
Phone: +41 78 987 65 43 | Address: Lucerne, Switzerland

EDUCATION & CERTIFICATIONS:
• Bachelor of Science in Computer Science,
  ETH Zurich (2024)

• AWS Certified Solutions Architect,
  Amazon Web Services (2025)
""",

    "Alexander Vance (Unbacked / Ghost Claim Only)": """
Alexander Vance | AHV: 756.4432.1109.88 | Email: alex@vance.io

EDUCATION & CERTIFICATIONS:
• Ph.D. in Quantum Machine Learning,
  Geneva Advanced Tech Institute (2025)
"""

}


# ==========================================
# CANDIDATE CV INPUT
# ==========================================

cv_text = st.sidebar.text_area(
    "Or Paste Raw CV Text Here:",
    PRESETS[preset],
    height=220
)

run_btn = st.sidebar.button(
    "⚡ Run VeriClaim AI Triage",
    type="primary"
)


# ==========================================
# MAIN DASHBOARD LAYOUT
# ==========================================

col1, col2 = st.columns([1, 1])


# ==========================================
# LAYER 1: LOCAL EDGE PROCESSING
# & PII SCRUBBING
# ==========================================

with col1:

    st.subheader(
        "1. Local Edge Processing & PII Scrubbing"
    )

    if run_btn or cv_text:

        # ------------------------------------------
        # LOCAL PII SCRUBBER LOGIC
        # ------------------------------------------

        # Remove Swiss AHV numbers
        scrubbed = re.sub(
            r'\b\d{3}\.\d{4}\.\d{4}\.\d{2}\b',
            '[REDACTED AHV]',
            cv_text
        )

        # Remove email addresses
        scrubbed = re.sub(
            r'[\w\.-]+@[\w\.-]+\.\w+',
            '[REDACTED EMAIL]',
            scrubbed
        )

        # Remove phone numbers
        scrubbed = re.sub(
            r'\+?\d[\d\s-]{8,}\d',
            '[REDACTED PHONE]',
            scrubbed
        )

        st.success(
            "✓ Local PII pattern-based scrubbing completed (demo)"
        )

        st.text_area(
            "Cleaned Qualification Text Stream (Passed to LLM):",
            scrubbed,
            height=180
        )


        # ==========================================
        # LAYER 2: LLM NLU ENTITY EXTRACTION
        # ==========================================

        st.subheader(
            "2. LLM NLU Entity Extraction (JSON Payload)"
        )

        with st.spinner(
            "Simulating qualification entity extraction..."
        ):

            time.sleep(0.5)

            claims = []

            # ------------------------------------------
            # HSLU QUALIFICATION EXTRACTION
            # ------------------------------------------

            if (
                "Lucerne University" in scrubbed
                or "HSLU" in scrubbed
            ):

                claims.append({
                    "degree": "Master of Science in Business Administration",
                    "institution": "Lucerne University of Applied Sciences and Arts",
                    "year": "2026"
                })


            # ------------------------------------------
            # ETH ZURICH QUALIFICATION EXTRACTION
            # ------------------------------------------

            if "ETH Zurich" in scrubbed:

                claims.append({
                    "degree": "Bachelor of Science in Computer Science",
                    "institution": "ETH Zurich",
                    "year": "2024"
                })


            # ------------------------------------------
            # AWS CERTIFICATION EXTRACTION
            # ------------------------------------------

            if "Amazon Web Services" in scrubbed:

                claims.append({
                    "degree": "AWS Certified Solutions Architect",
                    "institution": "Amazon Web Services",
                    "year": "2025"
                })


            # ------------------------------------------
            # GLOBAL AI INSTITUTE EXTRACTION
            # ------------------------------------------

            if "Global AI Institute" in scrubbed:

                claims.append({
                    "degree": "Senior AI Strategy Consultant",
                    "institution": "Global AI Institute",
                    "year": "2025"
                })


            # ------------------------------------------
            # GENEVA ADVANCED TECH INSTITUTE EXTRACTION
            # ------------------------------------------

            if "Geneva Advanced Tech Institute" in scrubbed:

                claims.append({
                    "degree": "Ph.D. in Quantum Machine Learning",
                    "institution": "Geneva Advanced Tech Institute",
                    "year": "2025"
                })


        # ------------------------------------------
        # DISPLAY EXTRACTED JSON CLAIMS
        # ------------------------------------------

        st.json(claims)


# ==========================================
# LAYER 3: AUTHORITATIVE DIRECTORY TRIAGE
# & LAYER 4: GHOST CLAIM GAP ANALYSIS
# ==========================================

with col2:

    st.subheader(
        "3. Authoritative Directory Triage & Gap Analysis"
    )


    # ==========================================
    # DEMO AUTHORITATIVE ISSUER DIRECTORY
    # ==========================================

    AUTHORITATIVE_DIRECTORY = {

        "Lucerne University of Applied Sciences and Arts": "did:webvh:hslu",

        "ETH Zurich": "did:webvh:ethz",

        "Amazon Web Services": "did:webvh:aws"

    }


    if run_btn or cv_text:

        st.markdown(
            "**Recruiter ATS Trust Signals:**"
        )

        verifiable_count = 0

        ghost_count = 0


        # ------------------------------------------
        # CHECK EACH EXTRACTED CLAIM
        # ------------------------------------------

        for claim in claims:

            inst = claim["institution"]


            # ------------------------------------------
            # CLAIM HAS A MATCHING DIRECTORY ENTRY
            # ------------------------------------------

            if inst in AUTHORITATIVE_DIRECTORY:

                verifiable_count += 1

                st.markdown(
                    f"🟢 **ISSUER DIRECTORY MATCH FOUND** | "
                    f"`{claim['degree']}`"
                )

                st.caption(
                    f"Issuer DID Key: "
                    f"`{AUTHORITATIVE_DIRECTORY[inst]}` "
                    f"| Demo directory match"
                )


            # ------------------------------------------
            # GHOST / UNBACKED CLAIM DETECTION
            # ------------------------------------------

            else:

                ghost_count += 1

                st.markdown(
                    f"🟡 **GHOST CLAIM FLAGGED** | "
                    f"`{claim['degree']}`"
                )

                st.caption(
                    f"Issuer: `{inst}` "
                    f"| ⚠️ No matching issuer found "
                    f"in the demonstration directory."
                )


        # ==========================================
        # TRIAGE SUMMARY
        # ==========================================

        st.divider()

        st.markdown("### 📊 Candidate Triage Summary")

        metric_col1, metric_col2 = st.columns(2)

        with metric_col1:

            st.metric(
                label="Issuer Directory Matches",
                value=verifiable_count
            )

        with metric_col2:

            st.metric(
                label="Unbacked Claims",
                value=ghost_count
            )


        # ==========================================
        # LAYER 5: OPENID4VP PRESENTATION REQUEST
        # ==========================================

        st.divider()

        st.subheader(
            "4. OpenID4VP Presentation Request Generator"
        )


        # ------------------------------------------
        # IF MATCHING ISSUERS ARE FOUND
        # ------------------------------------------

        if verifiable_count > 0:

            st.info(
                f"Ready to generate a demonstration request "
                f"for {verifiable_count} credential(s) "
                f"via swiyu / EUDI Wallet."
            )


            # ------------------------------------------
            # GENERATE WALLET REQUEST
            # ------------------------------------------

            if st.button(
                "📲 Generate OpenID4VP Wallet Request"
            ):

                st.success(
                    "Demonstration request generated! "
                    "No actual wallet notification has been sent."
                )


                # ------------------------------------------
                # OPENID4VP REQUEST PAYLOAD
                # ------------------------------------------

                wallet_request = {

                    "type": "OpenID4VP_Request",

                    "client_id": "vericlaim-ats-session-4092",

                    "presentation_definition": {

                        "id": "degree_verification_request"

                    }

                }


                # ------------------------------------------
                # DISPLAY JSON PAYLOAD
                # ------------------------------------------

                st.code(
                    json.dumps(
                        wallet_request,
                        indent=2
                    ),
                    language="json"
                )


        # ------------------------------------------
        # IF NO MATCHING ISSUERS ARE FOUND
        # ------------------------------------------

        else:

            st.warning(
                "No matching issuers found in the demo directory. "
                "Candidate qualifications require manual verification."
            )