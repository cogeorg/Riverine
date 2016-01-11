!function(){
    _scatterplot = {};
    _scatterplot.formatData = function(){
        //implement if additional formatting is required 
    }

    _scatterplot.draw = function(_data, headers, svg, margin, width, height, xlabel, ylabel){

        var xScale = d3.scale.linear()
        	.domain(d3.extent(_data, function(d){return d.xaxis;}))
        	.range([0, width]);
            	
        var yScale = d3.scale.linear()
        	.domain(d3.extent(_data, function(d){return d.yaxis;}))
        	.range([height, 0]);
        	
        var xAxis = d3.svg.axis()
        	.scale(xScale)
        	.orient("bottom");
        
        var yAxis = d3.svg.axis()
        	.scale(yScale)
        	.orient("left");

        var colors = d3.scale.category10()
            .domain(_data.map(function(d){return d.ID;}));

        var dot = svg.selectAll("g")
            .data(_data)
            .enter().append("g");
			  
            dot.append("circle")				
            .attr("cx", function(d){return xScale(d.xaxis);})
            .attr("cy", function(d){return yScale(d.yaxis)})
            .attr("r", function(d){return (d["weight"])?d.weight:2;})
            .style("fill", function(d){return colors(d.ID);})
            .attr("data-legend", function(d){return d.ID;})
            .attr("data-legend-color", function(d){return colors(d.ID);})
        			
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
