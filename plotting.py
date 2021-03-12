#motion_detector will be executed before importing df from plotting
from motion_detector import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

"""
Create bokeh graph based off of start and stop times of figures
entering into frame. Importing hover tool to show start and end times
when hovering over plot.
"""

df["Start_string"]=df["Start"].dt.strftime("%Y - %m - %d %H: %M: %S")
df["End_string"]=df["End"].dt.strftime("%Y - %m - %d %H: %M: %S")

cds=ColumnDataSource(df)

p=figure(x_axis_type="datetime", height=100, width=500, title="Motion Graph")
p.yaxis.minor_tick_line_color=None
p.yaxis.ticker.desired_num_ticks=1

hover=HoverTool(tooltips=[("Start", "@Start_string"),("End", "@End_string")])
p.add_tools(hover)

q=p.quad(left="Start",right="End",bottom=0,top=1, color="green",source=cds)

output_file("Graph.html")
show(p)
