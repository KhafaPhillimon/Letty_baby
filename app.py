"""
AI Solutions – SaaS Log Analytics Platform
Refined SaaS-style Interface (Senior Developer Edition)
"""

import dash
from dash import dcc, html, dash_table, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import flask

# ── SaaS Design System ───────────────────────────────────────────────────────
BG      = "#fcfcfc"  # Ultra-clean white-grey
SIDEBAR = "#ffffff"
CARD_BG = "#ffffff"
ACCENT  = "#2563eb"  # Sharp SaaS Blue
TEXT    = "#0f172a"  # Slate-900
MUTED   = "#64748b"  # Slate-500
BORDER  = "#e2e8f0"  # Slate-200
SUCCESS = "#10b981"  # Emerald-500
DANGER  = "#ef4444"  # Rose-500

# ── Authorised users ─────────────────────────────────────────────────────────
USERS = {
    "admin":  "aisolutions2026",
    "letty":  "dashboard123",
    "viewer": "view2026",
}

# ── Data Loading ─────────────────────────────────────────────────────────────
CSV_PATH = "AI_Solutions_Web_Log_Dataset.csv"

def load_data():
    df = pd.read_csv(CSV_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"], dayfirst=True)
    df["date"]      = df["timestamp"].dt.date
    df["hour"]      = df["timestamp"].dt.hour
    df["week"]      = df["timestamp"].dt.isocalendar().week.astype(int)
    df["status_code"] = df["status_code"].astype(str)
    return df

df = load_data()

SERVICE_COLOURS = {
    "Job Request":       "#2563eb",
    "Demo Request":      "#0ea5e9",
    "Demo Submission":   "#3b82f6",
    "AI Assistant":      "#6366f1",
    "Promotional Event": "#f59e0b",
    "Prototype Request": "#10b981",
    "Homepage":          "#94a3b8",
    "Image Asset":       "#cbd5e1",
    "CSS Asset":         "#e2e8f0",
    "Job Application":   "#06b6d4",
    "Contact Page":      "#f43f5e",
}

# ── Dash Setup ───────────────────────────────────────────────────────────────
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)
app.title = "AI Solutions"
GOOGLE_FONT = "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"

# ═══════════════════════════════════════════════════════════════════════════════
#  COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════════
def stat_card(title, value, subtitle="", colour=ACCENT):
    return html.Div(
        style={
            "background": CARD_BG, "borderRadius": "12px",
            "padding": "24px", "flex": "1",
            "border": f"1px solid {BORDER}",
            "transition": "transform 0.2s, box-shadow 0.2s",
        },
        children=[
            html.P(title, style={"color": MUTED, "fontSize": "11px", "fontWeight": "600", "margin": "0 0 8px", "letterSpacing": "0.05em", "textTransform": "uppercase"}),
            html.H2(value, style={"color": TEXT, "fontSize": "28px", "fontWeight": "700", "margin": "0 0 2px"}),
            html.P(subtitle, style={"color": MUTED, "fontSize": "12px", "margin": "0", "display": "flex", "alignItems": "center"}),
        ]
    )

def section_title(text):
    return html.H3(text, style={"color": TEXT, "fontSize": "14px", "fontWeight": "600", "margin": "0 0 24px", "letterSpacing": "-0.01em"})

def chart_card(children):
    return html.Div(style={"background": CARD_BG, "borderRadius": "12px", "padding": "28px", "border": f"1px solid {BORDER}"}, children=children)

chart_style = {
    "plot_bgcolor":  "rgba(0,0,0,0)",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "font_family":   "Inter, sans-serif",
    "font_color":    TEXT,
    "margin":        dict(l=10, r=10, t=10, b=10),
}

# ═══════════════════════════════════════════════════════════════════════════════
#  LOGIN PAGE
# ═══════════════════════════════════════════════════════════════════════════════
login_layout = html.Div(
    style={"minHeight": "100vh", "background": BG, "display": "flex", "alignItems": "center", "justifyContent": "center", "fontFamily": "Inter, sans-serif"},
    children=[
        html.Link(rel="stylesheet", href=GOOGLE_FONT),
        html.Div(
            style={"width": "100%", "maxWidth": "360px", "textAlign": "center"},
            children=[
                html.Img(src="/assets/logo.png", style={"height": "64px", "marginBottom": "24px"}),
                html.H1("AI Solutions", style={"color": TEXT, "fontSize": "24px", "fontWeight": "700", "margin": "0 0 8px", "letterSpacing": "-0.02em"}),
                html.P("Log Analytics Platform", style={"color": MUTED, "fontSize": "14px", "marginBottom": "32px"}),
                
                html.Div(
                    style={"background": CARD_BG, "borderRadius": "12px", "padding": "32px", "border": f"1px solid {BORDER}", "textAlign": "left", "boxShadow": "0 4px 6px -1px rgba(0,0,0,0.05)"},
                    children=[
                        html.Label("Username", style={"color": TEXT, "fontSize": "13px", "fontWeight": "500"}),
                        dcc.Input(id="login-username", type="text", placeholder="Enter username", debounce=True, style={"width": "100%", "height": "42px", "padding": "0 12px", "background": "white", "border": f"1px solid {BORDER}", "borderRadius": "6px", "color": TEXT, "fontSize": "14px", "marginTop": "6px", "marginBottom": "20px", "boxSizing": "border-box", "outline": "none"}),
                        html.Label("Password", style={"color": TEXT, "fontSize": "13px", "fontWeight": "500"}),
                        dcc.Input(id="login-password", type="password", placeholder="••••••••", debounce=True, style={"width": "100%", "height": "42px", "padding": "0 12px", "background": "white", "border": f"1px solid {BORDER}", "borderRadius": "6px", "color": TEXT, "fontSize": "14px", "marginTop": "6px", "marginBottom": "12px", "boxSizing": "border-box", "outline": "none"}),
                        html.Div(id="login-error", style={"color": DANGER, "fontSize": "12px", "marginBottom": "20px", "minHeight": "18px"}),
                        html.Button("Sign In", id="login-btn", n_clicks=0, style={"width": "100%", "padding": "12px", "background": TEXT, "border": "none", "borderRadius": "6px", "color": "white", "fontSize": "14px", "fontWeight": "600", "cursor": "pointer"}),
                    ]
                ),
                html.P("© 2026 AI Solutions", style={"color": MUTED, "fontSize": "12px", "marginTop": "32px"}),
            ]
        )
    ]
)

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGES
# ═══════════════════════════════════════════════════════════════════════════════
def generate_overview_page(filtered):
    total = len(filtered)
    success_cnt = len(filtered[filtered["status_code"] == "200"])
    error_cnt   = len(filtered[filtered["status_code"] == "500"])
    countries_n = filtered["country"].nunique()
    success_pct = f"{success_cnt/total*100:.1f}%" if total > 0 else "0%"

    kpi = html.Div(
        style={"display": "flex", "gap": "24px", "marginBottom": "32px"},
        children=[
            stat_card("Total Traffic", f"{total:,}", "Individual requests"),
            stat_card("Success Rate", success_pct, f"{success_cnt} Successful"),
            stat_card("Critical Errors", f"{error_cnt}", "Status 500"),
            stat_card("Market Reach", str(countries_n), "Active countries"),
        ]
    )
    return html.Div([
        kpi,
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr", "gap": "24px"},
            children=[
                chart_card([
                    section_title("Operational Overview"),
                    html.P("Monitor real-time AI infrastructure performance. This platform provides deep visibility into traffic origins, service load, and response metrics across the global AI Solutions network.", style={"color": MUTED, "lineHeight": "1.6", "fontSize": "14px"}),
                    html.Div(style={"height": "1px", "background": BORDER, "margin": "24px 0"}),
                    html.Div(style={"display": "flex", "alignItems": "center", "gap": "8px"}, children=[
                        html.Div(style={"width": "6px", "height": "6px", "borderRadius": "50%", "background": SUCCESS}),
                        html.P("All systems functional", style={"color": SUCCESS, "fontSize": "12px", "fontWeight": "600", "margin": "0"})
                    ])
                ])
            ]
        )
    ])

def generate_countries_page(filtered):
    country_counts = filtered.groupby("country").size().reset_index(name="count")
    fig_map = px.choropleth(country_counts, locations="country", locationmode="country names", color="count", color_continuous_scale="Blues")
    fig_map.update_layout(**chart_style, geo=dict(bgcolor="rgba(0,0,0,0)", showframe=False))

    fig_bar = px.bar(country_counts.sort_values("count", ascending=False), x="country", y="count", color_discrete_sequence=[ACCENT])
    fig_bar.update_layout(**chart_style)

    return html.Div(style={"display": "grid", "gap": "32px"}, children=[
        chart_card([section_title("Geographical Distribution"), dcc.Graph(figure=fig_map, config={"displayModeBar": False})]),
        chart_card([section_title("Traffic by Region"), dcc.Graph(figure=fig_bar, config={"displayModeBar": False})])
    ])

def generate_services_page(filtered):
    service_counts = filtered.groupby("service_type").size().reset_index(name="count")
    fig_pie = px.pie(service_counts, names="service_type", values="count", color="service_type", color_discrete_map=SERVICE_COLOURS, hole=0.7)
    fig_pie.update_layout(**chart_style)
    fig_pie.update_traces(textinfo="none")

    fig_bar = px.bar(service_counts.sort_values("count", ascending=True), x="count", y="service_type", orientation="h", color="service_type", color_discrete_map=SERVICE_COLOURS)
    fig_bar.update_layout(**chart_style, showlegend=False)

    return html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "32px"}, children=[
        chart_card([section_title("Service Composition"), dcc.Graph(figure=fig_pie, config={"displayModeBar": False})]),
        chart_card([section_title("Usage breakdown"), dcc.Graph(figure=fig_bar, config={"displayModeBar": False})])
    ])

def generate_trends_page(filtered):
    daily = filtered.groupby("date").size().reset_index(name="requests")
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=daily["date"], y=daily["requests"], mode="lines", line=dict(color=ACCENT, width=2.5), fill="tozeroy", fillcolor="rgba(37, 99, 235, 0.08)"))
    fig_trend.update_layout(**chart_style, xaxis=dict(showgrid=False), yaxis=dict(gridcolor=BORDER))

    fig_scatter = px.scatter(filtered[filtered["response_size"]>0], x="timestamp", y="response_size", color="service_type", color_discrete_map=SERVICE_COLOURS, opacity=0.5)
    fig_scatter.update_layout(**chart_style)

    return html.Div(style={"display": "grid", "gap": "32px"}, children=[
        chart_card([section_title("Traffic Velocity"), dcc.Graph(figure=fig_trend, config={"displayModeBar": False})]),
        chart_card([section_title("Data Transfer Density"), dcc.Graph(figure=fig_scatter, config={"displayModeBar": False})])
    ])

def generate_statistics_page(filtered):
    stats_data = []
    for service in filtered["service_type"].unique():
        subset = filtered[(filtered["service_type"] == service) & (filtered["response_size"] > 0)]["response_size"]
        if not subset.empty:
            stats_data.append({"Service": service, "Count": len(subset), "Mean": f"{subset.mean():,.0f} B", "Peak": f"{subset.max():,} B"})
    
    stats_table = dash_table.DataTable(
        data=stats_data,
        style_table={"overflowX": "auto"},
        style_header={"backgroundColor": "white", "color": TEXT, "fontWeight": "600", "fontSize": "11px", "borderBottom": f"1px solid {TEXT}", "padding": "12px", "textTransform": "uppercase"},
        style_cell={"backgroundColor": "white", "color": TEXT, "border": "none", "borderBottom": f"1px solid {BORDER}", "padding": "16px", "fontSize": "13px", "fontFamily": "Inter, sans-serif"},
    )

    status_counts = filtered.groupby("status_code").size().reset_index(name="count")
    fig_status = px.pie(status_counts, names="status_code", values="count", color_discrete_sequence=px.colors.qualitative.Prism, hole=0.75)
    fig_status.update_layout(**chart_style)

    return html.Div(style={"display": "grid", "gridTemplateColumns": "2fr 1fr", "gap": "32px"}, children=[
        chart_card([section_title("Performance Metrics"), stats_table]),
        chart_card([section_title("Status Code Health"), dcc.Graph(figure=fig_status, config={"displayModeBar": False})])
    ])

def generate_logs_page(filtered):
    display_cols = ["timestamp","ip_address","country","method","page","service_type","status_code"]
    raw_df = filtered[display_cols].head(100).copy()
    raw_df["timestamp"] = raw_df["timestamp"].astype(str)

    raw_table = dash_table.DataTable(
        data=raw_df.to_dict("records"),
        columns=[{"name": c.replace("_"," ").title(), "id": c} for c in display_cols],
        page_size=15,
        style_table={"overflowX": "auto"},
        style_header={"backgroundColor": "white", "color": TEXT, "fontWeight": "600", "fontSize": "11px", "borderBottom": f"1px solid {TEXT}", "padding": "12px"},
        style_cell={"backgroundColor": "white", "color": TEXT, "borderBottom": f"1px solid {BORDER}", "padding": "14px", "fontSize": "12px", "fontFamily": "Inter, sans-serif"},
    )
    return chart_card([section_title("Recent Activity Logs"), raw_table])

# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN LAYOUT
# ═══════════════════════════════════════════════════════════════════════════════
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="session-store", storage_type="session"),
    html.Div(id="page-content"),
])

def dashboard_layout(pathname):
    nav_links = [
        ("/", "Dashboard"),
        ("/countries", "Analytics"),
        ("/services", "Services"),
        ("/trends", "Velocity"),
        ("/statistics", "Reporting"),
        ("/logs", "Events"),
    ]
    
    sidebar_items = []
    for path, label in nav_links:
        is_active = pathname == path or (pathname == "" and path == "/")
        sidebar_items.append(
            dcc.Link(
                label, href=path,
                style={
                    "display": "block", "color": TEXT if is_active else MUTED,
                    "padding": "10px 16px", "borderRadius": "8px", "textDecoration": "none",
                    "fontSize": "13px", "fontWeight": "500",
                    "background": f"{BORDER}40" if is_active else "transparent",
                    "marginBottom": "4px", "transition": "background 0.2s"
                }
            )
        )

    return html.Div(
        style={"fontFamily": "Inter, sans-serif", "background": BG, "minHeight": "100vh", "display": "flex"},
        children=[
            html.Link(rel="stylesheet", href=GOOGLE_FONT),
            # Sidebar
            html.Div(
                style={"width": "240px", "background": SIDEBAR, "padding": "32px 20px", "display": "flex", "flexDirection": "column", "borderRight": f"1px solid {BORDER}", "minHeight": "100vh", "flexShrink": "0"},
                children=[
                    html.Div(
                        style={"marginBottom": "40px", "padding": "0 12px"},
                        children=[
                            html.Img(src="/assets/logo.png", style={"height": "32px", "marginBottom": "12px"}),
                            html.H2("AI Solutions", style={"color": TEXT, "fontSize": "16px", "fontWeight": "700", "margin": "0", "letterSpacing": "-0.01em"}),
                        ]
                    ),
                    *sidebar_items,
                    html.Div(style={"flex": "1"}),
                    html.Button("Log out", id="logout-btn", n_clicks=0, style={"width": "100%", "padding": "10px", "background": "transparent", "border": f"1px solid {BORDER}", "borderRadius": "8px", "color": MUTED, "fontSize": "12px", "cursor": "pointer", "fontWeight": "500"}),
                ]
            ),
            # Main content
            html.Div(
                style={"flex": "1", "padding": "48px 64px", "overflowY": "auto", "height": "100vh", "boxSizing": "border-box"},
                children=[
                    html.Div(
                        style={"display": "flex", "justifyContent": "space-between", "alignItems": "flex-end", "marginBottom": "40px"},
                        children=[
                            html.Div([
                                html.P("Insights", style={"color": ACCENT, "fontSize": "11px", "fontWeight": "700", "textTransform": "uppercase", "letterSpacing": "0.1em", "margin": "0 0 4px"}),
                                html.H1("Platform Analytics", style={"color": TEXT, "fontSize": "28px", "fontWeight": "700", "margin": "0", "letterSpacing": "-0.02em"}),
                            ]),
                            html.Div(
                                style={"display": "flex", "gap": "12px", "alignItems": "center"},
                                children=[
                                    dcc.Dropdown(id="filter-country", options=[{"label": "All Markets", "value": "ALL"}] + [{"label": c, "value": c} for c in sorted(df["country"].unique())], value="ALL", clearable=False, style={"width": "160px", "fontSize": "12px"}),
                                    dcc.Dropdown(id="filter-service", options=[{"label": "All Services", "value": "ALL"}] + [{"label": s, "value": s} for s in sorted(df["service_type"].unique())], value="ALL", clearable=False, style={"width": "160px", "fontSize": "12px"}),
                                ]
                            ),
                        ]
                    ),
                    html.Div(id="dynamic-page-content")
                ]
            )
        ]
    )

# ── Callbacks ────────────────────────────────────────────────────────────────
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    Input("session-store", "data"),
)
def display_page(pathname, session):
    if session and session.get("logged_in"):
        return dashboard_layout(pathname)
    return login_layout

@app.callback(
    Output("dynamic-page-content", "children"),
    Input("url", "pathname"),
    Input("filter-country", "value"),
    Input("filter-service", "value"),
)
def update_dynamic_content(pathname, country_filter, service_filter):
    if not pathname: return dash.no_update
    
    filtered = df.copy()
    if country_filter and country_filter != "ALL":
        filtered = filtered[filtered["country"] == country_filter]
    if service_filter and service_filter != "ALL":
        filtered = filtered[filtered["service_type"] == service_filter]

    if pathname == "/countries":
        return generate_countries_page(filtered)
    elif pathname == "/services":
        return generate_services_page(filtered)
    elif pathname == "/trends":
        return generate_trends_page(filtered)
    elif pathname == "/statistics":
        return generate_statistics_page(filtered)
    elif pathname == "/logs":
        return generate_logs_page(filtered)
    else:
        return generate_overview_page(filtered)

@app.callback(
    Output("session-store", "data"),
    Output("login-error", "children"),
    Input("login-btn", "n_clicks"),
    State("login-username", "value"),
    State("login-password", "value"),
    prevent_initial_call=True,
)
def handle_login(n_clicks, username, password):
    if not username or not password:
        return dash.no_update, "Please enter credentials."
    if username in USERS and USERS[username] == password:
        return {"logged_in": True, "user": username}, ""
    return dash.no_update, "Authentication failed."

@app.callback(
    Output("session-store", "data", allow_duplicate=True),
    Output("url", "pathname", allow_duplicate=True),
    Input("logout-btn", "n_clicks"),
    prevent_initial_call=True,
)
def handle_logout(n_clicks):
    if n_clicks > 0:
        return {"logged_in": False}, "/"
    return dash.no_update, dash.no_update

if __name__ == "__main__":
    app.run(debug=True, port=8050)
