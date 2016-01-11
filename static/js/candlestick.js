!function(){
    _candlestick = {};

    var dateFormat = d3.time.format("%d/%m/%Y");

    var bullish = "green";
    var bearish = "red";

    var tip = d3.tip()
      .attr('class', 'd3-tip')
      .offset([-10, 0])
      .html(function(d) {
      	color = d.close>=d.open?bullish:bearish;
      	str = "";
        str = str + "<strong>Open:</strong> <span style='color:" + color +"'>" + d.open + "</span>";
        str = str + "</br><strong>Close:</strong> <span style='color:" + color +"'>" + d.close + "</span>";
        str = str + "</br><strong>Low:</strong> <span style='color:" + color +"'>" + d.low + "</span>";
        str = str + "</br><strong>High:</strong> <span style='color:" + color +"'>" + d.high + "</span>";
    
        return str;
      });


    _candlestick.formatData = function(modelData, headers){
        _data = new Array(modelData.length);
        var i, j;
        for (i=0; i<modelData.length; ++i){
            _data[i] = new Object;
            for (j=0; j<headers.length; ++j){
                _data[i][headers[j].toLowerCase()] = modelData[i][j];
            }
            _data[i].date = dateFormat.parse(_data[i].date);
        }
        return _data;
    }
    
    _candlestick.draw = function(_data, svg, margin, width, height, ylabel){

        var x = d3.time.scale()
        	.range([0, width]);
        	
        var y = d3.scale.linear()
        	.range([height,0]);
        	
        var xAxis = d3.svg.axis()
            .scale(x)
            .orient('bottom')
            .ticks(d3.time.days, 1)
            .tickFormat(d3.time.format('%d/%m'))
            .tickSize(0)
            .tickPadding(10)
            .innerTickSize(-height)
            .outerTickSize(0);	
        		
        var yAxis = d3.svg.axis()
        	.scale(y)
        	.orient("left")
        	.tickPadding(5)
            .innerTickSize(-width)
            .outerTickSize(0);	

        svg.attr("class", "candlestick");	
        	
        svg.call(tip);
    
        x.domain(d3.extent(_data, function(d) { return d.date; }));
        //y.domain([0, d3.max(_data,function(d){return d.high})]);
        y.domain([0, 500]);
    
        var candlestick_width = Math.abs(x(_data[0].date)-x(_data[1].date))*0.1;
    			
        candlestick = svg.selectAll("g")
            .data(_data)
           .enter().append("g")
            .attr("class", "candlestick")
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide);				  	
    	
    	
        svg.append("g").attr("class", "x axis").attr("transform", "translate(0,"+height+")").call(xAxis)								
    			  		
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
           .append("text")				
            .attr("transform", "rotate(-90)")
            .attr("y", -40)
            //.attr("x", -height/3)
            .attr("dy", ".71em")
            .attr("text-anchor", "end")
            .text(ylabel);				
    			
        //high
        candlestick.append("line")
            .attr("x1", function(d){return x(d.date)-candlestick_width/2;} ) 
            .attr("y1", function(d){return y(d.high);}) 
            .attr("x2", function(d){return x(d.date)+candlestick_width/2;}) 
            .attr("y2", function(d){return y(d.high);}); 
				
        //low
        candlestick.append("line")
            .attr("x1", function(d){return x(d.date)-candlestick_width/2;} ) 
            .attr("y1", function(d){return y(d.low);}) 
            .attr("x2", function(d){return x(d.date)+candlestick_width/2;}) 
            .attr("y2", function(d){return y(d.low);});					
		
        //"candle-wick"
        candlestick.append("line")
            .attr("x1", function(d){return x(d.date);})
            .attr("y1", function(d){return y(d.high);})
            .attr("x2", function(d){return x(d.date);})
            .attr("y2", function(d){return y(d.low);});	
				
        //open and close
        candlestick.append("rect")
            .attr("x", function(d){return x(d.date)-candlestick_width/2;})
            .attr("y", function(d){return y(Math.max(d.open, d.close));})
            .attr("width", candlestick_width)
            .attr("height", function(d){return Math.abs(y(d.open)-y(d.close));})
            .style("fill", function(d){ return d.close>=d.open?bullish:bearish;});			
    }
}();