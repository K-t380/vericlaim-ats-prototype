import streamlit as st
import json
import re


# PAGE CONFIGURATION

st.set_page_config(
    page_title="VeriClaim AI — Qualification Verification Gateway",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        max-width: 1450px;
    }

    [data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.06);
        padding: 18px;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.15);
    }

    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# APPLICATION HEADER

st.title("🎓 VeriClaim AI — Qualification Verification Gateway")

#st.markdown(
 #   "**Vendor-Neutral Middleware for Resume Qualification Extraction "
  #  "& OpenID4VP Digital Credential Verification**"
#)

#st.caption(
    #"VeriClaim AI identifies digital verification channels through "
    #"educational issuer directories. It does not evaluate applicant "
    #"honesty, trustworthiness, or hiring suitability."
#)

st.divider()


# AUTHORITATIVE ISSUER DIRECTORY

AUTHORITATIVE_DIRECTORY = {

    "Lucerne University of Applied Sciences and Arts": {
        "did": "did:webvh:hslu",
        "name": "Hochschule Luzern (HSLU)",
        "registry": "Swiss Higher Education Directory (SWITCH)"
    },

    "Hochschule Luzern (HSLU)": {
        "did": "did:webvh:hslu",
        "name": "Hochschule Luzern (HSLU)",
        "registry": "Swiss Higher Education Directory (SWITCH)"
    },

    "ETH Zurich": {
        "did": "did:webvh:ethz",
        "name": "ETH Zurich (Swiss Federal Institute of Technology)",
        "registry": "Swiss Federal Higher Education Register"
    },

    "Amazon Web Services": {
        "did": "did:webvh:aws",
        "name": "Amazon Web Services Training & Certification",
        "registry": "Open Credentialing Registry"
    },

    "Università della Svizzera italiana (USI)": {
        "did": "did:webvh:usi",
        "name": "Università della Svizzera italiana (USI)",
        "registry": "Swiss Higher Education Directory (SWITCH)"
    }

}


# CANDIDATE DATASET

CANDIDATE_DATASET = [

    {
        "candidate_number": 1,
        "candidate_id": "CV-001",
        "candidate_name": "Sarah Jenkins",
        "language": "English",

        "scenario_label": (
            "Candidate #1 (CV-001): Sarah Jenkins — "
            "Multi-Channel Verification"
        ),

        "raw_cv_text": """
Sarah Jenkins | Candidate ID: CV-001

AHV: 756.9218.3491.12 | Email: sarah.j@example.com
Phone: +41 79 123 45 67
Address: Gotthardstrasse 14, 6003 Lucerne, Switzerland

EDUCATION & CERTIFICATIONS:

• Master of Science in Business Administration,
  Lucerne University of Applied Sciences and Arts (2026)

• Senior AI Strategy Consultant,
  Global AI Institute (2025)

EXPERIENCE:

• Digital Marketing Specialist,
  RetailTech AG (2023–Present)
""",

        "claims": [
            {
                "degree": "MSc in Business Administration",
                "institution": "Lucerne University of Applied Sciences and Arts",
                "year": "2026"
            },
            {
                "degree": "Senior AI Strategy Consultant",
                "institution": "Global AI Institute",
                "year": "2025"
            }
        ]
    },

    {
        "candidate_number": 2,
        "candidate_id": "CV-002",
        "candidate_name": "Marc Dubois",
        "language": "French / English",

        "scenario_label": (
            "Candidate #2 (CV-002): Marc Dubois — "
            "Full Digital Channel Availability"
        ),

        "raw_cv_text": """
Marc Dubois | Candidate ID: CV-002

AHV: 756.1092.8374.01 | Email: marc.dubois@tech.ch
Phone: +41 78 987 65 43
Adresse: Avenue de Gare 8, 1003 Lausanne

FORMATION & CERTIFICATION:

• Bachelor of Science in Computer Science,
  ETH Zurich (2024)

• AWS Certified Solutions Architect,
  Amazon Web Services (2025)

EXPÉRIENCE PROFESSIONNELLE:

• Software Engineer,
  CloudServices SA (2024–Present)
""",

        "claims": [
            {
                "degree": "BSc in Computer Science",
                "institution": "ETH Zurich",
                "year": "2024"
            },
            {
                "degree": "AWS Certified Solutions Architect",
                "institution": "Amazon Web Services",
                "year": "2025"
            }
        ]
    },

    {
        "candidate_number": 3,
        "candidate_id": "CV-003",
        "candidate_name": "Alexander Vance",
        "language": "English",

        "scenario_label": (
            "Candidate #3 (CV-003): Alexander Vance — "
            "Standard Verification Channel"
        ),

        "raw_cv_text": """
Alexander Vance | Candidate ID: CV-003

AHV: 756.4432.1109.88 | Email: alex@vance-analytics.io
Phone: +41 76 555 43 21
Location: Zurich, Switzerland

SUMMARY:

Senior Data Scientist with doctorate in quantum computing.

EDUCATION:

• Ph.D. in Quantum Machine Learning,
  Geneva Advanced Tech Institute (2025)
""",

        "claims": [
            {
                "degree": "Ph.D. in Quantum Machine Learning",
                "institution": "Geneva Advanced Tech Institute",
                "year": "2025"
            }
        ]
    },

    {
        "candidate_number": 4,
        "candidate_id": "CV-004",
        "candidate_name": "Lukas Weber",
        "language": "German",

        "scenario_label": (
            "Candidate #4 (CV-004): Lukas Weber — "
            "Multilingual Formal CV (HSLU)"
        ),

        "raw_cv_text": """
Lukas Weber | Candidate ID: CV-004

AHV: 756.3321.9988.54
E-Mail: lukas.weber@luzern-marketing.ch
Telefon: +41 41 228 11 22
Adresse: Hirschmattstrasse 25, 6003 Luzern

AUSBILDUNG & ZERTIFIKATE:

• Bachelor of Science in Business Administration,
  Hochschule Luzern (HSLU) (2023)

• Certificate of Advanced Studies (CAS) Digital Marketing,
  HSLU (2025)

• International Growth Hacking Master,
  WebAcademy Online (2026)

BERUFSERFAHRUNG:

• Junior Marketing Manager,
  CentralSwiss Media AG (2023–2026)
""",

        "claims": [
            {
                "degree": "BSc in Business Administration",
                "institution": "Hochschule Luzern (HSLU)",
                "year": "2023"
            },
            {
                "degree": "CAS Digital Marketing",
                "institution": "Hochschule Luzern (HSLU)",
                "year": "2025"
            },
            {
                "degree": "International Growth Hacking Master",
                "institution": "WebAcademy Online",
                "year": "2026"
            }
        ]
    },

    {
        "candidate_number": 5,
        "candidate_id": "CV-005",
        "candidate_name": "Elena Rossi",
        "language": "Italian / English",

        "scenario_label": (
            "Candidate #5 (CV-005): Elena Rossi — "
            "Multiple Qualifications Profile"
        ),

        "raw_cv_text": """
Elena Rossi | Candidate ID: CV-005

AHV: 756.8812.0043.66
Email: elena.rossi@ticino-ai.ch
Phone: +41 91 825 33 44
Address: Lugano, Switzerland

ACADEMIC & PROFESSIONAL CREDENTIALS:

• Master of Science in Informatics,
  Università della Svizzera italiana (USI) (2024)

• Certified Blockchain & Web3 Architect,
  Swiss Crypto Association (2025)

• Executive Leadership Program,
  European Business School Online (2026)
""",

        "claims": [
            {
                "degree": "MSc in Informatics",
                "institution": "Università della Svizzera italiana (USI)",
                "year": "2024"
            },
            {
                "degree": "Certified Blockchain & Web3 Architect",
                "institution": "Swiss Crypto Association",
                "year": "2025"
            },
            {
                "degree": "Executive Leadership Program",
                "institution": "European Business School Online",
                "year": "2026"
            }
        ]
    }

]


# PROCESSING FUNCTIONS

def scrub_pii(text, candidate_name):

    cleaned = re.sub(
        r'\b756\.\d{4}\.\d{4}\.\d{2}\b',
        '[REDACTED SWISS AHV NUMBER]',
        text
    )

    cleaned = re.sub(
        r'[\w.+-]+@[\w.-]+\.\w+',
        '[REDACTED EMAIL ADDRESS]',
        cleaned
    )

    cleaned = re.sub(
        r'\+41(?:[\s().-]*\d){9}',
        '[REDACTED PHONE NUMBER]',
        cleaned
    )

    cleaned = re.sub(
        r'(?i)\b(Address|Adresse|Location)\s*:\s*[^|\n]+',
        r'\1: [REDACTED RESIDENTIAL ADDRESS]',
        cleaned
    )

    cleaned = re.sub(
        re.escape(candidate_name),
        '[REDACTED APPLICANT NAME]',
        cleaned,
        flags=re.IGNORECASE
    )

    return cleaned


def triage_claims(claims):

    processed = []

    for claim in claims:

        institution = claim["institution"]

        if institution in AUTHORITATIVE_DIRECTORY:

            directory_entry = AUTHORITATIVE_DIRECTORY[institution]

            processed.append({
                **claim,
                "status": "DIGITAL_VERIFICATION_AVAILABLE",
                "issuer_did": directory_entry["did"],
                "official_name": directory_entry["name"],
                "registry": directory_entry["registry"],
                "recommended_action": (
                    "Request a digitally signed qualification credential "
                    "through the candidate's digital identity wallet."
                )
            })

        else:

            processed.append({
                **claim,
                "status": "DIGITAL_VERIFICATION_UNAVAILABLE",
                "issuer_did": None,
                "official_name": institution,
                "registry": "Standard Verification Channel",
                "recommended_action": (
                    "Use traditional verification procedures, such as "
                    "direct institutional confirmation or "
                    "applicant-provided documentation."
                )
            })

    return processed


def build_wallet_request(candidate_id, candidate_number, claims):

    return {
        "type": "OpenID4VP_Presentation_Request",
        "client_id": f"vericlaim-ats-{candidate_id.lower()}",
        "candidate_reference": candidate_id,
        "candidate_number": candidate_number,
        "presentation_definition": {
            "id": "qualification_verification_request",
            "purpose": (
                "Consented verification of stated "
                "educational and professional credentials"
            ),
            "input_descriptors": [
                {
                    "id": f"qualification_{index + 1}",
                    "name": claim["degree"],
                    "issuer": claim["institution"],
                    "format": {
                        "sd-jwt-vc": {
                            "alg": ["ES256"]
                        }
                    }
                }
                for index, claim in enumerate(claims)
            ]
        }
    }


# SIDEBAR — CANDIDATE APPLICATION INGESTION

st.sidebar.header("📁 Candidate Application Queue")

selected_option = st.sidebar.selectbox(
    "Select Candidate Profile:",
    options=CANDIDATE_DATASET,
    format_func=lambda x: x["scenario_label"]
)

candidate_num = selected_option["candidate_number"]
candidate_id = selected_option["candidate_id"]
candidate_name = selected_option["candidate_name"]

st.sidebar.markdown(
    f"**Candidate Number:** #{candidate_num}"
)

st.sidebar.markdown(
    f"**Application Reference:** `{candidate_id}`"
)

st.sidebar.markdown(
    f"**Language Detected:** {selected_option['language']}"
)

st.sidebar.divider()

cv_input = st.sidebar.text_area(
    "Resume Stream (ATS Ingestion):",
    value=selected_option["raw_cv_text"],
    height=220,
    key=f"cv_input_{candidate_id}"
)


# MAIN VIEW — CANDIDATE HEADER

col_c1, col_c2, col_c3, col_c4 = st.columns(
    [1.5, 2, 1.5, 2]
)

with col_c1:

    st.markdown(f"### Candidate #{candidate_num}")
    st.caption(f"Ref: **{candidate_id}**")

with col_c2:

    st.markdown(f"**Applicant Name:** {candidate_name}")
    st.caption(
        f"Primary Language: {selected_option['language']}"
    )

with col_c3:

    st.markdown("**Processing Status:**")
    st.markdown("🟢 PII FILTER ACTIVE")

with col_c4:

    st.markdown("**Verification Protocol:**")
    st.markdown("`OpenID4VP / SD-JWT-VC`")

st.markdown("---")


# QUALIFICATION PROCESSING

claims = selected_option["claims"]

processed_claims = triage_claims(claims)

available_claims = [
    claim
    for claim in processed_claims
    if claim["status"] == "DIGITAL_VERIFICATION_AVAILABLE"
]

unavailable_claims = [
    claim
    for claim in processed_claims
    if claim["status"] == "DIGITAL_VERIFICATION_UNAVAILABLE"
]

available_count = len(available_claims)
unavailable_count = len(unavailable_claims)

scrubbed = scrub_pii(cv_input, candidate_name)


# DIGITAL VERIFICATION INDICATORS

st.subheader("📊 Digital Verification Indicators")

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.metric(
        "Total Qualifications",
        len(claims),
        help="Total qualifications identified in the application."
    )

with m2:

    st.metric(
        "Digital Verification Available",
        available_count,
        delta="Issuer Directory Matched",
        help="Qualifications with matching issuer directory entries."
    )

with m3:

    st.metric(
        "Digital Verification Unavailable",
        unavailable_count,
        delta=(
            "Standard Review"
            if unavailable_count > 0
            else "None"
        ),
        delta_color="off",
        help="Qualifications requiring alternative verification channels."
    )

with m4:

    st.metric(
        "Candidate Consent Channel",
        "OpenID4VP",
        delta="Wallet Request Supported"
    )

st.markdown(" ")


# MAIN DASHBOARD TABS

tab_overview, tab_privacy, tab_schema, tab_wallet = st.tabs([

    "📋 Qualification Verification Overview",

    "🛡️ Edge Privacy & PII Sanitization",

    "🤖 NLU JSON Schema Extraction",

    "📲 OpenID4VP Wallet Request"

])


# TAB 1 — QUALIFICATION VERIFICATION OVERVIEW

with tab_overview:

    st.markdown(
        "#### Digital Verification Availability Status"
    )

   # st.markdown(
    #    "This overview presents the qualifications identified "
     #   "from the resume alongside their available verification "
      #  "pathways and recommended next steps."
    #)

   # st.caption(
    #    "Digital channel availability reflects issuer directory matching, "
     #   "not confirmation of the candidate's qualification."
    #)

    st.markdown(" ")

    for idx, pc in enumerate(processed_claims, 1):

        with st.container(border=True):

            col_a, col_b = st.columns([3, 1.3])

            with col_a:

                st.markdown(
                    f"#### 🎓 {pc['degree']}"
                )

                st.markdown(
                    f"**Institution:** {pc['institution']}"
                )

                st.markdown(
                    f"**Qualification Year:** {pc['year']}"
                )

            with col_b:

                if pc["status"] == "DIGITAL_VERIFICATION_AVAILABLE":

                    st.success(
                        "🟢 DIGITAL VERIFICATION AVAILABLE"
                    )

                else:

                    st.warning(
                        "🟡 DIGITAL VERIFICATION UNAVAILABLE"
                    )

            st.divider()

            if pc["status"] == "DIGITAL_VERIFICATION_AVAILABLE":

                st.markdown(
                    f"**Registry Match:** {pc['registry']}"
                )

                st.markdown(
                    f"**Issuer DID Key:** `{pc['issuer_did']}`"
                )

                st.markdown(
                    "**Verification Channel:** OpenID4VP Digital Wallet"
                )

                st.markdown(
                    "✅ **Recommended Action:** "
                    f"{pc['recommended_action']}"
                )

            else:

                st.markdown(
                    "**Verification Channel:** "
                    "Standard Institutional Verification"
                )

                st.markdown(
                    "ℹ️ **Verification Status:** "
                    "No matching digital issuer entry identified "
                    "in the configured directory."
                )

                st.markdown(
                    "📋 **Recommended Action:** "
                    f"{pc['recommended_action']}"
                )

               # st.caption(
                #    "The absence of a digital verification channel "
                 #   "does not indicate an invalid qualification."
                #)

    st.markdown("### Verification Summary")

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:

        st.success(
            f"**{available_count} qualification(s)** "
            "have a matching digital verification channel."
        )

    with summary_col2:

        if unavailable_count > 0:

            st.warning(
                f"**{unavailable_count} qualification(s)** "
                "require standard verification procedures."
            )

        else:

            st.success(
                "All qualifications have matching issuer directory entries."
            )


# TAB 2 — EDGE PRIVACY & PII SANITIZATION

with tab_privacy:

    st.markdown(
        "#### Personal Information Protection"
    )

  #  st.caption(
   #     "Personal identifiers are redacted from the qualification "
    #    "processing stream in accordance with data minimization principles."
    #)

    col_p1, col_p2 = st.columns(2)

    with col_p1:

        st.markdown(
            "**Original ATS Input Stream:**"
        )

        st.text_area(
            "Original Application",
            cv_input,
            height=250,
            disabled=True,
            label_visibility="collapsed"
        )

    with col_p2:

        st.markdown(
            "**Sanitized Qualification Stream:**"
        )

        st.text_area(
            "Sanitized Application",
            scrubbed,
            height=250,
            disabled=True,
            label_visibility="collapsed"
        )

    st.success(
        "✓ Personal identifier redaction completed"
    )

    st.markdown("**Privacy Controls**")

    st.markdown(
        "✅ Swiss AHV number redaction"
    )

    st.markdown(
        "✅ Email address redaction"
    )

    st.markdown(
        "✅ Phone number redaction"
    )

    st.markdown(
        "✅ Residential address field redaction"
    )

    st.markdown(
        "✅ Applicant name redaction"
    )

    #st.caption(
     #   "Automated redaction identifies supported personal data patterns. "
      #  "Additional validation is required for unrecognized identifiers."
    #)


# TAB 3 — NLU JSON SCHEMA EXTRACTION

with tab_schema:

    st.markdown(
        "#### Structured Entity Extraction Payload"
    )

    st.caption(
        "Standardized qualification records prepared for "
        "digital verification and ATS integration."
    )

    schema_payload = {

        "candidate_id": candidate_id,

        "candidate_number": candidate_num,

        "applicant_name": candidate_name,

        "pii_sanitized_locally": True,

        "qualifications_extracted": [

            {
                "claim_id": f"C{i+1}",

                "degree_title": p["degree"],

                "institution_stated": p["institution"],

                "graduation_year": p["year"],

                "verification_availability_status": p["status"],

                "matched_issuer_did": p["issuer_did"],

                "recommended_verification_action": p["recommended_action"]

            }

            for i, p in enumerate(processed_claims)

        ]

    }

    st.json(schema_payload)

    st.download_button(
        label="⬇️ Export Qualification Data",
        data=json.dumps(
            schema_payload,
            indent=2,
            ensure_ascii=False
        ),
        file_name=f"{candidate_id}_qualifications.json",
        mime="application/json"
    )


# TAB 4 — OPENID4VP WALLET REQUEST

with tab_wallet:

    st.markdown(
        "#### OpenID for Verifiable Presentations "
        "(OpenID4VP) Request Dispatcher"
    )

  #  st.caption(
   #     "Candidate-controlled digital credential verification "
    #    "through compatible identity wallets."
    #)

    if available_count > 0:

        st.info(
            f"Ready to prepare digital credential requests for "
            f"**{available_count} qualification(s)** "
            f"with matching issuer directory entries."
        )

        col_w1, col_w2 = st.columns([1.5, 2])

        with col_w1:

            st.markdown("#### Verification Request")

            st.markdown(
                f"**Candidate:** {candidate_name}"
            )

            st.markdown(
                f"**Application Reference:** `{candidate_id}`"
            )

            st.markdown(
                f"**Qualifications:** {available_count}"
            )

            st.markdown(
                "**Verification Protocol:** OpenID4VP"
            )

            st.markdown(
                "**Candidate Consent:** Required"
            )

            st.markdown(" ")

            if st.button(
                "📲 Prepare OpenID4VP Wallet Request",
                type="primary",
                use_container_width=True
            ):

                st.session_state[
                    f"wallet_request_{candidate_id}"
                ] = True

                st.success(
                    f"✓ Verification request prepared for "
                    f"Candidate #{candidate_num} ({candidate_name})"
                )

            #if st.session_state.get(
             #   f"wallet_request_{candidate_id}",
              #  False
            #):

               # st.markdown(
                #    "**Request Status:** Ready for Wallet Integration"
               # )

           # st.markdown("#### Candidate Experience")

           # st.markdown(
            #    "**1. Wallet Request** — Candidate receives "
             #   "a credential presentation request through "
              #  "a supported wallet interaction."
            #)

            #st.markdown(
             #   "**2. Qualification Review** — Candidate reviews "
              #  "the requested qualification information."
            #)

            #st.markdown(
             #   "**3. Selective Disclosure** — Candidate authorizes "
              #  "or declines disclosure of the requested credentials."
            #)

          #  st.markdown(
           #     "**4. Credential Validation** — The verifier validates "
            #    "the issuer signature and presented credential."
            #)

        with col_w2:

            st.markdown(
                "#### OpenID4VP Request Payload"
            )

            wallet_request = build_wallet_request(
                candidate_id,
                candidate_num,
                available_claims
            )

            st.code(
                json.dumps(
                    wallet_request,
                    indent=2,
                    ensure_ascii=False
                ),
                language="json"
            )

            st.download_button(
                label="⬇️ Export Wallet Request",
                data=json.dumps(
                    wallet_request,
                    indent=2,
                    ensure_ascii=False
                ),
                file_name=f"{candidate_id}_openid4vp_request.json",
                mime="application/json",
                use_container_width=True
            )

        st.divider()

        st.markdown(
            "#### Qualifications Eligible for Digital Verification"
        )

        for claim in available_claims:

            st.markdown(
                f"✅ **{claim['degree']}** — "
                f"{claim['institution']}"
            )

        if unavailable_count > 0:

            st.markdown(
                "#### Qualifications Requiring Alternative Verification"
            )

            for claim in unavailable_claims:

                st.markdown(
                    f"📋 **{claim['degree']}** — "
                    f"{claim['institution']}"
                )

                st.caption(
                    f"Recommended Action: {claim['recommended_action']}"
                )

    else:

        st.warning(
            "No automated digital verification channels "
            "are currently registered for this candidate profile."
        )

        st.markdown(
            "#### Recommended Verification Actions"
        )

        for claim in unavailable_claims:

            st.markdown(
                f"**Qualification:** {claim['degree']}"
            )

            st.markdown(
                f"**Institution:** {claim['institution']}"
            )

            st.info(
                claim["recommended_action"]
            )

        st.markdown(
            "**Verification Route:** Standard Institutional Review"
        )


# APPLICATION FOOTER

st.divider()

st.caption(
    "© 2026 VeriClaim AI | Qualification Verification Gateway"
)
