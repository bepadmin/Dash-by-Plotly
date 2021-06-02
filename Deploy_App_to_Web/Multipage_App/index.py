import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import vgames, global_sales, ch1

from apps.ucdavis import ucdavisch1

from pathlib import Path

pathlist = Path('.').glob('**/*.py')
for path in pathlist:
     # because path is object not string
     path_in_str = str(path)
     print(path_in_str)
     


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    # html.Div([
    #     dcc.Link('Video Games|', href='/apps/vgames'),
    #     dcc.Link('Other Products', href='/apps/global_sales'),
    # ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
             [Input('url', 'pathname')])
def display_page(pathname):
   if pathname == '/apps/vgames':
       return vgames.layout
   if pathname == '/apps/global_sales':
       return global_sales.layout
   if pathname == '/apps/ch1':
       return ch1.layout   
   else:
       return "404 Page Error! Please choose a link"

# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/apps/vgames':
#         return vgames.layout
#     if pathname == '/apps/global_sales':
#         return global_sales.layout
#     if pathname == '/apps/ch1':
#         return ch1.layout   
#     else:
#         return "404 Page Error! Please choose a link"




if __name__ == '__main__':
    app.run_server(debug=False)
