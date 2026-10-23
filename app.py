import streamlit as st
import json
import re


st.set_page_config(
    page_title="VeriClaim AI | Qualification Verification",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# APPLICATION STYLING
# ==========================================

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        max-width: 1450px;
    }

    [data-testid="stMetric"] {
        background-color: #f8fafc;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }

    [data-testid="stMetricLabel"] {
        font-size: 14px;
        font-weight: 500;
    }

    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    div[data-testid="stExpander"] {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# ISSUER DIRECTORY
# ==========================================

AUTHORITATIVE_DIRECTORY = {
    "Lucerne University of Applied Sciences and Arts": {
        "issuer_id": "HSLU",
        "name": "Hochschule Luzern (HSLU)",
        "category": "Higher Education"
    },
    "ETH Zurich": {
        "issuer_id": "ETHZ",
        "name": "ETH Zurich",
        "category": "Higher Education"
    },
    "Amazon Web Services": {
        "issuer_id": "AWS",
        "name": "Amazon Web Services Training & Certification",
        "category": "Professional Certification"
    },
    "Università della Svizzera italiana (USI)": {
        "issuer_id": "USI",
        "name": "Università della Svizzera italiana",
        "category": "Higher Education"
    }
}

ISSUER_ALIASES = {
    "HSLU": "Lucerne University of Applied Sciences and Arts",
    "Hochschule Luzern (HSLU)": "Lucerne University of Applied Sciences and Arts",
    "Hochschule Luzern": "Lucerne University of Applied Sciences and Arts"
}


# ==========================================
# CANDIDATE DATASET
# ==========================================

CANDIDATE_DATASET = [
    {
        "candidate_number": 1,
        "candidate_id": "CV-001",
        "candidate_name": "Sarah Jenkins",
        "language": "English",
        "scenario_label": "CV-001 | Sarah Jenkins",
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
"""
    },
    {
        "candidate_number": 2,
        "candidate_id": "CV-002",
        "candidate_name": "Marc Dubois",
        "language": "French / English",
        "scenario_label": "CV-002 | Marc Dubois",
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
"""
    },
    {
        "candidate_number": 3,
        "candidate_id": "CV-003",
        "candidate_name": "Alexander Vance",
        "language": "English",
        "scenario_label": "CV-003 | Alexander Vance",
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
"""
    },
    {
        "candidate_number": 4,
        "candidate_id": "CV-004",
        "candidate_name": "Lukas Weber",
        "language": "German",
        "scenario_label": "CV-004 | Lukas Weber",
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
"""
    },
    {
        "candidate_number": 5,
        "candidate_id": "CV-005",
        "candidate_name": "Elena Rossi",
        "language": "Italian / English",
        "scenario_label": "CV-005 | Elena Rossi",
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
"""
    }
]


# ==========================================
# PROCESSING FUNCTIONS
# ==========================================

def scrub_pii(text, candidate_name):

    cleaned = re.sub(
        r'\b756\.\d{4}\.\d{4}\.\d{2}\b',
        '[REDACTED AHV]',
        text
    )

    cleaned = re.sub(
        r'[\w.+-]+@[\w.-]+\.\w+',
        '[REDACTED EMAIL]',
        cleaned
    )

    cleaned = re.sub(
        r'\+41(?:[\s().-]*\d){9}',
        '[REDACTED PHONE]',
        cleaned
    )

    cleaned = re.sub(
        r'(?i)\b(Address|Adresse|Location)\s*:\s*[^|\n]+',
        r'\1: [REDACTED ADDRESS]',
        cleaned
    )

    cleaned = re.sub(
        re.escape(candidate_name),
        '[REDACTED NAME]',
        cleaned,
        flags=re.IGNORECASE
    )

    return cleaned


def extract_qualifications(text):

    claims = []
    in_education_section = False
    current_entry = ""

    education_headers = (
        "EDUCATION",
        "FORMATION",
        "AUSBILDUNG",
        "ACADEMIC",
        "CERTIFICATIONS"
    )

    stop_headers = (
        "EXPERIENCE",
        "EXPÉRIENCE",
        "BERUFSERFAHRUNG",
        "SUMMARY"
    )

    def process_entry(entry):

        match = re.match(
            r'^(.+?),\s*(.+?)\s*\((\d{4})\)$',
            entry.strip()
        )

        if not match:
            return

        degree, institution, year = match.groups()

        institution = ISSUER_ALIASES.get(
            institution.strip(),
            institution.strip()
        )

        claims.append({
            "degree": degree.strip(),
            "institution": institution,
            "year": year
        })

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        upper_line = line.upper()

        if upper_line.startswith(stop_headers):

            if current_entry:
                process_entry(current_entry)
                current_entry = ""

            in_education_section = False
            continue

        if upper_line.startswith(education_headers):

            if current_entry:
                process_entry(current_entry)
                current_entry = ""

            in_education_section = True
            continue

        if not in_education_section:
            continue

        if line.startswith(("•", "-")):

            if current_entry:
                process_entry(current_entry)

            current_entry = line.lstrip("•- ").strip()

        elif current_entry:

            current_entry += " " + line

    if current_entry:
        process_entry(current_entry)

    return claims


def triage_claims(claims):

    results = []

    for claim in claims:

        institution = claim["institution"]

        directory_entry = AUTHORITATIVE_DIRECTORY.get(
            institution
        )

        if directory_entry:

            results.append({
                **claim,
                "status": "ISSUER_DIRECTORY_MATCH",
                "issuer_id": directory_entry["issuer_id"],
                "official_name": directory_entry["name"],
                "category": directory_entry["category"]
            })

        else:

            results.append({
                **claim,
                "status": "MANUAL_VERIFICATION",
                "issuer_id": None,
                "official_name": institution,
                "category": "Alternative Verification"
            })

    return results


def build_wallet_request(candidate_id, claims):

    return {
        "type": "OpenID4VP_Presentation_Request",
        "client_id": f"vericlaim-ats-{candidate_id.lower()}",
        "candidate_reference": candidate_id,
        "presentation_definition": {
            "id": "qualification_verification_request",
            "purpose": "Verification of educational and professional credentials",
            "input_descriptors": [
                {
                    "id": f"credential_{index + 1}",
                    "name": claim["degree"],
                    "purpose": f"Credential issued by {claim['institution']}",
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


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🎓 VeriClaim AI")

st.sidebar.caption("Qualification Verification Gateway")

st.sidebar.divider()

st.sidebar.subheader("Candidate Applications")

selected_candidate = st.sidebar.selectbox(
    "Select Application",
    CANDIDATE_DATASET,
    format_func=lambda x: x["scenario_label"]
)

candidate_num = selected_candidate["candidate_number"]
candidate_id = selected_candidate["candidate_id"]
candidate_name = selected_candidate["candidate_name"]

st.sidebar.markdown(
    f"**Application Reference:** `{candidate_id}`"
)

st.sidebar.markdown(
    f"**Candidate:** {candidate_name}"
)

st.sidebar.markdown(
    f"**Language:** {selected_candidate['language']}"
)

st.sidebar.divider()

st.sidebar.subheader("Resume Input")

if st.session_state.get("selected_candidate_id") != candidate_id:

    st.session_state["cv_text"] = selected_candidate["raw_cv_text"]
    st.session_state["selected_candidate_id"] = candidate_id

cv_input = st.sidebar.text_area(
    "Application Document",
    height=250,
    key="cv_text"
)

st.sidebar.divider()

st.sidebar.caption(
    "VeriClaim AI | Recruitment Verification Infrastructure"
)


# ==========================================
# APPLICATION HEADER
# ==========================================

st.title("🎓 VeriClaim AI")

st.markdown(
    "### Qualification Verification Gateway"
)

st.markdown(
    "Structured qualification intelligence and digital credential verification "
    "for modern recruitment workflows."
)

st.divider()


# ==========================================
# CANDIDATE INFORMATION
# ==========================================

col1, col2, col3, col4 = st.columns(
    [1.5, 2, 1.5, 2]
)

with col1:

    st.markdown("**Application ID**")
    st.markdown(f"### {candidate_id}")

with col2:

    st.markdown("**Candidate**")
    st.markdown(f"### {candidate_name}")

with col3:

    st.markdown("**Document Language**")
    st.markdown(selected_candidate["language"])

with col4:

    st.markdown("**Verification Protocol**")
    st.markdown("`OpenID4VP / SD-JWT-VC`")

st.divider()


# ==========================================
# QUALIFICATION PROCESSING
# ==========================================

sanitized_cv = scrub_pii(
    cv_input,
    candidate_name
)

claims = extract_qualifications(sanitized_cv)

processed_claims = triage_claims(claims)

available_claims = [
    claim
    for claim in processed_claims
    if claim["status"] == "ISSUER_DIRECTORY_MATCH"
]

manual_claims = [
    claim
    for claim in processed_claims
    if claim["status"] == "MANUAL_VERIFICATION"
]

available_count = len(available_claims)
unavailable_count = len(manual_claims)


# ==========================================
# VERIFICATION INDICATORS
# ==========================================

st.subheader("📊 Verification Overview")

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.metric(
        "Total Qualifications",
        len(claims)
    )

with m2:

    st.metric(
        "Issuer Directory Matches",
        available_count
    )

with m3:

    st.metric(
        "Manual Verification",
        unavailable_count
    )

with m4:

    st.metric(
        "Verification Protocol",
        "OpenID4VP"
    )

st.markdown(" ")


# ==========================================
# APPLICATION TABS
# ==========================================

tab_overview, tab_privacy, tab_schema, tab_wallet = st.tabs([
    "📋 Qualifications",
    "🛡️ Data Privacy",
    "🤖 Structured Data",
    "📲 Wallet Verification"
])


# ==========================================
# TAB 1: QUALIFICATIONS
# ==========================================

with tab_overview:

    st.subheader("Qualification Verification Status")

    st.caption(
        "Directory matching identifies potential verification routes. "
        "A qualification is confirmed only after its supporting "
        "credential has been validated."
    )

    if not processed_claims:

        st.info(
            "No qualifications identified in the current application."
        )

    for index, claim in enumerate(processed_claims, 1):

        with st.container(border=True):

            col_a, col_b = st.columns([3, 1.5])

            with col_a:

                st.markdown(
                    f"#### {index}. {claim['degree']}"
                )

                st.markdown(
                    f"**Institution:** {claim['institution']}"
                )

                st.caption(
                    f"Qualification Year: {claim['year']}"
                )

            with col_b:

                if claim["status"] == "ISSUER_DIRECTORY_MATCH":

                    st.success("🟢 Issuer Identified")

                    st.caption(
                        f"Reference: {claim['issuer_id']}"
                    )

                    st.caption(
                        "Digital credential request eligible"
                    )

                else:

                    st.warning("🟡 Manual Review")

                    st.caption(
                        "No matching issuer directory entry"
                    )

                    st.caption(
                        "Alternative verification required"
                    )


# ==========================================
# TAB 2: DATA PRIVACY
# ==========================================

with tab_privacy:

    st.subheader("Personal Information Protection")

    st.markdown(
        "Personal identifiers are redacted from the qualification "
        "processing stream."
    )

    col_p1, col_p2 = st.columns(2)

    with col_p1:

        st.markdown("**Original Application Document**")

        st.text_area(
            "Original CV",
            cv_input,
            height=300,
            disabled=True,
            label_visibility="collapsed"
        )

    with col_p2:

        st.markdown("**Sanitized Processing Document**")

        st.text_area(
            "Sanitized CV",
            sanitized_cv,
            height=300,
            disabled=True,
            label_visibility="collapsed"
        )

    st.success("✓ Personal information redaction completed")

    st.caption(
        "Redaction covers recognized personal identifiers, "
        "including AHV numbers, email addresses, phone numbers, "
        "names and address fields."
    )


# ==========================================
# TAB 3: STRUCTURED DATA
# ==========================================

with tab_schema:

    st.subheader("Structured Qualification Data")

    st.markdown(
        "Normalized qualification records prepared for "
        "verification and ATS integration."
    )

    schema_payload = {
        "application_reference": candidate_id,
        "candidate_number": candidate_num,
        "candidate_name": candidate_name,
        "qualification_count": len(processed_claims),
        "qualifications": [
            {
                "claim_id": f"C{index + 1}",
                "degree": claim["degree"],
                "institution": claim["institution"],
                "year": claim["year"],
                "verification_status": claim["status"],
                "issuer_reference": claim["issuer_id"]
            }
            for index, claim in enumerate(processed_claims)
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
        mime="application/json",
        use_container_width=False
    )


# ==========================================
# TAB 4: WALLET VERIFICATION
# ==========================================

with tab_wallet:

    st.subheader("Digital Credential Verification")

    st.markdown(
        "Prepare an OpenID4VP credential presentation request "
        "for candidate-controlled disclosure."
    )

    if available_count > 0:

        st.info(
            f"**{available_count} qualification(s)** identified "
            f"for a potential digital credential request."
        )

        col_w1, col_w2 = st.columns([1.3, 2])

        with col_w1:

            st.markdown("#### Verification Request")

            st.markdown(
                f"**Candidate:** {candidate_name}"
            )

            st.markdown(
                f"**Application:** `{candidate_id}`"
            )

            st.markdown(
                f"**Credentials Requested:** {available_count}"
            )

            st.markdown(
                "**Candidate Consent:** Required"
            )

            st.markdown(" ")

            prepare_request = st.button(
                "📲 Prepare Wallet Request",
                type="primary",
                use_container_width=True
            )

            if prepare_request:

                st.session_state["prepared_request"] = candidate_id

                st.success(
                    "✓ Credential presentation request prepared"
                )

        with col_w2:

            st.markdown("#### Request Details")

            wallet_request = build_wallet_request(
                candidate_id,
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

            if st.session_state.get("prepared_request") == candidate_id:

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

        st.markdown("#### Candidate Consent Process")

        st.markdown(
            "1. **Credential Request** — A verification request "
            "is presented through a compatible wallet interaction."
        )

        st.markdown(
            "2. **Candidate Review** — The candidate reviews "
            "the requested qualification information."
        )

        st.markdown(
            "3. **Selective Disclosure** — The candidate chooses "
            "whether to authorize credential sharing."
        )

        st.markdown(
            "4. **Credential Validation** — The verifier checks "
            "the presented credential and issuer signature."
        )

    else:

        st.warning(
            "No matching digital credential issuer identified."
        )

        st.markdown(
            "**Recommended Verification Route:** "
            "Direct institutional confirmation or "
            "applicant-provided documentation."
        )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "© 2026 VeriClaim AI | Qualification Verification Gateway"
)
