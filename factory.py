class PlotlyFactory:
    def __init__(self, fig = None):
        self.fig = copy.deepcopy(fig)
    def create_fig(self, rows = 1, cols = 1):
        self.fig = make_subplots(rows= rows, cols = cols)
    def set_title(self, title ='', kwargs =  {'x': .5 , 'y':.95, 'font': {'size': 20, 'color' : 'black', 'family': 'Arial'} }):
        """
        set title of the plot
        
        Paramters:
        ----------------
        title: str 
            title text of the plot
        kwargs: dictionary
        
        default: {'x':.5, 'y':.9}
            Valid properties:
            font
                Sets the title font. Note that the title's font used to
                be customized by the now deprecated `titlefont`
                attribute.
            pad
                Sets the padding of the title. Each padding value only
                applies when the corresponding `xanchor`/`yanchor`
                value is set accordingly. E.g. for left padding to take
                effect, `xanchor` must be set to "left". The same rule
                applies if `xanchor`/`yanchor` is determined
                automatically. Padding is muted if the respective
                anchor value is "middle*/*center".
            text
                Sets the plot's title. Note that before the existence
                of `title.text`, the title's contents used to be
                defined as the `title` attribute itself. This behavior
                has been deprecated.
            x
                Sets the x position with respect to `xref` in
                normalized coordinates from 0 (left) to 1 (right).
            xanchor
                Sets the title's horizontal alignment with respect to
                its x position. "left" means that the title starts at
                x, "right" means that the title ends at x and "center"
                means that the title's center is at x. "auto" divides
                `xref` by three and calculates the `xanchor` value
                automatically based on the value of `x`.
            xref
                Sets the container `x` refers to. "container" spans the
                entire `width` of the plot. "paper" refers to the width
                of the plotting area only.
            y
                Sets the y position with respect to `yref` in
                normalized coordinates from 0 (bottom) to 1 (top).
                "auto" places the baseline of the title onto the
                vertical center of the top margin.
            yanchor
                Sets the title's vertical alignment with respect to its
                y position. "top" means that the title's cap line is at
                y, "bottom" means that the title's baseline is at y and
                "middle" means that the title's midline is at y. "auto"
                divides `yref` by three and calculates the `yanchor`
                value automatically based on the value of `y`.
            yref
                Sets the container `y` refers to. "container" spans the
                entire `height` of the plot. "paper" refers to the
                height of the plotting area only.
        """
        title_dict = {'text': title}
        title_dict.update(kwargs)
        self.fig.update_layout(title = title_dict)
    def set_size(self,height, width):
        self.fig.update_layout(height= height, width = width)
    def set_xaxis(self, title ='', kwargs = {}, date_break = 'remove_weekend',num_x = None, cols= None):
        """
            function that set xaxis of the data
        Parameters:
        -------------
        title: str
            title of the graph
        kwargs: 
            other property of the keyword arguments,
        date_break: str or list of value
            choice: 'remove_weekend', 'dropna'
        num_x : int >=2
            which subplot axis to add date_slider, default None
        cols: int
            diminsion of the subplots if applicable 
        """
        if date_break == 'remove_weekend':
            xaxis_dict= { 'title_text': title,
                'rangebreaks':[
                # NOTE: Below values are bound (not single values), ie. hide x to y
                dict(bounds=["sat", "mon"]),
            ]}
        else:
            if date_break =='dropna':
                if num_x is None:
                    date_break = self.fig['data'][0]['x']
                else:
                    if cols is None:
                        assert 1==0, 'cols need to be specified'
                    row = (num_x-1)//cols+1
                    col = num_x%cols
                    if col == 0:
                        col =cols
                    date_break = set()
                    for trace in self.fig.select_traces(row = row, col = col):
                        temp = set(trace['x'])
                        date_break = date_break.union(temp)
                    date_break = list(date_break)  
            date_break = sorted(date_break)
            dt_all = pd.date_range(start=date_break[0], end=date_break[-1])
            dt_obs = [d.strftime("%Y-%m-%d") for d in date_break]
            dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]
            xaxis_dict= { 'title_text': title,
                'rangebreaks':[
                dict(values=dt_breaks)
            ]}
        xaxis_dict.update(kwargs)
        if num_x is None:
            self.fig.update_xaxes(xaxis_dict)
        else:
            num_x = str(num_x)
            self.fig.update_layout( {f'xaxis{num_x}' : xaxis_dict}
        
        )
    def set_yaxis(self, title ='', kwargs = {},num_y = None):
        """
            function that set yaxis of the plot 
        Parameters:
        -------------
        title: str
            title of the yaxis
        kwargs: 
            other property of the keyword arguments,
        num_x : int >=2
            which subplot axis to add date_slider, default None
        """
        yaxis_dict= { 'title_text': title,}
        yaxis_dict.update(kwargs)
        if num_y is None:
            self.fig.update_yaxes(yaxis_dict)
        else:
            num_y = str(num_y)
            self.fig.update_layout( {f'yaxis{num_y}' : yaxis_dict}
        
        )
    def add_date_slider(self, slider_display = False, num_x = None):
        """
        add slider to the plot
        Parameters
        -----------
        slider_display: bool
            whether or not display the slider display
        num_x : int >=2
            which subplot axis to add date_slider, default None
        """
        if num_x is None:
            num_x = ''
        else:
            num_x = str(num_x)
        date_slider_dict = {
            f'xaxis{num_x}' :dict(
                    rangeselector=dict(
                        buttons=list([
                            dict(count=1,
                                 label="1m",
                                 step="month",
                                 stepmode="backward"),
                            dict(count=6,
                                 label="6m",
                                 step="month",
                                 stepmode="backward"),
                            dict(count=1,
                                 label="YTD",
                                 step="year",
                                 stepmode="todate"),
                            dict(count=1,
                                 label="1y",
                                 step="year",
                                 stepmode="backward"),
                            dict(step="all")
                        ])
                    ),
                    rangeslider=dict(
                        visible=slider_display
                    ),
                    type="date"
                )
        }
        self.fig.update_layout(
                date_slider_dict
                
    )
    def update_layout(self, kwargs = {'template': 'seaborn'}):
        self.fig.update_layout(**kwargs)
    def add_annotation(self, text, num_x, x = .5,y = .5 ):
        self.fig['layout'].update(
    annotations=[
    dict(
        x=x, y=y, # annotation point
        xref=f'x{num_x}', 
        yref=f'y{num_x}',
        text= text,
        showarrow=False,
        arrowhead=7,
        ax=10,
        ay=70
        ),
    ])
    def add_vline(self,x, row, col,text = '',):
        import datetime
        self.fig.add_vrect(x0=x, x1= x,
                           annotation_text=text, row = row, col= col,\
                           line_dash="dash", line_color="black", line_width = 2,\
                          annotation_position="top left",
              annotation_textangle = 90,)
    def add_hline(self,y, row, col,text = '',):
        import datetime
        self.fig.add_hrect(y0=y, y1= y,
                           annotation_text=text, row = row, col= col, line_dash="dash",\
                           line_color="black", line_width = 2,\
                          annotation_position="top right",
              annotation_textangle = 0,)
