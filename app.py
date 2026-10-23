import streamlit as st
import json
import re


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="VeriClaim AI — Qualification Verification Gateway",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# APPLICATION HEADER
# ==========================================

st.title("🎓 VeriClaim AI — Qualification Verification Gateway")

st.markdown(
    "**Vendor-Neutral Middleware for Resume Qualification Extraction "
    "& OpenID4VP Digital Credential Verification**"
)

st.caption(
    "ℹ️ VeriClaim AI identifies potential digital verification channels "
    "through educational issuer directories. It does not evaluate "
    "applicant honesty, trustworthiness, or hiring suitability."
)

st.divider()


# ==========================================
# AUTHORITATIVE DIRECTORY SIMULATION
# ELM / DID:WEBVH
# ==========================================

# Demonstration directory only.
# DID identifiers and registry associations below are illustrative.
# They are not live registry records or verified issuer identifiers.

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


# ==========================================
# SYNTHETIC CANDIDATE BENCHMARK DATASET
# ==========================================

CANDIDATE_DATASET = [

    # ======================================
    # CANDIDATE 1: SARAH JENKINS
    # ======================================

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


    # ======================================
    # CANDIDATE 2: MARC DUBOIS
    # ======================================

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


    # ======================================
    # CANDIDATE 3: ALEXANDER VANCE
    # ======================================

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


    # ======================================
    # CANDIDATE 4: LUKAS WEBER
    # ======================================

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


    # ======================================
    # CANDIDATE 5: ELENA ROSSI
    # ======================================

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


# ==========================================
# SIDEBAR: CANDIDATE APPLICATION INGESTION
# ==========================================

st.sidebar.header("📁 Candidate Application Queue")

selected_option = st.sidebar.selectbox(
    "Select Candidate Profile:",
    options=CANDIDATE_DATASET,
    format_func=lambda x: x["scenario_label"]
)


# ==========================================
# SELECTED CANDIDATE METADATA
# ==========================================

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


# ==========================================
# ATS RESUME INGESTION
# ==========================================

cv_input = st.sidebar.text_area(
    "Resume Stream (ATS Ingestion):",
    selected_option["raw_cv_text"],
    height=220
)

st.sidebar.caption(
    "Demo mode: qualification claims are provided by the "
    "selected benchmark profile. Editing the CV text does not "
    "automatically update the extracted claims."
)


# ==========================================
# MAIN VIEW: CANDIDATE HEADER
# ==========================================

col_c1, col_c2, col_c3, col_c4 = st.columns(
    [1.5, 2, 1.5, 2]
)


with col_c1:

    st.markdown(
        f"### Candidate #{candidate_num}"
    )

    st.caption(
        f"Ref: **{candidate_id}**"
    )


with col_c2:

    st.markdown(
        f"**Applicant Name:** {candidate_name}"
    )

    st.caption(
        f"Primary Language: {selected_option['language']}"
    )


with col_c3:

    st.markdown(
        "**Processing Status:**"
    )

    st.markdown(
        "🟢 PII REDACTION DEMO"
    )


with col_c4:

    st.markdown(
        "**Verification Protocol:**"
    )

    st.markdown(
        "`OpenID4VP / SD-JWT-VC`"
    )


st.markdown("---")


# ==========================================
# LAYER 1: QUALIFICATION CLAIM PROCESSING
# ==========================================

# Benchmark claims are pre-defined for each candidate.
# This is a simulation of structured LLM extraction.

claims = selected_option["claims"]

available_count = 0

unavailable_count = 0

processed_claims = []


# ==========================================
# LAYER 2: DIRECTORY ALIGNMENT
# ==========================================

for c in claims:

    inst = c["institution"]

    if inst in AUTHORITATIVE_DIRECTORY:

        available_count += 1

        processed_claims.append({

            **c,

            "status": "DIGITAL_VERIFICATION_AVAILABLE",

            "issuer_did": AUTHORITATIVE_DIRECTORY[inst]["did"],

            "official_name": AUTHORITATIVE_DIRECTORY[inst]["name"],

            "registry": AUTHORITATIVE_DIRECTORY[inst]["registry"]

        })

    else:

        unavailable_count += 1

        processed_claims.append({

            **c,

            "status": "DIGITAL_VERIFICATION_UNAVAILABLE",

            "issuer_did": None,

            "official_name": inst,

            "registry": "Standard Manual Review / Non-Digital Channel"

        })


# ==========================================
# DIGITAL VERIFICATION INDICATORS
# ==========================================

st.subheader(
    "📊 Digital Verification Indicators"
)

m1, m2, m3, m4 = st.columns(4)


# ------------------------------------------
# METRIC 1: TOTAL QUALIFICATIONS
# ------------------------------------------

with m1:

    st.metric(
        "Total Qualifications",
        len(claims),
        help=(
            "Total academic and professional qualifications "
            "listed in the candidate benchmark profile."
        )
    )


# ------------------------------------------
# METRIC 2: DIGITAL VERIFICATION AVAILABLE
# ------------------------------------------

with m2:

    st.metric(
        "Digital Verification Available",
        available_count,
        delta="Demo Directory Match",
        help=(
            "Qualifications with matching entries in the "
            "illustrative issuer directory. This is not "
            "cryptographic verification."
        )
    )


# ------------------------------------------
# METRIC 3: DIGITAL VERIFICATION UNAVAILABLE
# ------------------------------------------

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
        help=(
            "Qualifications without a matching entry "
            "in the demonstration directory."
        )
    )


# ------------------------------------------
# METRIC 4: CANDIDATE CONSENT CHANNEL
# ------------------------------------------

with m4:

    st.metric(
        "Candidate Consent Channel",
        "OpenID4VP",
        delta="Demo Request Ready"
    )


st.markdown(" ")


# ==========================================
# MAIN DASHBOARD TABS
# ==========================================

tab_overview, tab_privacy, tab_schema, tab_wallet = st.tabs([

    "📋 Qualification Verification Overview",

    "🛡️ Edge Privacy & PII Sanitization",

    "🤖 NLU JSON Schema Extraction",

    "📲 OpenID4VP Wallet Request"

])


# ==========================================
# TAB 1: QUALIFICATION VERIFICATION OVERVIEW
# ==========================================

with tab_overview:

    st.markdown(
        "#### Digital Verification Availability Status"
    )

    st.markdown(
        "This overview presents the qualifications identified "
        "from the resume alongside their potential verification "
        "pathways. "
        "**The availability or absence of a digital channel "
        "does not determine the validity of a candidate's "
        "qualification.**"
    )

    st.info(
        "Registry matches in this prototype are simulated. "
        "No live issuer lookup or credential verification "
        "has been performed."
    )

    st.markdown(" ")


    # ------------------------------------------
    # DISPLAY EACH QUALIFICATION
    # ------------------------------------------

    for idx, pc in enumerate(processed_claims, 1):

        if pc["status"] == "DIGITAL_VERIFICATION_AVAILABLE":

            st.markdown(
                f"### 🎓 {pc['degree']}"
            )

            st.success(
                "DIGITAL VERIFICATION CHANNEL AVAILABLE "
                "(DEMO DIRECTORY MATCH)"
            )

            st.markdown(
                f"**Institution:** {pc['institution']}"
            )

            st.markdown(
                f"**Year:** {pc['year']}"
            )

            st.markdown(
                f"**Registry Label:** {pc['registry']}"
            )

            st.markdown(
                f"**Illustrative Issuer DID:** `{pc['issuer_did']}`"
            )

            st.caption(
                "A matching issuer entry exists in the "
                "demonstration directory. Actual credential "
                "availability and authenticity remain unverified."
            )

            st.divider()


        else:

            st.markdown(
                f"### 📄 {pc['degree']}"
            )

            st.warning(
                "DIGITAL VERIFICATION CHANNEL UNAVAILABLE "
                "IN DEMO DIRECTORY"
            )

            st.markdown(
                f"**Institution:** {pc['institution']}"
            )

            st.markdown(
                f"**Year:** {pc['year']}"
            )

            st.info(
                "No matching issuer was identified in the "
                "demonstration directory for this qualification."
            )

            st.markdown(
                "**Recommended Action:** Traditional verification "
                "channel, such as direct institutional inquiry "
                "or applicant-provided documentation."
            )

            st.caption(
                "The absence of a digital verification channel "
                "is not evidence of an invalid or fraudulent claim."
            )

            st.divider()


# ==========================================
# TAB 2: EDGE PRIVACY & PII SANITIZATION
# ==========================================

with tab_privacy:

    st.markdown(
        "#### PII Sanitization Demonstration "
        "(Swiss revDSG & EU GDPR Context)"
    )

    st.caption(
        "This prototype uses Python regular expressions "
        "to redact selected personal identifiers before "
        "downstream processing. The processing occurs "
        "in the Streamlit application's Python environment."
    )


    # ==========================================
    # LOCAL PII SCRUBBING
    # ==========================================

    # ------------------------------------------
    # REDACT SWISS AHV NUMBERS
    # ------------------------------------------

    scrubbed = re.sub(
        r'\b756\.\d{4}\.\d{4}\.\d{2}\b',
        '[REDACTED SWISS AHV NUMBER]',
        cv_input
    )


    # ------------------------------------------
    # REDACT EMAIL ADDRESSES
    # ------------------------------------------

    scrubbed = re.sub(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        '[REDACTED EMAIL ADDRESS]',
        scrubbed
    )


    # ------------------------------------------
    # REDACT PHONE NUMBERS
    # ------------------------------------------

    scrubbed = re.sub(
        r'\+?\d[\d\s-]{8,}\d',
        '[REDACTED PHONE NUMBER]',
        scrubbed
    )


    # ------------------------------------------
    # REDACT KNOWN RESIDENTIAL ADDRESSES
    # ------------------------------------------

    scrubbed = re.sub(
        r'Gotthardstrasse \d+, \d+ \w+'
        r'|Avenue de Gare \d+, \d+ \w+'
        r'|Hirschmattstrasse \d+, \d+ \w+',
        '[REDACTED RESIDENTIAL ADDRESS]',
        scrubbed
    )


    # ------------------------------------------
    # REDACT SELECTED CANDIDATE NAME
    # ------------------------------------------

    scrubbed = scrubbed.replace(
        candidate_name,
        '[REDACTED APPLICANT NAME]'
    )


    # ==========================================
    # PRIVACY COMPARISON COLUMNS
    # ==========================================

    col_p1, col_p2 = st.columns(2)


    # ------------------------------------------
    # ORIGINAL ATS INPUT
    # ------------------------------------------

    with col_p1:

        st.markdown(
            "**Original ATS Input Stream:**"
        )

        st.text_area(
            "Local Ingestion",
            cv_input,
            height=250,
            disabled=True,
            label_visibility="collapsed"
        )


    # ------------------------------------------
    # SANITIZED QUALIFICATION STREAM
    # ------------------------------------------

    with col_p2:

        st.markdown(
            "**Sanitized Qualification Stream:**"
        )

        st.text_area(
            "Sanitized Stream",
            scrubbed,
            height=250,
            disabled=True,
            label_visibility="collapsed"
        )


    st.success(
        "✓ Demonstration PII redaction completed. "
        "No external LLM API is called by this prototype."
    )

    st.warning(
        "This rule-based scrubber is not a complete "
        "anonymization system and does not establish "
        "GDPR or Swiss revDSG compliance. "
        "Additional privacy controls and validation "
        "would be required for production."
    )


# ==========================================
# TAB 3: NLU JSON SCHEMA EXTRACTION
# ==========================================

with tab_schema:

    st.markdown(
        "#### Structured Entity Extraction Payload (JSON Schema)"
    )

    st.caption(
        "Standardized qualification index payload. "
        "The extracted claims are supplied by the synthetic "
        "benchmark dataset rather than a live language model."
    )


    # ==========================================
    # STRUCTURED JSON PAYLOAD
    # ==========================================

    schema_payload = {

        "candidate_id": candidate_id,

        "candidate_number": candidate_num,

        "applicant_name": candidate_name,

        "pii_sanitized_locally": True,

        "extraction_mode": "SYNTHETIC_BENCHMARK",

        "qualifications_extracted": [

            {

                "claim_id": f"C{i+1}",

                "degree_title": p["degree"],

                "institution_stated": p["institution"],

                "graduation_year": p["year"],

                "verification_availability_status": p["status"],

                "matched_issuer_did": p["issuer_did"]

            }

            for i, p in enumerate(processed_claims)

        ]

    }


    # ------------------------------------------
    # DISPLAY JSON
    # ------------------------------------------

    st.json(schema_payload)


# ==========================================
# TAB 4: OPENID4VP WALLET REQUEST GENERATOR
# ==========================================

with tab_wallet:

    st.markdown(
        "#### OpenID for Verifiable Presentations "
        "(OpenID4VP) Request Dispatcher"
    )

    st.caption(
        "The demonstration models a candidate-consented "
        "digital credential verification process using "
        "swiyu / EUDI Wallet concepts. "
        "No real wallet connection or push notification "
        "is implemented."
    )


    # ==========================================
    # DIGITAL VERIFICATION AVAILABLE
    # ==========================================

    if available_count > 0:

        st.info(
            f"Ready to generate a demonstration request for "
            f"**{available_count} qualification(s)** with "
            f"matching issuer entries."
        )


        # ------------------------------------------
        # WALLET INTERFACE COLUMNS
        # ------------------------------------------

        col_w1, col_w2 = st.columns([1.5, 2])


        # ==========================================
        # WALLET REQUEST ACTION
        # ==========================================

        with col_w1:

            if st.button(
                "📲 Generate OpenID4VP Wallet Request",
                type="primary",
                use_container_width=True
            ):

                st.success(
                    f"✓ Demonstration verification request generated "
                    f"for Candidate #{candidate_num} "
                    f"({candidate_name})!"
                )

                st.warning(
                    "Simulation only: No request was dispatched "
                    "to an actual candidate wallet."
                )

                st.markdown(
                    "**Illustrative Candidate Experience:**"
                )

                st.caption(
                    "1. Candidate receives a verification request "
                    "through a supported wallet interaction."
                )

                st.caption(
                    "2. Candidate reviews the qualification "
                    "information requested."
                )

                st.caption(
                    "3. Candidate approves or declines disclosure "
                    "through their wallet."
                )

                st.caption(
                    "4. The verifier validates the presented "
                    "digital credential and its issuer."
                )


        # ==========================================
        # OPENID4VP REQUEST JSON
        # ==========================================

        with col_w2:

            st.markdown(
                "**OpenID4VP Request Payload — "
                "Illustrative Specification:**"
            )


            wallet_request = {

                "type": "OpenID4VP_Presentation_Request",

                "client_id": (
                    f"vericlaim-ats-{candidate_id.lower()}"
                ),

                "candidate_reference": candidate_id,

                "candidate_number": candidate_num,

                "presentation_definition": {

                    "id": "qualification_verification_request",

                    "purpose": (
                        "Consented verification of stated "
                        "educational credentials"
                    ),

                    "input_descriptors": [

                        {

                            "id": "educational_credential",

                            "format": {

                                "sd-jwt-vc": {

                                    "alg": ["ES256"]

                                }

                            },

                            "schema": [

                                {

                                    "uri": "elm:academic_credential"

                                }

                            ]

                        }

                    ]

                }

            }


            # ------------------------------------------
            # DISPLAY WALLET REQUEST PAYLOAD
            # ------------------------------------------

            st.code(
                json.dumps(
                    wallet_request,
                    indent=2,
                    ensure_ascii=False
                ),
                language="json"
            )


    # ==========================================
    # DIGITAL VERIFICATION UNAVAILABLE
    # ==========================================

    else:

        st.warning(
            "No automated digital verification channels "
            "are registered in the demonstration directory "
            "for this profile."
        )

        st.info(
            "Standard verification procedures are recommended, "
            "such as institutional confirmation or "
            "applicant-provided documentation."
        )


# ==========================================
# APPLICATION FOOTER
# ==========================================

st.divider()

st.caption(
    "VeriClaim AI | Vendor-Neutral Qualification Verification "
    "Middleware | Streamlit Proof of Concept"
)

st.caption(
    "Demonstration only. No live registry lookup, "
    "cryptographic credential validation, external LLM "
    "inference, or wallet dispatch is performed."
)
