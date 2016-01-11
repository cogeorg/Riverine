!function(){
    _histogram = {};

    _histogram.formatData = function(data, headers){
        _data = new Object;
        var i,j;
        for (i=0; i<headers.length; ++i){
            _data[i] = new Array;
            for (j=0; j<data.length; ++j){
                _data[i][j] = data[j][i];
            }
        }
        return _data;
    }

    _histogram.draw = function(_data, headers, svg, margin, width, height, xlabel, ylabel){

        var i;

        var keys = new Array;
        var _minX, _maxX;
        _minX = d3.min(_data[0])
        _maxX = d3.max(_data[0])
        var _stub;
        for (i=0; i<headers.length; ++i){
            keys.push(i);
            _stub = d3.extent(_data[i]);
            if (_stub[0]<_minX)
                _minX = _stub[0];
            if (_stub[1]>_maxX)
                _maxX = _stub[1];
        }

        var xScale = d3.scale.linear()
        	.domain([_minX-0.1*_maxX, 1.4*_maxX])
        	.range([0, width]);

        var histogram = d3.layout.histogram()
        	.frequency(false)
        	.bins(xScale.ticks(40)); 

        var hist_data = new Object;
        _maxY = 0;

        for (i=0; i<headers.length; ++i){
            hist_data[i] = histogram(_data[i]);
            _stub = d3.max(hist_data[i], function(d){return d.y;})
            if (_stub > _maxY ){
                _maxY = _stub;
            }
        }        

        if (_maxY>=.9)
            _maxY = 1;
        else if (_maxY>=.8)
            _maxY = .9;
        else if (_maxY>=.7)
            _maxY = .8;
        else if (_maxY>=.6)
            _maxY = .7;
        else if (_maxY>=.5)
            _maxY = .6;
        else if (_maxY>=.4)
            _maxY = .5;
        else if (_maxY>=.3)
            _maxY = .4;
        else if (_maxY>=.2)
            _maxY = .3;
        else if (_maxY>=.1)
            _maxY = .2;
        else
            _maxY = .1;
            	
        var yScale = d3.scale.linear()
        	.domain([0, _maxY])
        	.range([height, 0]);
        	
        var xAxis = d3.svg.axis()
        	.scale(xScale)
        	.orient("bottom");
        
        var yAxis = d3.svg.axis()
        	.scale(yScale)
        	.orient("left")
        	.tickFormat(d3.format("%"))

        var colors = d3.scale.category10()
            .domain(keys);

        for (i=0; i<headers.length; ++i){        
            var hist = hist_data[i];
            var hist_barWidth = Math.abs(xScale(hist[0].x+hist[0].dx)-xScale(hist[1].x+hist[1].dx))  
            var bar = svg.selectAll("g")
            	.data(hist)
              .enter().append("rect")
            	.attr("class", "bar")
            	.attr("x", function(d){return xScale(d.x)+1;})
            	.attr("y", function(d){return yScale(d.y);})
            	.attr("width", function(d){return hist_barWidth-1;}) //x(d.dx)
            	.attr("height", function(d){return height-yScale(d.y);}) //	
            	.attr("data-legend", headers[i])
            	.attr("data-legend-color", colors(i))
                 .style("opacity", ".5")
                 .style("fill", colors(i))
        }
        			
        svg.append("g")
        	.attr("class", "x axis")
        	.attr("transform", "translate(0,"+height+")")
        	.call(xAxis)
          .append("text")
          	.attr("class", "label")
          	.attr("x", width)	
          	.attr("y", -6)
          	.style("text-anchor", "end")
          	.text(xlabel);	

        svg.append("g")
        	.attr("class", "y axis")	
        	.call(yAxis)
           .append("text")
        	   .attr("transform", "rotate(-90)")
        	   .attr("y", 6)
        	   .attr("dy", ".71em")
        	   .style("text-anchor", "end")
        	   .style("font-size", "10px")
        	   .text(ylabel);	

        legend = svg.append("g")
        	.attr("class", "legend")
        	.attr("transform", "translate("+(width-100)+",0)")
        	.style("font-size", "10px")
        	.call(d3.legend);
    }
}();