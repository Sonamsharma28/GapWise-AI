import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_pdf(filename):
    # Tight, clean margins to fit into exact 2 professional pages
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=32,
        bottomMargin=32
    )
    
    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#1e40af")   # Deep Navy Blue
    secondary_color = colors.HexColor("#2563eb") # Royal Blue
    dark_neutral = colors.HexColor("#0f172a")    # Slate 900
    light_bg = colors.HexColor("#f8fafc")        # Slate 50
    border_color = colors.HexColor("#cbd5e1")    # Slate 300

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=22,
        textColor=primary_color,
        spaceAfter=2
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=secondary_color,
        spaceAfter=6
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=primary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=secondary_color,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=dark_neutral,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1e3a8a")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10.5,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=dark_neutral
    )

    story = []

    # ================= PAGE 1 =================
    story.append(Paragraph("GAPWISE AI", title_style))
    story.append(Paragraph("AI-Based Learning Gap Detection & Personalized Learning System", subtitle_style))
    story.append(Paragraph("<b>Smart India Hackathon 2026</b> | Problem Statement ID: <b>SIH027</b> | Theme: <b>EdTech & Adaptive Learning</b> | Team: <b>HexaMind</b>", body_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=secondary_color, spaceBefore=2, spaceAfter=8))

    # Core USP Callout Box
    usp_text = Paragraph("<b>Core Philosophy:</b> <i>\"Don't just detect what students got wrong. Discover why.\"</i><br/>"
                         "Instead of simply scoring <code>Quadratic Equations = Weak</code>, GapWise AI traverses a 12-concept prerequisite DAG backwards (Basic Algebra &rarr; Algebraic Identities &rarr; Factorisation &rarr; Quadratic Equations) to identify foundational learning bottlenecks.", callout_style)
    usp_table = Table([[usp_text]], colWidths=[540])
    usp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#eff6ff")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#bfdbfe")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(usp_table)
    story.append(Spacer(1, 4))

    # PART 1: TECHNICAL & ARCHITECTURAL BREAKDOWN
    story.append(Paragraph("PART 1: TECHNICAL & ARCHITECTURAL BREAKDOWN", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.6, color=border_color, spaceBefore=1, spaceAfter=6))

    story.append(Paragraph("1. System Architecture & Tech Stack", h2_style))
    arch_data = [
        [Paragraph("Layer", table_header_style), Paragraph("Technologies", table_header_style), Paragraph("Key Capabilities & Responsibilities", table_header_style)],
        [Paragraph("<b>Frontend</b>", table_cell_style), Paragraph("React 18, Vite, Tailwind CSS, Recharts, Lucide Icons", table_cell_style), Paragraph("Interactive SVG Knowledge Graph, 4-tab concept lessons, real-time practice feedback, Recharts timeline.", table_cell_style)],
        [Paragraph("<b>Backend</b>", table_cell_style), Paragraph("Python 3.11+, FastAPI, SQLAlchemy 2.0, Pydantic v2", table_cell_style), Paragraph("Async REST APIs, weighted gap detection, BFS prerequisite engine, topological DAG learning path generator.", table_cell_style)],
        [Paragraph("<b>Database</b>", table_cell_style), Paragraph("PostgreSQL (Neon) / SQLite (Dev)", table_cell_style), Paragraph("17 normalized tables: Users, Concepts, Prerequisites, Questions, Mastery, Paths, Practice, Reassessments.", table_cell_style)],
        [Paragraph("<b>AI / RAG</b>", table_cell_style), Paragraph("TF-IDF Vectorizer + Pedagogical Fallback + OpenAI", table_cell_style), Paragraph("Curriculum RAG grounded in student mastery context; 100% functional offline or without external API keys.", table_cell_style)],
        [Paragraph("<b>Auth</b>", table_cell_style), Paragraph("JWT (python-jose) + Direct Bcrypt", table_cell_style), Paragraph("Stateless token auth, role-based access control (Student vs Teacher isolation), password hashing.", table_cell_style)],
    ]
    t_arch = Table(arch_data, colWidths=[65, 160, 315])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. Key Algorithms & Core Engines", h2_style))
    story.append(Paragraph("<b>A. Difficulty-Weighted Mastery Calculation (<code>services/gap_detection.py</code>):</b> Questions are weighted by cognitive depth: Level 1 (1.0x), Level 2 (1.5x), Level 3+ (2.0x). Formula: <code>Score = (Sum of Weighted Correct / Total Possible Weighted Score) * 100</code>. Classification: <b>Mastered</b> (&ge;75%), <b>Developing</b> (40%–74%), <b>Needs Attention</b> (&lt;40%).", body_style))
    
    story.append(Paragraph("<b>B. Prerequisite Root-Cause Engine (<code>services/prerequisite_engine.py</code>):</b> Uses <b>Breadth-First Search (BFS)</b> backwards across the 12-concept prerequisite DAG. Recursively traces incoming dependencies to pinpoint the deepest unmet prerequisite (e.g. Factorisation at 33% score), producing an explainable root-cause diagnostic chain.", body_style))

    story.append(Paragraph("<b>C. Topological Learning Path Generator (<code>services/learning_path.py</code>):</b> Performs a <b>Topological Sort</b> on weak concepts. Root-cause concepts are placed first in sequence. Advanced concepts are placed in a <b>locked state</b> until foundational prerequisites achieve mastery (&ge;75%), preventing cognitive overload.", body_style))

    story.append(Paragraph("<b>D. Continuous Adaptive Reassessment Loop:</b> Creates a closed-loop adaptive cycle: <code>ASSESS &rarr; DETECT &rarr; DIAGNOSE &rarr; PERSONALIZE &rarr; LEARN &rarr; PRACTICE &rarr; REASSESS &rarr; IMPROVE</code>. Reassessments generate a direct <b>Before vs. After Comparison Table</b> with quantified growth deltas.", body_style))

    story.append(PageBreak())

    # ================= PAGE 2 =================
    story.append(Paragraph("PART 2: SIH 2026 PRESENTATION SCRIPT & JUDGES' DEFENSE", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.6, color=border_color, spaceBefore=1, spaceAfter=6))

    story.append(Paragraph("1. The Pitch Script (Step-by-Step with Live Demo Walkthrough)", h2_style))
    
    steps_data = [
        [Paragraph("Time", table_header_style), Paragraph("Phase", table_header_style), Paragraph("What to Say & Actions on Screen", table_header_style)],
        [
            Paragraph("0:00 - 1:00", table_cell_style),
            Paragraph("<b>The Hook</b>", table_cell_style),
            Paragraph("<i>'Respected Judges, when a 10th-grade student fails Quadratic Equations, schools give him 50 more quadratic equations. But the student isn't failing quadratics — he fails because he never understood <b>Factorisation</b>. Traditional EdTech tells you WHAT is wrong. <b>GapWise AI</b> discovers WHY.'</i>", table_cell_style)
        ],
        [
            Paragraph("1:00 - 2:00", table_cell_style),
            Paragraph("<b>Diagnostic Test & AI Diagnosis</b>", table_cell_style),
            Paragraph("<b>Screen:</b> Log in via 1-Click Demo Student &rarr; Open Assessment.<br/>"
                      "<i>'Aryan takes our 12-concept diagnostic test. Look at our <b>AI Root Learning Gap Diagnosis</b>: our engine traversed the prerequisite graph and diagnosed that Factorisation is the root bottleneck blocking Quadratic Equations.'</i>", table_cell_style)
        ],
        [
            Paragraph("2:00 - 3:00", table_cell_style),
            Paragraph("<b>Knowledge Graph & Learning Path</b>", table_cell_style),
            Paragraph("<b>Screen:</b> Click Knowledge Graph &rarr; Open Learning Path.<br/>"
                      "<i>'Here is our interactive SVG Knowledge Graph color-coding mastery in real-time. Notice that in the Learning Path, Quadratic Equations is <b>locked</b> until Aryan finishes the Factorisation module.'</i>", table_cell_style)
        ],
        [
            Paragraph("3:00 - 4:00", table_cell_style),
            Paragraph("<b>Practice & Reassessment</b>", table_cell_style),
            Paragraph("<b>Screen:</b> Practice Question &rarr; Take Reassessment.<br/>"
                      "<i>'Aryan studies the 4-tab module, practices with instant step-by-step reasoning, and takes a Reassessment. Look at the <b>Before vs After Table</b>: Factorisation jumped from 33% to 85%, and Quadratic Equations is now unlocked!'</i>", table_cell_style)
        ],
        [
            Paragraph("4:00 - 5:00", table_cell_style),
            Paragraph("<b>Teacher View & Closing</b>", table_cell_style),
            Paragraph("<b>Screen:</b> Log in as Teacher &rarr; Show Heatmap.<br/>"
                      "<i>'Teachers get class difficulty heatmaps and student drilldown profiles showing individual learning gaps for targeted intervention. GapWise AI is production-ready, verified with automated test suites.'</i>", table_cell_style)
        ]
    ]

    t_steps = Table(steps_data, colWidths=[55, 110, 375])
    t_steps.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ]))
    story.append(t_steps)
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. Top Judges' Q&A Defense", h2_style))
    
    qa_list = [
        ("Q1: How is this different from Khan Academy or BYJU'S?",
         "Standard platforms evaluate topics in isolation. If a student fails Quadratic Equations on Khan Academy, they recommend more quadratic videos. GapWise AI has a formal Directed Acyclic Prerequisite Graph. We trace backwards through graph dependencies to identify and fix foundational gaps first."),
        ("Q2: What if the school has no internet or no OpenAI API key?",
         "Our core gap detection, BFS prerequisite traversal, and topological path generation algorithms run deterministically on our backend without external APIs. Even our AI Mentor includes a built-in pedagogical fallback engine using curriculum TF-IDF retrieval."),
        ("Q3: Can this scale to other subjects like Physics or Chemistry?",
         "Yes! The architecture is completely subject-agnostic. Adding Physics only requires defining concept nodes and prerequisite links (e.g., Vectors -> Kinematics -> Newton's Laws). Zero changes to the backend engine are required.")
    ]

    for q, a in qa_list:
        qa_content = Paragraph(f"<b>{q}</b><br/>{a}", body_style)
        qa_table = Table([[qa_content]], colWidths=[540])
        qa_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), light_bg),
            ('BOX', (0,0), (-1,-1), 0.5, border_color),
            ('LEFTPADDING', (0,0), (-1,-1), 7),
            ('RIGHTPADDING', (0,0), (-1,-1), 7),
            ('TOPPADDING', (0,0), (-1,-1), 3.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ]))
        story.append(qa_table)
        story.append(Spacer(1, 3))

    doc.build(story)
    print(f"PDF generated successfully at: {filename}")

if __name__ == "__main__":
    pdf_path = os.path.join(os.getcwd(), "GapWise_AI_SIH2026_Pitch_and_Architecture.pdf")
    create_pdf(pdf_path)
