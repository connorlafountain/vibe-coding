"""
Plot Generator Service - Generates interactive Plotly graphs from IHI test data
"""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json
from pathlib import Path

# Create directory for uploads
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def detect_test_type(file_path):
    """Detect if this is commissioning or temp/humidity data"""
    filename = os.path.basename(file_path).lower()

    # Check filename patterns
    if any(keyword in filename for keyword in ['temp', 'humidity', 'rh']):
        return "temp_humidity"
    elif any(keyword in filename for keyword in ['commission', 'cx', 'ihi', 'result']):
        return "commissioning"

    # Try to detect from Excel structure
    try:
        # Check sheet names
        xl = pd.ExcelFile(file_path)
        sheet_names = [s.lower() for s in xl.sheet_names]

        # Commissioning files typically have sheets like "Charge 1", "Discharge 1", etc.
        if any('charge' in s or 'discharge' in s or 'crr' in s or 'drr' in s for s in sheet_names):
            return "commissioning"

        # Default to temp_humidity if can't determine
        return "temp_humidity"
    except:
        # If can't read, default to commissioning
        return "commissioning"


def generate_commissioning_plots(file_path, project_id):
    """Generate interactive Plotly plots for IHI commissioning test data"""
    plot_htmls = []
    base_filename = Path(file_path).stem

    try:
        # File parameters
        sheet_offset = 0
        header_row = 13

        # Read data from Excel file
        try:
            chrg_1 = pd.read_excel(file_path, 1+sheet_offset, skiprows=header_row, index_col=1)
            dchg_1 = pd.read_excel(file_path, 2+sheet_offset, skiprows=header_row, index_col=1)
            chrg_2 = pd.read_excel(file_path, 3+sheet_offset, skiprows=header_row, index_col=1)
            dchg_2 = pd.read_excel(file_path, 4+sheet_offset, skiprows=header_row, index_col=1)
            chrg_3 = pd.read_excel(file_path, 5+sheet_offset, skiprows=header_row, index_col=1)
            dchg_3 = pd.read_excel(file_path, 6+sheet_offset, skiprows=header_row, index_col=1)
            crr = pd.read_excel(file_path, 7+sheet_offset, index_col=1)
            drr = pd.read_excel(file_path, 8+sheet_offset, index_col=1)
            otc = pd.read_excel(file_path, 9+sheet_offset, index_col=1)
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return []

        cap_tests = [chrg_1, dchg_1, chrg_2, dchg_2, chrg_3, dchg_3]
        titles = ["Capacity Test #1 - Charge", "Capacity Test #1 - Discharge",
                  "Capacity Test #2 - Charge", "Capacity Test #2 - Discharge",
                  "Capacity Test #3 - Charge", "Capacity Test #3 - Discharge"]

        # Generate Capacity Test Plots
        for idx, test_data in enumerate(cap_tests):
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=("SOC (%)", "Power (kW)"),
                vertical_spacing=0.15
            )

            # SOC plot (top)
            fig.add_trace(
                go.Scatter(x=test_data.index, y=test_data.iloc[:, 1],
                          mode='lines', name='SOC'),
                row=1, col=1
            )

            # Power plots (bottom)
            fig.add_trace(
                go.Scatter(x=test_data.index, y=test_data.iloc[:, 2],
                          mode='lines', name=test_data.columns[2]),
                row=2, col=1
            )
            fig.add_trace(
                go.Scatter(x=test_data.index, y=test_data.iloc[:, 3],
                          mode='lines', name=test_data.columns[3]),
                row=2, col=1
            )
            fig.add_trace(
                go.Scatter(x=test_data.index, y=test_data.iloc[:, 4],
                          mode='lines', name=test_data.columns[4]),
                row=2, col=1
            )

            fig.update_layout(
                title_text=titles[idx],
                height=600,
                showlegend=True,
                hovermode='x unified'
            )

            fig.update_xaxes(title_text="Time", row=2, col=1)
            fig.update_yaxes(title_text="SOC (%)", row=1, col=1)
            fig.update_yaxes(title_text="Power (kW)", row=2, col=1)

            plot_htmls.append({
                'title': titles[idx],
                'html': fig.to_html(include_plotlyjs='cdn', div_id=f'plot_{project_id}_{idx}')
            })

        # Generate Charge Ramp Rate Plot
        crr_len = min(300, len(crr))
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("SOC (%)", "Power (kW)"),
            vertical_spacing=0.15
        )

        fig.add_trace(
            go.Scatter(x=crr.index[0:crr_len], y=crr.iloc[0:crr_len, 1],
                      mode='lines', name='SOC'),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(x=crr.index[0:crr_len], y=crr.iloc[0:crr_len, 2],
                      mode='lines', name=crr.columns[2]),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=crr.index[0:crr_len], y=crr.iloc[0:crr_len, 3],
                      mode='lines', name=crr.columns[3]),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=crr.index[0:crr_len], y=crr.iloc[0:crr_len, 4],
                      mode='lines', name=crr.columns[4]),
            row=2, col=1
        )

        fig.update_layout(
            title_text="Charge Ramp Rate Test",
            height=600,
            showlegend=True,
            hovermode='x unified'
        )

        fig.update_xaxes(title_text="Time", row=2, col=1)
        fig.update_yaxes(title_text="SOC (%)", row=1, col=1)
        fig.update_yaxes(title_text="Power (kW)", row=2, col=1)

        plot_htmls.append({
            'title': 'Charge Ramp Rate Test',
            'html': fig.to_html(include_plotlyjs='cdn', div_id=f'plot_{project_id}_crr')
        })

        # Generate Discharge Ramp Rate Plot
        drr_len = min(300, len(drr))
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("SOC (%)", "Power (kW)"),
            vertical_spacing=0.15
        )

        fig.add_trace(
            go.Scatter(x=drr.index[0:drr_len], y=drr.iloc[0:drr_len, 1],
                      mode='lines', name='SOC'),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(x=drr.index[0:drr_len], y=drr.iloc[0:drr_len, 2],
                      mode='lines', name=drr.columns[2]),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=drr.index[0:drr_len], y=drr.iloc[0:drr_len, 3],
                      mode='lines', name=drr.columns[3]),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=drr.index[0:drr_len], y=drr.iloc[0:drr_len, 4],
                      mode='lines', name=drr.columns[4]),
            row=2, col=1
        )

        fig.update_layout(
            title_text="Discharge Ramp Rate Test",
            height=600,
            showlegend=True,
            hovermode='x unified'
        )

        fig.update_xaxes(title_text="Time", row=2, col=1)
        fig.update_yaxes(title_text="SOC (%)", row=1, col=1)
        fig.update_yaxes(title_text="Power (kW)", row=2, col=1)

        plot_htmls.append({
            'title': 'Discharge Ramp Rate Test',
            'html': fig.to_html(include_plotlyjs='cdn', div_id=f'plot_{project_id}_drr')
        })

        # Generate Output Transition Control Plot
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("SOC (%)", "Power (kW)"),
            vertical_spacing=0.15
        )

        fig.add_trace(
            go.Scatter(x=otc.index, y=otc.iloc[:, 1],
                      mode='lines', name='SOC'),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(x=otc.index, y=otc.iloc[:, 2],
                      mode='lines', name=otc.columns[2]),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=otc.index, y=otc.iloc[:, 3],
                      mode='lines', name=otc.columns[3]),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=otc.index, y=otc.iloc[:, 4],
                      mode='lines', name=otc.columns[4]),
            row=2, col=1
        )

        fig.update_layout(
            title_text="Output Transition Control Test",
            height=600,
            showlegend=True,
            hovermode='x unified'
        )

        fig.update_xaxes(title_text="Time", row=2, col=1)
        fig.update_yaxes(title_text="SOC (%)", row=1, col=1)
        fig.update_yaxes(title_text="Power (kW)", row=2, col=1)

        plot_htmls.append({
            'title': 'Output Transition Control Test',
            'html': fig.to_html(include_plotlyjs='cdn', div_id=f'plot_{project_id}_otc')
        })

    except Exception as e:
        print(f"Error generating commissioning plots: {e}")
        import traceback
        traceback.print_exc()

    return plot_htmls


def generate_temp_humidity_plots(file_path, project_id):
    """Generate interactive Plotly plots for temperature and humidity data"""
    plot_htmls = []
    base_filename = Path(file_path).stem

    try:
        # Read the Excel file
        header_row = 1
        idx_col = 1

        data = pd.read_excel(file_path, index_col=idx_col, skiprows=header_row)

        # Remove non-local timestamp if exists
        if 't_stamp' in data.columns:
            data = data.drop('t_stamp', axis=1)

        # Acceptance Criteria
        max_temp = 30
        max_humidity = 80

        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("Relative Humidity (%)", "Container Temperature (°C)"),
            vertical_spacing=0.12
        )

        # Top plot for humidity
        for x in range(0, data.shape[1], 4):
            if x < data.shape[1]:
                fig.add_trace(
                    go.Scatter(x=data.index, y=data.iloc[:, x],
                              mode='lines', name=data.columns[x]),
                    row=1, col=1
                )

        # Add humidity threshold line
        fig.add_hline(y=max_humidity, line_dash="dash", line_color="red",
                     annotation_text="Max Humidity (80%)", row=1, col=1)

        # Bottom plot for temperature
        for y in range(0, data.shape[1], 4):
            if y+1 < data.shape[1]:
                fig.add_trace(
                    go.Scatter(x=data.index, y=data.iloc[:, y+1],
                              mode='lines', name=data.columns[y+1]),
                    row=2, col=1
                )
            if y+2 < data.shape[1]:
                try:
                    fig.add_trace(
                        go.Scatter(x=data.index, y=data.iloc[:, y+2],
                                  mode='lines', name=data.columns[y+2]),
                        row=2, col=1
                    )
                except:
                    pass
            if y+3 < data.shape[1]:
                try:
                    fig.add_trace(
                        go.Scatter(x=data.index, y=data.iloc[:, y+3],
                                  mode='lines', name=data.columns[y+3]),
                        row=2, col=1
                    )
                except:
                    pass

        # Add temperature threshold line
        fig.add_hline(y=max_temp, line_dash="dash", line_color="red",
                     annotation_text="Max Temperature (30°C)", row=2, col=1)

        fig.update_layout(
            title_text="Container Conditions - Temperature & Humidity",
            height=700,
            showlegend=True,
            hovermode='x unified'
        )

        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Relative Humidity (%)", range=[0, 100], row=1, col=1)
        fig.update_yaxes(title_text="Temperature (°C)", row=2, col=1)

        plot_htmls.append({
            'title': 'Temperature & Humidity Monitoring',
            'html': fig.to_html(include_plotlyjs='cdn', div_id=f'plot_{project_id}_temp_humidity')
        })

    except Exception as e:
        print(f"Error generating temp/humidity plots: {e}")
        import traceback
        traceback.print_exc()

    return plot_htmls


def generate_plots_from_file(file_path, project_id):
    """
    Main entry point: detect test type and generate appropriate interactive plots
    Returns: dict with test_type and list of plot HTML divs
    """
    test_type = detect_test_type(file_path)

    if test_type == "commissioning":
        plot_htmls = generate_commissioning_plots(file_path, project_id)
    else:
        plot_htmls = generate_temp_humidity_plots(file_path, project_id)

    return {
        "test_type": test_type,
        "plots": plot_htmls  # Now returns list of {'title': ..., 'html': ...} dicts
    }
