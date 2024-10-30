# Additional Python Notes
# ------------------------

# Capitalization matters in Python. Python is case-sensitive: min and Min are different.
# Spelling matters in Python. You must match the spelling of functions and variables exactly.
# Indentation matters in Python. Indentation is used to define code blocks and must be consistent.

# Functions
# ---------
# Functions are used to group code together and make it more readable and reusable.
# We define custom functions that can be called later in the code.
# Functions are blocks of logic that can take inputs, perform work, and return outputs.

# Defining Functions
# ------------------
# Define a function using the def keyword, followed by the function name, parentheses, and a colon. 
# The function name should describe what the function does.
# In the parentheses, specify the inputs needed as arguments the function takes.

# For example:
#    The function filtered_data() takes no arguments.
#    The function between(min, max) takes two arguments, a minimum and maximum value.
#    Arguments can be positional or keyword arguments, labeled with a parameter name.

# The function body is indented (consistently!) after the colon. 
# Use the return keyword to return a value from a function.

# Calling Functions
# -----------------
# Call a function by using its name followed by parentheses and any required arguments.
    
# Decorators
# ----------
# Use the @ symbol to decorate a function with a decorator.
# Decorators a concise way of calling a function on a function.
# We don't typically write decorators, but we often use them.

import plotly.express as px
from palmerpenguins import load_penguins
from shiny.express import input, ui, render
from shinywidgets import render_widget, render_plotly
import seaborn as sns
import matplotlib.pyplot as plt
from shiny import reactive

penguins = load_penguins()

# Set the page options with the title "Karto's Penguins Data" and make it fillable
ui.page_opts(title="Karto's Penguins Data", fillable=True)

# Add a Shiny UI sidebar for user interaction
with ui.sidebar(
    position="right", bg="#f8f8f8", open="open"
):  # Set sidebar open by default
    ui.h2("Sidebar")  # Add a second-level header titled "Sidebar"

    # Create a dropdown input for choosing a column
    ui.input_selectize(
        "selected_attribute",
        "Select column to visualize",
        choices=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
        selected="bill_length_mm",
    )

    # Create a numeric input for Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Plotly bin numeric", 1, min=1, max=10)

    # Create a slider input for Seaborn bins
    ui.input_slider(
        "seaborn_bin_count", "Seaborn bin count", 10, 100, 20, step=5, animate=True
    )

    # Create a checkbox group to filter species
    ui.input_checkbox_group(
        "selected_species_list",
        "Select a species",
        choices=["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie"],
        inline=True,
    )

    # Add a horizontal rule in the sidebar
    ui.hr()

    # Add a hyperlink to the sidebar for GitHub repository
    ui.h5("GitHub Code Repository")
    ui.a(
        "cintel-02-data-karto",
        href="https://github.com/wkarto/cintel-02-data",
        target="_blank",
    )

# Main content layout
with ui.layout_columns():
    # Display the Plotly Histogram
    with ui.card():
        ui.card_header("Plotly Histogram")

        @render_plotly
        def plotly_histogram():
            return px.histogram(
                filtered_data(),
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species",
            )

    # Display Data Table (showing all data)
    with ui.card():
        ui.card_header("Data Table")

        @render.data_frame
        def data_table():
            return render.DataTable(filtered_data())

    # Display Data Grid (showing all data)
    with ui.card():
        ui.card_header("Data Grid")

        @render.data_frame
        def data_grid():
            return render.DataGrid(filtered_data())


# Display the Scatterplot and Seaborn Histogram
with ui.layout_columns():
    # Plotly Scatterplot (showing all species)
    with ui.card():
        ui.card_header("Plotly Scatterplot: Species")

        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                data_frame=filtered_data(),
                x="body_mass_g",
                y="bill_depth_mm",
                color="species",
                labels={
                    "bill_depth_mm": "Bill Depth (mm)",
                    "body_mass_g": "Body Mass (g)",
                },
            )

    # Seaborn Histogram (showing all species)
    with ui.card():
        ui.card_header("Seaborn Histogram: All Species")

        @render.plot
        def seaborn_histogram():
            hist = sns.histplot(
                data=filtered_data(), x="body_mass_g", bins=input.seaborn_bin_count()
            )
            hist.set_xlabel("Mass (g)")
            hist.set_ylabel("Count")
            return hist
            
    # Summary Statistics Table
    with ui.card():
        ui.card_header("Summary Statistics")
        
        @render.data_frame
        def summary_table():
            summary = penguins.describe()
            return summary.reset_index()  # Reset index for display

@reactive.calc
def filtered_data():
    # Filter the penguins DataFrame by the species selected by the user
    selected_species = input.selected_species_list()
    filtered_df = penguins[penguins["species"].isin(selected_species)]
    return filtered_df
