"""
Plot Generator Service - Adapts IHI plotting scripts to save images
"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import matplotlib.dates as md
import os
import json
from pathlib import Path

# Create directories for uploads and plots
UPLOAD_DIR = Path("uploads")
PLOTS_DIR = Path("static/plots")
UPLOAD_DIR.mkdir(exist_ok=True)
PLOTS_DIR.mkdir(exist_ok=True)


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
    """Generate plots for IHI commissioning test data"""
    plot_paths = []
    base_filename = Path(file_path).stem

    try:
        # File parameters (simplified from original script)
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
            # Return empty list if can't read file
            return []

        cap_tests = [chrg_1, dchg_1, chrg_2, dchg_2, chrg_3, dchg_3]
        titles = ["Capacity Test #1 - Charge", "Capacity Test #1 - Discharge",
                  "Capacity Test #2 - Charge", "Capacity Test #2 - Discharge",
                  "Capacity Test #3 - Charge", "Capacity Test #3 - Discharge"]

        # Generate Capacity Test Plots
        for idx, test_data in enumerate(cap_tests):
            fig = plt.figure(figsize=(10, 5))

            plt.subplot(211)
            plt.plot(test_data.iloc[:, 1])
            plt.ylabel("SOC (%)")
            plt.title(titles[idx])
            plt.grid(which='major', axis='both')
            plt.gca().xaxis.set_major_locator(md.HourLocator(interval=1))
            plt.gca().xaxis.set_major_formatter(md.DateFormatter('%D %H:%M'))
            plt.xticks(rotation=45)

            plt.subplot(212)
            plt.plot(test_data.iloc[:, 2], label=test_data.columns[2])
            plt.plot(test_data.iloc[:, 3], label=test_data.columns[3])
            plt.plot(test_data.iloc[:, 4], label=test_data.columns[4])
            plt.ylabel("Power (kW)")
            plt.legend()
            plt.grid(which='both', axis='both')
            plt.gca().xaxis.set_major_locator(md.HourLocator(interval=1))
            plt.gca().xaxis.set_major_formatter(md.DateFormatter('%D %H:%M'))
            plt.xticks(rotation=45)

            plt.tight_layout()

            # Save plot
            plot_filename = f"project_{project_id}_{base_filename}_capacity_{idx+1}.png"
            plot_path = PLOTS_DIR / plot_filename
            plt.savefig(plot_path, dpi=150, bbox_inches='tight')
            plt.close(fig)

            plot_paths.append(f"/static/plots/{plot_filename}")

        # Generate Charge Ramp Rate Plot
        crr_len = min(300, len(crr))
        fig = plt.figure(figsize=(10, 5))

        plt.subplot(211)
        plt.plot(crr.iloc[0:crr_len, 1])
        plt.ylabel("SOC (%)")
        plt.title("Charge Ramp Rate Test")
        plt.grid(which='major', axis='both')
        plt.gca().xaxis.set_major_locator(md.SecondLocator(interval=5))
        plt.gca().xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
        plt.xticks(rotation=45)

        plt.subplot(212)
        plt.plot(crr.iloc[0:crr_len, 2], label=crr.columns[2])
        plt.plot(crr.iloc[0:crr_len, 3], label=crr.columns[3])
        plt.plot(crr.iloc[0:crr_len, 4], label=crr.columns[4])
        plt.ylabel("Power (kW)")
        plt.legend()
        plt.grid(which='both', axis='both')
        plt.gca().xaxis.set_major_locator(md.SecondLocator(interval=5))
        plt.gca().xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
        plt.xticks(rotation=45)

        plt.tight_layout()
        plot_filename = f"project_{project_id}_{base_filename}_crr.png"
        plot_path = PLOTS_DIR / plot_filename
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        plot_paths.append(f"/static/plots/{plot_filename}")

        # Generate Discharge Ramp Rate Plot
        drr_len = min(300, len(drr))
        fig = plt.figure(figsize=(10, 5))

        plt.subplot(211)
        plt.plot(drr.iloc[0:drr_len, 1])
        plt.ylabel("SOC (%)")
        plt.title("Discharge Ramp Rate Test")
        plt.grid(which='major', axis='both')
        plt.gca().xaxis.set_major_locator(md.SecondLocator(interval=5))
        plt.gca().xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
        plt.xticks(rotation=45)

        plt.subplot(212)
        plt.plot(drr.iloc[0:drr_len, 2], label=drr.columns[2])
        plt.plot(drr.iloc[0:drr_len, 3], label=drr.columns[3])
        plt.plot(drr.iloc[0:drr_len, 4], label=drr.columns[4])
        plt.ylabel("Power (kW)")
        plt.legend()
        plt.grid(which='both', axis='both')
        plt.gca().xaxis.set_major_locator(md.SecondLocator(interval=5))
        plt.gca().xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
        plt.xticks(rotation=45)

        plt.tight_layout()
        plot_filename = f"project_{project_id}_{base_filename}_drr.png"
        plot_path = PLOTS_DIR / plot_filename
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        plot_paths.append(f"/static/plots/{plot_filename}")

        # Generate Output Transition Control Plot
        fig = plt.figure(figsize=(10, 5))

        plt.subplot(211)
        plt.plot(otc.iloc[:, 1])
        plt.ylabel("SOC (%)")
        plt.title("Output Transition Control Test")
        plt.grid(which='major', axis='both')
        plt.gca().xaxis.set_major_locator(md.HourLocator(interval=1))
        plt.gca().xaxis.set_major_formatter(md.DateFormatter('%D %H:%M'))
        plt.xticks(rotation=45)

        plt.subplot(212)
        plt.plot(otc.iloc[:, 2], label=otc.columns[2])
        plt.plot(otc.iloc[:, 3], label=otc.columns[3])
        plt.plot(otc.iloc[:, 4], label=otc.columns[4])
        plt.ylabel("Power (kW)")
        plt.legend()
        plt.grid(which='both', axis='both')
        plt.gca().xaxis.set_major_locator(md.HourLocator(interval=1))
        plt.gca().xaxis.set_major_formatter(md.DateFormatter('%D %H:%M'))
        plt.xticks(rotation=45)

        plt.tight_layout()
        plot_filename = f"project_{project_id}_{base_filename}_otc.png"
        plot_path = PLOTS_DIR / plot_filename
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        plot_paths.append(f"/static/plots/{plot_filename}")

    except Exception as e:
        print(f"Error generating commissioning plots: {e}")
        import traceback
        traceback.print_exc()

    return plot_paths


def generate_temp_humidity_plots(file_path, project_id):
    """Generate plots for temperature and humidity data"""
    plot_paths = []
    base_filename = Path(file_path).stem

    try:
        # Read the Excel file (simplified - assuming single file for POC)
        header_row = 1
        idx_col = 1

        data = pd.read_excel(file_path, index_col=idx_col, skiprows=header_row)

        # Remove non-local timestamp if exists
        if 't_stamp' in data.columns:
            data = data.drop('t_stamp', axis=1)

        # Acceptance Criteria
        max_temp = 30
        max_humidity = 80

        # Generate plot
        fig = plt.figure(figsize=(10, 5))

        # Top plot for humidity
        plt.subplot(211)
        for x in range(0, data.shape[1], 4):
            if x < data.shape[1]:
                plt.plot(data.iloc[:, x], label=data.columns[x])
                # Add percentage text
                over_80 = 100 * (data.iloc[:, x] > 80).sum() / len(data.iloc[:, x])
                plt.text(data.index[0], 10*(x/4+1),
                        f'{data.columns[x]}: {over_80:.2f}% over 80% ({len(data.iloc[:, x])} points)',
                        fontsize=10)

        plt.legend()
        plt.axhline(y=max_humidity, linestyle='--', color='r')
        plt.gca().set_ylim(0, 100)
        plt.ylabel("Relative Humidity (%)")
        plt.title("Container Conditions - Humidity")
        plt.grid(which='major', axis='both')
        plt.gca().xaxis.set_major_locator(md.DayLocator(interval=7))
        plt.gca().xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)

        # Bottom plot for temperature
        plt.subplot(212)
        for y in range(0, data.shape[1], 4):
            if y+1 < data.shape[1]:
                plt.plot(data.iloc[:, y+1], label=data.columns[y+1])
            if y+2 < data.shape[1]:
                try:
                    plt.plot(data.iloc[:, y+2], label=data.columns[y+2])
                except:
                    pass
            if y+3 < data.shape[1]:
                try:
                    plt.plot(data.iloc[:, y+3], label=data.columns[y+3])
                except:
                    pass

        plt.legend()
        plt.axhline(y=max_temp, color='r', linestyle='--')
        plt.ylabel("Container Temperature (C)")
        plt.grid(which='major', axis='both')
        plt.gca().xaxis.set_major_locator(md.DayLocator(interval=7))
        plt.gca().xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)

        plt.tight_layout()

        # Save plot
        plot_filename = f"project_{project_id}_{base_filename}_temp_humidity.png"
        plot_path = PLOTS_DIR / plot_filename
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        plt.close(fig)

        plot_paths.append(f"/static/plots/{plot_filename}")

    except Exception as e:
        print(f"Error generating temp/humidity plots: {e}")
        import traceback
        traceback.print_exc()

    return plot_paths


def generate_plots_from_file(file_path, project_id):
    """
    Main entry point: detect test type and generate appropriate plots
    Returns: dict with test_type and list of plot paths
    """
    test_type = detect_test_type(file_path)

    if test_type == "commissioning":
        plot_paths = generate_commissioning_plots(file_path, project_id)
    else:
        plot_paths = generate_temp_humidity_plots(file_path, project_id)

    return {
        "test_type": test_type,
        "plot_paths": plot_paths
    }
