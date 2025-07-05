from fpdf import FPDF

# Initialize PDF
pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Jinja2 Template Essentials: Student-Friendly Cheatsheet", ln=True)

# Set regular font for body text
pdf.set_font("Arial", "", 12)

# Sections of the cheatsheet
sections = [
    ("🎯 Must-Know Filters (~10)", [
        "|e – escape HTML (for safe rendering)",
        "|safe – mark string as safe (disable escaping)",
        "|length – number of items",
        "|default('value') – default if undefined",
        "|replace('a', 'b') – string replacement",
        "|join(', ') – join list into string",
        "|lower / |upper / |capitalize – text transforms",
        "|urlencode – encode for URLs"
    ]),
    ("🔁 Loop Variables", [
        "loop.index – 1-based index",
        "loop.index0 – 0-based index",
        "loop.first – True on first iteration",
        "loop.last – True on last iteration",
        "loop.revindex – countdown from end"
    ]),
    ("🧱 Template Tags", [
        "{% for item in list %} – loop",
        "{% if condition %} – conditional",
        "{% else %}, {% elif %}",
        "{% set var = value %} – define local variable",
        "{% include 'file.html' %} – import partial",
        "{% block content %}, {% extends 'base.html' %} – inheritance",
        "{% macro name(args) %} – reusable template function"
    ]),
    ("🔍 Useful Tests (`is`)", [
        "is defined / not defined",
        "is none / not none",
        "is string / is number",
        "is iterable / mapping"
    ]),
    ("🧠 Global Functions", [
        "range(start, end)",
        "dict(a=1, b=2)",
        "url_for('route_name') – Flask routing",
        "int(), str(), list()"
    ]),
    ("📚 Flask Context Globals (auto-available)", [
        "request – current request data",
        "session – session dict",
        "config – app config",
        "g – global context object"
    ]),
    ("✅ Tip:", [
        "Use {{ var | pprint }} to explore objects in debug mode.",
        "Visit https://jinja.palletsprojects.com for full docs."
    ])
]

# Add sections to PDF
for title, items in sections:
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, title, ln=True)
    pdf.set_font("Arial", "", 12)
    for item in items:
        pdf.multi_cell(0, 8, f"• {item}")
    pdf.ln(2)

# Save PDF
cheatsheet_path = "/static/Jinja2_Cheatsheet.pdf"
pdf.output(cheatsheet_path)
cheatsheet_path
