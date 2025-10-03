#!/usr/bin/env python3
"""Create beautiful interactive charts using Plotly."""
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def read_csv(path: str) -> pd.DataFrame:
    """Read CSV with semicolon delimiter."""
    df = pd.read_csv(path, sep=';', parse_dates=['Timestamp'], dayfirst=True)
    # Clean column names
    df.columns = df.columns.str.strip()
    return df


def create_all_charts(df: pd.DataFrame) -> list:
    """Create all charts and return list of dicts: {fig, desc}."""
    charts = []
    
    # Dark theme template
    template = "plotly_dark"
    colors = px.colors.qualitative.Set3
    
    # Column names (exact, from CSV)
    region_col = 'Where do you live? (Region)'
    conn_col = 'What is your main type of internet connection?'
    stability_col = 'How would you rate the stability of your internet connection in 2025?'
    hours_no_internet_col = 'On average, how many hours per day do you not have internet connection?'
    outage_freq_col = 'How often did you experience power outages in 2025?'
    outage_duration_col = 'What was the average duration of outages (hours) in 2025?'
    backup_yes_col = 'Do you have a backup power source (e.g., UPS, generator, solar energy)?'
    backup_type_col = 'If yes, what kind of backup power source do you have?'
    backup_duration_col = 'If yes, how long can it provide power on average per day?'
    device_col = 'What number and type of devices are available to you?'
    workplace_col = 'Do you have a separate workplace at home?'
    accessories_col = 'Do you have the necessary accessories (webcam, headset)?'
    ergonomic_col = 'Is your workplace ergonomically equipped (chair, desk, lighting, ventilation)?'

    # Short titles for charts
    short_titles = {
        region_col: 'Region distribution',
        conn_col: 'Internet connection type',
        stability_col: 'Connection stability rating',
        hours_no_internet_col: 'Hours without internet (per day)',
        outage_freq_col: 'Power outage frequency',
        outage_duration_col: 'Outage duration (hours)',
        backup_yes_col: 'Backup power availability',
        backup_type_col: 'Types of backup power',
        backup_duration_col: 'Backup power duration (hours)',
        device_col: 'Available device type',
        workplace_col: 'Separate workplace at home',
        accessories_col: 'Accessories availability',
        ergonomic_col: 'Workplace ergonomics'
    }

    # 1. Region distribution (Pie)
    region_counts = df[region_col].value_counts()
    fig1 = go.Figure(data=go.Pie(
        labels=list(region_counts.index),
        values=[int(v) for v in region_counts.values],
        hole=0.4,
        marker=dict(colors=colors),
        textinfo='label+value+percent',
        textposition='auto'
    ))
    fig1.update_layout(
        title=f"{short_titles[region_col]} (n={int(region_counts.sum())})",
        template=template,
        height=500,
        showlegend=True
    )
    # Description
    top_reg = region_counts.idxmax()
    top_share = round(100 * int(region_counts.max()) / int(region_counts.sum()), 1)
    desc1 = f"Top region: {top_reg} ({top_share}%). Total regions: {len(region_counts)}."
    charts.append({"fig": fig1, "desc": desc1})
    
    # 2. Internet connection type (Pie)
    conn_counts = df[conn_col].value_counts()
    fig2 = go.Figure(data=go.Pie(
        labels=list(conn_counts.index),
        values=[int(v) for v in conn_counts.values],
        hole=0.4,
        marker=dict(colors=colors),
        textinfo='label+value+percent',
        textposition='auto'
    ))
    fig2.update_layout(
        title=f"{short_titles[conn_col]}",
        template=template,
        height=500
    )
    top_conn = conn_counts.idxmax()
    top_conn_share = round(100 * int(conn_counts.max()) / int(conn_counts.sum()), 1)
    desc2 = f"Most common connection: {top_conn} ({top_conn_share}%)."
    charts.append({"fig": fig2, "desc": desc2})
    
    # 3. Stability rating (Pie)
    stability_counts = df[stability_col].value_counts()
    fig3 = go.Figure(data=go.Pie(
        labels=list(stability_counts.index),
        values=[int(v) for v in stability_counts.values],
        hole=0.4,
        marker=dict(colors=['#00ff88', '#ff6b6b']),
        textinfo='label+value+percent',
        textposition='auto'
    ))
    fig3.update_layout(
        title=f"{short_titles[stability_col]}",
        template=template,
        height=500
    )
    if len(stability_counts) >= 1:
        major_label = stability_counts.idxmax()
        major_share = round(100 * int(stability_counts.max()) / int(stability_counts.sum()), 1)
        desc3 = f"Majority rated: {major_label} ({major_share}%)."
    else:
        desc3 = "No stability data."
    charts.append({"fig": fig3, "desc": desc3})
    
    # 4. Hours without internet (Histogram or annotation)
    hours_col = hours_no_internet_col
    s_hours = pd.to_numeric(df[hours_col].replace(',', '.', regex=True), errors='coerce')
    s_hours = s_hours.dropna()
    if len(s_hours) == 0:
        fig4 = go.Figure()
        fig4.update_layout(title=f"{short_titles[hours_col]}", template=template, height=400)
        fig4.add_annotation(text="No data", showarrow=False, x=0.5, y=0.5, xref='paper', yref='paper', font=dict(size=16))
        charts.append({"fig": fig4, "desc": "All responses are zero or missing."})
    elif s_hours.sum() == 0:
        fig4 = go.Figure()
        fig4.update_layout(title=f"{short_titles[hours_col]}", template=template, height=400)
        fig4.add_annotation(text="All respondents reported 0 hours per day without internet", showarrow=False, x=0.5, y=0.5, xref='paper', yref='paper', font=dict(size=16))
        charts.append({"fig": fig4, "desc": "All respondents reported 0 hours without internet."})
    else:
        fig4 = go.Figure(data=go.Histogram(
            x=s_hours,
            nbinsx=10,
            marker=dict(color='#00d4ff', line=dict(color='#ffffff', width=1))
        ))
        fig4.update_layout(
            title=f"{short_titles[hours_col]}",
            xaxis_title="Hours",
            yaxis_title="Count",
            template=template,
            height=400
        )
        desc4 = f"Median: {round(float(s_hours.median()),2)} h; Mean: {round(float(s_hours.mean()),2)} h."
        charts.append({"fig": fig4, "desc": desc4})
    
    # 5. Power outage frequency (Bar)
    outage_freq = df[outage_freq_col].value_counts()
    fig5 = go.Figure(data=go.Bar(
        x=outage_freq.index,
        y=outage_freq.values,
        marker=dict(color='#ff9f43', line=dict(color='#ffffff', width=1))
    ))
    fig5.update_layout(
        title=f"{short_titles[outage_freq_col]}",
        xaxis_title="Frequency",
        yaxis_title="Count",
        template=template,
        height=400
    )
    desc5 = ", ".join([f"{k}: {int(v)}" for k, v in outage_freq.items()])
    charts.append({"fig": fig5, "desc": desc5})
    
    # 6. Outage duration (Box plot)
    duration_col = outage_duration_col
    s_duration_all = pd.to_numeric(df[duration_col].replace(',', '.', regex=True), errors='coerce').dropna()
    # Show only positive durations; if all non-positive, add explanation
    s_duration = s_duration_all[s_duration_all > 0]
    if len(s_duration_all) == 0:
        fig6 = go.Figure()
        fig6.update_layout(title=f"{short_titles[duration_col]}", template=template, height=450)
        fig6.add_annotation(text="No data available for outage duration", showarrow=False, x=0.5, y=0.5, xref='paper', yref='paper', font=dict(size=16))
        charts.append({"fig": fig6, "desc": "No outage duration data."})
    elif len(s_duration) == 0:
        fig6 = go.Figure()
        fig6.update_layout(title=f"{short_titles[duration_col]}", template=template, height=450)
        fig6.add_annotation(text="All respondents reported 0 hours (no outages or zero-duration)", showarrow=False, x=0.5, y=0.5, xref='paper', yref='paper', font=dict(size=16))
        charts.append({"fig": fig6, "desc": "All durations are zero."})
    else:
        duration_counts = s_duration.round(3).value_counts().sort_index()
        fig6 = go.Figure(data=go.Bar(
            x=[float(x) for x in duration_counts.index],
            y=[int(y) for y in duration_counts.values],
            marker=dict(color='#ee5a6f', line=dict(color='#ffffff', width=1)),
            text=[int(y) for y in duration_counts.values],
            textposition='auto'
        ))
        fig6.update_layout(
            title=f"{short_titles[duration_col]}",
            xaxis_title="Hours",
            yaxis_title="Count",
            template=template,
            height=450
        )
        desc6 = f"min={round(float(s_duration.min()),3)}h, median={round(float(s_duration.median()),3)}h, max={round(float(s_duration.max()),3)}h"
        charts.append({"fig": fig6, "desc": desc6})
    
    # 7. Backup power source (Pie)
    backup_counts = df[backup_yes_col].value_counts()
    fig7 = go.Figure(data=go.Pie(
        labels=list(backup_counts.index),
        values=[int(v) for v in backup_counts.values],
        hole=0.4,
        marker=dict(colors=['#ff6b6b', '#51cf66']),
        textinfo='label+value+percent',
        textposition='auto'
    ))
    fig7.update_layout(
        title=f"{short_titles[backup_yes_col]}",
        template=template,
        height=500
    )
    share_yes = round(100 * int(backup_counts.get('Yes', 0)) / int(backup_counts.sum()), 1) if int(backup_counts.sum()) else 0
    desc7 = f"Yes: {int(backup_counts.get('Yes',0))} ({share_yes}%), No: {int(backup_counts.get('No',0))}."
    charts.append({"fig": fig7, "desc": desc7})
    
    # 8. Type of backup (Horizontal Bar for better readability)
    backup_type = df[backup_type_col].value_counts()
    backup_type = backup_type[(backup_type.index != '-') & (backup_type.index.str.strip() != '')]
    if len(backup_type) > 0:
        labels_bt = [str(l) for l in list(backup_type.index)]
        values_bt = [int(v) for v in list(backup_type.values)]
        fig8 = go.Figure(data=go.Bar(
            y=labels_bt,
            x=values_bt,
            orientation='h',
            marker=dict(color='#a29bfe', line=dict(color='#ffffff', width=1)),
            text=values_bt,
            textposition='auto'
        ))
        fig8.update_layout(
            title=f"{short_titles[backup_type_col]} (actual users)",
            xaxis_title="Count",
            yaxis_title="Type",
            template=template,
            height=400
        )
        desc8 = ", ".join([f"{labels_bt[i]}: {values_bt[i]}" for i in range(len(labels_bt))])
        charts.append({"fig": fig8, "desc": desc8})
    
    # 9. Backup duration (Bar chart with actual values only)
    backup_duration_col = backup_duration_col
    df_backup_dur = df[backup_duration_col].replace(',', '.', regex=True)
    try:
        df_backup_dur = pd.to_numeric(df_backup_dur, errors='coerce')
        df_backup_dur = df_backup_dur[df_backup_dur > 0].dropna()
        if len(df_backup_dur) > 0:
            duration_counts = df_backup_dur.value_counts().sort_index()
            x_vals = [float(x) for x in list(duration_counts.index)]
            y_vals = [int(y) for y in list(duration_counts.values)]
            fig9 = go.Figure(data=go.Bar(
                x=x_vals,
                y=y_vals,
                marker=dict(color='#fd79a8', line=dict(color='#ffffff', width=1)),
                text=y_vals,
                textposition='auto'
            ))
            fig9.update_layout(
                title=f"{short_titles[backup_duration_col]} (actual users)",
                xaxis_title="Hours",
                yaxis_title="Count",
                template=template,
                height=450
            )
            desc9 = ", ".join([f"{x_vals[i]}h: {y_vals[i]}" for i in range(len(x_vals))])
            charts.append({"fig": fig9, "desc": desc9})
    except Exception:
        pass
    
    # 10. Device type (Pie)
    device_counts = df[device_col].value_counts()
    fig10 = go.Figure(data=go.Pie(
        labels=list(device_counts.index),
        values=[int(v) for v in device_counts.values],
        hole=0.4,
        marker=dict(colors=colors),
        textinfo='label+value+percent',
        textposition='auto'
    ))
    fig10.update_layout(
        title=f"{short_titles[device_col]}",
        template=template,
        height=500
    )
    desc10 = ", ".join([f"{k}: {int(v)}" for k, v in device_counts.items()])
    charts.append({"fig": fig10, "desc": desc10})
    
    # 11. Separate workplace (Pie)
    workplace_counts = df[workplace_col].value_counts()
    fig11 = go.Figure(data=go.Pie(
        labels=list(workplace_counts.index),
        values=[int(v) for v in workplace_counts.values],
        hole=0.4,
        marker=dict(colors=['#51cf66', '#ff6b6b']),
        textinfo='label+value+percent',
        textposition='auto'
    ))
    fig11.update_layout(
        title=f"{short_titles[workplace_col]}",
        template=template,
        height=500
    )
    desc11 = ", ".join([f"{k}: {int(v)}" for k, v in workplace_counts.items()])
    charts.append({"fig": fig11, "desc": desc11})
    
    # 12. Accessories (Pie)
    accessories_counts = df[accessories_col].value_counts()
    fig12 = go.Figure(data=go.Pie(
        labels=list(accessories_counts.index),
        values=[int(v) for v in accessories_counts.values],
        hole=0.4,
        marker=dict(colors=['#51cf66', '#ffd93d']),
        textinfo='label+value+percent',
        textposition='auto'
    ))
    fig12.update_layout(
        title=f"{short_titles[accessories_col]}",
        template=template,
        height=500
    )
    desc12 = ", ".join([f"{k}: {int(v)}" for k, v in accessories_counts.items()])
    charts.append({"fig": fig12, "desc": desc12})
    
    # 13. Ergonomic equipment (Bar)
    ergo_counts = df[ergonomic_col].value_counts()
    fig13 = go.Figure(data=go.Bar(
        x=ergo_counts.index,
        y=ergo_counts.values,
        marker=dict(color=['#51cf66', '#ffd93d', '#ff6b6b'], line=dict(color='#ffffff', width=1))
    ))
    fig13.update_layout(
        title=f"{short_titles[ergonomic_col]}",
        xaxis_title="Level",
        yaxis_title="Count",
        template=template,
        height=400
    )
    desc13 = ", ".join([f"{k}: {int(v)}" for k, v in ergo_counts.items()])
    charts.append({"fig": fig13, "desc": desc13})
    
    return charts


def create_html_report(charts: list, output_path: str):
    """Combine all charts into single HTML file."""
    html_parts = [
        """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Internet Connection Stability Analysis</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        body {
            background-color: #1a1a1a;
            color: #e0e0e0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            margin: 0;
            padding: 20px;
        }
        h1 {
            text-align: center;
            color: #00d4ff;
            font-size: 2.5em;
            margin: 30px 0;
        }
        .chart-container {
            max-width: 1200px;
            margin: 40px auto;
            background: #2d2d2d;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 212, 255, 0.1);
        }
        .chart {
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>📊 Internet Connection Stability Analysis</h1>
    <div class="chart-container">
"""
    ]
    
    for idx, item in enumerate(charts):
        fig = item["fig"]
        desc = item.get("desc", "")
        chart_html = fig.to_html(
            full_html=False,
            include_plotlyjs=False,
            div_id=f"chart_{idx}"
        )
        html_parts.append(f'<div class="chart">{chart_html}<div style="margin-top:8px;color:#9aa4b2;">{desc}</div></div>')
    
    html_parts.append("""
    </div>
</body>
</html>
""")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_parts))


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to CSV file")
    parser.add_argument("--output", default="charts_report.html", help="Output HTML file")
    args = parser.parse_args()
    
    print("📖 Reading CSV...")
    df = read_csv(args.input)
    print(f"✓ Loaded {len(df)} rows, {len(df.columns)} columns")
    
    print("\n📊 Creating charts...")
    charts = create_all_charts(df)
    print(f"✓ Created {len(charts)} charts")
    
    print(f"\n💾 Saving to {args.output}...")
    create_html_report(charts, args.output)
    print("✓ Done!")
    print(f"\n🌐 Open: {args.output}")


if __name__ == "__main__":
    main()

